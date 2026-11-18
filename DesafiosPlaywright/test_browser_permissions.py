from playwright.sync_api import Page, expect

from config import BASE_URL
from BrowserPermissionsPage import BrowserPermissionsPage

PERMISOS = ["geolocation", "notifications", "camera", "microphone", "clipboard-read"]


def test_sin_otorgar_nada_los_cinco_permisos_arrancan_en_prompt(page: Page) -> None:
    permisos_page = BrowserPermissionsPage(page)
    page.goto(f"{BASE_URL}/permissions")

    for permiso in PERMISOS:
        expect(permisos_page.estado(permiso)).to_have_text("prompt")


# `BrowserContext.grant_permissions` no solo otorga lo que se le pasa: a
# partir de ahí trata la lista como la única fuente de verdad y pone en
# "denied" a cualquier otro permiso de la tabla que no haya sido incluido,
# aunque antes estuviera en "prompt" y nunca se lo haya tocado. Como la
# página sincroniza la tabla con un listener de "change" (igual que el
# banner de CookieConsentPage), el cambio se ve sin recargar: alcanza con
# otorgar a mitad del test.

def test_otorgar_un_permiso_puntual_niega_al_resto_en_vez_de_dejarlo_en_prompt(
    page: Page,
) -> None:
    permisos_page = BrowserPermissionsPage(page)
    page.goto(f"{BASE_URL}/permissions")

    page.context.grant_permissions(["geolocation", "notifications"])

    expect(permisos_page.estado("geolocation")).to_have_text("granted")
    expect(permisos_page.estado("notifications")).to_have_text("granted")
    expect(permisos_page.estado("camera")).to_have_text("denied")
    expect(permisos_page.estado("microphone")).to_have_text("denied")
    expect(permisos_page.estado("clipboard-read")).to_have_text("denied")


def test_pedir_notificaciones_con_el_permiso_ya_otorgado_se_resuelve_sin_dialogo(
    page: Page,
) -> None:
    permisos_page = BrowserPermissionsPage(page)
    page.goto(f"{BASE_URL}/permissions")
    page.context.grant_permissions(["notifications"])

    permisos_page.boton_pedir_notificaciones.click()

    expect(permisos_page.resultado_notificaciones).to_have_text("Notifications: granted")


# Copiar usa `navigator.clipboard.writeText()`, que en Chromium no exige el
# permiso "clipboard-read" -- ese permiso sólo custodia la lectura. Por eso
# "Copy" funciona igual aunque la tabla siga mostrando "prompt".

def test_copiar_al_portapapeles_no_necesita_el_permiso_clipboard_read(page: Page) -> None:
    permisos_page = BrowserPermissionsPage(page)
    page.goto(f"{BASE_URL}/permissions")

    expect(permisos_page.estado("clipboard-read")).to_have_text("prompt")

    permisos_page.campo_texto_clipboard.fill("Copiado desde QaTest")
    permisos_page.boton_copiar.click()

    expect(permisos_page.resultado_clipboard).to_have_text("Copied: Copiado desde QaTest")


# Pegar sí usa `readText()`, que necesita el permiso. En headless no hay
# usuario que responda al diálogo que el navegador mostraría en un caso
# real, así que mientras el permiso está en "prompt" el intento no queda
# pendiente: Chromium lo resuelve solo, en contra del pedido, y la propia
# tabla pasa de "prompt" a "denied" como efecto colateral del intento
# fallido, no porque alguien lo haya negado explícitamente.

def test_pegar_sin_el_permiso_otorgado_falla_y_el_intento_deja_el_estado_en_denied(
    page: Page,
) -> None:
    permisos_page = BrowserPermissionsPage(page)
    page.goto(f"{BASE_URL}/permissions")

    expect(permisos_page.estado("clipboard-read")).to_have_text("prompt")

    permisos_page.boton_pegar.click()

    expect(permisos_page.resultado_clipboard).to_have_text("Paste failed: NotAllowedError")
    expect(permisos_page.estado("clipboard-read")).to_have_text("denied")


def test_pegar_con_el_permiso_otorgado_devuelve_exactamente_lo_copiado(page: Page) -> None:
    permisos_page = BrowserPermissionsPage(page)
    page.goto(f"{BASE_URL}/permissions")
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])

    permisos_page.campo_texto_clipboard.fill("Pegado desde QaTest")
    permisos_page.boton_copiar.click()
    permisos_page.campo_texto_clipboard.fill("texto distinto, para confirmar que lo pegado no es coincidencia")
    permisos_page.boton_pegar.click()

    expect(permisos_page.resultado_clipboard).to_have_text("Pasted: Pegado desde QaTest")

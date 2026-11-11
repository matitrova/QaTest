from playwright.sync_api import Page

from config import BASE_URL
from CookieConsentPage import CookieConsentPage


def test_sin_eleccion_previa_muestra_el_banner(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")

    assert cookie_page.banner.is_visible()
    assert cookie_page.texto_estado() == "Analytics cookies: not decided yet"
    assert cookie_page.cookie_consent() is None


# El panel con los checkboxes de "Necessary"/"Analytics" arranca oculto con el
# atributo HTML `hidden`, no con una clase CSS: "Customize" alterna ese
# atributo (y el aria-expanded del propio botón) a mano por JS, sin que haya
# ninguna animación de por medio que haga falta esperar.

def test_personalizar_muestra_y_oculta_el_panel_de_categorias(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")

    assert not cookie_page.panel_personalizar.is_visible()
    assert cookie_page.personalizar.get_attribute("aria-expanded") == "false"

    cookie_page.personalizar.click()
    assert cookie_page.panel_personalizar.is_visible()
    assert cookie_page.personalizar.get_attribute("aria-expanded") == "true"

    cookie_page.personalizar.click()
    assert not cookie_page.panel_personalizar.is_visible()
    assert cookie_page.personalizar.get_attribute("aria-expanded") == "false"


# El checkbox "Necessary" viene tildado y disabled de antemano: no se puede
# destildar aunque se quiera, a diferencia de "Analytics" que arranca
# destildado y habilitado.

def test_checkbox_necesarias_viene_tildado_y_bloqueado(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")
    cookie_page.personalizar.click()

    assert cookie_page.checkbox_necesarias.is_checked()
    assert cookie_page.checkbox_necesarias.is_disabled()
    assert not cookie_page.checkbox_analitica.is_checked()
    assert cookie_page.checkbox_analitica.is_enabled()


def test_aceptar_todo_guarda_all_y_saca_el_banner(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")

    cookie_page.aceptar_todo.click()

    assert cookie_page.cookie_consent() == "all"
    assert cookie_page.texto_estado() == "Analytics cookies: allowed"
    # El click dispara un location.reload(): no alcanza con que el banner
    # quede invisible, el servidor directamente deja de mandar el <div> en el
    # HTML una vez que la cookie ya está puesta.
    assert cookie_page.banner.count() == 0


def test_solo_necesarias_guarda_necessary_y_saca_el_banner(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")

    cookie_page.solo_necesarias.click()

    assert cookie_page.cookie_consent() == "necessary"
    assert cookie_page.texto_estado() == "Analytics cookies: blocked"
    assert cookie_page.banner.count() == 0


# "Save my choice" no manda un valor fijo: lee el estado del checkbox de
# Analytics en el momento del click y arma "all" o "necessary" a partir de
# eso, así que tildarlo primero termina guardando lo mismo que "Accept all".

def test_guardar_eleccion_con_analitica_tildada_equivale_a_aceptar_todo(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")
    cookie_page.personalizar.click()
    cookie_page.checkbox_analitica.check()

    cookie_page.guardar_eleccion.click()

    assert cookie_page.cookie_consent() == "all"
    assert cookie_page.texto_estado() == "Analytics cookies: allowed"


def test_guardar_eleccion_sin_tildar_analitica_equivale_a_solo_necesarias(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")
    cookie_page.personalizar.click()

    cookie_page.guardar_eleccion.click()

    assert cookie_page.cookie_consent() == "necessary"
    assert cookie_page.texto_estado() == "Analytics cookies: blocked"


def test_olvidar_eleccion_borra_la_cookie_y_vuelve_a_mostrar_el_banner(page: Page) -> None:
    cookie_page = CookieConsentPage(page)
    page.goto(f"{BASE_URL}/cookie_consent")
    cookie_page.aceptar_todo.click()
    assert cookie_page.cookie_consent() == "all"

    cookie_page.olvidar()

    assert cookie_page.cookie_consent() is None
    assert cookie_page.texto_estado() == "Analytics cookies: not decided yet"
    assert cookie_page.banner.is_visible()

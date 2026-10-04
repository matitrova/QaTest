import pytest
from playwright.sync_api import expect

from config import BASE_URL
from EntryAdPage import EntryAdPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py, test_context_menu.py y
    # test_notification_message.py: el script externo de Optimizely que
    # carga el layout de esta página puede colgar el evento "load".
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_anuncio_aparece_al_cargar(page):
    entry_ad_page = EntryAdPage(page)
    page.goto(f"{BASE_URL}/entry_ad")

    # El modal arranca en el HTML con style="display:none" y un
    # setTimeout() de 500ms recién después lo muestra -- no está visible
    # apenas termina de cargar la página, hay que esperarlo explícitamente
    # en vez de asumir que ya está ahí.
    expect(entry_ad_page.modal).to_be_visible(timeout=5000)


# El click del body cierra el modal vía $('body').on('click', dismissedAd),
# pero $('#modal .modal').on('click', e => e.stopPropagation()) corta esa
# burbuja para cualquier click hecho dentro de la caja del modal (el título
# o el cuerpo del texto, no el footer). Sin este caso, un test que solo
# probara "cerrar funciona" no distinguiría un cierre intencional de un
# cierre accidental por tocar el contenido.

def test_clic_dentro_del_modal_no_lo_cierra(page):
    entry_ad_page = EntryAdPage(page)
    page.goto(f"{BASE_URL}/entry_ad")
    expect(entry_ad_page.modal).to_be_visible(timeout=5000)

    entry_ad_page.hacer_clic_dentro_del_modal()
    page.wait_for_timeout(300)

    assert entry_ad_page.anuncio_visible() is True


def test_cerrar_anuncio_lo_oculta_y_no_reaparece_al_recargar(page):
    entry_ad_page = EntryAdPage(page)
    page.goto(f"{BASE_URL}/entry_ad")
    expect(entry_ad_page.modal).to_be_visible(timeout=5000)

    with page.expect_response(lambda r: r.url.endswith("/entry_ad") and r.request.method == "POST"):
        entry_ad_page.cerrar_anuncio()
    expect(entry_ad_page.modal).to_be_hidden()

    # El cierre no es solo un hide() del lado del cliente: el POST anterior
    # guarda la decisión en la sesión del servidor. Una nueva visita a la
    # misma URL ni siquiera manda el setTimeout que muestra el modal -- se
    # confirma visitando la página de nuevo, no recargando la misma.
    page.goto(f"{BASE_URL}/entry_ad")
    page.wait_for_timeout(700)

    assert entry_ad_page.anuncio_visible() is False


# Bug real del sitio: el texto de la página promete "to re-enable it, click
# here", pero el handler de #restart-ad llama a $.post('/entry-ad') -- con
# GUION -- mientras que el único endpoint que el servidor realmente usa
# para marcar la sesión es /entry_ad, con GUION BAJO (el mismo que dispara
# el botón de Cerrar). El típo hace que el POST de "reiniciar" pegue a una
# ruta que no existe. Se verifica con `page.request` en vez de clickear el
# link: el propio `<a href="">` dispara ADEMÁS una navegación real del
# navegador (no tiene `preventDefault()`), que en una corrida real puede
# cancelar ese POST antes de que termine -- probar el endpoint directo es
# lo único que da un resultado determinístico.

def test_reiniciar_pega_a_un_endpoint_que_no_existe(page):
    respuesta = page.request.post(f"{BASE_URL}/entry-ad")
    assert respuesta.status == 404


# Y porque ese POST nunca llega a buen puerto (ni siquiera le da tiempo,
# dado el punto anterior), "reiniciar" no reinicia nada: después de
# cerrarlo y clickear ese link, una visita aparte a la página sigue sin
# mostrar el anuncio.

def test_reiniciar_nunca_reactiva_el_anuncio(page):
    entry_ad_page = EntryAdPage(page)
    page.goto(f"{BASE_URL}/entry_ad")
    expect(entry_ad_page.modal).to_be_visible(timeout=5000)

    with page.expect_response(lambda r: r.url.endswith("/entry_ad") and r.request.method == "POST"):
        entry_ad_page.cerrar_anuncio()
    expect(entry_ad_page.modal).to_be_hidden()

    entry_ad_page.hacer_clic_en_reiniciar()
    page.wait_for_timeout(1500)

    page.goto(f"{BASE_URL}/entry_ad")
    page.wait_for_timeout(700)

    assert entry_ad_page.anuncio_visible() is False

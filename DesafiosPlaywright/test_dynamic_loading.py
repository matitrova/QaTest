from playwright.sync_api import expect

from config import BASE_URL
from DynamicLoadingPage import DynamicLoadingPage


# El sitio simula una carga real de ~5 segundos antes de mostrar el
# resultado; el timeout default de expect() (5000ms) queda demasiado
# justo y hace flaky el test, así que se estira acá explícitamente en
# vez de agregar un sleep() a ciegas.
TIMEOUT_CARGA_MS = 10_000


def test_elemento_oculto_que_se_muestra(page):
    # Ejemplo 1: el "Hello World!" ya está en el DOM desde el principio,
    # solo que oculto con display:none hasta que termina la carga.
    dynamic_page = DynamicLoadingPage(page)
    page.goto(f"{BASE_URL}/dynamic_loading/1")

    dynamic_page.hacer_clic_en_start()

    expect(dynamic_page.finish_text).to_be_visible(timeout=TIMEOUT_CARGA_MS)
    assert "Hello World!" in dynamic_page.finish_text.inner_text()


def test_elemento_que_se_agrega_al_dom(page):
    # Ejemplo 2: acá el elemento no existe en el DOM hasta que termina
    # la carga -- esperar por "visible" no alcanza si el locator todavía
    # no encontró nada; expect().to_be_visible() reintenta hasta que el
    # elemento aparece, evitando un sleep() a ciegas.
    dynamic_page = DynamicLoadingPage(page)
    page.goto(f"{BASE_URL}/dynamic_loading/2")

    dynamic_page.hacer_clic_en_start()

    expect(dynamic_page.finish_text).to_be_visible(timeout=TIMEOUT_CARGA_MS)
    assert "Hello World!" in dynamic_page.finish_text.inner_text()

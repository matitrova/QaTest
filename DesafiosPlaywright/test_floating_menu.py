import pytest
from playwright.sync_api import expect

from config import BASE_URL
from FloatingMenuPage import FloatingMenuPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py, test_context_menu.py,
    # test_notification_message.py, test_entry_ad.py y test_exit_intent.py:
    # el script externo de Optimizely que carga el layout de esta página
    # puede colgar el evento "load".
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_menu_arranca_en_su_posicion_original(page):
    floating_menu_page = FloatingMenuPage(page)
    page.goto(f"{BASE_URL}/floating_menu")

    expect(floating_menu_page.menu).to_be_visible()
    assert floating_menu_page.estilo_top_del_menu() == "top: 0px;"


# stickyfloat.js no usa `position: fixed` (que el navegador resolvería solo):
# el menú se queda `position: absolute` todo el tiempo y es la librería la
# que, en cada scroll, recalcula a mano el `top` inline para que la caja
# siga pareciendo clavada cerca del borde superior del viewport. Por eso la
# aserción real no es sobre el valor de `top` (que crece con el scroll) sino
# sobre la posición resultante en pantalla (bounding_box), que es la que
# demuestra el efecto "floating".

def test_menu_permanece_cerca_del_borde_superior_al_scrollear(page):
    floating_menu_page = FloatingMenuPage(page)
    page.goto(f"{BASE_URL}/floating_menu")
    posicion_inicial = floating_menu_page.posicion_del_menu()

    floating_menu_page.hacer_scroll(2000)

    # Sin stickyfloat, un elemento position:absolute ubicado a y=32 del
    # documento terminaría en y = 32 - 2000 = -1968 (bien afuera del
    # viewport) tras este scroll. Que siga apareciendo pegado arriba es la
    # prueba de que la librería lo está reposicionando activamente.
    posicion_tras_scroll = floating_menu_page.posicion_del_menu()
    assert posicion_tras_scroll["y"] > posicion_inicial["y"] - 100
    assert posicion_tras_scroll["y"] < 50


def test_menu_vuelve_a_su_posicion_original_al_scrollear_arriba(page):
    floating_menu_page = FloatingMenuPage(page)
    page.goto(f"{BASE_URL}/floating_menu")
    posicion_inicial = floating_menu_page.posicion_del_menu()

    floating_menu_page.hacer_scroll(2000)
    floating_menu_page.hacer_scroll(-2300)

    assert page.evaluate("window.scrollY") == 0
    assert floating_menu_page.posicion_del_menu() == posicion_inicial
    assert floating_menu_page.estilo_top_del_menu() == "top: 0px;"


# Los links del menú (#home, #news, etc.) no apuntan a ningún elemento real
# de la página -- es contenido lorem ipsum sin esos ids -- así que no hay
# nada que "scrollear hacia" para verificar. Lo que sí es verificable es que
# el link sigue siendo un elemento clickeable de verdad (no un overlay roto
# ni algo que quedó por detrás de otro elemento) incluso mientras el menú
# está flotando a mitad de un scroll largo, y que el navegador actualiza el
# hash de la URL como corresponde a un link ancla normal.

def test_los_links_del_menu_siguen_siendo_clickeables_mientras_flota(page):
    floating_menu_page = FloatingMenuPage(page)
    page.goto(f"{BASE_URL}/floating_menu")
    floating_menu_page.hacer_scroll(2000)

    floating_menu_page.hacer_clic_en_link_home()

    assert page.url == f"{BASE_URL}/floating_menu#home"

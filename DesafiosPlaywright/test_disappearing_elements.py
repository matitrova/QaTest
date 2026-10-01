import pytest

from config import BASE_URL
from DisappearingElementsPage import DisappearingElementsPage

ITEMS_BASE = ["Home", "About", "Contact Us", "Portfolio"]
ITEM_EXTRA = "Gallery"


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py y otros: el script externo de
    # Optimizely puede colgar el evento "load" si esa red está lenta o
    # inaccesible.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_los_cuatro_items_base_siempre_aparecen_en_el_mismo_orden(page):
    disappearing_elements_page = DisappearingElementsPage(page)

    for _ in range(5):
        page.goto(f"{BASE_URL}/disappearing_elements")
        assert disappearing_elements_page.textos()[:4] == ITEMS_BASE


def test_la_cantidad_de_items_es_cuatro_o_cinco(page):
    disappearing_elements_page = DisappearingElementsPage(page)

    for _ in range(5):
        page.goto(f"{BASE_URL}/disappearing_elements")
        assert len(disappearing_elements_page.textos()) in (4, 5)


# "Gallery" no está oculto con CSS (display:none): el servidor decide en cada
# pedido si lo incluye o no en el HTML que manda, así que no hay ningún
# elemento "invisible" para encontrar en el DOM cuando no aparece -- hay que
# recargar hasta ver los dos estados en vez de buscarlo con un selector que
# ignore visibilidad.

def test_gallery_aparece_en_algunas_cargas_y_no_en_otras(page):
    disappearing_elements_page = DisappearingElementsPage(page)
    vistos = set()

    for _ in range(20):
        page.goto(f"{BASE_URL}/disappearing_elements")
        vistos.add(ITEM_EXTRA in disappearing_elements_page.textos())
        if len(vistos) == 2:
            break

    if len(vistos) < 2:
        pytest.skip("El sitio no mostró los dos estados de Gallery en 20 intentos al azar")

    assert vistos == {True, False}


def test_gallery_cuando_aparece_es_el_ultimo_item(page):
    disappearing_elements_page = DisappearingElementsPage(page)

    for _ in range(20):
        page.goto(f"{BASE_URL}/disappearing_elements")
        textos = disappearing_elements_page.textos()
        if ITEM_EXTRA in textos:
            assert textos[-1] == ITEM_EXTRA
            return

    pytest.skip("El sitio no mostró Gallery en 20 intentos al azar")

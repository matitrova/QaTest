import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from StaleElementPage import StaleElementPage


@pytest.fixture
def stale_element_page(page: Page) -> StaleElementPage:
    page.goto(f"{BASE_URL}/stale_element")
    return StaleElementPage(page)


def test_lista_inicial_tiene_tres_items_y_contador_en_cero(
    stale_element_page: StaleElementPage,
) -> None:
    expect(stale_element_page.items).to_have_count(3)
    expect(stale_element_page.contador).to_have_text("Rebuilt 0 times")
    expect(stale_element_page.estado_timer).to_have_text("Timer: off")


def test_reconstruir_una_vez_usa_singular_en_el_contador(
    stale_element_page: StaleElementPage,
) -> None:
    stale_element_page.reconstruir()

    expect(stale_element_page.contador).to_have_text("Rebuilt 1 time")


def test_reconstruir_dos_veces_usa_plural_en_el_contador(
    stale_element_page: StaleElementPage,
) -> None:
    stale_element_page.reconstruir()
    stale_element_page.reconstruir()

    expect(stale_element_page.contador).to_have_text("Rebuilt 2 times")


def test_los_items_mantienen_su_texto_despues_de_reconstruir(
    stale_element_page: StaleElementPage,
) -> None:
    # El texto de cada <li> es idéntico antes y después, pero -- como
    # muestran los tests de abajo -- son nodos del DOM distintos.
    stale_element_page.reconstruir()

    expect(stale_element_page.item(1)).to_have_text("Item 1")
    expect(stale_element_page.item(2)).to_have_text("Item 2")
    expect(stale_element_page.item(3)).to_have_text("Item 3")


def test_handle_de_un_item_queda_desconectado_del_dom_tras_reconstruir(
    stale_element_page: StaleElementPage,
) -> None:
    handle = stale_element_page.handle_del_item(1)
    assert handle.evaluate("el => el.isConnected") is True

    stale_element_page.reconstruir()

    # El botón armó un <li> nuevo con el mismo texto y lo puso en un <ul>
    # nuevo -- el <li> original que agarró el handle ya no es parte del
    # documento, aunque el handle en sí sigue siendo un objeto válido.
    assert handle.evaluate("el => el.isConnected") is False


def test_leer_texto_de_un_handle_obsoleto_no_falla_pero_clickearlo_si(
    stale_element_page: StaleElementPage,
) -> None:
    handle = stale_element_page.handle_del_item(2)

    stale_element_page.reconstruir()

    # text_content() solo lee una propiedad del nodo via JS -- no le
    # importa si ese nodo sigue colgado del document, así que no explota.
    assert handle.text_content() == "Item 2"

    # click() en cambio necesita que el elemento esté realmente en la
    # página (visible, estable, dentro del viewport) para poder clickearlo
    # de verdad, y ahí sí se nota que el nodo quedó obsoleto.
    with pytest.raises(Exception, match="not attached to the DOM"):
        handle.click(timeout=2000)


def test_locator_del_mismo_item_se_resuelve_de_nuevo_y_no_queda_obsoleto(
    stale_element_page: StaleElementPage,
) -> None:
    item_3 = stale_element_page.item(3)
    assert item_3.element_handle().evaluate("el => el.isConnected") is True

    stale_element_page.reconstruir()
    stale_element_page.reconstruir()

    # A diferencia del ElementHandle de arriba, un Locator no guarda una
    # referencia fija a un nodo: vuelve a buscar en el DOM actual cada vez
    # que se usa, así que sigue funcionando sin importar cuántas veces se
    # haya reconstruido la lista de en medio.
    expect(item_3).to_have_text("Item 3")
    assert item_3.element_handle().evaluate("el => el.isConnected") is True

import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from VirtualListPage import VirtualListPage


@pytest.fixture
def virtual_list_page(page: Page) -> VirtualListPage:
    page.goto(f"{BASE_URL}/virtual_list")
    return VirtualListPage(page)


def test_estado_inicial_solo_renderiza_las_primeras_filas_cerca_del_tope(
    virtual_list_page: VirtualListPage,
) -> None:
    primero, ultimo = virtual_list_page.rango_esperado(0, virtual_list_page.alto_de_viewport())

    expect(virtual_list_page.rango).to_have_text(
        f"Rows in the DOM: {primero} to {ultimo} of {virtual_list_page.TOTAL}"
    )
    expect(virtual_list_page.filas).to_have_count(ultimo - primero + 1)
    expect(virtual_list_page.fila(primero)).to_have_text(f"Item {primero}")
    expect(virtual_list_page.fila(ultimo)).to_have_text(f"Item {ultimo}")
    # La fila justo después del buffer calculado todavía no existe en el DOM
    # -- no alcanza con probar que "algunas" filas están, hay que confirmar
    # que el corte cae exactamente donde la fórmula de la página dice.
    expect(virtual_list_page.fila(ultimo + 1)).to_have_count(0)


def test_item_lejano_no_existe_en_el_dom_hasta_que_se_scrollea_cerca(
    virtual_list_page: VirtualListPage,
) -> None:
    # "Item 5000" no es un texto oculto por CSS: mientras no se scrollee
    # cerca, el nodo que lo contendría ni siquiera se crea.
    expect(virtual_list_page.item_por_texto("Item 5000")).to_have_count(0)

    virtual_list_page.scrollear_a(149970)  # tope del item 5000: (5000-1) * ROW

    expect(virtual_list_page.item_por_texto("Item 5000")).to_have_count(1)


def test_scrollear_saca_del_dom_las_filas_que_quedaron_lejos(
    virtual_list_page: VirtualListPage,
) -> None:
    virtual_list_page.scrollear_a(5000)

    primero, ultimo = virtual_list_page.rango_esperado(5000, virtual_list_page.alto_de_viewport())
    expect(virtual_list_page.rango).to_have_text(
        f"Rows in the DOM: {primero} to {ultimo} of {virtual_list_page.TOTAL}"
    )
    expect(virtual_list_page.filas).to_have_count(ultimo - primero + 1)
    # Item 1, que estaba en el DOM antes de scrollear, ya no está.
    expect(virtual_list_page.fila(1)).to_have_count(0)


def test_scrollear_al_fondo_no_pasa_del_total_de_items(
    virtual_list_page: VirtualListPage,
) -> None:
    virtual_list_page.scrollear_al_fondo()

    # El scroll real no llega a `scrollHeight`: el navegador lo tope a
    # `scrollHeight - clientHeight`, así que la fórmula de la página hay que
    # aplicarla sobre ese `scrollTop` real, no sobre la altura total del
    # contenido.
    primero, ultimo = virtual_list_page.rango_esperado(
        virtual_list_page.scroll_top_actual(), virtual_list_page.alto_de_viewport()
    )
    # El `min(TOTAL-1, ...)` de la página evita que el buffer final empuje
    # el rango más allá del último item real, aunque la cuenta cruda del
    # buffer (ultimo + BUFFER) lo pida.
    assert ultimo == virtual_list_page.TOTAL
    expect(virtual_list_page.rango).to_have_text(
        f"Rows in the DOM: {primero} to {ultimo} of {virtual_list_page.TOTAL}"
    )
    expect(virtual_list_page.fila(virtual_list_page.TOTAL)).to_have_text(
        f"Item {virtual_list_page.TOTAL}"
    )
    expect(virtual_list_page.fila(virtual_list_page.TOTAL + 1)).to_have_count(0)


def test_el_espacio_reservado_cubre_los_10000_items_aunque_casi_ninguno_este_renderizado(
    virtual_list_page: VirtualListPage,
) -> None:
    # El scroll "ve" una lista de 10.000 items porque el contenedor tiene la
    # altura completa reservada de antemano (TOTAL * ROW), no porque esos
    # 10.000 nodos existan: en cualquier momento la cantidad real de filas
    # en el DOM es un puñado, muy por debajo del total.
    assert (
        virtual_list_page.alto_total_del_contenido()
        == virtual_list_page.TOTAL * virtual_list_page.ROW
    )
    assert virtual_list_page.filas.count() < 50

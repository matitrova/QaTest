import pytest

from config import BASE_URL
from InfiniteScrollPage import InfiniteScrollPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py, test_shifting_content.py y
    # varios otros: el script externo de Optimizely puede colgar el evento
    # "load" si esa red está lenta o inaccesible.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_la_pagina_carga_al_menos_un_parrafo_sin_necesidad_de_scrollear(page):
    infinite_scroll_page = InfiniteScrollPage(page)
    page.goto(f"{BASE_URL}/infinite_scroll")

    assert infinite_scroll_page.cantidad_de_parrafos() >= 1


# jscroll decide si hay que pedir la próxima página mirando qué tan cerca del
# fondo del documento quedó el scroll, no si hubo "algún" scroll. Un scroll
# que se queda a mitad de página no cruza ese umbral, así que no debería
# agregar contenido nuevo -- a diferencia del scroll hasta el fondo del
# siguiente test.

def test_scrollear_sin_llegar_al_fondo_no_agrega_parrafos(page):
    infinite_scroll_page = InfiniteScrollPage(page)
    page.goto(f"{BASE_URL}/infinite_scroll")
    page.wait_for_timeout(500)
    cantidad_antes = infinite_scroll_page.cantidad_de_parrafos()

    infinite_scroll_page.scrollear_un_poco_sin_llegar_al_fondo()
    page.wait_for_timeout(1000)

    assert infinite_scroll_page.cantidad_de_parrafos() == cantidad_antes


def test_cada_scroll_hasta_el_fondo_agrega_un_parrafo_mas(page):
    infinite_scroll_page = InfiniteScrollPage(page)
    page.goto(f"{BASE_URL}/infinite_scroll")
    page.wait_for_timeout(500)

    for _ in range(3):
        cantidad_antes = infinite_scroll_page.cantidad_de_parrafos()
        infinite_scroll_page.scrollear_hasta_el_fondo()
        page.wait_for_timeout(1000)
        assert infinite_scroll_page.cantidad_de_parrafos() == cantidad_antes + 1

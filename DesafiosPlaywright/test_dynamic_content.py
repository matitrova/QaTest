from playwright.sync_api import Page

from config import BASE_URL
from DynamicContentPage import DynamicContentPage


def test_en_modo_dinamico_el_contenido_cambia_entre_recargas(page: Page) -> None:
    dynamic_content_page = DynamicContentPage(page)

    page.goto(f"{BASE_URL}/dynamic_content")
    primera_carga = [dynamic_content_page.fila(i) for i in range(dynamic_content_page.cantidad_de_filas())]

    page.goto(f"{BASE_URL}/dynamic_content")
    segunda_carga = [dynamic_content_page.fila(i) for i in range(dynamic_content_page.cantidad_de_filas())]

    assert primera_carga != segunda_carga


# La página promete "hacer estático" el contenido agregando ?with_content=static,
# pero el propio enunciado dice "to make SOME of the content static" -- no todo.
# Verificado contra el sitio real con varias recargas: las primeras dos filas
# (imagen + texto juntos) quedan exactamente fijas con ese parámetro.

def test_en_modo_estatico_las_primeras_dos_filas_quedan_fijas(page: Page) -> None:
    dynamic_content_page = DynamicContentPage(page)
    url = f"{BASE_URL}/dynamic_content?with_content=static"

    page.goto(url)
    primera_carga = [dynamic_content_page.fila(i) for i in range(2)]

    page.goto(url)
    segunda_carga = [dynamic_content_page.fila(i) for i in range(2)]

    assert primera_carga == segunda_carga


# Bug/comportamiento no documentado: a pesar del parámetro "static", la
# tercera fila sigue eligiendo imagen y texto al azar en cada recarga -- el
# sitio nunca prometió las tres, pero tampoco aclara cuántas quedan fijas.
# Como la tercera fila es aleatoria, una sola recarga no alcanza para
# demostrarlo (podría repetirse por casualidad); se recarga en un loop hasta
# encontrar dos valores distintos, el mismo patrón que ya usa este repo en
# test_shifting_content.py para probar aleatoriedad real.

def test_en_modo_estatico_la_tercera_fila_sigue_siendo_aleatoria(page: Page) -> None:
    dynamic_content_page = DynamicContentPage(page)
    url = f"{BASE_URL}/dynamic_content?with_content=static"
    terceras_filas = set()

    for _ in range(10):
        page.goto(url)
        terceras_filas.add(dynamic_content_page.fila(2))
        if len(terceras_filas) > 1:
            break

    assert len(terceras_filas) > 1


def test_el_sitio_siempre_muestra_exactamente_tres_filas(page: Page) -> None:
    dynamic_content_page = DynamicContentPage(page)

    page.goto(f"{BASE_URL}/dynamic_content")
    assert dynamic_content_page.cantidad_de_filas() == 3

    page.goto(f"{BASE_URL}/dynamic_content?with_content=static")
    assert dynamic_content_page.cantidad_de_filas() == 3

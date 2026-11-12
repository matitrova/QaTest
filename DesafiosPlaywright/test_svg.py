from playwright.sync_api import Page

from config import BASE_URL
from SvgPage import SvgPage


def test_estado_inicial_sin_nada_seleccionado(page: Page) -> None:
    svg_page = SvgPage(page)
    page.goto(f"{BASE_URL}/svg")

    assert svg_page.texto_resultado() == "Nothing selected"
    assert svg_page.barra_manzanas.get_attribute("fill") == "#334bc3"
    assert svg_page.barra_bananas.get_attribute("fill") == "#334bc3"
    assert svg_page.barra_cerezas.get_attribute("fill") == "#334bc3"
    assert svg_page.circulo.get_attribute("fill") == "#abe082"
    assert svg_page.texto_etiqueta_circulo() == "Click me"


# La página avisa que XPath necesita *[local-name()='rect'] por el namespace
# de SVG, pero eso es un problema puntual de XPath -- un selector CSS por id,
# como el que usa esta suite en todos los Page Objects, no distingue entre un
# <rect> y un <div> y encuentra el elemento sin ningún tratamiento especial.
def test_selector_css_por_id_encuentra_el_rect_sin_tratamiento_especial(page: Page) -> None:
    svg_page = SvgPage(page)
    page.goto(f"{BASE_URL}/svg")

    assert svg_page.barra_manzanas.count() == 1
    assert page.get_by_text("Bananas", exact=True).count() == 1


def test_click_en_una_barra_la_selecciona_y_muestra_su_valor(page: Page) -> None:
    svg_page = SvgPage(page)
    page.goto(f"{BASE_URL}/svg")

    svg_page.barra_bananas.click()

    assert svg_page.barra_bananas.get_attribute("fill") == "#f55524"
    assert svg_page.texto_resultado() == "Selected Bananas: 180"


# El handler de click de cada barra primero pisa el fill de las tres a
# #334bc3 y recién después pinta la que se clickeó -- clickear una segunda
# barra tiene que dejar destacada solo a esa, no a las dos.
def test_seleccionar_otra_barra_deselecciona_la_anterior(page: Page) -> None:
    svg_page = SvgPage(page)
    page.goto(f"{BASE_URL}/svg")

    svg_page.barra_manzanas.click()
    assert svg_page.barra_manzanas.get_attribute("fill") == "#f55524"

    svg_page.barra_cerezas.click()

    assert svg_page.barra_manzanas.get_attribute("fill") == "#334bc3"
    assert svg_page.barra_cerezas.get_attribute("fill") == "#f55524"
    assert svg_page.texto_resultado() == "Selected Cherries: 60"


def test_click_en_el_circulo_alterna_entre_verde_y_rojo(page: Page) -> None:
    svg_page = SvgPage(page)
    page.goto(f"{BASE_URL}/svg")

    svg_page.circulo.click()
    assert svg_page.circulo.get_attribute("fill") == "#961001"
    assert svg_page.texto_etiqueta_circulo() == "Clicked"
    assert svg_page.texto_resultado() == "Circle is red"

    svg_page.circulo.click()
    assert svg_page.circulo.get_attribute("fill") == "#abe082"
    assert svg_page.texto_etiqueta_circulo() == "Click me"
    assert svg_page.texto_resultado() == "Circle is green"


# El círculo y las barras comparten el mismo <p id="result">, pero cada
# listener solo lee y escribe su propio elemento -- clickear el círculo no
# toca el fill de ninguna barra, ni al revés.
def test_circulo_y_barras_no_se_afectan_entre_si(page: Page) -> None:
    svg_page = SvgPage(page)
    page.goto(f"{BASE_URL}/svg")

    svg_page.barra_manzanas.click()
    svg_page.circulo.click()

    assert svg_page.barra_manzanas.get_attribute("fill") == "#f55524"
    assert svg_page.circulo.get_attribute("fill") == "#961001"
    assert svg_page.texto_resultado() == "Circle is red"

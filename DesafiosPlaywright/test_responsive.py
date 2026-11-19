import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from ResponsivePage import ResponsivePage

VIEWPORT_DESKTOP = {"width": 1280, "height": 800}
VIEWPORT_MOBILE = {"width": 375, "height": 800}


@pytest.fixture
def responsive_page(page: Page) -> ResponsivePage:
    page.set_viewport_size(VIEWPORT_DESKTOP)
    page.goto(f"{BASE_URL}/responsive")
    return ResponsivePage(page)


def test_en_desktop_el_boton_hamburguesa_esta_oculto_y_el_layout_es_desktop(
    responsive_page: ResponsivePage,
) -> None:
    expect(responsive_page.boton_menu).to_be_hidden()
    expect(responsive_page.menu).to_be_visible()
    assert responsive_page.layout_actual() == "desktop"


def test_en_mobile_aparece_el_boton_hamburguesa_y_el_menu_arranca_cerrado(
    responsive_page: ResponsivePage, page: Page
) -> None:
    page.set_viewport_size(VIEWPORT_MOBILE)

    expect(responsive_page.boton_menu).to_be_visible()
    expect(responsive_page.boton_menu).to_have_attribute("aria-expanded", "false")
    expect(responsive_page.menu).to_be_hidden()
    assert responsive_page.layout_actual() == "mobile"


def test_click_en_hamburguesa_abre_el_menu_y_el_siguiente_click_lo_cierra(
    responsive_page: ResponsivePage, page: Page
) -> None:
    page.set_viewport_size(VIEWPORT_MOBILE)

    responsive_page.boton_menu.click()
    expect(responsive_page.menu).to_be_visible()
    expect(responsive_page.boton_menu).to_have_attribute("aria-expanded", "true")

    responsive_page.boton_menu.click()
    expect(responsive_page.menu).to_be_hidden()
    expect(responsive_page.boton_menu).to_have_attribute("aria-expanded", "false")


# El listener de click del nav hace dos cosas a la vez con cualquier link:
# escribe el resultado Y cierra el menú, aunque nadie haya tocado el botón
# hamburguesa después de abrirlo. En mobile eso importa porque el menú
# abierto vuelve a quedar oculto solo; en desktop (test de más abajo) el
# nav nunca estuvo oculto, así que ese cierre no cambia nada visible.

def test_click_en_un_link_del_menu_mobile_cierra_el_menu_y_actualiza_el_resultado(
    responsive_page: ResponsivePage, page: Page
) -> None:
    page.set_viewport_size(VIEWPORT_MOBILE)
    responsive_page.boton_menu.click()
    expect(responsive_page.menu).to_be_visible()

    responsive_page.link_de_menu("Products").click()

    expect(responsive_page.resultado_nav).to_have_text("You clicked Products")
    expect(responsive_page.menu).to_be_hidden()
    expect(responsive_page.boton_menu).to_have_attribute("aria-expanded", "false")


def test_en_desktop_un_click_en_el_link_actualiza_el_resultado_sin_boton_hamburguesa(
    responsive_page: ResponsivePage,
) -> None:
    responsive_page.link_de_menu("Pricing").click()

    expect(responsive_page.resultado_nav).to_have_text("You clicked Pricing")
    expect(responsive_page.menu).to_be_visible()


# El nombre del layout lo pone un pseudo-elemento CSS controlado por un
# media query (no JavaScript, no un reload): confirmar que cambia de ida y
# vuelta achicando y agrandando la misma página es la única forma de probar
# que es el viewport el que decide, no un estado que haya quedado pegado de
# una carga anterior.

def test_el_layout_cambia_de_desktop_a_mobile_y_vuelta_sin_recargar(
    responsive_page: ResponsivePage, page: Page
) -> None:
    assert responsive_page.layout_actual() == "desktop"

    page.set_viewport_size(VIEWPORT_MOBILE)
    assert responsive_page.layout_actual() == "mobile"

    page.set_viewport_size(VIEWPORT_DESKTOP)
    assert responsive_page.layout_actual() == "desktop"


def test_en_mobile_las_tarjetas_quedan_en_una_sola_columna(
    responsive_page: ResponsivePage, page: Page
) -> None:
    cajas_desktop = [box["x"] for box in (
        responsive_page.cards.nth(i).bounding_box() for i in range(3)
    )]
    # En desktop el grid es de 3 columnas: las tres tarjetas arrancan en un x distinto.
    assert len(set(cajas_desktop)) == 3

    page.set_viewport_size(VIEWPORT_MOBILE)

    cajas_mobile = [box["x"] for box in (
        responsive_page.cards.nth(i).bounding_box() for i in range(3)
    )]
    # En mobile el grid baja a 1 columna: las tres arrancan en el mismo x,
    # apiladas una debajo de la otra.
    assert len(set(cajas_mobile)) == 1

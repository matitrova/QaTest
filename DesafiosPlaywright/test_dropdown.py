from playwright.sync_api import expect

from config import BASE_URL
from DropdownPage import DropdownPage


def test_estado_inicial_es_el_placeholder(page):
    # La opción inicial ("Please select an option") está disabled en el
    # HTML -- no es una opción real, es un placeholder. Confirmar esto
    # evita que un cambio futuro la convierta en seleccionable sin que
    # nadie lo note.
    dropdown_page = DropdownPage(page)
    page.goto(f"{BASE_URL}/dropdown")

    expect(dropdown_page.dropdown).to_have_value("")


def test_seleccionar_opcion_1(page):
    dropdown_page = DropdownPage(page)
    page.goto(f"{BASE_URL}/dropdown")

    dropdown_page.seleccionar_por_valor("1")

    expect(dropdown_page.dropdown).to_have_value("1")


def test_cambiar_de_una_opcion_a_otra(page):
    # No alcanza con probar "seleccionar una opción" una sola vez --
    # también hay que confirmar que cambiar de una opción real a otra
    # (no desde el placeholder) deja el valor correcto, no el anterior.
    dropdown_page = DropdownPage(page)
    page.goto(f"{BASE_URL}/dropdown")

    dropdown_page.seleccionar_por_valor("1")
    dropdown_page.seleccionar_por_valor("2")

    expect(dropdown_page.dropdown).to_have_value("2")

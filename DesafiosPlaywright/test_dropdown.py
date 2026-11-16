import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from DropdownPage import DropdownPage


@pytest.fixture
def dropdown_page(page: Page) -> DropdownPage:
    page.goto(f"{BASE_URL}/dropdown")
    return DropdownPage(page)


def test_estado_inicial_es_el_placeholder(dropdown_page: DropdownPage) -> None:
    # La opción inicial ("Please select an option") está disabled en el
    # HTML -- no es una opción real, es un placeholder. Confirmar esto
    # evita que un cambio futuro la convierta en seleccionable sin que
    # nadie lo note.
    expect(dropdown_page.dropdown).to_have_value("")


def test_seleccionar_opcion_1(dropdown_page: DropdownPage) -> None:
    dropdown_page.seleccionar_por_valor("1")

    expect(dropdown_page.dropdown).to_have_value("1")


def test_cambiar_de_una_opcion_a_otra(dropdown_page: DropdownPage) -> None:
    # No alcanza con probar "seleccionar una opción" una sola vez --
    # también hay que confirmar que cambiar de una opción real a otra
    # (no desde el placeholder) deja el valor correcto, no el anterior.
    dropdown_page.seleccionar_por_valor("1")
    dropdown_page.seleccionar_por_valor("2")

    expect(dropdown_page.dropdown).to_have_value("2")

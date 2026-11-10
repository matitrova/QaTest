import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from MultipleDropdownPage import MultipleDropdownPage


@pytest.fixture
def multiple_dropdown_page(page: Page) -> MultipleDropdownPage:
    page.goto(f"{BASE_URL}/multiple_dropdown")
    return MultipleDropdownPage(page)


def test_ninguna_opcion_viene_tildada_al_cargar(
    multiple_dropdown_page: MultipleDropdownPage,
) -> None:
    expect(multiple_dropdown_page.opciones_tildadas()).to_have_count(0)

    for i in range(multiple_dropdown_page.opciones.count()):
        assert multiple_dropdown_page.opciones.nth(i).get_attribute("selected") is None


def test_seleccionar_varias_opciones_las_tilda_a_todas(
    multiple_dropdown_page: MultipleDropdownPage,
) -> None:
    multiple_dropdown_page.dropdown.select_option(["1", "3"])

    tildadas = multiple_dropdown_page.opciones_tildadas()
    expect(tildadas).to_have_count(2)
    assert tildadas.all_text_contents() == ["Option 1", "Option 3"]


def test_volver_a_seleccionar_destilda_las_anteriores(
    multiple_dropdown_page: MultipleDropdownPage,
) -> None:
    multiple_dropdown_page.dropdown.select_option(["1", "3"])
    expect(multiple_dropdown_page.opciones_tildadas()).to_have_count(2)

    multiple_dropdown_page.dropdown.select_option(["2"])

    tildadas = multiple_dropdown_page.opciones_tildadas()
    expect(tildadas).to_have_count(1)
    assert tildadas.all_text_contents() == ["Option 2"]


# El HTML de esta página nunca marca ninguna <option> con el atributo
# "selected" -- lo que cambia al elegir una opción es solo la propiedad
# .selected del DOM, que no se refleja en el HTML por sí sola. El propio
# listener de "change" de la página lee esa propiedad a mano y recién ahí
# agrega o quita el atributo en cada <option>, así que el atributo queda un
# paso por detrás de la propiedad real: confiar en el atributo sin que haya
# disparado el evento daría un falso negativo. select_option() de Playwright
# sí dispara "change", así que el atributo queda sincronizado después.

def test_el_atributo_selected_lo_sincroniza_a_mano_el_evento_change(
    multiple_dropdown_page: MultipleDropdownPage,
) -> None:
    opcion_1 = multiple_dropdown_page.opciones.nth(0)
    opcion_2 = multiple_dropdown_page.opciones.nth(1)

    multiple_dropdown_page.dropdown.select_option(["1"])
    assert opcion_1.get_attribute("selected") == "selected"
    assert opcion_2.get_attribute("selected") is None

    multiple_dropdown_page.dropdown.select_option(["2"])
    assert opcion_1.get_attribute("selected") is None
    assert opcion_2.get_attribute("selected") == "selected"


def test_seleccionar_las_cuatro_opciones_las_tilda_a_todas(
    multiple_dropdown_page: MultipleDropdownPage,
) -> None:
    multiple_dropdown_page.dropdown.select_option(["1", "2", "3", "4"])

    expect(multiple_dropdown_page.opciones_tildadas()).to_have_count(4)

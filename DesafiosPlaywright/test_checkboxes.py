import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from CheckboxesPage import CheckboxesPage


@pytest.fixture
def checkboxes_page(page: Page) -> CheckboxesPage:
    page.goto(f"{BASE_URL}/checkboxes")
    return CheckboxesPage(page)


def test_estado_inicial(checkboxes_page: CheckboxesPage) -> None:
    # La página arranca con el checkbox 1 destildado y el 2 tildado --
    # no es un detalle menor: si algún día alguien invierte el HTML,
    # este test lo detecta antes que los de toggle de abajo.
    expect(checkboxes_page.checkbox_1).not_to_be_checked()
    expect(checkboxes_page.checkbox_2).to_be_checked()


def test_tildar_checkbox_destildado(checkboxes_page: CheckboxesPage) -> None:
    checkboxes_page.checkbox_1.check()

    expect(checkboxes_page.checkbox_1).to_be_checked()
    # El 1 no debería afectar al 2 -- son independientes.
    expect(checkboxes_page.checkbox_2).to_be_checked()


def test_destildar_checkbox_tildado(checkboxes_page: CheckboxesPage) -> None:
    checkboxes_page.checkbox_2.uncheck()

    expect(checkboxes_page.checkbox_2).not_to_be_checked()
    expect(checkboxes_page.checkbox_1).not_to_be_checked()

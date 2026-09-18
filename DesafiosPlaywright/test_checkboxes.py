from playwright.sync_api import expect

from config import BASE_URL
from CheckboxesPage import CheckboxesPage


def test_estado_inicial(page):
    # La página arranca con el checkbox 1 destildado y el 2 tildado --
    # no es un detalle menor: si algún día alguien invierte el HTML,
    # este test lo detecta antes que los de toggle de abajo.
    checkboxes_page = CheckboxesPage(page)
    page.goto(f"{BASE_URL}/checkboxes")

    expect(checkboxes_page.checkbox_1).not_to_be_checked()
    expect(checkboxes_page.checkbox_2).to_be_checked()


def test_tildar_checkbox_destildado(page):
    checkboxes_page = CheckboxesPage(page)
    page.goto(f"{BASE_URL}/checkboxes")

    checkboxes_page.checkbox_1.check()

    expect(checkboxes_page.checkbox_1).to_be_checked()
    # El 1 no debería afectar al 2 -- son independientes.
    expect(checkboxes_page.checkbox_2).to_be_checked()


def test_destildar_checkbox_tildado(page):
    checkboxes_page = CheckboxesPage(page)
    page.goto(f"{BASE_URL}/checkboxes")

    checkboxes_page.checkbox_2.uncheck()

    expect(checkboxes_page.checkbox_2).not_to_be_checked()
    expect(checkboxes_page.checkbox_1).not_to_be_checked()

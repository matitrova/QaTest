from playwright.sync_api import expect

from config import BASE_URL
from AddRemoveElementsPage import AddRemoveElementsPage


def test_arranca_sin_elementos(page):
    add_remove_page = AddRemoveElementsPage(page)
    page.goto(f"{BASE_URL}/add_remove_elements/")

    expect(add_remove_page.botones_eliminar).to_have_count(0)


def test_agregar_un_elemento_lo_muestra(page):
    add_remove_page = AddRemoveElementsPage(page)
    page.goto(f"{BASE_URL}/add_remove_elements/")

    add_remove_page.agregar_elemento()

    expect(add_remove_page.botones_eliminar).to_have_count(1)


def test_agregar_varios_elementos_acumula(page):
    add_remove_page = AddRemoveElementsPage(page)
    page.goto(f"{BASE_URL}/add_remove_elements/")

    add_remove_page.agregar_elemento(veces=5)

    expect(add_remove_page.botones_eliminar).to_have_count(5)


def test_eliminar_uno_baja_el_contador(page):
    add_remove_page = AddRemoveElementsPage(page)
    page.goto(f"{BASE_URL}/add_remove_elements/")

    add_remove_page.agregar_elemento(veces=3)
    add_remove_page.eliminar_elemento()

    expect(add_remove_page.botones_eliminar).to_have_count(2)


def test_eliminar_todos_deja_la_lista_vacia(page):
    add_remove_page = AddRemoveElementsPage(page)
    page.goto(f"{BASE_URL}/add_remove_elements/")

    add_remove_page.agregar_elemento(veces=3)
    add_remove_page.eliminar_elemento()
    add_remove_page.eliminar_elemento()
    add_remove_page.eliminar_elemento()

    expect(add_remove_page.botones_eliminar).to_have_count(0)

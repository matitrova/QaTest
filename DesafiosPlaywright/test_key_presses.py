import pytest
from playwright.sync_api import expect

from config import BASE_URL
from KeyPressesPage import KeyPressesPage


@pytest.mark.parametrize(
    "tecla, texto_esperado",
    [
        ("a", "You entered: A"),
        ("7", "You entered: 7"),
        (" ", "You entered: SPACE"),
        ("Escape", "You entered: ESCAPE"),
        ("Backspace", "You entered: BACK_SPACE"),
        ("ArrowLeft", "You entered: LEFT"),
    ],
    ids=["letra", "digito", "espacio", "escape", "backspace", "flecha"],
)
def test_tecla_muestra_el_nombre_esperado(page, tecla, texto_esperado):
    # Cada tecla pasa por el mismo mapeo de KeyboardEvent.code a texto --
    # son seis variantes del mismo comportamiento, no seis comportamientos
    # distintos, así que un solo test parametrizado cubre los mismos casos
    # que antes vivían en seis funciones casi idénticas.
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar(tecla)

    expect(key_presses_page.resultado).to_have_text(texto_esperado)


def test_cada_tecla_pisa_el_resultado_anterior(page):
    # El handler reasigna innerHTML entero en cada keydown -- no acumula
    # texto de teclas anteriores, así que solo debe quedar la última.
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar("a")
    expect(key_presses_page.resultado).to_have_text("You entered: A")

    key_presses_page.presionar("b")
    expect(key_presses_page.resultado).to_have_text("You entered: B")


def test_enter_no_muestra_enter_sino_que_recarga_la_pagina(page):
    # A diferencia de cualquier otra tecla, Enter nunca llega a mostrarse:
    # el <input> vive solo dentro de un <form> sin ningún botón de submit,
    # y ese es justamente el caso en el que el propio navegador dispara el
    # submit implícito del formulario al presionar Enter. Como el form no
    # tiene "action" ni el input tiene "name", el submit recarga la misma
    # URL sin ningún dato -- se ve como si la tecla "no hiciera nada", pero
    # en realidad recargó la página entera y perdió lo que había escrito.
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.input.fill("hola")
    with page.expect_navigation():
        key_presses_page.input.press("Enter")

    expect(key_presses_page.resultado).to_have_text("")
    expect(key_presses_page.input).to_have_value("")

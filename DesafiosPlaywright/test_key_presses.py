from playwright.sync_api import expect

from config import BASE_URL
from KeyPressesPage import KeyPressesPage


def test_letra_muestra_su_nombre_en_mayuscula(page):
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar("a")

    expect(key_presses_page.resultado).to_have_text("You entered: A")


def test_digito_muestra_el_numero(page):
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar("7")

    expect(key_presses_page.resultado).to_have_text("You entered: 7")


def test_barra_espaciadora_muestra_space(page):
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar(" ")

    expect(key_presses_page.resultado).to_have_text("You entered: SPACE")


def test_escape_muestra_escape(page):
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar("Escape")

    expect(key_presses_page.resultado).to_have_text("You entered: ESCAPE")


def test_backspace_muestra_back_space_con_guion_bajo(page):
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar("Backspace")

    expect(key_presses_page.resultado).to_have_text("You entered: BACK_SPACE")


def test_flecha_muestra_la_direccion(page):
    key_presses_page = KeyPressesPage(page)
    page.goto(f"{BASE_URL}/key_presses")

    key_presses_page.presionar("ArrowLeft")

    expect(key_presses_page.resultado).to_have_text("You entered: LEFT")


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

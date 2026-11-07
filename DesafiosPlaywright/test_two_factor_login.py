import re

from playwright.sync_api import Page, expect

from config import BASE_URL
from TwoFactorLoginPage import TwoFactorLoginPage


def test_login_con_credenciales_invalidas_muestra_error_y_no_avanza(
    page: Page,
) -> None:
    two_factor_page = TwoFactorLoginPage(page)
    page.goto(f"{BASE_URL}/two_factor")

    two_factor_page.login("usuario_que_no_existe", "cualquier_cosa")

    expect(page).to_have_url(f"{BASE_URL}/two_factor")
    expect(two_factor_page.flash).to_contain_text(
        "Your username or password is invalid!"
    )


def test_login_correcto_pasa_a_la_pagina_del_codigo_con_un_otp_de_seis_digitos(
    page: Page,
) -> None:
    two_factor_page = TwoFactorLoginPage(page)
    page.goto(f"{BASE_URL}/two_factor")

    two_factor_page.login("tomsmith", "SuperSecretPassword!")

    expect(page).to_have_url(f"{BASE_URL}/two_factor/code")
    expect(two_factor_page.otp_code).to_be_visible()
    assert re.fullmatch(r"\d{6}", two_factor_page.leer_otp())


# El código mostrado en pantalla es el único válido en el servidor para esa
# sesión -- no hay forma de automatizar este paso leyendo un SMS real, pero
# tampoco hace falta: the-internet lo expone a propósito en el propio HTML
# para que se pueda probar el flujo completo sin un segundo canal.

def test_codigo_correcto_entra_a_la_secure_area(page: Page) -> None:
    two_factor_page = TwoFactorLoginPage(page)
    page.goto(f"{BASE_URL}/two_factor")
    two_factor_page.login("tomsmith", "SuperSecretPassword!")
    otp = two_factor_page.leer_otp()

    two_factor_page.verificar_codigo(otp)

    expect(page).to_have_url(f"{BASE_URL}/two_factor/secure")
    expect(two_factor_page.flash).to_contain_text(
        "You logged in with two-factor authentication!"
    )
    expect(two_factor_page.logout).to_be_visible()


# Un intento con un código equivocado no invalida el código real: vuelve a
# mostrar la misma página con el mismo OTP, y ese OTP sigue siendo aceptado
# después. No es "un intento y se quema", es "hasta que aciertes o expire".

def test_codigo_incorrecto_muestra_error_y_el_otp_real_sigue_sirviendo(
    page: Page,
) -> None:
    two_factor_page = TwoFactorLoginPage(page)
    page.goto(f"{BASE_URL}/two_factor")
    two_factor_page.login("tomsmith", "SuperSecretPassword!")
    otp = two_factor_page.leer_otp()

    two_factor_page.verificar_codigo("000000")

    expect(page).to_have_url(f"{BASE_URL}/two_factor/code")
    expect(two_factor_page.flash).to_contain_text("Your code is invalid!")

    two_factor_page.verificar_codigo(otp)

    expect(page).to_have_url(f"{BASE_URL}/two_factor/secure")


def test_logout_termina_la_sesion_y_vuelve_al_login(page: Page) -> None:
    two_factor_page = TwoFactorLoginPage(page)
    page.goto(f"{BASE_URL}/two_factor")
    two_factor_page.login("tomsmith", "SuperSecretPassword!")
    two_factor_page.verificar_codigo(two_factor_page.leer_otp())
    expect(page).to_have_url(f"{BASE_URL}/two_factor/secure")

    two_factor_page.logout.click()

    expect(page).to_have_url(f"{BASE_URL}/two_factor")


# Tanto la página del código como la secure area están protegidas del lado
# del servidor por la misma sesión: entrar directo a cualquiera de las dos
# sin haber iniciado el login en este mismo browser context redirige a
# /two_factor en vez de mostrar la página o fallar con 403/404.

def test_acceso_directo_a_secure_sin_sesion_redirige_a_two_factor(
    page: Page,
) -> None:
    page.goto(f"{BASE_URL}/two_factor/secure")

    expect(page).to_have_url(f"{BASE_URL}/two_factor")


def test_acceso_directo_a_code_sin_sesion_redirige_a_two_factor(page: Page) -> None:
    page.goto(f"{BASE_URL}/two_factor/code")

    expect(page).to_have_url(f"{BASE_URL}/two_factor")

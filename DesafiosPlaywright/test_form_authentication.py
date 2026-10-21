from playwright.sync_api import expect

from config import BASE_URL
from FormAuthenticationPage import FormAuthenticationPage


def test_login_con_credenciales_correctas_entra_a_la_secure_area(page):
    form_authentication_page = FormAuthenticationPage(page)
    page.goto(f"{BASE_URL}/login")

    form_authentication_page.login("tomsmith", "SuperSecretPassword!")

    expect(page).to_have_url(f"{BASE_URL}/secure")
    expect(form_authentication_page.flash).to_contain_text(
        "You logged into a secure area!"
    )
    expect(form_authentication_page.logout).to_be_visible()


def test_login_con_usuario_invalido_muestra_error_y_no_entra(page):
    form_authentication_page = FormAuthenticationPage(page)
    page.goto(f"{BASE_URL}/login")

    form_authentication_page.login("usuario_que_no_existe", "SuperSecretPassword!")

    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(form_authentication_page.flash).to_contain_text(
        "Your username is invalid!"
    )


def test_login_con_password_invalido_muestra_error_y_no_entra(page):
    form_authentication_page = FormAuthenticationPage(page)
    page.goto(f"{BASE_URL}/login")

    form_authentication_page.login("tomsmith", "password_incorrecta")

    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(form_authentication_page.flash).to_contain_text(
        "Your password is invalid!"
    )


# Con usuario Y contraseña incorrectos a la vez, el servidor solo informa el
# primer problema que encuentra (el usuario) y nunca llega a evaluar la
# contraseña: el mensaje es el mismo que con usuario inválido solo, no uno
# genérico de "credenciales incorrectas" ni los dos mensajes juntos.

def test_login_con_usuario_y_password_invalidos_prioriza_el_error_de_usuario(page):
    form_authentication_page = FormAuthenticationPage(page)
    page.goto(f"{BASE_URL}/login")

    form_authentication_page.login("usuario_que_no_existe", "password_incorrecta")

    expect(form_authentication_page.flash).to_contain_text(
        "Your username is invalid!"
    )


def test_logout_termina_la_sesion_y_vuelve_al_login(page):
    form_authentication_page = FormAuthenticationPage(page)
    page.goto(f"{BASE_URL}/login")
    form_authentication_page.login("tomsmith", "SuperSecretPassword!")
    expect(page).to_have_url(f"{BASE_URL}/secure")

    form_authentication_page.logout.click()

    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(form_authentication_page.flash).to_contain_text(
        "You logged out of the secure area!"
    )


# La protección de /secure es del servidor, no un router del lado del cliente:
# entrar ahí a mano, sin haber iniciado sesión antes en este mismo browser
# context (sin cookie de sesión), redirige a /login en vez de mostrar la
# página o un 403/404.

def test_acceso_directo_a_secure_sin_sesion_redirige_a_login(page):
    page.goto(f"{BASE_URL}/secure")

    expect(page).to_have_url(f"{BASE_URL}/login")

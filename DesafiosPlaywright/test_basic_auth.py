import pytest
import requests

from config import BASE_URL
from BasicAuthPage import BasicAuthPage


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    # HTTP Basic Auth es un diálogo nativo del navegador, no un dialog de JS:
    # no hay ningún "accept()" posible una vez que page.goto() ya disparó el
    # pedido, se queda esperando una interacción que Playwright no puede dar.
    # Las credenciales tienen que estar puestas en el contexto ANTES de
    # navegar, extendiendo el fixture de pytest-playwright en vez de pasarlas
    # por la URL (que Chromium ignora en navegación de primer nivel).
    return {
        **browser_context_args,
        "http_credentials": {"username": "admin", "password": "admin"},
    }


def test_credenciales_correctas_muestran_felicitacion(page):
    basic_auth_page = BasicAuthPage(page)
    page.goto(f"{BASE_URL}/basic_auth")

    assert "Congratulations" in basic_auth_page.mensaje_exito.inner_text()


def test_sin_credenciales_devuelve_401():
    # Se prueba con requests, no con el navegador: sin credenciales en el
    # contexto, el propio Chromium abriría su diálogo nativo de usuario y
    # contraseña y colgaría el test esperando una respuesta que nunca llega.
    respuesta = requests.get(f"{BASE_URL}/basic_auth")

    assert respuesta.status_code == 401


def test_credenciales_incorrectas_devuelven_401():
    respuesta = requests.get(f"{BASE_URL}/basic_auth", auth=("admin", "incorrecta"))

    assert respuesta.status_code == 401


def test_credenciales_correctas_devuelven_200():
    respuesta = requests.get(f"{BASE_URL}/basic_auth", auth=("admin", "admin"))

    assert respuesta.status_code == 200
    assert "Congratulations" in respuesta.text

import pytest
import requests
from playwright.sync_api import Error, Page, expect
from requests.auth import HTTPDigestAuth

from config import BASE_URL
from DigestAuthPage import DigestAuthPage


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args: dict) -> dict:
    # Al igual que Basic Auth, las credenciales tienen que estar puestas en
    # el contexto ANTES de navegar: Chromium resuelve todo el intercambio de
    # Digest (nonce, realm, qop) por su cuenta, Playwright solo le pasa el
    # usuario y contraseña con los que responder al challenge.
    return {
        **browser_context_args,
        "http_credentials": {"username": "admin", "password": "admin"},
    }


def test_credenciales_correctas_muestran_felicitacion(page: Page) -> None:
    digest_auth_page = DigestAuthPage(page)
    page.goto(f"{BASE_URL}/digest_auth")

    expect(digest_auth_page.mensaje_exito).to_contain_text("Congratulations")


def test_sin_credenciales_la_navegacion_falla_en_vez_de_colgarse(page: Page) -> None:
    # A diferencia de Basic Auth -- donde ir sin credenciales deja pendiente
    # un diálogo nativo que nunca se resuelve y hay que probarlo con requests
    # en su lugar --, Digest Auth sin credenciales en el contexto hace que
    # Chromium aborte la navegación de inmediato con un error de red, porque
    # no tiene con qué responder al challenge del servidor.
    context = page.context.browser.new_context()
    pagina_sin_auth = context.new_page()

    with pytest.raises(Error, match="ERR_INVALID_AUTH_CREDENTIALS"):
        pagina_sin_auth.goto(f"{BASE_URL}/digest_auth")

    context.close()


def test_credenciales_incorrectas_fallan_con_un_error_de_red_distinto(
    page: Page,
) -> None:
    # Con credenciales (aunque sean incorrectas) Chromium sí completa el
    # intercambio Digest y manda la respuesta al challenge -- el servidor la
    # rechaza con 401, y eso se ve en Playwright como un error de red
    # diferente al del caso sin credenciales: no es que falte con qué
    # responder, es que la respuesta que se mandó no vale.
    context = page.context.browser.new_context(
        http_credentials={"username": "admin", "password": "incorrecta"}
    )
    pagina_con_auth_mala = context.new_page()

    with pytest.raises(Error, match="ERR_HTTP_RESPONSE_CODE_FAILURE"):
        pagina_con_auth_mala.goto(f"{BASE_URL}/digest_auth")

    context.close()


def test_sin_credenciales_con_requests_devuelve_401() -> None:
    respuesta = requests.get(f"{BASE_URL}/digest_auth")

    assert respuesta.status_code == 401


def test_el_www_authenticate_pide_el_esquema_digest() -> None:
    respuesta = requests.get(f"{BASE_URL}/digest_auth")

    assert respuesta.headers["WWW-Authenticate"].startswith("Digest ")


def test_pasar_un_tuple_de_usuario_y_contrasena_se_interpreta_como_basic_y_da_400() -> None:
    # requests usa HTTPBasicAuth por default cuando `auth` es un tuple. Contra
    # un endpoint que espera Digest, eso manda un header Authorization con el
    # esquema que el servidor no pidió -- ni siquiera llega a evaluar la
    # contraseña, devuelve 400 en vez del 401 de credenciales rechazadas.
    respuesta = requests.get(f"{BASE_URL}/digest_auth", auth=("admin", "admin"))

    assert respuesta.status_code == 400


def test_credenciales_incorrectas_con_digest_devuelven_401() -> None:
    respuesta = requests.get(
        f"{BASE_URL}/digest_auth", auth=HTTPDigestAuth("admin", "incorrecta")
    )

    assert respuesta.status_code == 401


def test_credenciales_correctas_con_digest_devuelven_200() -> None:
    respuesta = requests.get(
        f"{BASE_URL}/digest_auth", auth=HTTPDigestAuth("admin", "admin")
    )

    assert respuesta.status_code == 200
    assert "Congratulations" in respuesta.text

import pytest
from playwright.sync_api import expect

from config import BASE_URL
from ForgotPasswordPage import ForgotPasswordPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en el resto de la suite: el script externo de
    # Optimizely puede colgar el evento "load" si esa red está lenta o
    # inaccesible.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


# El campo de este formulario es <input type="text">, no type="email": el
# propio HTML no le pide al navegador ninguna validación de formato. Cualquier
# string se manda tal cual al servidor, así que un email con formato inválido
# no se puede distinguir de uno válido en el cliente -- hay que mandarlo y ver
# qué devuelve el servidor en los dos casos.

def test_el_campo_email_no_tiene_validacion_de_formato_html(page):
    page.goto(f"{BASE_URL}/forgot_password")

    assert page.locator("#email").get_attribute("type") == "text"


# El formulario responde 500 Internal Server Error con cualquier email que
# tenga forma de email, sin importar que sea uno real. No hay ningún mensaje
# de "te enviamos un correo" que esta página pueda mostrar en los hechos.

def test_envio_con_email_valido_responde_500(page):
    forgot_password_page = ForgotPasswordPage(page)
    page.goto(f"{BASE_URL}/forgot_password")

    response = forgot_password_page.enviar("usuario@example.com")

    assert response.status == 500
    expect(forgot_password_page.titulo_resultado).to_have_text(
        "Internal Server Error"
    )


# El 500 no depende de que el email tenga mala forma: pasa igual con el campo
# vacío. Si el error fuera por una validación de formato que el servidor
# hiciera mal, un campo vacío debería fallar distinto (o antes) que un email
# con "@" -- en cambio, el resultado es idéntico en los dos casos, lo que
# descarta que sea un problema de parseo del valor ingresado.

def test_envio_con_email_vacio_tambien_responde_500(page):
    forgot_password_page = ForgotPasswordPage(page)
    page.goto(f"{BASE_URL}/forgot_password")

    response = forgot_password_page.enviar("")

    assert response.status == 500
    expect(forgot_password_page.titulo_resultado).to_have_text(
        "Internal Server Error"
    )


# Mismo resultado con un string que ni siquiera tiene forma de email (sin "@"
# ni dominio): los tres casos -- válido, vacío, basura -- dan exactamente el
# mismo 500, lo que confirma que el formulario está roto en el servidor para
# cualquier input, no solo para casos límite de validación.

def test_envio_con_texto_sin_forma_de_email_tambien_responde_500(page):
    forgot_password_page = ForgotPasswordPage(page)
    page.goto(f"{BASE_URL}/forgot_password")

    response = forgot_password_page.enviar("esto no es un email")

    assert response.status == 500
    expect(forgot_password_page.titulo_resultado).to_have_text(
        "Internal Server Error"
    )

import pytest
from playwright.sync_api import expect

from config import BASE_URL
from NotificationMessagePage import NotificationMessagePage

MENSAJES_CONOCIDOS = {
    "Action unsuccesful, please try again",
    "Action successful",
}


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py y test_context_menu.py: el
    # script externo de Optimizely puede colgar el evento "load".
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


# Cada visita a /notification_message elige uno de los dos mensajes al azar
# y redirige a /notification_message_rendered -- no hay forma de pedir "el
# mensaje de éxito" puntualmente, así que el test solo puede afirmar que el
# mensaje que aparece es uno de los dos conocidos, no cuál de los dos.

def test_mensaje_es_uno_de_los_dos_conocidos(page):
    notification_page = NotificationMessagePage(page)
    page.goto(f"{BASE_URL}/notification_message")

    assert notification_page.texto_flash() in MENSAJES_CONOCIDOS


# El mensaje de error tiene un typo en el sitio real ("unsuccesful", sin la
# segunda "s" de "success") -- se prueba tal cual está publicado, no la
# ortografía correcta, porque es lo que un usuario real ve.

def test_mensaje_de_error_tiene_el_typo_del_sitio(page):
    notification_page = NotificationMessagePage(page)

    for _ in range(15):
        page.goto(f"{BASE_URL}/notification_message")
        texto = notification_page.texto_flash()
        if texto == "Action unsuccesful, please try again":
            return

    pytest.skip("El sitio no mostró el mensaje de error en 15 intentos al azar")


# Bug del sitio: el mensaje de éxito y el de error comparten exactamente la
# misma clase CSS ("flash notice"), sin ninguna clase adicional que los
# distinga (a diferencia de otros sitios que usarían "flash success" /
# "flash error"). Un test que solo verificara la clase para saber si la
# acción fue exitosa siempre daría el mismo resultado, sin importar el
# mensaje real. Se recolectan ambas variantes visitando la página varias
# veces y se confirma que las dos comparten clase.

def test_clase_no_distingue_exito_de_error(page):
    notification_page = NotificationMessagePage(page)
    clases_por_mensaje = {}

    for _ in range(15):
        page.goto(f"{BASE_URL}/notification_message")
        clases_por_mensaje[notification_page.texto_flash()] = notification_page.clase_flash()
        if len(clases_por_mensaje) == len(MENSAJES_CONOCIDOS):
            break

    assert set(clases_por_mensaje) == MENSAJES_CONOCIDOS
    assert len(set(clases_por_mensaje.values())) == 1


def test_cerrar_mensaje_lo_oculta(page):
    notification_page = NotificationMessagePage(page)
    page.goto(f"{BASE_URL}/notification_message")

    assert notification_page.flash.is_visible()
    notification_page.cerrar()

    # El cierre no es instantáneo: Foundation le aplica un fadeOut de 300ms
    # antes de sacarlo del DOM, así que hay que esperarlo con expect() en vez
    # de verificar la visibilidad ni bien se hace clic.
    expect(notification_page.flash).to_be_hidden()

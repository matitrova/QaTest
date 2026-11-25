import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from WebsocketPage import WebsocketPage


@pytest.fixture
def websocket_page(page: Page) -> WebsocketPage:
    page.goto(f"{BASE_URL}/websocket")
    ws_page = WebsocketPage(page)
    ws_page.conectar()
    ws_page.esperar_conectado()
    return ws_page


def test_estado_inicial_desconectado_con_los_controles_bloqueados(page: Page) -> None:
    ws_page = WebsocketPage(page)
    page.goto(f"{BASE_URL}/websocket")

    expect(ws_page.connection_status).to_have_text("Disconnected")
    expect(ws_page.connect_button).to_be_enabled()
    expect(ws_page.disconnect_button).to_be_disabled()
    expect(ws_page.message_input).to_be_disabled()
    expect(ws_page.send_button).to_be_disabled()
    expect(ws_page.messages).to_have_count(0)


# El propio handler de "connect" deshabilita el botón de forma síncrona,
# en la misma línea que dispara el WebSocket -- antes de que exista
# ninguna confirmación real de que el socket terminó de abrir.
def test_conectar_deshabilita_el_boton_antes_de_terminar_de_conectar(
    page: Page,
) -> None:
    ws_page = WebsocketPage(page)
    page.goto(f"{BASE_URL}/websocket")

    ws_page.conectar()
    expect(ws_page.connect_button).to_be_disabled()

    ws_page.esperar_conectado()
    expect(ws_page.disconnect_button).to_be_enabled()
    expect(ws_page.message_input).to_be_enabled()
    expect(ws_page.send_button).to_be_enabled()
    assert page.evaluate("document.activeElement.id") == "message"


# El servidor manda un mensaje de bienvenida apenas se abre la conexión,
# antes de que el usuario escriba nada -- el único li que existe al llegar
# a "Connected" no es un eco de nada que se haya mandado.
def test_al_conectar_llega_un_mensaje_de_bienvenida_del_servidor(
    websocket_page: WebsocketPage,
) -> None:
    expect(websocket_page.messages).to_have_count(1)
    expect(websocket_page.ultimo_mensaje()).to_have_text(
        "Connected. Send a message and the server sends it back."
    )


# El mensaje de bienvenida usa la misma clase CSS ("message received") que
# el eco de un mensaje real -- no hay ningún atributo que distinga "esto lo
# mandó el servidor espontáneamente" de "esto es el eco de lo que mandé yo".
# Un test que confiara en la clase para saber el origen del mensaje no
# podría distinguir uno del otro.
def test_el_mensaje_de_bienvenida_comparte_clase_css_con_el_eco(
    websocket_page: WebsocketPage,
) -> None:
    bienvenida_class = websocket_page.ultimo_mensaje().get_attribute("class")

    websocket_page.enviar_mensaje("hola")
    expect(websocket_page.messages).to_have_count(3)

    eco_class = websocket_page.ultimo_mensaje().get_attribute("class")
    assert bienvenida_class == eco_class == "message received"


def test_enviar_un_mensaje_lo_agrega_como_sent_y_llega_el_eco_como_received(
    websocket_page: WebsocketPage,
) -> None:
    websocket_page.enviar_mensaje("hola servidor")

    expect(websocket_page.messages).to_have_count(3)
    textos = websocket_page.textos_mensajes()
    assert textos[1] == "hola servidor"
    assert textos[2] == "Echo: hola servidor"

    sent_class = websocket_page.messages.nth(1).get_attribute("class")
    received_class = websocket_page.messages.nth(2).get_attribute("class")
    assert sent_class == "message sent"
    assert received_class == "message received"
    expect(websocket_page.message_input).to_have_value("")


# El propio handler de submit del formulario corta en seco con
# `if (... || input.value === '') return;` -- un envío con el campo vacío
# no llega a mandar nada por el socket ni a agregar ningún mensaje nuevo,
# a diferencia de un mensaje con contenido real.
def test_enviar_con_el_input_vacio_no_agrega_ningun_mensaje(
    websocket_page: WebsocketPage,
) -> None:
    websocket_page.send_button.click()

    page = websocket_page.page
    page.wait_for_timeout(300)
    expect(websocket_page.messages).to_have_count(1)


def test_desconectar_manualmente_muestra_el_codigo_y_la_razon(
    websocket_page: WebsocketPage,
) -> None:
    websocket_page.desconectar()

    expect(websocket_page.connection_status).to_have_text(
        "Disconnected (code 1000: Closed by the page)"
    )
    expect(websocket_page.connect_button).to_be_enabled()
    expect(websocket_page.disconnect_button).to_be_disabled()
    expect(websocket_page.message_input).to_be_disabled()
    expect(websocket_page.send_button).to_be_disabled()


# El enunciado de la página promete que el servidor corta la conexión si
# un mensaje supera los 1000 caracteres. El mensaje de más de mil
# caracteres sí se agrega localmente como "sent" -- el cliente lo muestra
# antes de enterarse de que el servidor lo va a rechazar -- pero nunca
# llega su eco: el servidor cierra la conexión en cambio.
def test_un_mensaje_de_mas_de_mil_caracteres_cierra_la_conexion(
    websocket_page: WebsocketPage,
) -> None:
    websocket_page.enviar_mensaje("x" * 1001)

    websocket_page.esperar_desconectado()
    expect(websocket_page.connection_status).to_have_text(
        "Disconnected (code 1009: WebSocket frame length too large)"
    )
    expect(websocket_page.messages).to_have_count(2)
    assert websocket_page.ultimo_mensaje().get_attribute("class") == "message sent"


# El enunciado también promete un límite de 100 mensajes por conexión.
# Llegar justo a ese número cierra la conexión con un código y una razón
# distintos a los del mensaje demasiado largo -- dos formas distintas de
# que el servidor corte, cada una con su propio texto.
def test_el_limite_de_cien_mensajes_cierra_la_conexion(
    websocket_page: WebsocketPage,
) -> None:
    for indice in range(100):
        websocket_page.enviar_mensaje(f"mensaje {indice}")

    websocket_page.esperar_desconectado()
    expect(websocket_page.connection_status).to_have_text(
        "Disconnected (code 1000: Message limit (100) reached)"
    )
    expect(websocket_page.send_button).to_be_disabled()
    expect(websocket_page.connect_button).to_be_enabled()


# Al conectar, el propio script vacía "#messages" (`messages.innerHTML =
# ''`) antes de abrir el socket nuevo -- una reconexión no acumula los
# mensajes de la conexión anterior, arranca una lista completamente nueva.
def test_reconectar_despues_de_desconectar_limpia_los_mensajes_anteriores(
    websocket_page: WebsocketPage,
) -> None:
    websocket_page.enviar_mensaje("antes de desconectar")
    expect(websocket_page.messages).to_have_count(3)

    websocket_page.desconectar()
    websocket_page.esperar_desconectado()

    websocket_page.conectar()
    websocket_page.esperar_conectado()

    expect(websocket_page.messages).to_have_count(1)
    expect(websocket_page.ultimo_mensaje()).to_have_text(
        "Connected. Send a message and the server sends it back."
    )

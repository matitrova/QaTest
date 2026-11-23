import uuid

import pytest
from playwright.sync_api import Browser, Page, expect

from config import BASE_URL
from ChatPage import ChatPage


def _room() -> str:
    # El propio sitio recomienda usar una sala al azar en tests que corren en
    # paralelo, para que no se mezclen los mensajes de corridas distintas.
    return f"qa-{uuid.uuid4().hex[:10]}"


@pytest.fixture
def chat_page(page: Page) -> ChatPage:
    page.goto(f"{BASE_URL}/chat?room={_room()}")
    chat = ChatPage(page)
    chat.esperar_conectado()
    return chat


def test_controles_estan_deshabilitados_hasta_conectar_y_unirse(page: Page) -> None:
    chat = ChatPage(page)
    page.goto(f"{BASE_URL}/chat?room={_room()}")

    # Antes de que el WebSocket termine de conectar, ni siquiera el botón de
    # unirse está habilitado.
    expect(chat.join_button).to_be_disabled()
    expect(chat.message_input).to_be_disabled()
    expect(chat.send_button).to_be_disabled()

    chat.esperar_conectado()

    # Ya conectado pero sin nombre puesto todavía, se puede escribir el
    # nombre pero no mandar mensajes.
    expect(chat.join_button).to_be_enabled()
    expect(chat.name_input).to_be_enabled()
    expect(chat.message_input).to_be_disabled()
    expect(chat.send_button).to_be_disabled()

    chat.unirse("Ana")

    # Una vez adentro, el campo de nombre y el botón de unirse se bloquean
    # (no se puede cambiar de nombre sin recargar) y se habilita el chat.
    expect(chat.name_input).to_be_disabled()
    expect(chat.join_button).to_be_disabled()
    expect(chat.message_input).to_be_enabled()
    expect(chat.send_button).to_be_enabled()


def test_dos_usuarios_en_la_misma_sala_se_ven_los_mensajes(browser: Browser) -> None:
    room = _room()
    contexto_ana = browser.new_context()
    contexto_beto = browser.new_context()
    page_ana = contexto_ana.new_page()
    page_beto = contexto_beto.new_page()

    try:
        page_ana.goto(f"{BASE_URL}/chat?room={room}")
        page_beto.goto(f"{BASE_URL}/chat?room={room}")

        chat_ana = ChatPage(page_ana)
        chat_beto = ChatPage(page_beto)
        chat_ana.esperar_conectado()
        chat_beto.esperar_conectado()

        chat_ana.unirse("Ana")
        expect(chat_ana.ultimo_mensaje()).to_have_text("Ana joined")

        chat_beto.unirse("Beto")

        # El que se une ve su propio aviso de "joined", y el que ya estaba
        # también lo recibe.
        expect(chat_beto.ultimo_mensaje()).to_have_text("Beto joined")
        expect(chat_ana.ultimo_mensaje()).to_have_text("Beto joined")

        chat_ana.enviar_mensaje("hola Beto")

        # El mensaje llega a los dos, autor incluido -- al que lo manda
        # también, porque el servidor lo reenvía a todos los de la sala.
        expect(chat_beto.ultimo_mensaje()).to_have_text("Ana: hola Beto")
        expect(chat_ana.ultimo_mensaje()).to_have_text("Ana: hola Beto")
    finally:
        contexto_ana.close()
        contexto_beto.close()


def test_salas_distintas_no_comparten_mensajes(browser: Browser) -> None:
    contexto_1 = browser.new_context()
    contexto_2 = browser.new_context()
    page_1 = contexto_1.new_page()
    page_2 = contexto_2.new_page()

    try:
        page_1.goto(f"{BASE_URL}/chat?room={_room()}")
        page_2.goto(f"{BASE_URL}/chat?room={_room()}")

        chat_1 = ChatPage(page_1)
        chat_2 = ChatPage(page_2)
        chat_1.esperar_conectado()
        chat_2.esperar_conectado()

        chat_1.unirse("Ana")
        chat_2.unirse("Carla")
        chat_1.enviar_mensaje("mensaje que no debería cruzar de sala")

        # Como las salas son independientes, Carla nunca ve ni a Ana ni su
        # mensaje -- su único mensaje sigue siendo el aviso de su propia
        # llegada.
        page_2.wait_for_timeout(1000)
        assert chat_2.textos_mensajes() == ["Carla joined"]
    finally:
        contexto_1.close()
        contexto_2.close()


def test_avisa_cuando_alguien_se_va(browser: Browser) -> None:
    room = _room()
    contexto_ana = browser.new_context()
    contexto_beto = browser.new_context()
    page_ana = contexto_ana.new_page()
    page_beto = contexto_beto.new_page()

    try:
        page_ana.goto(f"{BASE_URL}/chat?room={room}")
        page_beto.goto(f"{BASE_URL}/chat?room={room}")

        chat_ana = ChatPage(page_ana)
        chat_beto = ChatPage(page_beto)
        chat_ana.esperar_conectado()
        chat_beto.esperar_conectado()

        chat_ana.unirse("Ana")
        chat_beto.unirse("Beto")
        expect(chat_ana.ultimo_mensaje()).to_have_text("Beto joined")

        # Cerrar la página (no solo navegar afuera) cierra el socket al
        # toque, así que el resto de la sala se entera enseguida.
        contexto_beto.close()

        expect(chat_ana.ultimo_mensaje()).to_have_text("Beto left", timeout=5000)
    finally:
        contexto_ana.close()


def test_el_mensaje_se_muestra_como_texto_plano_no_como_html(chat_page: ChatPage) -> None:
    chat_page.unirse("Ana")
    chat_page.enviar_mensaje("<b>hola</b> mundo")

    ultimo = chat_page.ultimo_mensaje()
    # El propio código de la página arma los mensajes con textContent, nunca
    # con innerHTML -- por eso las etiquetas llegan escapadas y se leen tal
    # cual se escribieron, no interpretadas como HTML real.
    expect(ultimo).to_have_text("Ana: <b>hola</b> mundo")
    assert "<b>" not in ultimo.inner_html()
    assert "&lt;b&gt;" in ultimo.inner_html()


def test_limites_de_longitud_de_nombre_y_mensaje(chat_page: ChatPage) -> None:
    # Límites impuestos por el atributo HTML maxlength, documentados en el
    # propio enunciado de la página (30 y 500 caracteres).
    assert chat_page.name_input.get_attribute("maxlength") == "30"
    assert chat_page.message_input.get_attribute("maxlength") == "500"

    chat_page.name_input.fill("x" * 50)
    assert len(chat_page.name_input.input_value()) == 30

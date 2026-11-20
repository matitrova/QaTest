import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from NetworkConsolePage import NetworkConsolePage


@pytest.fixture
def network_console_page(page: Page) -> NetworkConsolePage:
    page.goto(f"{BASE_URL}/network_console")
    return NetworkConsolePage(page)


def test_fetch_json_dispara_un_request_real_y_logea_la_respuesta(
    network_console_page: NetworkConsolePage,
) -> None:
    page = network_console_page.page
    with page.expect_response(
        lambda response: response.url.endswith("/network_console/data")
    ) as info:
        network_console_page.fetch_json_button.click()

    assert info.value.status == 200
    entrada = network_console_page.entrada_de_log("fetch-json")
    expect(entrada).to_have_text('Fetched JSON: {"fruit":"apple","count":3}')


# fetch() nunca rechaza su promesa por un status HTTP de error, solo por una
# falla de red -- el propio then() de la página sigue corriendo igual con un
# 500 que con un 200, así que "la página loguea la respuesta" no implica que
# el pedido haya salido bien.
def test_fetch_que_falla_devuelve_500_y_la_pagina_lo_logea_igual(
    network_console_page: NetworkConsolePage,
) -> None:
    page = network_console_page.page
    with page.expect_response(
        lambda response: response.url.endswith("/status_codes/500")
    ) as info:
        network_console_page.fetch_error_button.click()

    assert info.value.status == 500
    entrada = network_console_page.entrada_de_log("fetch-error")
    expect(entrada).to_have_text("Request failed with status 500")


def test_log_console_emite_log_warning_y_error_en_la_consola_real(
    network_console_page: NetworkConsolePage,
) -> None:
    page = network_console_page.page
    mensajes = []
    # El fixture autouse que aborta el script de Optimizely (conftest.py) le
    # hace creer al navegador que ese recurso falló de verdad, así que
    # también mete su propio "Failed to load resource" en la consola en
    # algún momento impredecible de la carga -- se filtra por el prefijo
    # propio de esta página para no depender de en qué orden lleguen los dos.
    page.on(
        "console",
        lambda msg: mensajes.append((msg.type, msg.text))
        if msg.text.startswith("the-internet:")
        else None,
    )

    network_console_page.log_console_button.click()

    entrada = network_console_page.entrada_de_log("log-console")
    expect(entrada).to_have_text("Logged a message, a warning and an error")
    assert mensajes == [
        ("log", "the-internet: a log message"),
        ("warning", "the-internet: a warning"),
        ("error", "the-internet: an error message"),
    ]


# El error se tira dentro de un setTimeout, así que escapa al try/catch de
# cualquier código síncrono alrededor del click -- la única forma de
# atraparlo desde afuera es un listener de "pageerror" en el Page, igual que
# haría un monitor de errores en producción. El propio texto que la página
# termina mostrando en pantalla no es el mismo que ese listener recibe: el
# "message" del ErrorEvent del navegador ya viene con el prefijo "Uncaught"
# puesto por el motor, y el script de la página le suma su propio "Uncaught
# error: " antes de loguearlo, así que en pantalla la palabra queda escrita
# dos veces con mayúscula distinta mientras que lo que de verdad cruzó al
# listener de Playwright es solo el mensaje del Error, sin ningún "Uncaught".
def test_throw_error_se_captura_como_pageerror_real_antes_de_que_la_pagina_lo_logee(
    network_console_page: NetworkConsolePage,
) -> None:
    page = network_console_page.page
    errores = []
    page.on("pageerror", lambda exc: errores.append(str(exc)))

    network_console_page.throw_error_button.click()

    entrada = network_console_page.entrada_de_log("throw-error")
    expect(entrada).to_have_text(
        "Uncaught error: Uncaught Error: the-internet: thrown on purpose"
    )
    assert errores == ["the-internet: thrown on purpose"]


# La página se sirve con Content-Security-Policy-Report-Only, no con
# Content-Security-Policy -- la diferencia es justamente que "Report-Only"
# nunca bloquea nada, solo avisa, así que el botón dispara el evento
# "securitypolicyviolation" (se loguea la violación) sin que el navegador
# llegue a frenar el <img>. La imagen termina en error igual, pero por una
# razón totalmente distinta y verificable aparte: el base64 que usa la
# página es un GIF truncado a propósito (le faltan los datos de imagen y el
# trailer), no un recurso bloqueado -- así que naturalWidth se queda en 0
# y la consola solo tira el "Failed to load resource" genérico de un
# decode fallido, nunca el mensaje de "Refused to load" que el navegador
# usa cuando de verdad frena algo por CSP.
def test_csp_violation_se_reporta_pero_no_bloquea_el_recurso_por_ser_report_only(
    page: Page,
) -> None:
    network_console_page = NetworkConsolePage(page)
    respuesta = page.goto(f"{BASE_URL}/network_console")

    assert (
        respuesta.headers.get("content-security-policy-report-only")
        == "img-src 'self'"
    )
    assert respuesta.headers.get("content-security-policy") is None

    errores_de_consola = []
    page.on(
        "console",
        lambda msg: errores_de_consola.append(msg.text)
        if msg.type == "error"
        else None,
    )

    network_console_page.csp_violation_button.click()

    entrada = network_console_page.entrada_de_log("csp-violation")
    expect(entrada).to_have_text("CSP violation: img-src (data)")

    imagen = network_console_page.event_log.locator("img")
    expect(imagen).to_have_count(1)
    page.wait_for_function(
        "() => { const img = document.querySelector('#event-log img');"
        " return img && img.complete; }"
    )
    assert imagen.evaluate("img => img.naturalWidth") == 0
    assert not any(
        "Content Security Policy" in texto or "Refused to load" in texto
        for texto in errores_de_consola
    )

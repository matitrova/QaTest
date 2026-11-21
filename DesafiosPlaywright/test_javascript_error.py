import re

from playwright.sync_api import Page

from config import BASE_URL
from JavascriptErrorPage import JavascriptErrorPage

MENSAJE_ESPERADO = re.compile(r"Cannot read propert(y|ies) .*(xyz|undefined)", re.IGNORECASE)


def test_el_error_se_captura_si_el_listener_se_registra_antes_de_navegar(
    page: Page,
) -> None:
    # El <body onload="loadError()"> de esta página llama a
    # document.propertyThatDoesNotExist.xyz, que explota apenas termina de
    # cargar -- antes de que el test tenga chance de hacer nada con la
    # página. Si el listener ya está puesto desde antes del goto(), lo
    # agarra igual: pageerror no es un evento que dependa de un timing fino
    # del lado del test, Playwright lo guarda y lo entrega al handler que
    # haya, sin importar si terminó de registrarse unos milisegundos antes.
    errores = []
    page.on("pageerror", lambda exc: errores.append(str(exc)))

    page.goto(f"{BASE_URL}/javascript_error")

    assert len(errores) == 1
    assert MENSAJE_ESPERADO.search(errores[0])


def test_el_mismo_error_se_pierde_si_el_listener_se_registra_despues_de_navegar(
    page: Page,
) -> None:
    # goto() por default espera el evento "load" de la página -- y el error
    # del onload ya se disparó y terminó *dentro* de ese mismo evento, antes
    # de que goto() le devuelva el control al test. Un listener de
    # pageerror registrado después de ese punto llegó tarde: no hay forma
    # de "re-escuchar" un error que ya pasó, así que queda sin ver nada,
    # aunque la página sea exactamente la misma que en el test de arriba.
    page.goto(f"{BASE_URL}/javascript_error")

    errores = []
    page.on("pageerror", lambda exc: errores.append(str(exc)))
    page.wait_for_timeout(300)

    assert errores == []


def test_la_excepcion_no_llega_como_mensaje_de_consola(page: Page) -> None:
    # pageerror y console son dos canales distintos de Playwright para dos
    # cosas distintas: "console" refleja llamadas reales a console.log/
    # warn/error desde el JS de la página, mientras que "pageerror" refleja
    # excepciones no atrapadas. Esta página nunca llama a console.error --
    # lanza una excepción real -- así que un test que sólo mire "console"
    # buscando errores de JS se queda sin ver nada, aunque la página esté
    # rompiendo en cada carga.
    mensajes_consola = []
    page.on("console", lambda msg: mensajes_consola.append(msg.type))

    page.goto(f"{BASE_URL}/javascript_error")
    page.wait_for_timeout(300)

    assert mensajes_consola == []


def test_el_error_del_onload_no_impide_que_el_contenido_se_vea(page: Page) -> None:
    # La excepción interrumpe el resto de la función loadError(), pero no
    # el renderizado del documento en sí -- el <body> ya estaba armado por
    # el HTML antes de que el navegador dispare onload. El párrafo se ve
    # igual de bien que si la página no tuviera ningún error.
    javascript_error_page = JavascriptErrorPage(page)

    page.goto(f"{BASE_URL}/javascript_error")

    assert page.title() == "Page with JavaScript errors on load"
    assert "error in the onload event" in javascript_error_page.parrafo.inner_text()

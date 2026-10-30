import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from HiddenLayersPage import HiddenLayersPage


def test_boton_verde_arranca_visible_y_sin_boton_azul(hidden_layers_page):
    assert hidden_layers_page.boton_verde.get_attribute("class") == HiddenLayersPage.CLASE_BOTON_VERDE
    assert hidden_layers_page.boton_azul.count() == 0


def test_click_en_boton_verde_agrega_un_boton_azul_en_las_mismas_coordenadas(hidden_layers_page):
    hidden_layers_page.clickear_boton_verde()

    # El handler de la página no reemplaza al botón verde: agrega un nuevo
    # `<div class="spa-view">` con `#blueButton` y un z-index más alto
    # dentro del mismo contenedor `position: relative`. Como ambos
    # `.spa-view` son `position: absolute; top: 0`, el botón nuevo queda
    # exactamente en el mismo lugar que el verde, tapándolo, en vez de
    # aparecer al lado o abajo.
    assert hidden_layers_page.boton_azul.count() == 1
    assert hidden_layers_page.boton_verde.bounding_box() == hidden_layers_page.boton_azul.bounding_box()


def test_un_segundo_click_normal_sobre_el_locator_verde_tapado_termina_en_timeout(hidden_layers_page):
    hidden_layers_page.clickear_boton_verde()

    # Es exactamente el escenario que la propia página describe: "make sure
    # that green button can not be hit twice". El botón verde sigue en el
    # DOM y sigue siendo `is_visible() == True` (tiene bounding box y no
    # tiene `display:none`/`visibility:hidden`), pero el chequeo de
    # actionability de Playwright también exige que el punto de click
    # "reciba eventos de puntero" -- y ahora el botón azul está encima. Un
    # click normal (sin `force`) reintenta hasta el timeout y nunca llega a
    # dispararse, en vez de clickear a ciegas lo que haya debajo.
    with pytest.raises(PlaywrightTimeoutError):
        hidden_layers_page.boton_verde.click(timeout=3000)


def test_forzar_el_click_en_el_boton_verde_tapado_dispara_el_boton_azul_de_verdad(page, hidden_layers_page):
    mensajes_consola = []
    page.on("console", lambda msg: mensajes_consola.append(msg.text))

    hidden_layers_page.clickear_boton_verde()
    mensajes_consola.clear()
    hidden_layers_page.clickear_boton_verde_forzado()

    # `force=True` no "engaña" a la página para que trate el click como si
    # fuera sobre el botón verde: el evento de mouse se dispara en las
    # coordenadas de `#greenButton`, pero el navegador decide el `target`
    # real por hit-testing contra lo que hay ahí en ese momento, que es
    # `#blueButton`. El propio handler de la página lo confirma logueando
    # "Blue button pressed", no "Green button pressed", y no se agrega
    # ningún aviso ni una tercera capa -- el click nunca llegó al verde.
    assert "Blue button pressed" in mensajes_consola
    assert "Green button pressed" not in mensajes_consola
    assert hidden_layers_page.aviso.count() == 0


def test_clickear_el_boton_azul_por_su_propio_locator_si_funciona_sin_force(page, hidden_layers_page):
    mensajes_consola = []
    page.on("console", lambda msg: mensajes_consola.append(msg.text))

    hidden_layers_page.clickear_boton_verde()
    mensajes_consola.clear()

    # La forma correcta de automatizar este escenario no es forzar el click
    # sobre el locator viejo, sino preguntarle al DOM cuál es el elemento
    # vigente y clickear ESE: un click normal sobre `#blueButton` pasa el
    # chequeo de actionability sin problema, porque de verdad es el tope
    # del stack en ese punto.
    hidden_layers_page.boton_azul.click()

    assert "Blue button pressed" in mensajes_consola

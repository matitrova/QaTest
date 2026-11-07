import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from RadioButtonsPage import RadioButtonsPage


@pytest.fixture
def radio_buttons_page(page: Page) -> RadioButtonsPage:
    page.goto(f"{BASE_URL}/radio_buttons")
    return RadioButtonsPage(page)


# A diferencia de la mayoría de los ejemplos de radio buttons, esta página no
# arranca sin nada seleccionado: "Blue" ya viene marcado en el HTML servido
# por el backend, y el párrafo de resultado lo refleja desde la primera carga.
def test_estado_inicial_tiene_blue_marcado_y_ningun_deporte(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    expect(radio_buttons_page.resultado).to_have_text("Color: blue, Sport: none")
    expect(radio_buttons_page.blue).to_be_checked()
    expect(radio_buttons_page.red).not_to_be_checked()
    expect(radio_buttons_page.green).not_to_be_checked()


# El navegador ya desmarca solo al resto del grupo cuando se tilda un radio
# nuevo (es nativo de <input type="radio"> con el mismo name), pero eso
# únicamente actualiza la propiedad `checked` en memoria. El HTML servido por
# el backend queda con el atributo `checked` todavía escrito sobre "Blue" --
# un elemento tildado por el usuario normalmente nunca vuelve a tocar su
# propio atributo HTML. Esta página sí lo hace: un handler de `onchange`
# reescribe a mano el atributo `checked` de todo el grupo (`setAttribute` /
# `removeAttribute`) para que quede sincronizado con el estado real, no solo
# la propiedad -- se verifica justamente esa sincronización explícita del
# atributo, no solo el resultado visible en pantalla.
def test_tildar_red_saca_el_atributo_checked_de_blue(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    assert radio_buttons_page.blue.get_attribute("checked") is not None

    radio_buttons_page.red.click()

    expect(radio_buttons_page.resultado).to_have_text("Color: red, Sport: none")
    expect(radio_buttons_page.red).to_be_checked()
    assert radio_buttons_page.red.get_attribute("checked") is not None
    expect(radio_buttons_page.blue).not_to_be_checked()
    assert radio_buttons_page.blue.get_attribute("checked") is None


def test_solo_un_color_puede_estar_marcado_a_la_vez(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    radio_buttons_page.red.click()
    radio_buttons_page.green.click()

    expect(radio_buttons_page.resultado).to_have_text("Color: green, Sport: none")
    expect(radio_buttons_page.green).to_be_checked()
    expect(radio_buttons_page.red).not_to_be_checked()
    expect(radio_buttons_page.blue).not_to_be_checked()


# "Tennis" es el único radio del grupo deporte sin id propio y sin ningún
# <label> que lo envuelva -- el HTML es un <input> suelto seguido del texto
# plano "Tennis", así que no se puede ubicar por id ni por rol+label. Se
# ubica por el atributo `value`, el único dato estable que lo distingue de
# Football y Hockey.
def test_tildar_tennis_no_afecta_al_color_ya_elegido(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    radio_buttons_page.green.click()

    radio_buttons_page.tennis.click()

    expect(radio_buttons_page.resultado).to_have_text("Color: green, Sport: tennis")
    expect(radio_buttons_page.green).to_be_checked()


def test_solo_un_deporte_puede_estar_marcado_a_la_vez(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    radio_buttons_page.tennis.click()
    radio_buttons_page.football.click()

    expect(radio_buttons_page.resultado).to_have_text("Color: blue, Sport: football")
    expect(radio_buttons_page.football).to_be_checked()
    expect(radio_buttons_page.tennis).not_to_be_checked()


# "Hockey (not available)" trae el atributo `disabled` desde el HTML servido
# por el backend, no deshabilitado por CSS ni por un script que corra
# después de la carga. Igual que con el botón bloqueado de
# /dynamic_controls, la prueba de que el bloqueo es real no es leer un
# estado sino intentar clickear y que falle: Playwright rechaza clickear un
# elemento disabled y tira timeout de "actionability" en vez de no hacer
# nada en silencio.
def test_hockey_esta_deshabilitado_y_no_se_puede_tildar(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    expect(radio_buttons_page.hockey).to_be_disabled()

    with pytest.raises(Exception, match="Timeout"):
        radio_buttons_page.hockey.click(timeout=2000)

    expect(radio_buttons_page.hockey).not_to_be_checked()


def test_el_click_fallido_sobre_hockey_no_altera_ningun_otro_estado(
    radio_buttons_page: RadioButtonsPage,
) -> None:
    radio_buttons_page.green.click()
    radio_buttons_page.football.click()

    with pytest.raises(Exception, match="Timeout"):
        radio_buttons_page.hockey.click(timeout=2000)

    expect(radio_buttons_page.resultado).to_have_text("Color: green, Sport: football")
    expect(radio_buttons_page.green).to_be_checked()
    expect(radio_buttons_page.football).to_be_checked()

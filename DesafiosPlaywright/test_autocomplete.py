import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from AutocompletePage import AutocompletePage


# Se navega con `?delay=50` para que el servidor simulado responda casi al
# toque -- el debounce de 300ms del propio input ya es tiempo de sobra para
# una suite que corre decenas de veces. El delay real (por default 500ms, el
# que corre en producción) se prueba aparte, sin este parámetro.
@pytest.fixture
def autocomplete_page(page: Page) -> AutocompletePage:
    page.goto(f"{BASE_URL}/autocomplete?delay=50")
    return AutocompletePage(page)


def test_estado_inicial_sin_sugerencias_ni_seleccion(
    autocomplete_page: AutocompletePage,
) -> None:
    expect(autocomplete_page.input).to_have_value("")
    expect(autocomplete_page.input).to_have_attribute("aria-expanded", "false")
    expect(autocomplete_page.lista).to_be_hidden()
    expect(autocomplete_page.status).to_have_text("")
    expect(autocomplete_page.seleccionado).to_have_text("Nothing selected")


# El endpoint de sugerencias compara por prefijo e ignora mayúsculas/minúsculas
# ("PEA" encuentra "Peach" y "Pear", no una comparación literal de substring),
# así que el test lo prueba con una consulta en mayúsculas de verdad en vez de
# asumirlo por el nombre del campo.
@pytest.mark.parametrize(
    "consulta, esperadas",
    [
        ("ap", ["Apple", "Apricot"]),
        ("PEA", ["Peach", "Pear"]),
        ("coco", ["Coconut"]),
        ("GUA", ["Guava"]),
    ],
)
def test_escribir_una_coincidencia_muestra_las_sugerencias_correctas(
    autocomplete_page: AutocompletePage, consulta: str, esperadas: list[str]
) -> None:
    autocomplete_page.input.fill(consulta)

    expect(autocomplete_page.lista).to_be_visible()
    expect(autocomplete_page.input).to_have_attribute("aria-expanded", "true")
    expect(autocomplete_page.status).to_have_text(f"{len(esperadas)} suggestions")
    expect(autocomplete_page.opciones()).to_have_text(esperadas)


def test_sin_coincidencias_la_lista_queda_vacia_y_oculta(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("xyz")

    expect(autocomplete_page.status).to_have_text("No suggestions")
    expect(autocomplete_page.lista).to_be_hidden()
    expect(autocomplete_page.input).to_have_attribute("aria-expanded", "false")
    expect(autocomplete_page.opciones()).to_have_count(0)


# Vaciar el campo no dispara ningún pedido al servidor: el propio listener de
# "input" corta camino con `if (!query) { close(); ...; return; }` antes de
# programar el debounce. La lista se cierra en el mismo tick, sin esperar los
# 300ms de debounce ni el delay simulado del servidor -- a diferencia de
# escribir texto nuevo, que sí pasa por las dos esperas.
def test_vaciar_el_input_cierra_la_lista_sin_pasar_por_el_servidor(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("ap")
    expect(autocomplete_page.lista).to_be_visible()

    autocomplete_page.input.fill("")

    expect(autocomplete_page.lista).to_be_hidden()
    expect(autocomplete_page.input).to_have_attribute("aria-expanded", "false")
    expect(autocomplete_page.status).to_have_text("")


def test_click_en_una_sugerencia_la_selecciona_y_cierra_la_lista(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("pe")
    expect(autocomplete_page.lista).to_be_visible()

    autocomplete_page.opcion("Pear").click()

    expect(autocomplete_page.input).to_have_value("Pear")
    expect(autocomplete_page.seleccionado).to_have_text("You selected: Pear")
    expect(autocomplete_page.lista).to_be_hidden()
    expect(autocomplete_page.input).to_have_attribute("aria-expanded", "false")


def test_flecha_abajo_resalta_la_primera_opcion_y_enter_la_confirma(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("ap")
    expect(autocomplete_page.lista).to_be_visible()

    autocomplete_page.input.press("ArrowDown")
    expect(autocomplete_page.input).to_have_attribute(
        "aria-activedescendant", "suggestion-0"
    )
    expect(autocomplete_page.opcion("Apple")).to_have_attribute(
        "aria-selected", "true"
    )

    autocomplete_page.input.press("Enter")

    expect(autocomplete_page.input).to_have_value("Apple")
    expect(autocomplete_page.seleccionado).to_have_text("You selected: Apple")
    expect(autocomplete_page.lista).to_be_hidden()


# El índice resaltado arranca en -1 ("nada elegido todavía") y la propia
# función de resaltado lo recalcula como `(index + cantidad) % cantidad`.
# Una vuelta hacia atrás intuitiva debería caer en la última opción, pero la
# primera flecha arriba pide el índice -2, no -1: con 8 sugerencias para "p",
# (-2 + 8) % 8 da 6 ("Plum", la anteúltima), no 7 ("Pomegranate", la última).
# Recién la segunda flecha arriba, ya con un índice real para restar, se
# comporta como se esperaría y retrocede un lugar más.
def test_primera_flecha_arriba_sin_seleccion_previa_resalta_la_anteultima_no_la_ultima(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("p")
    expect(autocomplete_page.opciones()).to_have_count(8)

    autocomplete_page.input.press("ArrowUp")
    expect(autocomplete_page.input).to_have_attribute(
        "aria-activedescendant", "suggestion-6"
    )
    expect(autocomplete_page.opcion("Plum")).to_have_attribute(
        "aria-selected", "true"
    )

    autocomplete_page.input.press("ArrowUp")
    expect(autocomplete_page.input).to_have_attribute(
        "aria-activedescendant", "suggestion-5"
    )
    expect(autocomplete_page.opcion("Pineapple")).to_have_attribute(
        "aria-selected", "true"
    )


# A diferencia de la flecha arriba desde el principio, la flecha abajo desde
# la última opción sí da la vuelta a la primera de forma intuitiva: el índice
# que se le pide a la función de resaltado es `cantidad`, no uno negativo, y
# `cantidad % cantidad` da 0 limpio.
def test_flecha_abajo_desde_la_ultima_opcion_da_la_vuelta_a_la_primera(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("p")
    expect(autocomplete_page.opciones()).to_have_count(8)

    for _ in range(8):
        autocomplete_page.input.press("ArrowDown")
    expect(autocomplete_page.input).to_have_attribute(
        "aria-activedescendant", "suggestion-7"
    )

    autocomplete_page.input.press("ArrowDown")

    expect(autocomplete_page.input).to_have_attribute(
        "aria-activedescendant", "suggestion-0"
    )


def test_escape_cierra_la_lista_sin_tocar_el_texto_ni_la_seleccion(
    autocomplete_page: AutocompletePage,
) -> None:
    autocomplete_page.input.fill("ap")
    expect(autocomplete_page.lista).to_be_visible()

    autocomplete_page.input.press("Escape")

    expect(autocomplete_page.lista).to_be_hidden()
    expect(autocomplete_page.input).to_have_attribute("aria-expanded", "false")
    expect(autocomplete_page.input).to_have_value("ap")
    expect(autocomplete_page.seleccionado).to_have_text("Nothing selected")


# El delay por default (500ms) es el que corre en producción -- las demás
# pruebas de esta suite navegan con `?delay=50` solo para no pagar esa espera
# en cada caso. Mientras el pedido está en vuelo el status muestra "Loading..."
# antes de reemplazarse por la cuenta real de sugerencias; `expect()` sondea
# hasta encontrar ese texto, así que no hace falta ningún `sleep` para
# capturarlo en la ventana exacta en la que existe.
def test_el_delay_por_default_pasa_por_un_estado_de_carga_antes_de_responder(
    page: Page,
) -> None:
    page.goto(f"{BASE_URL}/autocomplete")
    autocomplete_page = AutocompletePage(page)

    autocomplete_page.input.fill("ap")

    expect(autocomplete_page.status).to_have_text("Loading...")
    expect(autocomplete_page.status).to_have_text("2 suggestions")
    expect(autocomplete_page.opciones()).to_have_text(["Apple", "Apricot"])

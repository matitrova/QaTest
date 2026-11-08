import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from CustomDropdownPage import CustomDropdownPage


@pytest.fixture
def custom_dropdown_page(page: Page) -> CustomDropdownPage:
    page.goto(f"{BASE_URL}/custom_dropdown")
    return CustomDropdownPage(page)


# No es un <select>: es un <div role="combobox"> con un <div role="listbox">
# que arranca con el atributo `hidden`. select_option() no existe para esto
# -- cualquier interacción pasa por click o teclado, igual que vería un
# lector de pantalla.
def test_estado_inicial_el_listbox_esta_cerrado_y_sin_seleccion(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    expect(custom_dropdown_page.combo).to_have_text("Choose a fruit")
    expect(custom_dropdown_page.combo).to_have_attribute("aria-expanded", "false")
    expect(custom_dropdown_page.listbox).to_be_hidden()
    expect(custom_dropdown_page.resultado).to_have_text("Selected: nothing")


def test_click_en_el_combo_abre_el_listbox(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    custom_dropdown_page.combo.click()

    expect(custom_dropdown_page.combo).to_have_attribute("aria-expanded", "true")
    expect(custom_dropdown_page.listbox).to_be_visible()


def test_seleccionar_una_opcion_con_mouse_actualiza_combo_y_resultado(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    custom_dropdown_page.combo.click()
    custom_dropdown_page.opcion("mango").click()

    expect(custom_dropdown_page.combo).to_have_text("Mango")
    expect(custom_dropdown_page.combo).to_have_attribute("aria-expanded", "false")
    expect(custom_dropdown_page.listbox).to_be_hidden()
    expect(custom_dropdown_page.resultado).to_have_text("Selected: mango")
    expect(custom_dropdown_page.opcion("mango")).to_have_attribute(
        "aria-selected", "true"
    )


# "Cherry (out of stock)" trae aria-disabled="true" desde el HTML, no
# disabled de HTML nativo -- pero Playwright sí lo respeta al chequear
# "actionability" antes de clickear, igual que con un <option disabled>:
# el click nunca llega a dispararse y tira timeout en vez de no hacer nada
# en silencio. Es el mismo patrón que el radio "Hockey" de /radio_buttons.
def test_click_en_cherry_deshabilitada_no_selecciona_nada(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    custom_dropdown_page.combo.click()

    with pytest.raises(Exception, match="Timeout"):
        custom_dropdown_page.opcion("cherry").click(timeout=2000)

    expect(custom_dropdown_page.resultado).to_have_text("Selected: nothing")
    expect(custom_dropdown_page.combo).to_have_text("Choose a fruit")
    expect(custom_dropdown_page.opcion("cherry")).to_have_attribute(
        "aria-selected", "false"
    )


def test_seleccionar_con_teclado_sin_tocar_el_mouse(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    custom_dropdown_page.combo.focus()

    # La primera flecha solo abre el listbox (no mueve la selección todavía
    # -- el propio script hace `return` apenas abre), así que hacen falta
    # dos ArrowDown para llegar de "nada" a "banana".
    custom_dropdown_page.combo.press("ArrowDown")
    custom_dropdown_page.combo.press("ArrowDown")
    custom_dropdown_page.combo.press("Enter")

    expect(custom_dropdown_page.combo).to_have_text("Banana")
    expect(custom_dropdown_page.resultado).to_have_text("Selected: banana")


# Desde "banana" (índice 1), la siguiente opción en el DOM es la deshabilitada
# "cherry" (índice 2) -- el manejo de teclado la salta sola y deja el foco
# visual en "mango" (índice 3). Se confirma leyendo aria-activedescendant,
# el único lugar donde el script registra cuál opción está resaltada.
def test_flecha_abajo_salta_la_opcion_deshabilitada(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    custom_dropdown_page.combo.focus()

    custom_dropdown_page.combo.press("ArrowDown")  # abre, resalta apple
    custom_dropdown_page.combo.press("ArrowDown")  # banana
    custom_dropdown_page.combo.press("ArrowDown")  # salta cherry, cae en mango

    expect(custom_dropdown_page.combo).to_have_attribute(
        "aria-activedescendant", "fruit-mango"
    )

    custom_dropdown_page.combo.press("Enter")

    expect(custom_dropdown_page.combo).to_have_text("Mango")
    expect(custom_dropdown_page.resultado).to_have_text("Selected: mango")


def test_escape_cierra_el_listbox_sin_cambiar_la_seleccion(
    custom_dropdown_page: CustomDropdownPage,
) -> None:
    custom_dropdown_page.combo.click()
    custom_dropdown_page.opcion("orange").click()
    expect(custom_dropdown_page.resultado).to_have_text("Selected: orange")

    custom_dropdown_page.combo.click()
    expect(custom_dropdown_page.listbox).to_be_visible()
    custom_dropdown_page.combo.press("Escape")

    expect(custom_dropdown_page.listbox).to_be_hidden()
    expect(custom_dropdown_page.combo).to_have_attribute("aria-expanded", "false")
    expect(custom_dropdown_page.combo).to_have_text("Orange")
    expect(custom_dropdown_page.resultado).to_have_text("Selected: orange")


def test_click_afuera_del_combo_cierra_el_listbox(
    custom_dropdown_page: CustomDropdownPage, page: Page
) -> None:
    custom_dropdown_page.combo.click()
    expect(custom_dropdown_page.listbox).to_be_visible()

    page.locator("#fruit-label").click()

    expect(custom_dropdown_page.listbox).to_be_hidden()
    expect(custom_dropdown_page.combo).to_have_attribute("aria-expanded", "false")

import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from ReadonlyInputsPage import ReadonlyInputsPage


@pytest.fixture
def readonly_page(page: Page) -> ReadonlyInputsPage:
    page.goto(f"{BASE_URL}/readonly")
    return ReadonlyInputsPage(page)


# "Disabled (not the same as read-only)" lo dice el propio label: son dos
# estados distintos del HTML (readonly vs. disabled) con el mismo efecto
# visible de "no se puede escribir", así que hace falta probar cada uno por
# separado en vez de asumir que uno implica el otro.

def test_textfield_es_editable_por_defecto(readonly_page: ReadonlyInputsPage) -> None:
    expect(readonly_page.textfield).to_be_editable()
    expect(readonly_page.textfield).to_have_value("I am editable")

    readonly_page.textfield.fill("un valor cualquiera")

    expect(readonly_page.textfield).to_have_value("un valor cualquiera")


def test_campo_siempre_readonly_no_acepta_texto(readonly_page: ReadonlyInputsPage) -> None:
    expect(readonly_page.always_readonly).not_to_be_editable()
    # readonly no es disabled: el campo sigue habilitado y seleccionable,
    # solo no se puede modificar su valor.
    expect(readonly_page.always_readonly).to_be_enabled()

    with pytest.raises(Exception):
        readonly_page.always_readonly.fill("intento de edición", timeout=1000)

    expect(readonly_page.always_readonly).to_have_value("You cannot change me")


def test_campo_disabled_no_acepta_texto(readonly_page: ReadonlyInputsPage) -> None:
    expect(readonly_page.disabled).to_be_disabled()
    expect(readonly_page.disabled).not_to_be_editable()

    with pytest.raises(Exception):
        readonly_page.disabled.fill("intento de edición", timeout=1000)

    expect(readonly_page.disabled).to_have_value("I am disabled")


# El checkbox no agrega ni quita el atributo readonly de forma declarativa:
# un handler de JS lo setea a mano y, de paso, pisa el valor del campo con
# "You cannot change me" -- no lo deja con lo que el usuario haya tipeado
# antes de tildarlo.

def test_tildar_el_checkbox_vuelve_readonly_al_textfield_y_pisa_su_valor(
    readonly_page: ReadonlyInputsPage,
) -> None:
    readonly_page.textfield.fill("texto que se va a perder")

    readonly_page.checkbox.check()

    expect(readonly_page.textfield).not_to_be_editable()
    expect(readonly_page.textfield).to_have_value("You cannot change me")

    with pytest.raises(Exception):
        readonly_page.textfield.fill("otro intento", timeout=1000)


def test_destildar_el_checkbox_vuelve_editable_al_textfield(
    readonly_page: ReadonlyInputsPage,
) -> None:
    readonly_page.checkbox.check()
    expect(readonly_page.textfield).not_to_be_editable()

    readonly_page.checkbox.uncheck()

    expect(readonly_page.textfield).to_be_editable()
    expect(readonly_page.textfield).to_have_value("I am editable")

    readonly_page.textfield.fill("de nuevo se puede escribir")
    expect(readonly_page.textfield).to_have_value("de nuevo se puede escribir")


# El campo siempre-readonly y el disabled no tienen ningún control en la
# página que los afecte -- a diferencia del textfield, ningún click del
# checkbox debería cambiar su estado.

def test_el_checkbox_no_afecta_a_los_otros_dos_campos(
    readonly_page: ReadonlyInputsPage,
) -> None:
    readonly_page.checkbox.check()

    expect(readonly_page.always_readonly).not_to_be_editable()
    expect(readonly_page.always_readonly).to_have_value("You cannot change me")
    expect(readonly_page.disabled).to_be_disabled()
    expect(readonly_page.disabled).to_have_value("I am disabled")

import pytest
from playwright.sync_api import expect

from config import BASE_URL
from DynamicControlsPage import DynamicControlsPage


@pytest.fixture
def dynamic_controls_page(page):
    page.goto(f"{BASE_URL}/dynamic_controls")
    return DynamicControlsPage(page)


# El checkbox no se oculta con CSS: swapCheckbox() llama a check.remove(), así
# que durante el delay no hay ningún truco de visibilidad que probar, hay que
# confirmar que el nodo desaparece del DOM (count() == 0), no solo que deja
# de ser visible.

def test_quitar_checkbox_lo_elimina_del_dom_y_cambia_el_boton_a_add(dynamic_controls_page):
    expect(dynamic_controls_page.checkbox).to_have_count(1)
    expect(dynamic_controls_page.boton_checkbox).to_have_text("Remove")

    dynamic_controls_page.quitar_checkbox()

    expect(dynamic_controls_page.checkbox).to_have_count(0, timeout=4000)
    expect(dynamic_controls_page.boton_checkbox).to_have_text("Add")
    expect(dynamic_controls_page.mensaje).to_have_text("It's gone!")


def test_agregar_checkbox_lo_devuelve_al_dom_y_cambia_el_boton_a_remove(dynamic_controls_page):
    dynamic_controls_page.quitar_checkbox()
    expect(dynamic_controls_page.checkbox).to_have_count(0, timeout=4000)

    dynamic_controls_page.agregar_checkbox()

    expect(dynamic_controls_page.checkbox).to_have_count(1, timeout=4000)
    expect(dynamic_controls_page.boton_checkbox).to_have_text("Remove")
    expect(dynamic_controls_page.mensaje).to_have_text("It's back!")


# disableButton() hace $(locator).attr("disabled", true) de forma sincrónica,
# dentro del mismo handler de click, antes de arrancar el setTimeout de 3
# segundos -- no hace falta esperar nada para confirmarlo. Por eso un segundo
# click disparado mientras el primero todavía está en el delay nunca llega a
# ejecutar nada: Playwright rechaza clickear un botón disabled y tira timeout
# de actionability en vez de silenciosamente no hacer nada, que es justo la
# señal de que el botón quedó bloqueado de verdad.

def test_el_boton_queda_disabled_durante_el_delay_y_bloquea_un_segundo_click(dynamic_controls_page):
    dynamic_controls_page.quitar_checkbox()

    expect(dynamic_controls_page.boton_checkbox).to_be_disabled()
    expect(dynamic_controls_page.loading_checkbox).to_be_visible()

    with pytest.raises(Exception):
        dynamic_controls_page.boton_checkbox.click(timeout=500)

    expect(dynamic_controls_page.boton_checkbox).to_be_enabled(timeout=4000)
    expect(dynamic_controls_page.loading_checkbox).to_be_hidden()


# clearMessage() borra el <p id="message"> anterior antes de arrancar el
# siguiente delay, así que un ciclo completo quitar -> agregar nunca debería
# dejar dos mensajes superpuestos en el DOM, solo el último.

def test_un_ciclo_completo_de_quitar_y_agregar_deja_un_solo_mensaje(dynamic_controls_page):
    dynamic_controls_page.quitar_checkbox()
    expect(dynamic_controls_page.mensaje).to_have_text("It's gone!", timeout=4000)

    dynamic_controls_page.agregar_checkbox()
    expect(dynamic_controls_page.mensaje).to_have_text("It's back!", timeout=4000)
    expect(dynamic_controls_page.mensaje).to_have_count(1)


# swapInput() es el mismo mecanismo que swapCheckbox() pero sobre un atributo
# disabled del propio input en vez de removerlo del DOM -- el input nunca
# deja de existir, solo deja de poder tipearse.

def test_habilitar_input_lo_hace_editable_y_cambia_el_boton_a_disable(dynamic_controls_page):
    expect(dynamic_controls_page.input).to_be_disabled()
    expect(dynamic_controls_page.boton_input).to_have_text("Enable")

    dynamic_controls_page.habilitar_input()

    expect(dynamic_controls_page.input).to_be_enabled(timeout=4000)
    expect(dynamic_controls_page.boton_input).to_have_text("Disable")
    expect(dynamic_controls_page.mensaje).to_have_text("It's enabled!")

    dynamic_controls_page.input.fill("ya se puede escribir")
    expect(dynamic_controls_page.input).to_have_value("ya se puede escribir")


def test_deshabilitar_input_lo_vuelve_a_bloquear_y_cambia_el_boton_a_enable(dynamic_controls_page):
    dynamic_controls_page.habilitar_input()
    expect(dynamic_controls_page.input).to_be_enabled(timeout=4000)

    dynamic_controls_page.deshabilitar_input()

    expect(dynamic_controls_page.input).to_be_disabled(timeout=4000)
    expect(dynamic_controls_page.boton_input).to_have_text("Enable")
    expect(dynamic_controls_page.mensaje).to_have_text("It's disabled!")

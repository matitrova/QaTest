import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from NativeDialogPage import NativeDialogPage


def test_abrir_modal_muestra_resultado_y_queda_abierto(page: Page) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")

    dialog_page.abrir_modal()

    expect(dialog_page.result).to_have_text("Modal dialog is open")
    assert dialog_page.esta_abierto(dialog_page.modal_dialog) is True


def test_confirmar_modal_con_nombre_muestra_confirm_y_el_nombre(page: Page) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_modal()

    dialog_page.confirmar_modal("Matias")

    expect(dialog_page.result).to_have_text(
        "Modal dialog closed with: confirm (name: Matias)"
    )
    assert dialog_page.esta_abierto(dialog_page.modal_dialog) is False


def test_cancelar_modal_sin_nombre_muestra_solo_cancel(page: Page) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_modal()

    dialog_page.cancelar_modal()

    expect(dialog_page.result).to_have_text("Modal dialog closed with: cancel")


# El handler de 'cancel' marca closedWithEscape = true antes de que el navegador
# dispare 'close': da igual qué botón se hubiera clickeado antes o qué nombre
# haya en el campo, Escape pisa todo con un resultado fijo que no depende de
# returnValue ni del input.
def test_escape_cierra_el_modal_e_ignora_el_nombre_ya_escrito(page: Page) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_modal()
    dialog_page.modal_name.fill("Matias")

    page.keyboard.press("Escape")

    expect(dialog_page.result).to_have_text("Modal dialog closed with Escape")
    assert dialog_page.esta_abierto(dialog_page.modal_dialog) is False


# showModal() deja inerte al resto del documento: un click real sobre un campo
# de la página de atrás no puede llegar a destino mientras el modal esté
# abierto, y Playwright lo refleja como timeout de actionability en vez de
# clickear en silencio sin efecto.
def test_modal_abierto_bloquea_un_click_real_sobre_el_campo_de_la_pagina(
    page: Page,
) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_modal()

    with pytest.raises(Exception, match="Timeout"):
        dialog_page.page_input.click(timeout=2000)


# fill() no hace el mismo chequeo de actionability que click() (no exige que
# el punto reciba eventos de puntero), así que no explota con el mismo
# timeout. Pero tampoco llena el campo: internamente necesita enfocar el
# input antes de escribir, y un elemento inerte por estar detrás de un modal
# no puede recibir foco -- ni con un click real ni mediante el focus()
# interno de Playwright. El resultado es un no-op silencioso, sin ninguna
# excepción: un test que solo comprobara "fill() no tiró error" daría este
# caso por bueno sin haber escrito nada de verdad en el campo.
def test_modal_abierto_deja_fill_como_no_op_silencioso_sobre_el_campo(
    page: Page,
) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_modal()

    dialog_page.page_input.fill("se puede igual")

    expect(dialog_page.page_input).to_have_value("")


def test_abrir_no_modal_no_bloquea_un_click_real_sobre_el_campo_de_la_pagina(
    page: Page,
) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")

    dialog_page.abrir_no_modal()

    expect(dialog_page.result).to_have_text("Non-modal dialog is open")
    dialog_page.page_input.click(timeout=2000)
    dialog_page.page_input.type("hola")
    expect(dialog_page.page_input).to_have_value("hola")


# Escape solo cierra el diálogo mostrado con showModal(): el no-modal, abierto
# con show(), lo ignora por completo -- ni cambia el resultado ni pierde su
# atributo "open". El contraste entre los dos métodos no es solo "bloquea o
# no bloquea el fondo", también difiere en qué tecla lo cierra.
def test_escape_no_cierra_el_dialogo_no_modal(page: Page) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_no_modal()

    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    expect(dialog_page.result).to_have_text("Non-modal dialog is open")
    assert dialog_page.esta_abierto(dialog_page.non_modal_dialog) is True


def test_cerrar_no_modal_con_su_boton_actualiza_el_resultado(page: Page) -> None:
    dialog_page = NativeDialogPage(page)
    page.goto(f"{BASE_URL}/dialog")
    dialog_page.abrir_no_modal()

    dialog_page.cerrar_no_modal()

    expect(dialog_page.result).to_have_text("Non-modal dialog closed")
    assert dialog_page.esta_abierto(dialog_page.non_modal_dialog) is False

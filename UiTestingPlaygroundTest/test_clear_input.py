import pytest
from playwright.sync_api import expect

from ClearInputPage import CAMPO_CONTENTEDITABLE, CAMPOS_ESTANDAR, TODOS_LOS_CAMPOS


@pytest.mark.parametrize("id_campo", CAMPOS_ESTANDAR)
def test_fill_vacio_limpia_cada_control_estandar(clear_input_page, id_campo):
    # Son ocho tipos de <input>/<textarea> distintos (texto, password,
    # email, number, search, url, tel, textarea), pero para fill("") todos
    # se comportan igual: no es un comportamiento por tipo de campo, es uno
    # solo repetido ocho veces.
    clear_input_page.limpiar(id_campo)

    assert clear_input_page.valor_estandar(id_campo) == ""


def test_input_value_no_sirve_para_leer_el_contenteditable(clear_input_page):
    # input_value() es la forma estándar de leer un control de formulario,
    # pero un <div contenteditable> no es uno: no tiene la propiedad .value
    # que ese método necesita, y Playwright lo rechaza antes de intentar
    # leer nada, con el mismo error que daría sobre cualquier <div> común.
    with pytest.raises(Exception, match="not an <input>, <textarea> or <select>"):
        clear_input_page.valor_estandar(CAMPO_CONTENTEDITABLE)


def test_fill_vacio_tambien_limpia_el_contenteditable(clear_input_page):
    # A pesar de no ser un control de formulario, fill("") sí está permitido
    # sobre un elemento marcado contenteditable -- es el tercer tipo de
    # elemento, además de <input> y <textarea>, que Playwright acepta ahí.
    clear_input_page.limpiar(CAMPO_CONTENTEDITABLE)

    assert clear_input_page.contenido_real_contenteditable() == ""


def test_inner_text_del_contenteditable_no_queda_vacio_tras_limpiarlo(clear_input_page):
    # fill("") sobre el contenteditable deja un <br> huérfano en vez de un
    # elemento realmente vacío. text_content() (lo que la propia página usa
    # para decidir si el campo está vacío) ignora ese <br> y da "", pero
    # inner_text() -- el texto tal como se renderiza, que sí respeta los
    # saltos de línea -- da un salto de línea solo, no un string vacío. Una
    # verificación que comparara inner_text() contra "" fallaría acá aunque
    # el campo esté, a todo efecto práctico, limpio.
    clear_input_page.limpiar(CAMPO_CONTENTEDITABLE)

    assert clear_input_page.contenido_real_contenteditable() == ""
    assert clear_input_page.texto_visible_contenteditable() != ""
    assert clear_input_page.texto_visible_contenteditable() == "\n"


def test_limpiar_los_nueve_campos_deja_el_estado_en_todos_vacios(clear_input_page):
    for id_campo in TODOS_LOS_CAMPOS:
        clear_input_page.limpiar(id_campo)

    # El label de estado lo recalcula un listener de "input" propio de la
    # página sobre los nueve campos a la vez (incluido el contenteditable,
    # vía textContent, no inner_text), no algo que el test arme contando los
    # campos por su cuenta: confirma que los nueve eventos de limpieza de
    # verdad dispararon ese recálculo.
    expect(clear_input_page.estado).to_have_text("All fields are cleared!")


def test_campo_sin_tocar_sigue_contando_como_no_vacio(clear_input_page):
    for id_campo in CAMPOS_ESTANDAR:
        clear_input_page.limpiar(id_campo)

    # A propósito se deja el contenteditable sin limpiar, para confirmar que
    # el contador de "pendientes" también lo cuenta a él y no solo a los
    # ocho controles de formulario estándar.
    expect(clear_input_page.estado).to_have_text("Non-empty fields remaining: 1")

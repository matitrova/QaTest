from config import BASE_URL
from ShadowDomPage import PATRON_GUID, ShadowDomPage


# El componente <guid-generator> es un Custom Element que crea su propio
# "shadow root" abierto (attachShadow({mode: "open"})) y mete ahí el input y
# los dos botones -- no existen en el <body> del documento, solo dentro de
# ese árbol aparte. document.querySelector("#editField") desde el documento
# principal no los ve (lo confirma test_el_campo_vive_en_un_shadow_root_pero_
# no_es_visible_para_el_document_global), pero page.locator("#editField") de
# Playwright sí los encuentra con el mismo selector CSS de toda la vida, sin
# ningún ">>> " ni sintaxis especial: a diferencia de Selenium (que necesita
# pedir expandedShadowRoot/shadowRoot manualmente), Playwright atraviesa
# shadow roots abiertos de forma transparente.


def test_el_campo_vive_en_un_shadow_root_pero_no_es_visible_para_el_document_global(page):
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    assert shadow_dom_page.esta_dentro_de_un_shadow_root() is True
    assert shadow_dom_page.encontrable_desde_el_document_global() is False


def test_generar_guid_carga_un_valor_con_formato_de_guid_en_el_input(page):
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    assert shadow_dom_page.valor_actual() == ""

    shadow_dom_page.generar_guid()

    assert PATRON_GUID.match(shadow_dom_page.valor_actual())


def test_dos_clicks_en_generar_dan_dos_guids_distintos(page):
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    shadow_dom_page.generar_guid()
    primer_guid = shadow_dom_page.valor_actual()

    shadow_dom_page.generar_guid()
    segundo_guid = shadow_dom_page.valor_actual()

    assert PATRON_GUID.match(primer_guid)
    assert PATRON_GUID.match(segundo_guid)
    assert primer_guid != segundo_guid


# El enunciado de la página pide clickear el botón de copiar y comparar el
# clipboard contra el input. Contra este deploy puntual (http, no https) eso
# no se puede cumplir: el sitio corre en un origen no seguro, y la Clipboard
# API ni siquiera existe ahí -- no es un permiso denegado, navigator.clipboard
# es undefined directamente (confirmado con page.evaluate antes de clickear
# nada). El propio handler de la página llama a
# navigator.clipboard.writeText(...) sin ningún try/catch alrededor, así que
# el click no "falla silenciosamente": dispara un error real de la página
# (page.on("pageerror")), y el valor del input queda intacto porque la
# asignación a editField.value ocurre en el botón de generar, no en este.
def test_copiar_al_clipboard_dispara_un_error_real_porque_el_sitio_no_es_un_contexto_seguro(page):
    shadow_dom_page = ShadowDomPage(page)

    errores = []
    page.on("pageerror", lambda exc: errores.append(str(exc)))

    page.goto(f"{BASE_URL}/shadowdom")

    assert page.evaluate("() => typeof navigator.clipboard") == "undefined"

    shadow_dom_page.generar_guid()
    guid_generado = shadow_dom_page.valor_actual()

    shadow_dom_page.copiar_guid()
    page.wait_for_timeout(300)

    assert len(errores) == 1
    assert "writeText" in errores[0]
    assert shadow_dom_page.valor_actual() == guid_generado

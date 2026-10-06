import pytest
from playwright.sync_api import expect

from config import BASE_URL
from ExitIntentPage import ExitIntentPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py, test_context_menu.py,
    # test_notification_message.py y test_entry_ad.py: el script externo de
    # Optimizely que carga el layout de esta página puede colgar el evento "load".
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_modal_no_aparece_al_cargar(page):
    exit_intent_page = ExitIntentPage(page)
    page.goto(f"{BASE_URL}/exit_intent")

    expect(exit_intent_page.modal).to_be_hidden()


def test_salir_por_arriba_del_viewport_muestra_el_modal(page):
    exit_intent_page = ExitIntentPage(page)
    page.goto(f"{BASE_URL}/exit_intent")

    exit_intent_page.simular_salida_del_mouse_por_arriba()

    expect(exit_intent_page.modal).to_be_visible(timeout=2000)


# El sitio usa la librería ouibounce con `sensitivity` en su valor por
# default (20px): solo cuenta como "salida" un mouseleave del documento con
# clientY <= 20, es decir, por el borde superior. Moverse dentro de la
# página -- incluso hasta abajo del todo -- no dispara ningún mouseleave del
# documentElement, así que el modal no debería aparecer por eso.

def test_moverse_dentro_de_la_pagina_sin_salir_por_arriba_no_muestra_el_modal(page):
    exit_intent_page = ExitIntentPage(page)
    page.goto(f"{BASE_URL}/exit_intent")

    exit_intent_page.mover_mouse_sin_salir_por_arriba()
    page.wait_for_timeout(300)

    assert exit_intent_page.modal_visible() is False


# `$('#ouibounce-modal .modal').on('click', e => e.stopPropagation())` corta
# la burbuja para cualquier click dentro de la caja del modal (el cuerpo del
# texto, no el footer), igual que en /entry_ad. Sin este caso, un test que
# solo probara "cerrar funciona" no distinguiría un cierre intencional de
# uno accidental por tocar el propio contenido del modal.

def test_clic_dentro_del_modal_no_lo_cierra(page):
    exit_intent_page = ExitIntentPage(page)
    page.goto(f"{BASE_URL}/exit_intent")
    exit_intent_page.simular_salida_del_mouse_por_arriba()
    expect(exit_intent_page.modal).to_be_visible(timeout=2000)

    exit_intent_page.hacer_clic_dentro_del_modal()
    page.wait_for_timeout(300)

    assert exit_intent_page.modal_visible() is True


def test_cerrar_modal_con_el_footer_lo_oculta(page):
    exit_intent_page = ExitIntentPage(page)
    page.goto(f"{BASE_URL}/exit_intent")
    exit_intent_page.simular_salida_del_mouse_por_arriba()
    expect(exit_intent_page.modal).to_be_visible(timeout=2000)

    exit_intent_page.cerrar_modal()

    expect(exit_intent_page.modal).to_be_hidden()


# El sitio inicializa ouibounce con `aggressive: true`, que en la librería
# solo cambia una cosa: ignora la cookie que recordaría "ya se mostró" entre
# visitas futuras a la página. No hace que el modal pueda volver a
# dispararse más de una vez DENTRO de la misma carga -- apenas se muestra
# por primera vez, el propio callback interno de la librería (`disable`)
# saca los listeners de mouseleave/mouseenter/keydown del documento, pase lo
# que pase con la opción `aggressive`. Asumir lo contrario (que "agresivo"
# significa que puede reaparecer cada vez que el mouse vuelve a salir) fue
# el primer intento de este test, y falló: una segunda salida por arriba en
# la misma carga de página no reabre nada.

def test_una_vez_que_se_muestra_no_vuelve_a_dispararse_en_la_misma_carga(page):
    exit_intent_page = ExitIntentPage(page)
    page.goto(f"{BASE_URL}/exit_intent")
    exit_intent_page.simular_salida_del_mouse_por_arriba()
    expect(exit_intent_page.modal).to_be_visible(timeout=2000)

    exit_intent_page.cerrar_modal()
    expect(exit_intent_page.modal).to_be_hidden()

    exit_intent_page.simular_salida_del_mouse_por_arriba()
    page.wait_for_timeout(500)

    assert exit_intent_page.modal_visible() is False

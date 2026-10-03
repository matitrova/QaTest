import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config import BASE_URL
from VisibilityPage import VisibilityPage

BOTONES_QUE_SE_OCULTAN = [
    "boton_zero_width",
    "boton_overlapped",
    "boton_transparent",
    "boton_invisible",
    "boton_not_displayed",
    "boton_offscreen",
]


def test_todos_los_botones_arrancan_visibles(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")

    assert visibility_page.boton_removed.is_visible()
    for nombre in BOTONES_QUE_SE_OCULTAN:
        assert getattr(visibility_page, nombre).is_visible()


def test_removido_desaparece_del_dom(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    # A diferencia de los demás, este botón no queda oculto por CSS: el
    # propio JS lo saca del DOM (`$(...).remove()`). No hay ningún estado de
    # "invisible" para leer, count() tiene que dar directamente 0.
    assert visibility_page.boton_removed.count() == 0


def test_ancho_cero_no_es_visible(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    # El JS le agrega la clase "zerowidth" (width: 0, min-width: 0). Sigue
    # presente en el DOM, pero con un bounding box de ancho 0: Playwright lo
    # trata como no visible.
    assert not visibility_page.boton_zero_width.is_visible()
    assert visibility_page.boton_zero_width.bounding_box()["width"] == 0


def test_opacity_cero_playwright_lo_sigue_viendo_visible(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    # `opacity: 0` lo hace invisible a simple vista, pero Playwright no mira
    # la opacidad para decidir is_visible() -- solo el layout (bounding box)
    # y `visibility`/`display`. El botón sigue teniendo tamaño y
    # `visibility: visible`, así que is_visible() da True pese a ser
    # transparente. Confiar en is_visible() para saber "¿lo ve el usuario?"
    # sería un falso positivo acá.
    assert visibility_page.boton_transparent.is_visible()
    assert visibility_page.boton_transparent.evaluate(
        "el => getComputedStyle(el).opacity"
    ) == "0"


def test_visibility_hidden_no_es_visible(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    assert not visibility_page.boton_invisible.is_visible()


def test_display_none_no_es_visible_y_no_tiene_bounding_box(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    # `display: none` sí saca al elemento del flujo de layout -- a
    # diferencia de "zero width" o "visibility: hidden", ni siquiera tiene
    # un bounding box para leer.
    assert not visibility_page.boton_not_displayed.is_visible()
    assert visibility_page.boton_not_displayed.bounding_box() is None


def test_offscreen_playwright_lo_sigue_viendo_visible(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    # El JS lo manda a position: absolute; top/left: -9999px -- fuera del
    # área visible para un usuario real, pero igual de "visible" para
    # Playwright: tiene un bounding box válido (aunque con coordenadas
    # negativas) y ningún estilo de los que is_visible() chequea lo
    # descarta.
    assert visibility_page.boton_offscreen.is_visible()
    assert visibility_page.boton_offscreen.bounding_box()["x"] < 0


def test_overlapped_es_visible_pero_el_click_no_llega(page):
    visibility_page = VisibilityPage(page)
    page.goto(f"{BASE_URL}/visibility")
    visibility_page.ocultar()

    # El JS no toca ningún estilo del propio botón: superpone un `<div>`
    # transparente del mismo tamaño y posición por encima. is_visible() no
    # tiene en cuenta qué hay delante de un elemento, así que sigue dando
    # True. Pero un click de verdad sí choca con esa capa -- el chequeo de
    # "actionability" de Playwright espera a que el elemento reciba
    # eventos de puntero y nunca lo logra, así que termina en timeout en
    # vez de hacer click en el botón equivocado.
    assert visibility_page.boton_overlapped.is_visible()
    with pytest.raises(PlaywrightTimeoutError):
        visibility_page.boton_overlapped.click(timeout=3000)

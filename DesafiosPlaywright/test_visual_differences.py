import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from VisualDifferencesPage import VisualDifferencesPage

TITULO_BASE = "Sign up for our newsletter"
COLOR_BASE = "#043423"


def test_la_tarjeta_base_no_tiene_ningun_cambio_activado(page: Page) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff")

    assert visual_differences_page.texto_titulo() == TITULO_BASE
    assert visual_differences_page.logo_es_visible()
    assert visual_differences_page.estilo_de_la_tarjeta() is None
    assert visual_differences_page.desplazamiento_del_boton_en_px() == 0
    assert visual_differences_page.color_de_fondo_del_boton() == COLOR_BASE


# El enunciado de la página dice "?shift=0..50", pero el servidor no rechaza
# un valor fuera de ese rango: lo recorta al límite más cercano en vez de
# devolver un error o ignorarlo. El mismo patrón de clamping que ya está
# documentado para /live_updates, pero acá aplica a un estilo visual en vez
# de a una cantidad de updates.
@pytest.mark.parametrize(
    ("shift", "desplazamiento_esperado"),
    [(0, 0), (10, 10), (25, 25), (50, 50), (100, 50), (-5, 0)],
)
def test_shift_mueve_el_boton_y_se_recorta_al_rango_declarado(
    page: Page, shift: int, desplazamiento_esperado: int
) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff?shift={shift}")

    assert visual_differences_page.desplazamiento_del_boton_en_px() == desplazamiento_esperado


# Un valor que ni siquiera es un número no cuenta como "fuera de rango" para
# el servidor: no hay nada que recortar, así que el parámetro se descarta
# por completo y la tarjeta queda igual a la base, sin ningún error visible.
def test_shift_no_numerico_se_ignora_y_el_boton_queda_en_su_posicion_base(page: Page) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff?shift=abc")

    assert visual_differences_page.desplazamiento_del_boton_en_px() == 0


# De los tres colores válidos, "green" es justo el que ya usa la tarjeta
# base -- pedirlo no cambia nada visible, a diferencia de "red" y "blue".
# Un valor fuera de la lista (ni red, ni green, ni blue) no rompe nada: se
# ignora igual que un "shift" no numérico y la tarjeta queda en su color
# base.
@pytest.mark.parametrize(
    ("color", "color_esperado"),
    [("red", "#961001"), ("green", COLOR_BASE), ("blue", "#334bc3"), ("purple", COLOR_BASE)],
)
def test_color_cambia_el_fondo_del_boton_salvo_green_que_coincide_con_la_base(
    page: Page, color: str, color_esperado: str
) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff?color={color}")

    assert visual_differences_page.color_de_fondo_del_boton() == color_esperado


# "large" es el único valor de "font" que la página reconoce: agrega un
# font-size inline a la tarjeta completa (no solo al título). Cualquier otro
# valor ("huge", por ejemplo) se descarta igual que un shift o un color
# inválidos, y la tarjeta queda sin ningún style propio -- el mismo None que
# la base.
@pytest.mark.parametrize(
    ("font", "estilo_esperado"),
    [("large", "font-size: 1.15em;"), ("huge", None)],
)
def test_font_large_agranda_la_tarjeta_entera_un_valor_invalido_se_ignora(
    page: Page, font: str, estilo_esperado: str | None
) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff?font={font}")

    assert visual_differences_page.estilo_de_la_tarjeta() == estilo_esperado


# El logo no desaparece del DOM con hide_logo=true: sigue siendo el mismo
# <img>, solo que con "visibility: hidden" en vez de "display: none". La
# distinción importa porque is_visible() de Playwright sí distingue los dos
# casos, pero count() no -- el elemento sigue "existiendo" para cualquier
# locator que lo busque, oculto o no.
def test_hide_logo_oculta_el_logo_sin_quitarlo_del_dom(page: Page) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff?hide_logo=true")

    assert visual_differences_page.logo.count() == 1
    expect(visual_differences_page.logo).to_be_hidden()


# El typo solo toca el título ("newsletter" -> "newsleter", sin la segunda
# "t"): el resto de la tarjeta -- texto, color y posición del botón -- queda
# exactamente igual que en la base, para confirmar que el parámetro no tiene
# ningún efecto colateral sobre el resto del card.
def test_typo_cambia_solo_el_titulo_el_resto_de_la_tarjeta_no_se_modifica(page: Page) -> None:
    visual_differences_page = VisualDifferencesPage(page)
    page.goto(f"{BASE_URL}/visual_diff?typo=true")

    assert visual_differences_page.texto_titulo() == "Sign up for our newsleter"
    assert visual_differences_page.texto.inner_text() == "One email a month with new examples. No spam."
    assert visual_differences_page.desplazamiento_del_boton_en_px() == 0
    assert visual_differences_page.color_de_fondo_del_boton() == COLOR_BASE

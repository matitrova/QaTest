import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from NestedFramesPage import NestedFramesPage


@pytest.fixture
def nested_frames_page(page: Page) -> NestedFramesPage:
    page.goto(f"{BASE_URL}/nested_frames")
    return NestedFramesPage(page)


def test_frame_left_muestra_su_texto(nested_frames_page: NestedFramesPage) -> None:
    expect(nested_frames_page.contenido_left).to_have_text("LEFT")


def test_frame_middle_muestra_su_texto_en_su_div_content(
    nested_frames_page: NestedFramesPage,
) -> None:
    expect(nested_frames_page.contenido_middle).to_have_text("MIDDLE")


def test_frame_right_muestra_su_texto(nested_frames_page: NestedFramesPage) -> None:
    expect(nested_frames_page.contenido_right).to_have_text("RIGHT")


def test_frame_bottom_es_hermano_de_top_y_tambien_es_accesible(
    nested_frames_page: NestedFramesPage,
) -> None:
    # frame-bottom no está anidado dentro de frame-top -- confirma que la
    # página tiene dos ramas de frames independientes, no una sola cadena.
    expect(nested_frames_page.contenido_bottom).to_have_text("BOTTOM")


def test_left_y_right_no_tienen_el_div_content_que_si_tiene_middle(
    nested_frames_page: NestedFramesPage,
) -> None:
    assert nested_frames_page.frame_left.locator("#content").count() == 0
    assert nested_frames_page.frame_right.locator("#content").count() == 0


def test_frame_top_contiene_exactamente_tres_frames_hijos(
    nested_frames_page: NestedFramesPage,
) -> None:
    expect(nested_frames_page.frames_hijos_de_top()).to_have_count(3)


def test_buscar_frame_left_sin_pasar_por_frame_top_no_lo_encuentra(
    page: Page,
) -> None:
    # frame-left está dos niveles abajo de la página (page -> frame-top ->
    # frame-left). Encadenar el frame_locator desde la página directa,
    # saltando frame-top, no matchea nada: hay que atravesar cada nivel.
    page.goto(f"{BASE_URL}/nested_frames")
    frame_left_sin_encadenar = page.frame_locator('frame[name="frame-left"]').locator("body")

    assert frame_left_sin_encadenar.count() == 0

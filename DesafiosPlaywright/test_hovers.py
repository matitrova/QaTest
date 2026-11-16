import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from HoversPage import HoversPage


@pytest.fixture
def hovers_page(page: Page) -> HoversPage:
    page.goto(f"{BASE_URL}/hovers")
    return HoversPage(page)


def test_captions_ocultas_antes_de_pasar_el_mouse(hovers_page: HoversPage) -> None:
    # El CSS de la página es .figcaption { display: none } y
    # .figure:hover .figcaption { display: block } -- no es opacidad,
    # es display, así que to_be_visible() lo detecta bien sin trucos.
    for i in range(3):
        expect(hovers_page.caption_de(i)).not_to_be_visible()


def test_hover_muestra_solo_la_caption_correspondiente(hovers_page: HoversPage) -> None:
    hovers_page.pasar_el_mouse_por(1)

    expect(hovers_page.caption_de(1)).to_be_visible()
    expect(hovers_page.caption_de(1)).to_contain_text("name: user2")
    # Las otras dos no deberían activarse por el hover en la del medio.
    expect(hovers_page.caption_de(0)).not_to_be_visible()
    expect(hovers_page.caption_de(2)).not_to_be_visible()


def test_cada_figura_muestra_su_propio_nombre_y_link(hovers_page: HoversPage) -> None:
    for i in range(3):
        hovers_page.pasar_el_mouse_por(i)
        caption = hovers_page.caption_de(i)

        expect(caption).to_contain_text(f"name: user{i + 1}")
        expect(caption.locator("a")).to_have_attribute("href", f"/users/{i + 1}")

import pytest
from playwright.sync_api import expect

from config import BASE_URL
from HorizontalSliderPage import HorizontalSliderPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo motivo que en test_windows.py: el layout del sitio carga un
    # script de Optimizely ajeno a lo que se prueba, y si esa red está
    # lenta o inaccesible el evento "load" puede colgarse esperándolo.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_valor_inicial_es_cero(page):
    slider_page = HorizontalSliderPage(page)
    page.goto(f"{BASE_URL}/horizontal_slider")

    expect(slider_page.valor_mostrado).to_have_text("0")
    assert slider_page.slider.input_value() == "0"


def test_una_flecha_derecha_mueve_un_step(page):
    slider_page = HorizontalSliderPage(page)
    page.goto(f"{BASE_URL}/horizontal_slider")

    slider_page.enfocar()
    slider_page.presionar_flecha_derecha()

    expect(slider_page.valor_mostrado).to_have_text("0.5")


def test_varias_flechas_derecha_acumulan_y_una_izquierda_resta(page):
    slider_page = HorizontalSliderPage(page)
    page.goto(f"{BASE_URL}/horizontal_slider")

    slider_page.enfocar()
    slider_page.presionar_flecha_derecha(veces=3)
    expect(slider_page.valor_mostrado).to_have_text("1.5")

    slider_page.presionar_flecha_izquierda()
    expect(slider_page.valor_mostrado).to_have_text("1")


def test_no_supera_el_maximo_ni_baja_del_minimo(page):
    # min=0, max=5, step=0.5 -- el input debe frenar en los bordes, no
    # desbordar ni dar la vuelta.
    slider_page = HorizontalSliderPage(page)
    page.goto(f"{BASE_URL}/horizontal_slider")

    slider_page.enfocar()
    slider_page.presionar_flecha_derecha(veces=20)
    expect(slider_page.valor_mostrado).to_have_text("5")

    slider_page.presionar_flecha_izquierda(veces=20)
    expect(slider_page.valor_mostrado).to_have_text("0")


def test_click_en_el_extremo_salta_directo_al_valor_mas_cercano(page):
    # A diferencia de las flechas, clickear el slider no lo mueve de a un
    # step: salta directo al valor que corresponde a esa posición del
    # click. Clickear cerca del borde derecho debería ir directo al máximo.
    slider_page = HorizontalSliderPage(page)
    page.goto(f"{BASE_URL}/horizontal_slider")

    caja = slider_page.slider.bounding_box()
    slider_page.clickear_en(caja["width"] - 1)

    expect(slider_page.valor_mostrado).to_have_text("5")

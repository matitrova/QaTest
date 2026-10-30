from ClickPage import ClickPage


def test_click_fisico_pone_el_boton_verde(click_page):
    assert click_page.boton.get_attribute("class") == ClickPage.CLASE_INICIAL
    click_page.boton.click()
    assert click_page.boton.get_attribute("class") == ClickPage.CLASE_AL_CLICKEAR


def test_click_via_js_no_pone_el_boton_verde(click_page):
    # El propio nombre del botón lo advierte ("Ignores DOM Click Event"):
    # el handler de esta página descarta un click disparado vía JavaScript,
    # a diferencia del click físico de Playwright, que sí lo activa.
    click_page.clickear_via_js()
    assert click_page.boton.get_attribute("class") == ClickPage.CLASE_INICIAL

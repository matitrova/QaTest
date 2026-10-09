from config import BASE_URL
from AjaxDataPage import AjaxDataPage


def test_no_hay_contenido_cargado_antes_de_hacer_click(page):
    ajax_data_page = AjaxDataPage(page)
    page.goto(f"{BASE_URL}/ajax")

    assert ajax_data_page.contenido.inner_text() == ""
    assert not ajax_data_page.spinner.is_visible()


def test_al_hacer_click_el_spinner_aparece_de_inmediato(page):
    ajax_data_page = AjaxDataPage(page)
    page.goto(f"{BASE_URL}/ajax")

    ajax_data_page.disparar_pedido()

    # El spinner lo muestra el propio handler de click, antes del $.get():
    # tiene que estar visible ya, sin esperar nada de la respuesta del
    # servidor (que tarda 15 segundos reales).
    assert ajax_data_page.spinner.is_visible()
    assert ajax_data_page.contenido.inner_text() == ""


def test_despues_de_esperar_aparece_el_texto_cargado_por_ajax(page):
    ajax_data_page = AjaxDataPage(page)
    page.goto(f"{BASE_URL}/ajax")

    ajax_data_page.disparar_pedido()
    ajax_data_page.esperar_etiqueta()

    assert ajax_data_page.texto_etiqueta() == "Data loaded with AJAX get request."
    # El callback oculta el spinner con $('#spinner').hide() justo antes de
    # insertar el texto: para el momento en que la etiqueta ya está visible,
    # el spinner tiene que haber desaparecido.
    assert not ajax_data_page.spinner.is_visible()

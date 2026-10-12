from config import BASE_URL
from OverlappedPage import OverlappedPage


def test_escribir_sin_scroll_el_div_superpuesto_borra_el_texto(page):
    overlapped_page = OverlappedPage(page)
    page.goto(f"{BASE_URL}/overlapped")

    overlapped_page.escribir_name_sin_scroll("Matias")

    # El listener `input` de la página calcula el centro del input y pregunta
    # con `elementFromPoint` qué elemento hay ahí. Mientras el div gris
    # absoluto sigue tapando ese punto, la respuesta no es el input, así que
    # la propia página vacía el campo apenas termina de escribir.
    assert overlapped_page.valor_name() == ""


def test_escribir_con_scroll_previo_el_texto_queda_cargado(page):
    overlapped_page = OverlappedPage(page)
    page.goto(f"{BASE_URL}/overlapped")

    overlapped_page.escribir_name_con_scroll("Matias")

    # Al hacer scroll del contenedor interno, el input se desplaza fuera del
    # área que cubre el div superpuesto (que no se mueve con el scroll, está
    # posicionado respecto al contenedor externo). El punto central del
    # input queda libre y `elementFromPoint` sí devuelve el input, así que el
    # texto sobrevive.
    assert overlapped_page.valor_name() == "Matias"


def test_el_input_subject_tambien_esta_tapado_y_se_libera_con_el_mismo_scroll(page):
    overlapped_page = OverlappedPage(page)
    page.goto(f"{BASE_URL}/overlapped")

    # El mismo scroll que libera a #name también corre a #subject, que
    # arranca más abajo en el contenedor y queda totalmente visible. Lo
    # relevante no es el campo en sí (no tiene el listener que borra el
    # texto) sino confirmar que el scroll no lo deja tapado por otro motivo.
    overlapped_page.name_input.evaluate("el => el.scrollIntoView()")
    overlapped_page.subject_input.fill("QA")

    assert overlapped_page.subject_input.input_value() == "QA"

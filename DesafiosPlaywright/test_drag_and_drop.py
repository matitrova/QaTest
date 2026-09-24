from config import BASE_URL
from DragAndDropPage import DragAndDropPage


def test_arrastrar_columna_a_intercambia_contenido_con_b(page):
    drag_page = DragAndDropPage(page)
    page.goto(f"{BASE_URL}/drag_and_drop")

    assert drag_page.texto_de(drag_page.columna_a) == "A"
    assert drag_page.texto_de(drag_page.columna_b) == "B"

    drag_page.arrastrar_a_hacia_b()

    # El drop no mueve los elementos, intercambia su contenido: la columna A
    # sigue siendo la primera en el DOM, pero ahora muestra "B", y viceversa.
    assert drag_page.texto_de(drag_page.columna_a) == "B"
    assert drag_page.texto_de(drag_page.columna_b) == "A"


def test_arrastrar_dos_veces_vuelve_al_estado_original(page):
    drag_page = DragAndDropPage(page)
    page.goto(f"{BASE_URL}/drag_and_drop")

    drag_page.arrastrar_a_hacia_b()
    drag_page.arrastrar_a_hacia_b()

    assert drag_page.texto_de(drag_page.columna_a) == "A"
    assert drag_page.texto_de(drag_page.columna_b) == "B"

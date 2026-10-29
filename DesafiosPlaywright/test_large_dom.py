import pytest
from playwright.sync_api import expect

from config import BASE_URL
from LargeDomPage import LargeDomPage


@pytest.fixture
def large_dom_page(page):
    page.goto(f"{BASE_URL}/large")
    return LargeDomPage(page)


def test_no_siblings_anidado_50_divs_adentro_se_ubica_directo_por_id(large_dom_page):
    # El elemento no tiene hermanos: está envuelto en 50 <div> sin class ni
    # id, uno dentro del otro, antes de llegar al div.parent que los
    # contiene a todos. Ubicarlo por id no requiere bajar esa cadena a
    # mano -- Playwright lo encuentra igual de directo que si estuviera en
    # la raíz del documento, que es justo lo que esta página pone a prueba.
    expect(large_dom_page.no_siblings).to_have_text("No siblings")

    profundidad = large_dom_page.no_siblings.evaluate(
        "el => { let n = 0; let p = el.parentElement; "
        "while (p && p.tagName === 'DIV' && !p.getAttribute('class')) { "
        "n++; p = p.parentElement; } return n; }"
    )
    assert profundidad == 50


def test_sibling_1_2_y_sibling_1_3_si_son_hermanos_reales_en_su_tier(large_dom_page):
    # En cada tier, item-2 e item-3 sí son hermanos reales: ambos cuelgan
    # directo de item-1, que es su padre, no un tercer hermano.
    item_2 = large_dom_page.hermano(1, 2)

    mismo_padre = item_2.evaluate(
        "(el, selectorOtro) => el.parentElement === "
        "document.querySelector(selectorOtro).parentElement",
        "[id='sibling-1.3']",
    )
    assert mismo_padre is True


def test_sibling_1_1_es_padre_de_sibling_1_2_y_ancestro_de_todo_el_resto_de_tiers(
    large_dom_page,
):
    # La sección se llama "Siblings", pero item-1 de cada tier no es
    # hermano de item-2/item-3: es su padre. Y ese mismo <div> tampoco
    # cierra hasta después de contener completo al tier siguiente -- item-1
    # del tier 1 termina siendo ancestro de los 49 tiers restantes, incluido
    # el item-3 del tier 50. La profundidad real de la página viene de esa
    # cadena de contención entre los item-1 de cada nivel, no de hermanos
    # sueltos como sugiere el nombre de la sección.
    item_1_1 = large_dom_page.hermano(1, 1)

    es_padre_de_item_2 = item_1_1.evaluate(
        "(el, selectorHijo) => el === "
        "document.querySelector(selectorHijo).parentElement",
        "[id='sibling-1.2']",
    )
    es_ancestro_del_ultimo_tier = item_1_1.evaluate(
        "(el, selectorDescendiente) => el.contains("
        "document.querySelector(selectorDescendiente))",
        "[id='sibling-50.3']",
    )
    assert es_padre_de_item_2 is True
    assert es_ancestro_del_ultimo_tier is True


def test_tabla_es_una_grilla_completa_de_50_por_50_no_una_muestra_recortada(large_dom_page):
    # El nombre "Table" no aclara el tamaño real: son 50 filas de datos por
    # 50 columnas (2500 celdas), no las 6 columnas que se ven en pantalla
    # sin hacer scroll horizontal. La tabla además tiene un <thead> con una
    # fila de encabezados -- contar "tr" sin filtrar por tbody da 51 en vez
    # de 50 filas de datos. Verificar solo las primeras celdas dejaría
    # pasar una grilla recortada a mitad de camino.
    filas = large_dom_page.tabla.locator("tbody tr")
    expect(filas).to_have_count(50)
    expect(filas.first.locator("td")).to_have_count(50)

    expect(large_dom_page.celda(1, 1)).to_have_text("1.1")
    expect(large_dom_page.celda(1, 50)).to_have_text("1.50")
    expect(large_dom_page.celda(50, 1)).to_have_text("50.1")
    expect(large_dom_page.celda(50, 50)).to_have_text("50.50")

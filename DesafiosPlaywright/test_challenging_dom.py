import re

import pytest
from playwright.sync_api import expect

from config import BASE_URL
from ChallengingDomPage import ChallengingDomPage

COLUMNAS_ESPERADAS = [
    "Iuvaret",
    "Apeirian",
    "Adipisci",
    "Definiebas",
    "Consequuntur",
    "Phaedrum",
]


def test_los_tres_botones_tienen_clases_distintas_y_fijas(page):
    # El texto y el id de cada botón salen al azar en cada carga, pero el
    # orden y la clase CSS (plano / "alert" / "success") no cambian nunca:
    # es lo único confiable para distinguirlos.
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    expect(challenging_dom_page.boton(0)).to_have_class("button")
    expect(challenging_dom_page.boton(1)).to_have_class("button alert")
    expect(challenging_dom_page.boton(2)).to_have_class("button success")


def test_los_ids_de_los_botones_cambian_al_recargar(page):
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    ids_antes = challenging_dom_page.botones.evaluate_all(
        "elementos => elementos.map(el => el.id)"
    )

    page.reload()

    ids_despues = challenging_dom_page.botones.evaluate_all(
        "elementos => elementos.map(el => el.id)"
    )

    # Si alguno coincidiera por casualidad el test no probaría nada --
    # con un UUID por botón, la chance es despreciable.
    assert ids_antes != ids_despues
    assert len(ids_antes) == len(ids_despues) == 3


def test_click_en_un_boton_no_navega_a_otra_pagina(page):
    # Los tres <a> tienen href='' -- un click no debería sacar al usuario
    # de /challenging_dom ni lanzar ningún error de navegación.
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    challenging_dom_page.boton(1).click()

    expect(page).to_have_url(f"{BASE_URL}/challenging_dom")


def test_la_tabla_tiene_diez_filas(page):
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    expect(challenging_dom_page.filas).to_have_count(10)


@pytest.mark.parametrize("columna_indice, prefijo", list(enumerate(COLUMNAS_ESPERADAS)))
def test_cada_celda_de_una_columna_sigue_el_patron_prefijo_mas_indice_de_fila(
    page, columna_indice, prefijo
):
    # Ninguna celda tiene class ni id para ubicarla por atributo: solo se
    # puede verificar el patrón de texto que cada columna respeta
    # (prefijo fijo + número de fila), sin importar que el contenido
    # exacto cambie en cada carga.
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    patron = re.compile(rf"^{prefijo}\d$")
    for fila_indice in range(10):
        celda = challenging_dom_page.celda(fila_indice, columna_indice)
        expect(celda).to_have_text(patron)
        assert celda.inner_text() == f"{prefijo}{fila_indice}"


def test_cada_fila_tiene_un_link_de_editar_y_uno_de_borrar(page):
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    for fila_indice in range(10):
        acciones = challenging_dom_page.acciones_de_fila(fila_indice)
        expect(acciones).to_have_text(["edit", "delete"])


def test_el_canvas_tiene_id_fijo_y_dimensiones_fijas(page):
    # A diferencia de los botones y la tabla, el canvas sí tiene un id
    # estable -- no todo en esta página está pensado para ser difícil.
    challenging_dom_page = ChallengingDomPage(page)
    page.goto(f"{BASE_URL}/challenging_dom")

    expect(challenging_dom_page.canvas).to_be_visible()
    expect(challenging_dom_page.canvas).to_have_attribute("width", "599")
    expect(challenging_dom_page.canvas).to_have_attribute("height", "200")

import re

import pytest
from playwright.sync_api import expect

from config import BASE_URL
from TablesPage import TablesPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo motivo que en el resto de los tests de the-internet: un script
    # de Optimizely ajeno a lo que se prueba puede colgar el evento "load".
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_tabla_sin_class_arranca_en_el_orden_original(page):
    tables_page = TablesPage(page)
    page.goto(f"{BASE_URL}/tables", wait_until="networkidle")

    # Tabla 1 no tiene tablesorter con clases en las celdas: solo confirma
    # que, sin ordenar nada, el orden es el que trae el HTML.
    expect(tables_page.apellidos_tabla1).to_have_text(["Smith", "Bach", "Doe", "Conway"])


def test_ordenar_por_apellido_ascendente(page):
    tables_page = TablesPage(page)
    page.goto(f"{BASE_URL}/tables", wait_until="networkidle")
    tables_page.esperar_que_tablesorter_este_listo()

    tables_page.encabezado_apellido_tabla2.click()

    # tablesorter marca el <th> con esta clase recién cuando termina de
    # reordenar el <tbody> -- esperar la clase evita leer las celdas a
    # mitad del reordenamiento. La versión de tablesorter que usa este sitio
    # nombra las clases al revés de lo que sugiere su propio CSS (que habla
    # de "tablesorter-headerAsc/Desc"): en el DOM real son "headerSortDown"
    # para ascendente y "headerSortUp" para descendente.
    expect(tables_page.encabezado_apellido_tabla2.locator("..")).to_have_class(
        re.compile("headerSortDown")
    )
    expect(tables_page.apellidos_tabla2).to_have_text(["Bach", "Conway", "Doe", "Smith"])


def test_ordenar_por_apellido_descendente(page):
    tables_page = TablesPage(page)
    page.goto(f"{BASE_URL}/tables", wait_until="networkidle")
    tables_page.esperar_que_tablesorter_este_listo()

    tables_page.encabezado_apellido_tabla2.click()
    tables_page.encabezado_apellido_tabla2.click()

    expect(tables_page.encabezado_apellido_tabla2.locator("..")).to_have_class(
        re.compile("headerSortUp")
    )
    expect(tables_page.apellidos_tabla2).to_have_text(["Smith", "Doe", "Conway", "Bach"])


def test_ordenar_por_monto_es_numerico_no_alfabetico(page):
    tables_page = TablesPage(page)
    page.goto(f"{BASE_URL}/tables", wait_until="networkidle")
    tables_page.esperar_que_tablesorter_este_listo()

    tables_page.encabezado_monto_tabla2.click()

    expect(tables_page.encabezado_monto_tabla2.locator("..")).to_have_class(
        re.compile("headerSortDown")
    )
    montos = tables_page.montos_como_numeros()
    # $50.00 (Smith) y $51.00 (Conway) empiezan con "5" y "1" en sus
    # centavos-como-texto: si tablesorter ordenara alfabéticamente, "$100.00"
    # quedaría antes que "$51.00". El orden numérico real es el que importa.
    assert montos == sorted(montos)
    assert montos[-1] == 100.0


def test_ordenar_por_monto_descendente(page):
    tables_page = TablesPage(page)
    page.goto(f"{BASE_URL}/tables", wait_until="networkidle")
    tables_page.esperar_que_tablesorter_este_listo()

    tables_page.encabezado_monto_tabla2.click()
    tables_page.encabezado_monto_tabla2.click()

    expect(tables_page.encabezado_monto_tabla2.locator("..")).to_have_class(
        re.compile("headerSortUp")
    )
    montos = tables_page.montos_como_numeros()
    assert montos == sorted(montos, reverse=True)
    assert montos[0] == 100.0

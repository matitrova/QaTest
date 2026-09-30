import pytest
from playwright.sync_api import expect

from config import BASE_URL
from StatusCodesPage import StatusCodesPage


@pytest.mark.parametrize("codigo", [200, 301, 404, 500])
def test_status_code_en_body_y_en_response(page, codigo):
    # El código HTTP real de la respuesta y el texto que el propio
    # sitio imprime en el body son dos fuentes independientes --
    # las dos tienen que coincidir con lo que el sitio promete.
    status_codes_page = StatusCodesPage(page)
    response = page.goto(f"{BASE_URL}/status_codes/{codigo}")

    assert response.status == codigo
    expect(status_codes_page.mensaje).to_have_text(
        status_codes_page.texto_esperado(codigo)
    )


def test_301_no_redirige_a_ningun_lado(page):
    # Un 301 real trae un header Location y el navegador termina en
    # otra URL. Este "301" del sitio no trae Location -- Playwright
    # no tiene a dónde redirigir, así que la página se queda en la
    # misma URL que se pidió, sirviendo su propio contenido con ese
    # status. No alcanza con mirar el status code para confirmar esto:
    # hay que confirmar también que la URL final no cambió.
    page.goto(f"{BASE_URL}/status_codes/301")

    assert page.url == f"{BASE_URL}/status_codes/301"


def test_pagina_principal_linkea_los_cuatro_codigos(page):
    page.goto(f"{BASE_URL}/status_codes")

    for codigo in (200, 301, 404, 500):
        expect(
            page.locator(f"a[href='status_codes/{codigo}']")
        ).to_be_visible()

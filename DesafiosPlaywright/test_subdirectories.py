import pytest
import requests
from playwright.sync_api import Page, expect

from config import BASE_URL
from SubdirectoriesPage import SubdirectoriesPage


@pytest.mark.parametrize(
    "ruta, titulo, otras_rutas",
    [
        (
            "/subdirectories",
            "Subdirectories",
            ("/subdirectories/one", "/subdirectories/two"),
        ),
        (
            "/subdirectories/one",
            "Subdirectory One",
            ("/subdirectories", "/subdirectories/two"),
        ),
        (
            "/subdirectories/two",
            "Subdirectory Two",
            ("/subdirectories", "/subdirectories/one"),
        ),
    ],
)
def test_cada_pagina_linkea_a_las_otras_dos_pero_nunca_a_si_misma(
    page: Page, ruta: str, titulo: str, otras_rutas: tuple[str, str]
) -> None:
    subdirectories_page = SubdirectoriesPage(page)
    page.goto(f"{BASE_URL}{ruta}")

    expect(subdirectories_page.titulo).to_have_text(titulo)
    expect(subdirectories_page.miga_de_pan).to_have_text(ruta)
    expect(subdirectories_page.links).to_have_count(2)
    for otra_ruta in otras_rutas:
        expect(subdirectories_page.link_hacia(otra_ruta)).to_be_visible()
    expect(subdirectories_page.link_hacia(ruta)).to_have_count(0)


def test_click_navega_el_anillo_completo_actualizando_titulo_y_miga_de_pan(
    page: Page,
) -> None:
    subdirectories_page = SubdirectoriesPage(page)
    page.goto(f"{BASE_URL}/subdirectories")

    with page.expect_navigation():
        subdirectories_page.link_hacia("/subdirectories/one").click()
    expect(subdirectories_page.titulo).to_have_text("Subdirectory One")
    expect(subdirectories_page.miga_de_pan).to_have_text("/subdirectories/one")

    with page.expect_navigation():
        subdirectories_page.link_hacia("/subdirectories/two").click()
    expect(subdirectories_page.titulo).to_have_text("Subdirectory Two")
    expect(subdirectories_page.miga_de_pan).to_have_text("/subdirectories/two")

    with page.expect_navigation():
        subdirectories_page.link_hacia("/subdirectories").click()
    expect(subdirectories_page.titulo).to_have_text("Subdirectories")
    expect(subdirectories_page.miga_de_pan).to_have_text("/subdirectories")


@pytest.mark.parametrize(
    "ruta",
    [
        "/subdirectories/",
        "/subdirectories/one/",
        "/subdirectories/two/",
        "/subdirectories/tres",
    ],
)
def test_barra_final_o_ruta_inexistente_devuelven_404_sin_el_layout_del_sitio(
    ruta: str,
) -> None:
    # El sitio no tolera una barra final en estas rutas: a diferencia de
    # /subdirectories (sin barra, 200), agregarle una devuelve 404 igual
    # que pedir un subdirectorio que directamente no existe. En los dos
    # casos el cuerpo es un "<h1>Not Found</h1>" de 18 bytes exactos, sin
    # el nav, el div de flash-messages ni el footer "Powered by" que trae
    # toda otra página real de este sitio -- la ruta nunca llegó a
    # resolver ningún layout de la app, el framework devolvió directo un
    # "pass" de ruteo (header x-cascade: pass) antes de montar nada.
    response = requests.get(f"{BASE_URL}{ruta}")

    assert response.status_code == 404
    assert response.headers["x-cascade"] == "pass"
    assert response.text == "<h1>Not Found</h1>"
    assert "Powered by" not in response.text

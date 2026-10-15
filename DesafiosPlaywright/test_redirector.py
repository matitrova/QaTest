import requests
from playwright.sync_api import expect

from config import BASE_URL
from RedirectorPage import RedirectorPage


def test_link_resuelve_contra_la_raiz_no_contra_redirector():
    # El href del link es "redirect", sin barra inicial: una URL relativa.
    # /redirector no tiene barra final, así que su "directorio" es la raíz
    # del sitio -- el link resuelve a {BASE_URL}/redirect, no a
    # {BASE_URL}/redirector/redirect como sugeriría el nombre de la página.
    response_bajo_redirector = requests.get(
        f"{BASE_URL}/redirector/redirect", allow_redirects=False
    )
    response_en_la_raiz = requests.get(
        f"{BASE_URL}/redirect", allow_redirects=False
    )

    assert response_bajo_redirector.status_code == 404
    assert response_en_la_raiz.status_code == 302


def test_redirect_es_302_con_location_a_status_codes():
    # El sitio devuelve un 302 real con header Location, a diferencia de
    # /status_codes/301 que imprime el texto "301" sin redirigir a ningún
    # lado. Acá sí hay una redirección real que seguir.
    response = requests.get(f"{BASE_URL}/redirect", allow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == f"{BASE_URL}/status_codes"


def test_click_en_el_link_termina_en_status_codes(page):
    redirector_page = RedirectorPage(page)
    page.goto(f"{BASE_URL}/redirector")

    with page.expect_navigation():
        redirector_page.link_redirect.click()

    assert page.url == f"{BASE_URL}/status_codes"
    expect(page.locator("h3")).to_have_text("Status Codes")

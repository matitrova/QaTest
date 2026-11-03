import pytest

from config import BASE_URL
from GeolocationPage import GeolocationPage

COORDENADAS = [
    (-34.6037, -58.3816),  # Buenos Aires
    (40.4168, -3.7038),  # Madrid
]


@pytest.fixture(params=COORDENADAS)
def coordenadas_simuladas(request):
    return request.param


@pytest.fixture
def browser_context_args(browser_context_args, coordenadas_simuladas):
    # navigator.geolocation.getCurrentPosition() pide permiso del navegador
    # y depende del GPS/red real de la máquina: sin mockearlo, el test
    # quedaría esperando un diálogo de permiso que headless nunca resuelve,
    # o devolvería coordenadas distintas según dónde corra. Seteando
    # "geolocation" y otorgando el permiso en el contexto ANTES de navegar,
    # el resultado es determinístico y el test prueba que la página refleja
    # exactamente la posición simulada, no una coincidencia con el entorno.
    latitud, longitud = coordenadas_simuladas
    return {
        **browser_context_args,
        "geolocation": {"latitude": latitud, "longitude": longitud},
        "permissions": ["geolocation"],
    }


def test_muestra_la_latitud_y_longitud_simuladas(page, coordenadas_simuladas):
    latitud, longitud = coordenadas_simuladas
    geolocation_page = GeolocationPage(page)
    page.goto(f"{BASE_URL}/geolocation")

    geolocation_page.boton_donde_estoy.click()

    assert float(geolocation_page.latitud.inner_text()) == latitud
    assert float(geolocation_page.longitud.inner_text()) == longitud


def test_el_link_a_google_maps_usa_las_mismas_coordenadas(page, coordenadas_simuladas):
    latitud, longitud = coordenadas_simuladas
    geolocation_page = GeolocationPage(page)
    page.goto(f"{BASE_URL}/geolocation")

    geolocation_page.boton_donde_estoy.click()

    href = geolocation_page.link_mapa.get_attribute("href")
    assert f"q={latitud},{longitud}" in href

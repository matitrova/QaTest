import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from SlowApiPage import SlowApiPage


@pytest.fixture
def slow_api_page(page: Page) -> SlowApiPage:
    page.goto(f"{BASE_URL}/slow_api")
    return SlowApiPage(page)


def test_sin_fallos_responde_en_el_primer_intento(slow_api_page: SlowApiPage) -> None:
    slow_api_page.configurar(delay_ms=0, fail=0, status=500, retry=True)
    slow_api_page.llamar()

    expect(slow_api_page.status_text).to_have_text("Data loaded on attempt 1")
    expect(slow_api_page.attempts).to_have_count(1)
    expect(slow_api_page.attempts.nth(0)).to_have_text("200: Data loaded on attempt 1")


def test_con_reintentos_activados_reintenta_hasta_tener_exito(
    slow_api_page: SlowApiPage,
) -> None:
    # fail=2 con reintentos: los intentos 1 y 2 fallan con 500 y el 3ro
    # responde bien, todo dentro del límite de 3 reintentos que el propio
    # script declara (MAX_RETRIES). Cada reintento espera 1 segundo real
    # antes de reintentar, así que esto tarda ~2 segundos de verdad.
    slow_api_page.configurar(delay_ms=0, fail=2, status=500, retry=True)
    slow_api_page.llamar()

    expect(slow_api_page.status_text).to_have_text(
        "Data loaded on attempt 3", timeout=8_000
    )
    expect(slow_api_page.attempts).to_have_count(3)
    expect(slow_api_page.attempts.nth(0)).to_have_text("500: Attempt 1 failed with 500")
    expect(slow_api_page.attempts.nth(1)).to_have_text("500: Attempt 2 failed with 500")
    expect(slow_api_page.attempts.nth(2)).to_have_text("200: Data loaded on attempt 3")


def test_sin_reintentos_se_rinde_en_el_primer_fallo(slow_api_page: SlowApiPage) -> None:
    # Con el checkbox de reintentos destildado, un solo fallo alcanza para
    # rendirse: no hay segunda vuelta aunque el servidor hubiera respondido
    # bien en el siguiente intento.
    slow_api_page.configurar(delay_ms=0, fail=1, status=429, retry=False)
    slow_api_page.llamar()

    expect(slow_api_page.status_text).to_have_text(
        "Gave up after 1 attempt (last status 429)"
    )
    expect(slow_api_page.attempts).to_have_count(1)


def test_con_reintentos_se_rinde_tras_agotar_los_reintentos(
    slow_api_page: SlowApiPage,
) -> None:
    # fail=5 supera los 3 reintentos disponibles (1 intento inicial + 3
    # reintentos = 4 intentos como máximo), así que el 4to intento también
    # falla y ahí se rinde en vez de probar una 5ta vez. ~3 segundos reales
    # por los tres reintentos de 1 segundo cada uno.
    slow_api_page.configurar(delay_ms=0, fail=5, status=503, retry=True)
    slow_api_page.llamar()

    expect(slow_api_page.status_text).to_have_text(
        "Gave up after 4 attempts (last status 503)", timeout=8_000
    )
    expect(slow_api_page.attempts).to_have_count(4)


def test_boton_se_deshabilita_mientras_la_llamada_esta_en_curso(
    slow_api_page: SlowApiPage,
) -> None:
    # Con un delay real (1000ms) alcanza para observar el estado intermedio:
    # el botón se deshabilita apenas se dispara la llamada y recién vuelve a
    # habilitarse cuando la página ya tiene una respuesta final.
    slow_api_page.configurar(delay_ms=1000, fail=0, status=500, retry=True)
    slow_api_page.llamar()

    expect(slow_api_page.call_button).to_be_disabled()
    expect(slow_api_page.status_text).to_have_text("Loading (attempt 1)...")
    expect(slow_api_page.status_text).to_have_text(
        "Data loaded on attempt 1", timeout=8_000
    )
    expect(slow_api_page.call_button).to_be_enabled()

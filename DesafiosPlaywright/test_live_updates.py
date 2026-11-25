from playwright.sync_api import Page, Request, expect

from config import BASE_URL
from LiveUpdatesPage import LiveUpdatesPage


# El servidor manda 5 actualizaciones separadas por ~1 segundo cuando no se
# pide nada por la URL: el timeout default de expect() (5000ms) queda
# demasiado justo contra esa duración y hace flaky el test.
TIMEOUT_LARGO_MS = 10_000


def test_estado_inicial_sin_actualizaciones(page: Page) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates")

    expect(live_updates_page.estado_conexion).to_have_text("Not connected")
    expect(live_updates_page.actualizaciones).to_have_count(0)
    expect(live_updates_page.boton_iniciar).to_be_enabled()


def test_el_boton_se_deshabilita_apenas_se_hace_click(page: Page) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=3&interval=300")

    live_updates_page.iniciar()

    expect(live_updates_page.boton_iniciar).to_be_disabled()


def test_count_e_interval_de_la_url_se_respetan_dentro_del_rango_valido(
    page: Page,
) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=3&interval=200")

    live_updates_page.iniciar()

    expect(live_updates_page.actualizaciones).to_have_count(3, timeout=TIMEOUT_LARGO_MS)
    expect(live_updates_page.actualizaciones.last).to_have_text("Update 3 of 3")
    expect(live_updates_page.estado_conexion).to_have_text(
        "Done: the server sent all updates"
    )


def test_sin_parametros_en_la_url_llegan_cinco_actualizaciones_por_defecto(
    page: Page,
) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates")

    live_updates_page.iniciar()

    expect(live_updates_page.actualizaciones).to_have_count(5, timeout=TIMEOUT_LARGO_MS)
    expect(live_updates_page.actualizaciones.last).to_have_text("Update 5 of 5")


# El servidor recorta count a como mucho 10 aunque se le pida más: pedir 20
# por la URL (un valor que sí pasa el filtro numérico del propio cliente,
# ver más abajo) sigue trayendo solo 10 actualizaciones.
def test_un_count_mayor_a_diez_se_recorta_a_diez(page: Page) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=20&interval=200")

    live_updates_page.iniciar()

    expect(live_updates_page.actualizaciones).to_have_count(10, timeout=TIMEOUT_LARGO_MS)
    expect(live_updates_page.actualizaciones.last).to_have_text("Update 10 of 10")


# Simétrico al anterior: pedir count=0 no deja al servidor sin nada para
# mandar, lo recorta hacia arriba a 1 actualización en vez de a 0.
def test_un_count_menor_a_uno_se_recorta_a_uno(page: Page) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=0")

    live_updates_page.iniciar()

    expect(live_updates_page.actualizaciones).to_have_count(1, timeout=TIMEOUT_LARGO_MS)
    expect(live_updates_page.actualizaciones.last).to_have_text("Update 1 of 1")


def test_el_data_id_de_cada_actualizacion_sigue_el_lastEventId_en_orden(
    page: Page,
) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=3&interval=200")

    live_updates_page.iniciar()
    expect(live_updates_page.actualizaciones).to_have_count(3, timeout=TIMEOUT_LARGO_MS)

    for indice, actualizacion in enumerate(live_updates_page.actualizaciones.all(), start=1):
        expect(actualizacion).to_have_attribute("data-id", str(indice))


# El propio script de la página sólo reenvía count/interval a la URL del
# EventSource si pasan /^\d+$/ -- un valor no numérico en la URL nunca
# llega a mandarse. Pegándole directo al endpoint (/live_updates/events?
# count=abc) el servidor sí responde, pero con count=abc tratado como 1
# actualización en vez de las 5 por defecto (verificado con curl aparte).
# Para la página esto es invisible: como el cliente nunca llega a mandar
# ese parámetro, el servidor ve el pedido como si no hubiera count en
# absoluto y cae en su default de 5, no en el de 1 del endpoint pelado.
def test_un_count_invalido_en_la_url_se_descarta_y_cae_al_default_del_servidor(
    page: Page,
) -> None:
    pedidos_a_events: list[Request] = []
    page.on(
        "request",
        lambda request: pedidos_a_events.append(request)
        if "/live_updates/events" in request.url
        else None,
    )

    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=abc&interval=abc")

    live_updates_page.iniciar()
    expect(live_updates_page.actualizaciones).to_have_count(5, timeout=TIMEOUT_LARGO_MS)

    assert len(pedidos_a_events) == 1
    assert "count=" not in pedidos_a_events[0].url
    assert "interval=" not in pedidos_a_events[0].url


def test_al_terminar_el_boton_se_reactiva(page: Page) -> None:
    live_updates_page = LiveUpdatesPage(page)
    page.goto(f"{BASE_URL}/live_updates?count=1&interval=200")

    live_updates_page.iniciar()
    expect(live_updates_page.estado_conexion).to_have_text(
        "Done: the server sent all updates", timeout=TIMEOUT_LARGO_MS
    )

    expect(live_updates_page.boton_iniciar).to_be_enabled()

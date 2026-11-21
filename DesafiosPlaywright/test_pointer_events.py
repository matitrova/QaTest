import pytest
from playwright.sync_api import Page

from config import BASE_URL
from PointerEventsPage import PointerEventsPage


@pytest.fixture
def pointer_events_page(page: Page) -> PointerEventsPage:
    page.goto(f"{BASE_URL}/pointer_events")
    return PointerEventsPage(page)


def test_arrastrar_first_debajo_de_third_reordena_la_lista(
    pointer_events_page: PointerEventsPage,
) -> None:
    assert pointer_events_page.orden_actual() == ["First", "Second", "Third", "Fourth"]

    pointer_events_page.arrastrar_item_sobre("First", "Third")

    assert pointer_events_page.orden_actual() == ["Second", "Third", "First", "Fourth"]


def test_swipe_largo_a_la_derecha_se_detecta_como_tal(
    pointer_events_page: PointerEventsPage,
) -> None:
    pointer_events_page.swipe(150)

    # El pointerType viaja en el propio evento nativo -- no es algo que la
    # página adivine a partir del mouse, así que un swipe de mouse se reporta
    # explícitamente como "mouse", a diferencia de un swipe real por touch.
    assert pointer_events_page.resultado_swipe.inner_text() == "Swiped right (mouse)"


def test_swipe_largo_a_la_izquierda_se_detecta_como_tal(
    pointer_events_page: PointerEventsPage,
) -> None:
    pointer_events_page.swipe(-150)

    assert pointer_events_page.resultado_swipe.inner_text() == "Swiped left (mouse)"


def test_swipe_corto_no_cuenta_como_swipe(
    pointer_events_page: PointerEventsPage,
) -> None:
    # La página descarta cualquier desplazamiento de menos de 50px, sin
    # importar la dirección -- un click casi sin mover el mouse no debería
    # contar como "arrastrar para un lado".
    pointer_events_page.swipe(20)

    assert pointer_events_page.resultado_swipe.inner_text() == "Too short to be a swipe"


def test_presion_corta_no_dispara_long_press(
    pointer_events_page: PointerEventsPage,
) -> None:
    pointer_events_page.presionar_boton(duracion_ms=0)

    assert pointer_events_page.resultado_press.inner_text() == "Short press (hold for 800 ms)"


def test_mantener_presionado_800ms_dispara_long_press(
    pointer_events_page: PointerEventsPage,
) -> None:
    pointer_events_page.presionar_boton(duracion_ms=1000)

    assert pointer_events_page.resultado_press.inner_text() == "Long press"

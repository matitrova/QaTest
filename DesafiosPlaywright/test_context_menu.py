import pytest

from config import BASE_URL
from ContextMenuPage import ContextMenuPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py: el script externo de Optimizely
    # que carga el layout del sitio puede colgar el evento "load" y volver
    # flaky la navegación -- se aborta ese pedido para depender solo del
    # sitio bajo prueba.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


# El listener de "dialog" se registra ANTES del clic derecho, igual que en
# javascript_alerts: si el diálogo aparece sin un handler enganchado,
# Playwright lo descarta solo.

def test_clic_derecho_dispara_alert(page):
    context_menu_page = ContextMenuPage(page)
    page.goto(f"{BASE_URL}/context_menu")

    mensajes = []
    page.once("dialog", lambda dialog: (mensajes.append(dialog.message), dialog.accept()))
    context_menu_page.hacer_clic_derecho_en_hot_spot()
    page.wait_for_timeout(200)

    assert mensajes == ["You selected a context menu"]


# El elemento solo tiene un handler de "oncontextmenu", no de "onclick": un
# clic izquierdo sobre el mismo cuadro no dispara ningún diálogo. Sin este
# caso, un test que solo probara el clic derecho no distinguiría "cualquier
# clic abre el diálogo" de "específicamente el clic derecho lo abre".

def test_clic_izquierdo_no_dispara_alert(page):
    context_menu_page = ContextMenuPage(page)
    page.goto(f"{BASE_URL}/context_menu")

    mensajes = []
    page.on("dialog", lambda dialog: (mensajes.append(dialog.message), dialog.accept()))
    context_menu_page.hacer_clic_izquierdo_en_hot_spot()
    page.wait_for_timeout(200)

    assert mensajes == []

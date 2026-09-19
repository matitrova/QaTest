import pytest
from playwright.sync_api import expect

from config import BASE_URL
from WindowsPage import WindowsPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # El layout de the-internet.herokuapp.com carga un script de Optimizely
    # (dominio externo, ajeno a lo que se está probando). Si esa red está
    # lenta o inaccesible, el evento "load" puede colgarse esperándolo y
    # la navegación se vuelve flaky -- se aborta ese pedido explícitamente
    # para que el test dependa solo del sitio bajo prueba.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_abrir_nueva_ventana(page):
    windows_page = WindowsPage(page)
    page.goto(f"{BASE_URL}/windows")

    nueva_pagina = windows_page.hacer_clic_en_abrir_ventana()
    nueva_pagina.wait_for_load_state()

    expect(nueva_pagina).to_have_url(f"{BASE_URL}/windows/new")
    expect(nueva_pagina.locator("h3")).to_have_text("New Window")

    nueva_pagina.close()


def test_ventana_original_no_se_modifica(page):
    windows_page = WindowsPage(page)
    page.goto(f"{BASE_URL}/windows")

    nueva_pagina = windows_page.hacer_clic_en_abrir_ventana()
    nueva_pagina.wait_for_load_state()

    # La pestaña original sigue siendo la misma página, no un redirect
    expect(page).to_have_url(f"{BASE_URL}/windows")
    expect(windows_page.titulo).to_have_text("Opening a new window")
    assert len(page.context.pages) == 2

    nueva_pagina.close()


def test_cerrar_nueva_ventana_no_afecta_original(page):
    windows_page = WindowsPage(page)
    page.goto(f"{BASE_URL}/windows")

    nueva_pagina = windows_page.hacer_clic_en_abrir_ventana()
    nueva_pagina.wait_for_load_state()
    nueva_pagina.close()

    assert len(page.context.pages) == 1
    expect(windows_page.titulo).to_have_text("Opening a new window")

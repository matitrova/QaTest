import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from SpaPage import SpaPage


@pytest.fixture
def spa_page(page: Page) -> SpaPage:
    page.goto(f"{BASE_URL}/spa")
    return SpaPage(page)


def test_home_view_al_cargar_sin_navegaciones(spa_page: SpaPage) -> None:
    expect(spa_page.titulo_vista).to_have_text("Home")
    expect(spa_page.texto_vista).to_have_text(
        "Welcome to the single-page app."
    )
    expect(spa_page.contador).to_have_text(
        "Page loaded once; views shown without a reload: 0"
    )
    expect(spa_page.link_de_nav("Home")).to_have_attribute("aria-current", "page")
    expect(spa_page.link_de_nav("About")).not_to_have_attribute("aria-current", "page")


def test_click_en_about_cambia_la_vista_sin_recargar_la_pagina(
    spa_page: SpaPage, page: Page
) -> None:
    spa_page.marcar_carga_actual()

    spa_page.link_de_nav("About").click()

    expect(spa_page.titulo_vista).to_have_text("About")
    expect(spa_page.texto_vista).to_have_text("This view was drawn by JavaScript.")
    expect(spa_page.contador).to_have_text(
        "Page loaded once; views shown without a reload: 1"
    )
    expect(page).to_have_url(f"{BASE_URL}/spa/about")
    assert not spa_page.hubo_reload()
    expect(spa_page.link_de_nav("About")).to_have_attribute("aria-current", "page")
    expect(spa_page.link_de_nav("Home")).not_to_have_attribute("aria-current", "page")


# El handler de click compara el href del link contra location.pathname antes
# de hacer nada: "if (link.getAttribute('href') === location.pathname) return;".
# Al cargar la página la vista activa ya es Home en /spa, así que clickear el
# propio link de Home -- sin haber navegado a ningún otro lado antes -- cae en
# esa guarda y no hace nada, ni siquiera suma al contador de navegaciones.
def test_click_en_el_link_ya_activo_no_incrementa_el_contador(
    spa_page: SpaPage,
) -> None:
    spa_page.link_de_nav("Home").click()

    expect(spa_page.titulo_vista).to_have_text("Home")
    expect(spa_page.contador).to_have_text(
        "Page loaded once; views shown without a reload: 0"
    )


def test_back_y_forward_disparan_popstate_y_actualizan_la_vista(
    spa_page: SpaPage, page: Page
) -> None:
    spa_page.link_de_nav("About").click()
    spa_page.link_de_nav("Contact").click()
    expect(spa_page.contador).to_have_text(
        "Page loaded once; views shown without a reload: 2"
    )

    page.go_back()
    expect(spa_page.titulo_vista).to_have_text("About")
    expect(page).to_have_url(f"{BASE_URL}/spa/about")
    expect(spa_page.contador).to_have_text(
        "Page loaded once; views shown without a reload: 3"
    )

    page.go_forward()
    expect(spa_page.titulo_vista).to_have_text("Contact")
    expect(page).to_have_url(f"{BASE_URL}/spa/contact")
    expect(spa_page.contador).to_have_text(
        "Page loaded once; views shown without a reload: 4"
    )


def test_navegar_directo_a_url_de_vista_muestra_esa_vista_desde_la_primera_carga(
    page: Page,
) -> None:
    page.goto(f"{BASE_URL}/spa/about")
    spa = SpaPage(page)

    expect(spa.titulo_vista).to_have_text("About")
    expect(spa.contador).to_have_text(
        "Page loaded once; views shown without a reload: 0"
    )
    expect(spa.link_de_nav("About")).to_have_attribute("aria-current", "page")


# El regex del cliente que decide la vista a partir de la URL acepta una
# barra final opcional: "/^\/spa\/(about|contact)\/?$/". Pero esa barra nunca
# llega a ejecutar ese código: el servidor responde 404 para "/spa/about/"
# antes de que el navegador reciba ningún HTML ni corra ningún script -- el
# "\/?" del regex es código muerto, cubre una URL que el propio sitio nunca
# sirve.
def test_url_con_barra_final_no_existe_en_el_servidor(page: Page) -> None:
    respuesta_sin_barra = page.request.get(f"{BASE_URL}/spa/about")
    assert respuesta_sin_barra.status == 200

    respuesta_con_barra = page.request.get(f"{BASE_URL}/spa/about/")
    assert respuesta_con_barra.status == 404

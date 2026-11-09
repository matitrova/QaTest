import requests
from playwright.sync_api import Page, expect

from config import BASE_URL
from JqueryUiMenuPage import JqueryUiMenuPage


def test_los_submenus_estan_cerrados_antes_de_cualquier_hover(page: Page) -> None:
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    expect(menu_page.submenu_disabled).to_be_hidden()
    expect(menu_page.submenu_enabled).to_be_hidden()


def test_hover_en_disabled_no_abre_su_submenu(page: Page) -> None:
    # "Disabled" tiene aria-disabled="true" y, a diferencia de "Enabled",
    # el widget de jQuery UI lo excluye de la interacción: pasar el mouse
    # por encima no dispara el mismo evento que abre los demás submenús,
    # así que "Should not see this" nunca llega a mostrarse.
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    menu_page.link_disabled.hover()
    page.wait_for_timeout(300)

    expect(menu_page.submenu_disabled).to_be_hidden()
    expect(menu_page.link_should_not_see).to_be_hidden()


def test_hover_en_enabled_abre_su_submenu(page: Page) -> None:
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    menu_page.link_enabled.hover()

    expect(menu_page.submenu_enabled).to_be_visible(timeout=2000)


def test_hover_en_downloads_abre_el_submenu_anidado_sin_cerrar_el_padre(
    page: Page,
) -> None:
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    menu_page.link_enabled.hover()
    expect(menu_page.submenu_enabled).to_be_visible(timeout=2000)

    menu_page.link_downloads.hover()

    expect(menu_page.submenu_downloads).to_be_visible(timeout=2000)
    # El submenú padre sigue abierto: entrar al hijo no lo cierra.
    expect(menu_page.submenu_enabled).to_be_visible()


def test_los_tres_enlaces_de_descarga_apuntan_a_archivos_reales_y_distintos(
    page: Page,
) -> None:
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    menu_page.link_enabled.hover()
    menu_page.link_downloads.hover()
    expect(menu_page.submenu_downloads).to_be_visible(timeout=2000)

    hrefs = {
        "pdf": menu_page.enlace_pdf.get_attribute("href"),
        "csv": menu_page.enlace_csv.get_attribute("href"),
        "excel": menu_page.enlace_excel.get_attribute("href"),
    }
    assert len(set(hrefs.values())) == 3

    content_types_esperados = {
        "pdf": "application/pdf",
        "csv": "text/csv",
        "excel": "application/vnd.ms-excel",
    }
    for clave, href in hrefs.items():
        response = requests.get(f"{BASE_URL}{href}", timeout=10)
        assert response.status_code == 200
        assert response.headers["Content-Type"].startswith(
            content_types_esperados[clave]
        )
        assert "attachment" in response.headers["Content-Disposition"]
        assert len(response.content) > 0


def test_click_en_pdf_dispara_una_descarga_real_del_navegador(
    page: Page, tmp_path
) -> None:
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    menu_page.link_enabled.hover()
    menu_page.link_downloads.hover()
    expect(menu_page.submenu_downloads).to_be_visible(timeout=2000)

    with page.expect_download() as info_descarga:
        menu_page.enlace_pdf.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "menu.pdf"
    destino = tmp_path / descarga.suggested_filename
    descarga.save_as(destino)
    assert destino.stat().st_size > 0
    # Un click que dispara una descarga no navega: seguimos en la misma página.
    assert page.url == f"{BASE_URL}/jqueryui/menu"


def test_back_to_jqueryui_es_un_link_real_que_navega(page: Page) -> None:
    # A diferencia de "Downloads", que solo abre un submenú, este item del
    # mismo nivel es un link real: lleva a /jqueryui de verdad.
    menu_page = JqueryUiMenuPage(page)
    page.goto(f"{BASE_URL}/jqueryui/menu")

    menu_page.link_enabled.hover()
    expect(menu_page.submenu_enabled).to_be_visible(timeout=2000)

    with page.expect_navigation():
        menu_page.link_volver.click()

    assert page.url == f"{BASE_URL}/jqueryui"
    expect(page.locator("h3")).to_have_text("JQuery UI")

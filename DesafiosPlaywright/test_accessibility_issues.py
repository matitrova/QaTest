from playwright.sync_api import Page

from config import BASE_URL
from AccessibilityIssuesPage import AccessibilityIssuesPage

REGLAS_ESPERADAS = [
    "image-alt",
    "label",
    "select-name",
    "button-name",
    "link-name",
    "color-contrast",
    "aria-roles",
    "heading-order",
]


def test_la_tabla_documenta_los_ocho_axe_rules_esperados(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert accessibility_page.reglas_documentadas() == REGLAS_ESPERADAS


def test_profile_image_no_tiene_alt(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert accessibility_page.profile_image.get_attribute("alt") is None


def test_search_input_y_size_select_no_tienen_label_asociado(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert not accessibility_page.tiene_label_asociado(accessibility_page.search_input)
    assert not accessibility_page.tiene_label_asociado(accessibility_page.size_select)


def test_icon_button_y_icon_link_no_tienen_aria_label(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert accessibility_page.icon_button.get_attribute("aria-label") is None
    assert accessibility_page.icon_link.get_attribute("aria-label") is None


def test_faint_text_usa_un_gris_claro_de_bajo_contraste(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert accessibility_page.faint_text.get_attribute("style") == "color: #cccccc;"


def test_bad_role_tiene_el_rol_aria_mal_escrito(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert accessibility_page.bad_role.get_attribute("role") == "buton"


# El único heading dentro de ".example" antes de este widget es el <h3> del
# título de la página -- de ahí al <h6> de acá se saltean h4 y h5, que la
# jerarquía de la página no usa en ningún otro lado.
def test_skipped_heading_salta_de_h3_a_h6(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    assert accessibility_page.etiqueta_del_heading() == "H6"


def test_el_link_de_mostrar_fixed_lleva_a_la_version_sin_issues(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues")

    with page.expect_navigation():
        accessibility_page.link_version_alternativa.click()

    assert page.url == f"{BASE_URL}/accessibility_issues?fixed=true"


def test_en_la_version_fixed_los_ocho_widgets_quedan_resueltos(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues?fixed=true")

    assert accessibility_page.profile_image.get_attribute("alt") == "Profile photo"
    assert accessibility_page.tiene_label_asociado(accessibility_page.search_input)
    assert accessibility_page.tiene_label_asociado(accessibility_page.size_select)
    assert accessibility_page.icon_button.get_attribute("aria-label") == "Settings"
    assert accessibility_page.icon_link.get_attribute("aria-label") == "Home"
    assert accessibility_page.faint_text.get_attribute("style") == "color: #595959;"
    assert accessibility_page.bad_role.get_attribute("role") == "button"
    assert accessibility_page.etiqueta_del_heading() == "H4"


def test_el_link_de_la_version_fixed_vuelve_a_la_version_con_issues(page: Page) -> None:
    accessibility_page = AccessibilityIssuesPage(page)
    page.goto(f"{BASE_URL}/accessibility_issues?fixed=true")

    with page.expect_navigation():
        accessibility_page.link_version_alternativa.click()

    assert page.url == f"{BASE_URL}/accessibility_issues"

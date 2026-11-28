from playwright.sync_api import Page

from AdvancedShadowDomPage import AdvancedShadowDomPage
from config import BASE_URL


def test_un_locator_simple_atraviesa_dos_niveles_de_shadow_root_abierto(page: Page) -> None:
    shadow_dom_page = AdvancedShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom_advanced")

    assert shadow_dom_page.resultado_anidado.text_content() == "The button has not been clicked"

    shadow_dom_page.boton_shadow_anidado.click()

    assert (
        shadow_dom_page.resultado_anidado.text_content()
        == "You clicked the button in the inner shadow root"
    )


def test_un_shadow_root_cerrado_es_tan_inaccesible_para_playwright_como_para_un_script(page: Page) -> None:
    shadow_dom_page = AdvancedShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom_advanced")

    assert shadow_dom_page.shadow_root_cerrado_es_null() is True
    # La página anuncia que "WebDriver" sí puede entrar a un shadow root
    # cerrado aunque los scripts no -- pero para los selectores CSS de
    # Playwright, que se resuelven igual que los de cualquier script, el
    # contenido de adentro queda tan afuera de alcance como para la propia
    # página.
    assert shadow_dom_page.texto_cerrado.count() == 0
    assert shadow_dom_page.input_cerrado.count() == 0


def test_los_slots_usan_el_nodo_asignado_salvo_el_que_no_tiene_nada_proyectado(page: Page) -> None:
    shadow_dom_page = AdvancedShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom_advanced")

    assert shadow_dom_page.texto_asignado_al_slot("title") == "Title from the light DOM"
    assert shadow_dom_page.texto_asignado_al_slot("body") == "Body from the light DOM"
    # El HTML liviano no tiene ningún hijo con slot="footer", así que ese
    # slot no tiene ningún nodo asignado -- su fallback nunca se reemplaza.
    assert shadow_dom_page.texto_asignado_al_slot("footer") is None


def test_el_formulario_no_envia_sin_elegir_estrella_por_la_validacion_personalizada(page: Page) -> None:
    shadow_dom_page = AdvancedShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom_advanced")

    shadow_dom_page.campo_nombre.fill("Mati")
    shadow_dom_page.enviar_formulario()

    # El formulario tiene novalidate: la única validación que corre es la
    # del propio custom element vía ElementInternals.setValidity(), con un
    # mensaje de error elegido por el componente, no uno genérico del browser.
    assert shadow_dom_page.resultado_form.text_content() == "Error: Pick a rating"


def test_elegir_una_estrella_actualiza_los_iconos_y_permite_enviar_el_formulario(page: Page) -> None:
    shadow_dom_page = AdvancedShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom_advanced")

    assert shadow_dom_page.iconos_de_estrellas() == ["☆", "☆", "☆", "☆", "☆"]

    shadow_dom_page.elegir_estrella(3)

    assert shadow_dom_page.iconos_de_estrellas() == ["★", "★", "★", "☆", "☆"]

    shadow_dom_page.campo_nombre.fill("Mati")
    shadow_dom_page.enviar_formulario()

    assert shadow_dom_page.resultado_form.text_content() == "Submitted name: Mati, rating: 3"

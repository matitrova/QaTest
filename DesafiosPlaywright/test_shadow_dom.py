from playwright.sync_api import Page

from config import BASE_URL
from ShadowDomPage import ShadowDomPage


def test_hay_dos_custom_elements_con_shadow_root_abierto(page: Page) -> None:
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    assert shadow_dom_page.hosts.count() == 2
    assert shadow_dom_page.tiene_shadow_root_abierto(0) is True
    assert shadow_dom_page.tiene_shadow_root_abierto(1) is True


def test_el_primer_elemento_proyecta_un_span_como_slot(page: Page) -> None:
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    assert shadow_dom_page.nodo_proyectado_al_slot(0) == "SPAN"
    assert shadow_dom_page.texto_renderizado(0) == "Let's have some different text!"


def test_el_segundo_elemento_proyecta_una_lista_como_slot(page: Page) -> None:
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    assert shadow_dom_page.nodo_proyectado_al_slot(1) == "UL"
    assert shadow_dom_page.texto_renderizado(1) == "Let's have some different text!\nIn a list!"


# El <p> que vive dentro del shadow root solo tiene, en el árbol liviano, el
# contenido de fallback del <slot> -- el nodo real que el navegador proyecta
# ahí al pintar la página no es descendiente de ese <p> en el DOM, así que
# text_content() no lo alcanza y devuelve el texto que nunca se ve en pantalla.
def test_leer_el_parrafo_interno_devuelve_el_fallback_no_el_texto_proyectado(page: Page) -> None:
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    assert shadow_dom_page.texto_crudo_del_parrafo_interno(0) == "My default text"
    assert shadow_dom_page.texto_crudo_del_parrafo_interno(1) == "My default text"
    assert shadow_dom_page.texto_renderizado(0) != shadow_dom_page.texto_crudo_del_parrafo_interno(0)


def test_los_dos_elementos_son_independientes_entre_si(page: Page) -> None:
    shadow_dom_page = ShadowDomPage(page)
    page.goto(f"{BASE_URL}/shadowdom")

    primero = shadow_dom_page.texto_renderizado(0)
    segundo = shadow_dom_page.texto_renderizado(1)

    assert primero != segundo
    assert primero in segundo

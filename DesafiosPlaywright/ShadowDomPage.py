from base_page import BasePage
from playwright.sync_api import Locator, Page


class ShadowDomPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # <my-paragraph> es un custom element con shadow root abierto. Su
        # <p id="..."> interno no tiene contenido propio: solo envuelve un
        # <slot>, que en runtime se rellena con los nodos que el HTML "liviano"
        # (fuera del shadow root) le asigna vía el atributo slot="my-text".
        self.hosts: Locator = page.locator("my-paragraph")
        self.parrafos_internos: Locator = page.locator("my-paragraph p")

    def texto_renderizado(self, indice: int) -> str:
        # inner_text() sobre el custom element (el host, fuera del shadow
        # root) sigue el árbol ya aplanado por el navegador, con el <slot>
        # reemplazado por lo que de verdad se ve en pantalla.
        return self.hosts.nth(indice).inner_text()

    def texto_crudo_del_parrafo_interno(self, indice: int) -> str:
        # El mismo texto, pero leído directamente del <p> que vive DENTRO
        # del shadow root. Ese <p> solo contiene el <slot> con su contenido
        # de fallback ("My default text") -- el nodo proyectado de verdad
        # nunca estuvo ahí en el árbol liviano, así que text_content() no lo
        # ve. Sirve para probar, dentro del propio test, por qué hay que leer
        # el texto desde el host y no desde el elemento que lo "contiene".
        return self.parrafos_internos.nth(indice).text_content() or ""

    def tiene_shadow_root_abierto(self, indice: int) -> bool:
        return self.hosts.nth(indice).evaluate("el => el.shadowRoot !== null")

    def nodo_proyectado_al_slot(self, indice: int) -> str:
        return self.hosts.nth(indice).evaluate(
            "el => el.shadowRoot.querySelector('slot').assignedNodes()[0].tagName"
        )

from base_page import BasePage
from playwright.sync_api import Page


class ResponsivePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_menu = page.locator("#menu-toggle")
        self.menu = page.locator("#site-nav")
        self.resultado_nav = page.locator("#nav-result")
        self.cards = page.locator("#cards .card")

    def link_de_menu(self, texto: str):
        return self.menu.get_by_role("link", name=texto)

    def layout_actual(self) -> str:
        # El nombre del layout no es texto del DOM: lo pone un pseudo-elemento
        # ::after por CSS (`#layout-name::after { content: "desktop"; }` /
        # "mobile" bajo el media query). `text_content()` sobre #layout-name
        # da siempre vacío porque ese contenido nunca es un nodo de texto; hay
        # que leerlo con `getComputedStyle(el, "::after").content`, que además
        # devuelve el valor con comillas literales (`'"desktop"'`) porque así
        # serializa la propiedad CSS `content`.
        valor = self.page.eval_on_selector(
            "#layout-name", "el => getComputedStyle(el, '::after').content"
        )
        return valor.strip('"')

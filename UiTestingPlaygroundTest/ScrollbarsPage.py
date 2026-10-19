from base_page import BasePage
from playwright.sync_api import Page


class ScrollbarsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # El contenedor scrolleable es el único div con overflow-y/overflow-x
        # en la página: scrollea tanto vertical como horizontalmente porque
        # el contenido interno (600x300) es más grande que la ventana visible
        # que deja (300x150).
        self.contenedor = page.locator("div[style*='overflow-y: scroll']")
        self.boton = page.locator("#hidingButton")

    def box_contenedor(self):
        return self.contenedor.bounding_box()

    def box_boton(self):
        return self.boton.bounding_box()

    def scroll_actual(self):
        return self.contenedor.evaluate("el => [el.scrollLeft, el.scrollTop]")

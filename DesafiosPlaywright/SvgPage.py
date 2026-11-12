from base_page import BasePage
from playwright.sync_api import Locator, Page


class SvgPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.resultado: Locator = page.locator("#result")
        self.barra_manzanas: Locator = page.locator("#bar-apples")
        self.barra_bananas: Locator = page.locator("#bar-bananas")
        self.barra_cerezas: Locator = page.locator("#bar-cherries")
        self.circulo: Locator = page.locator("#toggle-circle")
        self.etiqueta_circulo: Locator = page.locator("#circle-label")

    def texto_resultado(self) -> str:
        return self.resultado.inner_text()

    def texto_etiqueta_circulo(self) -> str:
        # <text> es un elemento SVG, no HTML: inner_text() asume un
        # HTMLElement y tira "Node is not an HTMLElement". text_content()
        # sí funciona porque lee el nodo de texto crudo sin pasar por el
        # layout box que inner_text() necesita.
        return self.etiqueta_circulo.text_content() or ""

from base_page import BasePage
from playwright.sync_api import Page


class InputsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.input_numero = page.locator("input[type=number]")

    def escribir(self, texto):
        self.input_numero.fill("")
        self.input_numero.type(texto)

    def presionar_flecha_arriba(self, veces=1):
        for _ in range(veces):
            self.input_numero.press("ArrowUp")

    def presionar_flecha_abajo(self, veces=1):
        for _ in range(veces):
            self.input_numero.press("ArrowDown")

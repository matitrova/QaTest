from base_page import BasePage
from playwright.sync_api import Locator, Page


class AutocompletePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.input: Locator = page.locator("#autocomplete")
        self.lista: Locator = page.locator("#suggestions")
        self.status: Locator = page.locator("#status")
        self.seleccionado: Locator = page.locator("#selected")

    def opciones(self) -> Locator:
        return self.lista.locator("[role=option]")

    def opcion(self, texto: str) -> Locator:
        return self.lista.get_by_role("option", name=texto, exact=True)

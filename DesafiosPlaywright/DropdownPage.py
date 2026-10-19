from base_page import BasePage
from playwright.sync_api import Page


class DropdownPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.dropdown = page.locator("#dropdown")

    def seleccionar_por_valor(self, valor):
        self.dropdown.select_option(value=valor)

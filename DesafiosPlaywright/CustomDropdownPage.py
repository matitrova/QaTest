from base_page import BasePage
from playwright.sync_api import Locator, Page


class CustomDropdownPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.combo: Locator = page.locator("#fruit-combo")
        self.listbox: Locator = page.locator("#fruit-listbox")
        self.resultado: Locator = page.locator("#result")

    def opcion(self, valor: str) -> Locator:
        return self.page.locator(f"#fruit-{valor}")

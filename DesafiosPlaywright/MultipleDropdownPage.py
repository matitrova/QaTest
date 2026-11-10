from base_page import BasePage
from playwright.sync_api import Locator, Page


class MultipleDropdownPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.dropdown = page.locator("#multiple-dropdown")
        self.opciones = page.locator("#multiple-dropdown option")

    def opciones_tildadas(self) -> Locator:
        return self.dropdown.locator("option:checked")

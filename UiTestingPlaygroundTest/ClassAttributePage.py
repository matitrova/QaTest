from base_page import BasePage
from playwright.sync_api import Page


class ClassAttributePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_success = page.locator("button.btn-success")
        self.boton_warning = page.locator("button.btn-warning")
        self.boton_primary = page.locator("button.btn-primary")

    def hacer_clic_en_primary(self):
        self.boton_primary.click()

    def hacer_clic_en_success(self):
        self.boton_success.click()

    def hacer_clic_en_warning(self):
        self.boton_warning.click()

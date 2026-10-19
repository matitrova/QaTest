from base_page import BasePage
from playwright.sync_api import Page


class BasicAuthPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.mensaje_exito = page.locator(".example p")

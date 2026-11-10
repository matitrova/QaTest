from base_page import BasePage
from playwright.sync_api import Page


class ABTestingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.titulo = page.locator(".example h3")
        self.descripcion = page.locator(".example p")

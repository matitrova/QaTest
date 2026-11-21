from base_page import BasePage
from playwright.sync_api import Locator, Page


class JavascriptErrorPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.parrafo: Locator = page.locator("body p")

from base_page import BasePage
from playwright.sync_api import Page


class RedirectorPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.link_redirect = page.locator("#redirect")

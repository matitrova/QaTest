from base_page import BasePage
from playwright.sync_api import Page


class DisappearingElementsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.locator(".example ul li a")

    def textos(self):
        return self.items.all_inner_texts()

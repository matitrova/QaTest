from base_page import BasePage
from playwright.sync_api import Page


class DynamicLoadingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.start_button = page.locator("#start button")
        self.finish_text = page.locator("#finish")

    def hacer_clic_en_start(self):
        self.start_button.click()

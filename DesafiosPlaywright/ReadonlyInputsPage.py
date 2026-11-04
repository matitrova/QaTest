from base_page import BasePage
from playwright.sync_api import Page


class ReadonlyInputsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.checkbox = page.locator("#checkbox")
        self.textfield = page.locator("#textfield")
        self.always_readonly = page.locator("#always-readonly")
        self.disabled = page.locator("#disabled")

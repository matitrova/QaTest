from base_page import BasePage
from playwright.sync_api import Page


class SlowApiPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.delay_input = page.locator("#delay")
        self.fail_input = page.locator("#fail")
        self.status_select = page.locator("#status")
        self.retry_checkbox = page.locator("#retry")
        self.call_button = page.locator("#call-api")
        self.status_text = page.locator("#status-text")
        self.attempts = page.locator("#attempts li")

    def configurar(self, *, delay_ms: int, fail: int, status: int, retry: bool) -> None:
        self.delay_input.fill(str(delay_ms))
        self.fail_input.fill(str(fail))
        self.status_select.select_option(str(status))
        if self.retry_checkbox.is_checked() != retry:
            self.retry_checkbox.click()

    def llamar(self) -> None:
        self.call_button.click()

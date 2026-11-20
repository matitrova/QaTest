from base_page import BasePage
from playwright.sync_api import Locator, Page


class NetworkConsolePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.fetch_json_button = page.locator("#fetch-json")
        self.fetch_error_button = page.locator("#fetch-error")
        self.log_console_button = page.locator("#log-console")
        self.throw_error_button = page.locator("#throw-error")
        self.csp_violation_button = page.locator("#csp-violation")
        self.event_log = page.locator("#event-log")

    def entrada_de_log(self, clase: str) -> Locator:
        return self.event_log.locator(f"li.{clase}")

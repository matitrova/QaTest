from base_page import BasePage
from playwright.sync_api import Page


class AlertsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.alert_button = page.locator("#alertButton")
        self.confirm_button = page.locator("#confirmButton")
        self.prompt_button = page.locator("#promptButton")

    def hacer_clic_en_alert(self):
        self.alert_button.click()

    def hacer_clic_en_confirm(self):
        self.confirm_button.click()

    def hacer_clic_en_prompt(self):
        self.prompt_button.click()

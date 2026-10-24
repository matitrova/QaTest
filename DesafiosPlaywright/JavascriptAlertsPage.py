from base_page import BasePage
from playwright.sync_api import Page


class JavascriptAlertsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.alert_button = page.locator('button[onclick="jsAlert()"]')
        self.confirm_button = page.locator('button[onclick="jsConfirm()"]')
        self.prompt_button = page.locator('button[onclick="jsPrompt()"]')
        self.result_text = page.locator("#result")

    def hacer_clic_en_alert(self) -> None:
        self.alert_button.click()

    def hacer_clic_en_confirm(self) -> None:
        self.confirm_button.click()

    def hacer_clic_en_prompt(self) -> None:
        self.prompt_button.click()

from base_page import BasePage
from playwright.sync_api import Page


class FormAuthenticationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.submit = page.locator("button[type='submit']")
        self.flash = page.locator("#flash")
        self.logout = page.locator("a.button.secondary.radius")

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

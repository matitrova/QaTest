from base_page import BasePage
from playwright.sync_api import Page


class TwoFactorLoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_submit = page.locator("#two-factor-login button[type='submit']")
        self.otp_code = page.locator("#otp-code")
        self.code = page.locator("#code")
        self.code_submit = page.locator("#two-factor-code button[type='submit']")
        self.flash = page.locator("#flash")
        self.logout = page.locator("a.button.secondary.radius")

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_submit.click()

    def leer_otp(self) -> str:
        return self.otp_code.inner_text()

    def verificar_codigo(self, code: str) -> None:
        self.code.fill(code)
        self.code_submit.click()

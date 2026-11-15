from base_page import BasePage
from playwright.sync_api import Locator, Page


class FormValidationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username: Locator = page.locator("#username")
        self.email: Locator = page.locator("#email")
        self.age: Locator = page.locator("#age")
        self.website: Locator = page.locator("#website")
        self.password: Locator = page.locator("#password")
        self.terms: Locator = page.locator("#terms")
        self.boton_enviar: Locator = page.locator("button[type=submit]")
        self.resultado: Locator = page.locator("#result")

    def error(self, campo: str) -> Locator:
        return self.page.locator(f"#{campo}-error")

    def completar(
        self,
        username: str = "zzqatest",
        email: str = "zzqatest@example.com",
        age: str = "25",
        website: str = "",
        password: str = "password123",
        terms: bool = True,
    ) -> None:
        self.username.fill(username)
        self.email.fill(email)
        self.age.fill(age)
        self.website.fill(website)
        self.password.fill(password)
        if terms:
            self.terms.check()
        else:
            self.terms.uncheck()

    def enviar(self) -> None:
        self.boton_enviar.click()

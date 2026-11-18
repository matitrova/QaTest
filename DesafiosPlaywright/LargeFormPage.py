from base_page import BasePage
from playwright.sync_api import Locator, Page


class LargeFormPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name: Locator = page.locator("#first-name")
        self.last_name: Locator = page.locator("#last-name")
        self.email: Locator = page.locator("input[name=email]")
        self.age: Locator = page.locator("input[name=age]")
        self.country: Locator = page.locator("#country")
        self.languages: Locator = page.locator("select[name='languages[]']")
        self.experience: Locator = page.locator("#experience")
        self.experience_valor: Locator = page.locator("#experience-value")
        self.terms: Locator = page.locator("#terms")
        self.boton_enviar: Locator = page.locator("button#submit")
        self.boton_reset: Locator = page.locator("button[type=reset]")
        self.titulo: Locator = page.locator("h3")
        self.tabla_resultado: Locator = page.locator("#submitted-data")

    def contacto(self, valor: str) -> Locator:
        return self.page.locator(f"input[name=contact][value={valor}]")

    def interes(self, valor: str) -> Locator:
        return self.page.locator(f"input.interest[value={valor}]")

    def fila(self, campo: str) -> Locator:
        return self.tabla_resultado.locator(f'tr:has(td:text-is("{campo}"))')

    def valor_en_tabla(self, campo: str) -> Locator:
        return self.fila(campo).locator("td").nth(1)

from base_page import BasePage
from playwright.sync_api import Locator, Page


class DynamicContentPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.filas: Locator = page.locator(".large-10.columns.large-centered > .row")

    def cantidad_de_filas(self) -> int:
        return self.filas.count()

    def fila(self, indice: int) -> tuple[str | None, str]:
        fila = self.filas.nth(indice)
        imagen = fila.locator("img").get_attribute("src")
        texto = fila.locator(".large-10.columns").inner_text().strip()
        return imagen, texto

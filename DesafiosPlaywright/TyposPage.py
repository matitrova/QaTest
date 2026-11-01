from base_page import BasePage
from playwright.sync_api import Locator, Page


class TyposPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.titulo: Locator = page.locator("div.example h3")
        self._parrafos: Locator = page.locator("div.example p")

    def texto_titulo(self) -> str:
        return self.titulo.inner_text()

    def texto_introductorio(self) -> str:
        return self._parrafos.nth(0).inner_text()

    def texto_variable(self) -> str:
        return self._parrafos.nth(1).inner_text()

    def cantidad_de_parrafos(self) -> int:
        return self._parrafos.count()

from base_page import BasePage
from playwright.sync_api import Locator, Page


class LargeDomPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.no_siblings = page.locator("#no-siblings")
        self.tabla = page.locator("#large-table")

    def hermano(self, tier: int, item: int) -> Locator:
        return self.page.locator(f"[id='sibling-{tier}.{item}']")

    def celda(self, fila: int, columna: int) -> Locator:
        return self.tabla.locator(f".row-{fila} .column-{columna}")

from base_page import BasePage
from playwright.sync_api import Locator, Page


class HoversPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.figuras = page.locator(".figure")

    def figura(self, indice: int) -> Locator:
        return self.figuras.nth(indice)

    def caption_de(self, indice: int) -> Locator:
        return self.figura(indice).locator(".figcaption")

    def pasar_el_mouse_por(self, indice: int) -> None:
        self.figura(indice).hover()

from base_page import BasePage
from playwright.sync_api import Page


class InfiniteScrollPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.parrafos = page.locator(".jscroll-added")

    def cantidad_de_parrafos(self) -> int:
        return self.parrafos.count()

    def scrollear_un_poco_sin_llegar_al_fondo(self) -> None:
        self.page.evaluate("window.scrollTo(0, 50)")

    def scrollear_hasta_el_fondo(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

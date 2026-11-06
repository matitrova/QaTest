from base_page import BasePage
from playwright.sync_api import ElementHandle, Locator, Page


class StaleElementPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_reconstruir: Locator = page.locator("#rerender")
        self.items: Locator = page.locator("li.item")
        self.contador: Locator = page.locator("#render-count")
        self.estado_timer: Locator = page.locator("#timer-status")

    def item(self, indice: int) -> Locator:
        return self.page.locator(f"li.item[data-index='{indice}']")

    def handle_del_item(self, indice: int) -> ElementHandle:
        # A diferencia de un Locator, un ElementHandle apunta a un nodo del
        # DOM concreto y no se vuelve a resolver solo: si ese nodo se tira
        # a la basura, el handle se queda apuntando a un nodo "obsoleto".
        handle = self.item(indice).element_handle()
        assert handle is not None
        return handle

    def reconstruir(self) -> None:
        self.boton_reconstruir.click()

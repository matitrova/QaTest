from base_page import BasePage
from playwright.sync_api import Page


class ContextMenuPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.hot_spot = page.locator("#hot-spot")

    def hacer_clic_derecho_en_hot_spot(self) -> None:
        self.hot_spot.click(button="right")

    def hacer_clic_izquierdo_en_hot_spot(self) -> None:
        self.hot_spot.click()

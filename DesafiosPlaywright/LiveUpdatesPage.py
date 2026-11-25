from base_page import BasePage
from playwright.sync_api import Locator, Page


class LiveUpdatesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_iniciar: Locator = page.locator("#start")
        self.estado_conexion: Locator = page.locator("#connection")
        self.actualizaciones: Locator = page.locator("#updates li.update")

    def iniciar(self) -> None:
        self.boton_iniciar.click()

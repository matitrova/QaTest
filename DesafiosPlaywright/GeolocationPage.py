from base_page import BasePage
from playwright.sync_api import Page


class GeolocationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_donde_estoy = page.get_by_role("button", name="Where am I?")
        self.latitud = page.locator("#lat-value")
        self.longitud = page.locator("#long-value")
        self.link_mapa = page.locator("#map-link a")

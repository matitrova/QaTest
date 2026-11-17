from base_page import BasePage
from playwright.sync_api import Page


class LocalePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.saludo = page.locator("#greeting")
        self.idioma_del_servidor = page.locator("#server-language")
        self.idioma_del_navegador = page.locator("#browser-language")
        self.zona_horaria_del_navegador = page.locator("#browser-timezone")
        self.fecha_formateada = page.locator("#formatted-date")
        self.numero_formateado = page.locator("#formatted-number")
        self.precio_formateado = page.locator("#formatted-price")

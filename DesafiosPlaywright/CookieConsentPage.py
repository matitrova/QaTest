from base_page import BasePage
from playwright.sync_api import Page


class CookieConsentPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.banner = page.locator("#cookie-banner")
        self.estado = page.locator("#consent-status")
        self.olvidar_eleccion = page.locator("#reset-consent")
        self.aceptar_todo = page.locator("#accept-all")
        self.solo_necesarias = page.locator("#reject-all")
        self.personalizar = page.locator("#customize")
        self.panel_personalizar = page.locator("#cookie-settings")
        self.checkbox_necesarias = page.locator("#necessary-cookies")
        self.checkbox_analitica = page.locator("#analytics-cookies")
        self.guardar_eleccion = page.locator("#save-settings")

    def texto_estado(self) -> str:
        return self.estado.inner_text()

    def cookie_consent(self) -> str | None:
        for cookie in self.page.context.cookies():
            if cookie["name"] == "cookie_consent":
                return cookie["value"]
        return None

    def olvidar(self) -> None:
        self.olvidar_eleccion.click()

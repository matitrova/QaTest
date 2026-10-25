from base_page import BasePage
from playwright.sync_api import Page


class HiddenLayersPage(BasePage):
    CLASE_BOTON_VERDE = "btn btn-success"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_verde = page.locator("#greenButton")
        self.boton_azul = page.locator("#blueButton")
        self.aviso = page.locator(".bg-warning")

    def clickear_boton_verde(self) -> None:
        self.boton_verde.click()

    def clickear_boton_verde_forzado(self) -> None:
        # `force=True` salta el chequeo de actionability de Playwright (que
        # incluye "no está tapado por otro elemento"), pero sigue
        # disparando un click real vía CDP en las coordenadas del elemento.
        # El navegador resuelve el target de ese click por hit-testing real,
        # igual que con un usuario físico: si hay otro elemento encima en
        # esas coordenadas, el evento llega a ESE elemento, no al que pedía
        # el locator.
        self.boton_verde.click(force=True)

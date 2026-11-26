import re

from base_page import BasePage
from playwright.sync_api import Locator, Page


class VisualDifferencesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.tarjeta: Locator = page.locator("#card")
        self.logo: Locator = page.locator("#card-logo")
        self.titulo: Locator = page.locator("#card-title")
        self.texto: Locator = page.locator("#card-text")
        self.boton: Locator = page.locator("#card-button")

    def texto_titulo(self) -> str:
        return self.titulo.inner_text()

    def logo_es_visible(self) -> bool:
        return self.logo.is_visible()

    def estilo_de_la_tarjeta(self) -> str | None:
        return self.tarjeta.get_attribute("style")

    def desplazamiento_del_boton_en_px(self) -> int:
        estilo = self.boton.get_attribute("style") or ""
        coincidencia = re.search(r"left:\s*(-?\d+)px", estilo)
        assert coincidencia is not None, f"No se encontró 'left' en el style: {estilo!r}"
        return int(coincidencia.group(1))

    def color_de_fondo_del_boton(self) -> str:
        estilo = self.boton.get_attribute("style") or ""
        coincidencia = re.search(r"background-color:\s*(#[0-9a-f]+)", estilo)
        assert coincidencia is not None, f"No se encontró 'background-color' en el style: {estilo!r}"
        return coincidencia.group(1)

from base_page import BasePage
from playwright.sync_api import Page


import re

PATRON_GUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


class ShadowDomPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.campo_guid = page.locator("#editField")
        self.boton_generar = page.locator("#buttonGenerate")
        self.boton_copiar = page.locator("#buttonCopy")

    def generar_guid(self) -> None:
        self.boton_generar.click()

    def copiar_guid(self) -> None:
        self.boton_copiar.click()

    def valor_actual(self) -> str:
        return self.campo_guid.input_value()

    def esta_dentro_de_un_shadow_root(self) -> bool:
        return self.campo_guid.evaluate("el => el.getRootNode() instanceof ShadowRoot")

    def encontrable_desde_el_document_global(self) -> bool:
        return self.page.evaluate("() => document.querySelector('#editField')") is not None

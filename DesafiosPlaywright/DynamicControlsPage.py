from base_page import BasePage
from playwright.sync_api import Page


class DynamicControlsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_checkbox = page.locator("#checkbox-example button")
        # El HTML original tiene un <div id="checkbox"> que envuelve al
        # <input> (sin id propio), pero toggleCheckboxControls() reinserta
        # el checkbox como `<div><input id='checkbox'>...</div>` -- el id
        # pasa del div al input cuando se lo agrega de nuevo. Un locator que
        # sirva en los dos estados no puede depender de dónde vive el id.
        self.checkbox = page.locator("#checkbox-example input[type='checkbox']")
        self.loading_checkbox = page.locator("#checkbox-example #loading")
        self.boton_input = page.locator("#input-example button")
        self.input = page.locator("#input-example input")
        self.loading_input = page.locator("#input-example #loading")
        self.mensaje = page.locator("#message")

    def quitar_checkbox(self) -> None:
        self.boton_checkbox.click()

    def agregar_checkbox(self) -> None:
        self.boton_checkbox.click()

    def habilitar_input(self) -> None:
        self.boton_input.click()

    def deshabilitar_input(self) -> None:
        self.boton_input.click()

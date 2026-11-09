from base_page import BasePage
from playwright.sync_api import Locator, Page


class NativeDialogPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.open_modal_button = page.locator("#open-modal")
        self.open_non_modal_button = page.locator("#open-non-modal")
        self.modal_dialog = page.locator("#modal-dialog")
        self.modal_name = page.locator("#modal-name")
        self.modal_confirm = page.locator("#modal-confirm")
        self.modal_cancel = page.locator("#modal-cancel")
        self.non_modal_dialog = page.locator("#non-modal-dialog")
        self.non_modal_close = page.locator("#non-modal-close")
        self.page_input = page.locator("#page-input")
        self.result = page.locator("#result")

    def abrir_modal(self) -> None:
        self.open_modal_button.click()

    def abrir_no_modal(self) -> None:
        self.open_non_modal_button.click()

    def confirmar_modal(self, nombre: str = "") -> None:
        if nombre:
            self.modal_name.fill(nombre)
        self.modal_confirm.click()

    def cancelar_modal(self, nombre: str = "") -> None:
        if nombre:
            self.modal_name.fill(nombre)
        self.modal_cancel.click()

    def cerrar_no_modal(self) -> None:
        self.non_modal_close.click()

    def esta_abierto(self, dialogo: Locator) -> bool:
        return dialogo.evaluate("el => el.open")

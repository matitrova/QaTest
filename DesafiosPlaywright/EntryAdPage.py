from base_page import BasePage
from playwright.sync_api import Page


class EntryAdPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.modal = page.locator("#modal")
        self.modal_body = page.locator("#modal .modal-body")
        self.cerrar = page.locator("#modal .modal-footer")
        self.reiniciar = page.locator("#restart-ad")

    def anuncio_visible(self) -> bool:
        return self.modal.is_visible()

    def hacer_clic_dentro_del_modal(self) -> None:
        self.modal_body.click()

    def cerrar_anuncio(self) -> None:
        self.cerrar.click()

    def hacer_clic_en_reiniciar(self) -> None:
        self.reiniciar.click()

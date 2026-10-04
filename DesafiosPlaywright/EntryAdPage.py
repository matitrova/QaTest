class EntryAdPage:
    def __init__(self, page):
        self.page = page
        self.modal = page.locator("#modal")
        self.modal_body = page.locator("#modal .modal-body")
        self.cerrar = page.locator("#modal .modal-footer")
        self.reiniciar = page.locator("#restart-ad")

    def anuncio_visible(self):
        return self.modal.is_visible()

    def hacer_clic_dentro_del_modal(self):
        self.modal_body.click()

    def cerrar_anuncio(self):
        self.cerrar.click()

    def hacer_clic_en_reiniciar(self):
        self.reiniciar.click()

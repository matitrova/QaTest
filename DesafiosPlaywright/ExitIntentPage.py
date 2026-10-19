from base_page import BasePage
from playwright.sync_api import Page


class ExitIntentPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.modal = page.locator("#ouibounce-modal")
        self.contenido_modal = page.locator("#ouibounce-modal .modal-body")
        self.cerrar = page.locator("#ouibounce-modal .modal-footer")

    def modal_visible(self):
        return self.modal.is_visible()

    def simular_salida_del_mouse_por_arriba(self):
        # ouibounce solo dispara si el mouse sale del viewport con clientY
        # por debajo del umbral de sensibilidad (20px) -- hay que entrar a
        # la página primero y recién después salir por arriba, no alcanza
        # con mover el mouse a cualquier coordenada negativa.
        self.page.mouse.move(400, 300)
        self.page.mouse.move(400, 0)
        self.page.mouse.move(400, -50)

    def mover_mouse_sin_salir_por_arriba(self):
        self.page.mouse.move(400, 300)
        self.page.mouse.move(400, 700)

    def hacer_clic_dentro_del_modal(self):
        self.contenido_modal.click()

    def cerrar_modal(self):
        self.cerrar.click()

from base_page import BasePage
from playwright.sync_api import Page


class ClientDelayPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_cliente = page.locator("#ajaxButton")
        self.spinner = page.locator("#spinner")
        self.contenido = page.locator("#content")
        self.etiqueta_cargada = page.locator("#content p")

    def disparar_calculo(self) -> None:
        self.boton_cliente.click()

    def esperar_etiqueta(self, timeout: int = 20000) -> None:
        # Los 15 segundos de este botón son un setTimeout en el navegador, no
        # una respuesta de servidor: no hay ningún pedido de red que esperar,
        # pero el timeout default de expect() (5000ms) sigue quedando corto
        # contra esa demora simulada.
        self.etiqueta_cargada.wait_for(state="visible", timeout=timeout)

    def texto_etiqueta(self) -> str:
        return self.etiqueta_cargada.inner_text()

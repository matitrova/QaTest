class ClientDelayPage:
    def __init__(self, page):
        self.page = page
        self.boton_cliente = page.locator("#ajaxButton")
        self.spinner = page.locator("#spinner")
        self.contenido = page.locator("#content")
        self.etiqueta_cargada = page.locator("#content p")

    def disparar_calculo(self):
        self.boton_cliente.click()

    def esperar_etiqueta(self, timeout=20000):
        # Los 15 segundos de este botón son un setTimeout en el navegador, no
        # una respuesta de servidor: no hay ningún pedido de red que esperar,
        # pero el timeout default de expect() (5000ms) sigue quedando corto
        # contra esa demora simulada.
        self.etiqueta_cargada.wait_for(state="visible", timeout=timeout)

    def texto_etiqueta(self):
        return self.etiqueta_cargada.inner_text()

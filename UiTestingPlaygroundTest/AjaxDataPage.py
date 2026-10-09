class AjaxDataPage:
    def __init__(self, page):
        self.page = page
        self.boton_ajax = page.locator("#ajaxButton")
        self.spinner = page.locator("#spinner")
        self.contenido = page.locator("#content")
        self.etiqueta_cargada = page.locator("#content p")

    def disparar_pedido(self):
        self.boton_ajax.click()

    def esperar_etiqueta(self, timeout=20000):
        # El servidor tarda 15 segundos reales en responder a /ajaxdata antes
        # de que el callback de $.get() inserte el <p>: hay que esperar ese
        # elemento en vez de asumir un tiempo fijo, con margen sobre esos 15s.
        self.etiqueta_cargada.wait_for(state="visible", timeout=timeout)

    def texto_etiqueta(self):
        return self.etiqueta_cargada.inner_text()

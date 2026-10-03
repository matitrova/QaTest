class ClickPage:
    CLASE_INICIAL = "btn btn-primary"
    CLASE_AL_CLICKEAR = "btn btn-success"

    def __init__(self, page):
        self.page = page
        self.boton = page.locator("#badButton")

    def clickear_via_js(self):
        # El handler de esta página filtra el evento de click por
        # `event.screenX > 0`: un click sintético disparado por JavaScript
        # (`.click()` del propio DOM) no trae coordenadas de pantalla
        # reales y queda afuera de ese filtro, a diferencia de un click
        # físico de verdad.
        self.page.evaluate("document.getElementById('badButton').click()")

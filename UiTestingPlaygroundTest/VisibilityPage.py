from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class VisibilityPage:
    def __init__(self, page):
        self.page = page
        self.boton_hide = page.locator("#hideButton")
        self.boton_removed = page.locator("#removedButton")
        self.boton_zero_width = page.locator("#zeroWidthButton")
        self.boton_overlapped = page.locator("#overlappedButton")
        self.capa_que_tapa = page.locator("#hidingLayer")
        self.boton_transparent = page.locator("#transparentButton")
        self.boton_invisible = page.locator("#invisibleButton")
        self.boton_not_displayed = page.locator("#notdisplayedButton")
        self.boton_offscreen = page.locator("#offscreenButton")

    def ocultar(self):
        self._esperar_que_jquery_este_disponible()
        self.boton_hide.click()
        # La capa que tapa a #overlappedButton se posiciona calculando el
        # left/top del botón con jQuery .position() en el propio handler de
        # click. Justo después del click, esa cuenta a veces todavía no
        # corrió: la capa queda en su posición inicial (height: 0) durante
        # un instante, y cualquier aserción sobre el solapamiento en ese
        # momento sería falsa aunque el bug sea real un instante después.
        self.page.wait_for_function(
            "document.getElementById('hidingLayer').getBoundingClientRect().height > 0"
        )

    def _esperar_que_jquery_este_disponible(self, intentos=3):
        # El botón Hide depende de un handler de jQuery cargado desde un CDN
        # externo (code.jquery.com). Si ese script no llega a tiempo -- una
        # red lenta o inestable, nada relacionado con este sitio -- el click
        # en Hide no hace nada: $ queda indefinido y el error ni siquiera
        # aparece en la consola de Playwright. Un reload reintenta la carga
        # desde cero en vez de quedarse esperando algo que ya falló.
        for intento in range(intentos):
            try:
                self.page.wait_for_function("typeof $ !== 'undefined'", timeout=8000)
                return
            except PlaywrightTimeoutError:
                if intento == intentos - 1:
                    raise
                self.page.reload()

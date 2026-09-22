class HorizontalSliderPage:
    def __init__(self, page):
        self.page = page
        self.slider = page.locator("input[type=range]")
        self.valor_mostrado = page.locator("#range")

    def enfocar(self):
        # Clickear el extremo izquierdo del track fuerza el foco real del
        # navegador y, de paso, deja el valor en el mínimo (0): un punto
        # de partida conocido para las pruebas con flechas.
        self.clickear_en(1)

    def presionar_flecha_derecha(self, veces=1):
        # locator.press() re-enfoca el elemento antes de cada tecla, a
        # diferencia de page.keyboard.press() -- ese usa el foco global de
        # la página, que en headless puede no haberse asentado todavía
        # justo después de un click y dejar la tecla sin efecto.
        for _ in range(veces):
            self.slider.press("ArrowRight")

    def presionar_flecha_izquierda(self, veces=1):
        for _ in range(veces):
            self.slider.press("ArrowLeft")

    def clickear_en(self, posicion_x):
        caja = self.slider.bounding_box()
        self.slider.click(position={"x": posicion_x, "y": caja["height"] / 2})

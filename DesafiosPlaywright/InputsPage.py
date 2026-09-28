class InputsPage:
    def __init__(self, page):
        self.page = page
        self.input_numero = page.locator("input[type=number]")

    def escribir(self, texto):
        self.input_numero.fill("")
        self.input_numero.type(texto)

    def presionar_flecha_arriba(self, veces=1):
        for _ in range(veces):
            self.input_numero.press("ArrowUp")

    def presionar_flecha_abajo(self, veces=1):
        for _ in range(veces):
            self.input_numero.press("ArrowDown")

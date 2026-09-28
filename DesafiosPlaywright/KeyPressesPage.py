class KeyPressesPage:
    def __init__(self, page):
        self.page = page
        self.input = page.locator("#target")
        self.resultado = page.locator("#result")

    def presionar(self, tecla):
        # locator.press() re-enfoca el input antes de la tecla, igual que en
        # HorizontalSliderPage -- necesario porque el listener de esta
        # página está en document.keydown, así que si el foco se pierde la
        # tecla no dispara nada y #result queda con el valor anterior.
        self.input.press(tecla)

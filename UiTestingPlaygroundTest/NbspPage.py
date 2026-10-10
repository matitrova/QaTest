ESPACIO_NORMAL = " "
ESPACIO_NO_SEPARABLE = " "


class NbspPage:
    def __init__(self, page):
        self.page = page
        # Por rol y texto visible: el propio motor de texto de Playwright
        # normaliza el nbsp a un espacio común al comparar, así que este
        # locator encuentra el botón sin que haga falta saber que el
        # espacio real es distinto.
        self.boton = page.get_by_role("button", name="My Button")

    def xpath_con_espacio_normal(self):
        return self.page.locator(f"xpath=//button[text()='My{ESPACIO_NORMAL}Button']")

    def xpath_con_nbsp(self):
        return self.page.locator(f"xpath=//button[text()='My{ESPACIO_NO_SEPARABLE}Button']")

    def texto_crudo(self):
        return self.boton.text_content()

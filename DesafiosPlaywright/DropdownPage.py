class DropdownPage:
    def __init__(self, page):
        self.page = page
        self.dropdown = page.locator("#dropdown")

    def seleccionar_por_valor(self, valor):
        self.dropdown.select_option(value=valor)

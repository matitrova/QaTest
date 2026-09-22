class HoversPage:
    def __init__(self, page):
        self.page = page
        self.figuras = page.locator(".figure")

    def figura(self, indice):
        return self.figuras.nth(indice)

    def caption_de(self, indice):
        return self.figura(indice).locator(".figcaption")

    def pasar_el_mouse_por(self, indice):
        self.figura(indice).hover()

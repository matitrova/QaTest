class LargeDomPage:
    def __init__(self, page):
        self.page = page
        self.no_siblings = page.locator("#no-siblings")
        self.tabla = page.locator("#large-table")

    def hermano(self, tier, item):
        return self.page.locator(f"[id='sibling-{tier}.{item}']")

    def celda(self, fila, columna):
        return self.tabla.locator(f".row-{fila} .column-{columna}")

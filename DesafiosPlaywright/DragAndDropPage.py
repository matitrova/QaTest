class DragAndDropPage:
    def __init__(self, page):
        self.page = page
        self.columna_a = page.locator("#column-a")
        self.columna_b = page.locator("#column-b")

    def texto_de(self, columna):
        return columna.locator("header").inner_text()

    def arrastrar_a_hacia_b(self):
        # Esta página implementa el intercambio a mano con los eventos nativos de
        # HTML5 Drag and Drop (dragstart/dragover/drop), no con una librería como
        # jQuery UI. drag_to() de Playwright dispara esa secuencia completa vía CDP,
        # a diferencia de un dispatchEvent manual que suele quedar incompleto.
        self.columna_a.drag_to(self.columna_b)

from base_page import BasePage
from playwright.sync_api import Locator, Page


class DragAndDropPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.columna_a = page.locator("#column-a")
        self.columna_b = page.locator("#column-b")

    def texto_de(self, columna: Locator) -> str:
        return columna.locator("header").inner_text()

    def arrastrar_a_hacia_b(self) -> None:
        # Esta página implementa el intercambio a mano con los eventos nativos de
        # HTML5 Drag and Drop (dragstart/dragover/drop), no con una librería como
        # jQuery UI. drag_to() de Playwright dispara esa secuencia completa vía CDP,
        # a diferencia de un dispatchEvent manual que suele quedar incompleto.
        self.columna_a.drag_to(self.columna_b)

import math

from base_page import BasePage
from playwright.sync_api import Locator, Page


class VirtualListPage(BasePage):
    TOTAL = 10000
    ROW = 30
    BUFFER = 5

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.viewport: Locator = page.locator("#viewport")
        self.filas: Locator = page.locator(".virtual-row")
        self.rango: Locator = page.locator("#rendered-range")

    def fila(self, indice: int) -> Locator:
        return self.page.locator(f".virtual-row[data-index='{indice}']")

    def item_por_texto(self, texto: str) -> Locator:
        return self.viewport.get_by_text(texto, exact=True)

    def alto_de_viewport(self) -> int:
        return self.viewport.evaluate("el => el.clientHeight")

    def scroll_top_actual(self) -> int:
        return self.viewport.evaluate("el => el.scrollTop")

    def alto_total_del_contenido(self) -> int:
        return self.page.locator("#spacer").evaluate("el => el.scrollHeight")

    def scrollear_a(self, scroll_top: int) -> None:
        self.viewport.evaluate("(el, top) => { el.scrollTop = top; }", scroll_top)

    def scrollear_al_fondo(self) -> None:
        self.viewport.evaluate("el => { el.scrollTop = el.scrollHeight; }")

    def rango_esperado(self, scroll_top: int, alto_viewport: int) -> tuple[int, int]:
        # Misma cuenta que hace el script de la página (índices 0-based):
        # primero = max(0, floor(scrollTop/ROW) - BUFFER)
        # ultimo  = min(TOTAL-1, ceil((scrollTop+alto)/ROW) + BUFFER)
        # Se devuelve en base 1 porque así numera la página el `data-index`
        # y el texto de "#rendered-range".
        primero = max(0, scroll_top // self.ROW - self.BUFFER)
        ultimo = min(self.TOTAL - 1, math.ceil((scroll_top + alto_viewport) / self.ROW) + self.BUFFER)
        return primero + 1, ultimo + 1

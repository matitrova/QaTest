from base_page import BasePage
from playwright.sync_api import Locator, Page


class ChallengingDomPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Cada <a> se regenera con un id (UUID) y un texto al azar en cada
        # carga de la página: ninguno de los dos sirve para ubicarlos de
        # forma estable. Lo único que no cambia es el orden y la clase CSS
        # de cada uno (plano / "alert" / "success"), así que se ubican por
        # posición dentro de su contenedor.
        self.botones = page.locator("div.large-2.columns a")
        # La tabla no tiene ningún atributo (ni id ni class) en filas o
        # celdas para agruparlas: solo position dentro de <table>.
        self.filas = page.locator("table tbody tr")
        # A diferencia de los botones y la tabla, el canvas sí tiene un id
        # fijo -- no todo en esta página es dinámico.
        self.canvas = page.locator("#canvas")

    def boton(self, indice: int) -> Locator:
        return self.botones.nth(indice)

    def fila(self, indice: int) -> Locator:
        return self.filas.nth(indice)

    def celda(self, fila_indice: int, columna_indice: int) -> Locator:
        return self.fila(fila_indice).locator("td").nth(columna_indice)

    def acciones_de_fila(self, fila_indice: int) -> Locator:
        return self.celda(fila_indice, 6).locator("a")

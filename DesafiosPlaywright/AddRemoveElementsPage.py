from base_page import BasePage
from playwright.sync_api import Page


class AddRemoveElementsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_agregar = page.get_by_role("button", name="Add Element")
        # Los botones de eliminar son todos idénticos (misma clase, sin id
        # ni atributo que los distinga entre sí) -- no hay forma de
        # verificar "cuál" se eliminó, solo cuántos quedan.
        self.botones_eliminar = page.locator("button.added-manually")

    def agregar_elemento(self, veces: int = 1) -> None:
        for _ in range(veces):
            self.boton_agregar.click()

    def eliminar_elemento(self) -> None:
        # El JS de la página remueve `#elements button:first-child`: el
        # primero agregado, no el último (FIFO, no LIFO como uno podría
        # asumir de un botón que dice "Delete" al lado del más reciente).
        self.botones_eliminar.first.click()

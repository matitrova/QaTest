from base_page import BasePage
from playwright.sync_api import Locator, Page


class PointerEventsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.lista_ordenable = page.locator("#sortable")
        self.orden_texto = page.locator("#order")
        self.area_swipe = page.locator("#swipe-area")
        self.resultado_swipe = page.locator("#swipe-result")
        self.boton_long_press = page.locator("#long-press")
        self.resultado_press = page.locator("#press-result")

    def item(self, nombre: str) -> Locator:
        return self.lista_ordenable.locator("li", has_text=nombre)

    def orden_actual(self) -> list[str]:
        texto = self.orden_texto.inner_text().removeprefix("Order: ")
        return [nombre.strip() for nombre in texto.split(",")]

    def arrastrar_item_sobre(self, nombre_origen: str, nombre_destino: str) -> None:
        # Esta lista no usa HTML5 drag and drop -- reordena a mano escuchando
        # pointerdown/pointermove/pointerup, y en cada pointermove decide en qué
        # posición va el elemento arrastrado mirando el mouse contra el punto medio
        # de cada <li>. Por eso hay que mover el mouse con varios pasos intermedios
        # (steps=10): un solo salto del origen al destino no dispara ningún
        # pointermove entre medio y la lista nunca se reordena.
        origen = self.item(nombre_origen)
        destino = self.item(nombre_destino)
        origen.scroll_into_view_if_needed()
        caja_origen = origen.bounding_box()
        caja_destino = destino.bounding_box()
        self._mover_mouse_al_centro(caja_origen)
        self.page.mouse.down()
        self.page.mouse.move(
            caja_destino["x"] + caja_destino["width"] / 2,
            caja_destino["y"] + caja_destino["height"] - 2,
            steps=10,
        )
        self.page.mouse.up()

    def swipe(self, distancia_x: int) -> None:
        self.area_swipe.scroll_into_view_if_needed()
        caja = self.area_swipe.bounding_box()
        y = caja["y"] + caja["height"] / 2
        inicio_x = caja["x"] + caja["width"] / 2
        self.page.mouse.move(inicio_x, y)
        self.page.mouse.down()
        self.page.mouse.move(inicio_x + distancia_x, y, steps=10)
        self.page.mouse.up()

    def presionar_boton(self, duracion_ms: int) -> None:
        self.boton_long_press.scroll_into_view_if_needed()
        self._mover_mouse_al_centro(self.boton_long_press.bounding_box())
        self.page.mouse.down()
        # El listener arranca un setTimeout(800) en el pointerdown: si el pointerup
        # llega antes de que venza, lo cancela y es "short press"; si no, es "long press".
        if duracion_ms:
            self.page.wait_for_timeout(duracion_ms)
        self.page.mouse.up()

    def _mover_mouse_al_centro(self, caja: dict) -> None:
        self.page.mouse.move(caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2)

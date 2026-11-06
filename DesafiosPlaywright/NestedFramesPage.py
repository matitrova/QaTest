from base_page import BasePage
from playwright.sync_api import FrameLocator, Locator, Page


class NestedFramesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # frame-left/middle/right no son hijos directos de la página: viven
        # dentro de frame-top, que a su vez es OTRO frameset. Hay que
        # encadenar frame_locator() nivel por nivel -- buscarlos directo
        # contra la página no encuentra nada (ver test de ese caso).
        self.frame_top: FrameLocator = page.frame_locator('frame[name="frame-top"]')
        self.frame_left: FrameLocator = self.frame_top.frame_locator('frame[name="frame-left"]')
        self.frame_middle: FrameLocator = self.frame_top.frame_locator('frame[name="frame-middle"]')
        self.frame_right: FrameLocator = self.frame_top.frame_locator('frame[name="frame-right"]')
        # frame-bottom, en cambio, es hermano de frame-top en el frameset
        # raíz: alcanza con un solo nivel de frame_locator sobre la página.
        self.frame_bottom: FrameLocator = page.frame_locator('frame[name="frame-bottom"]')

        self.contenido_left: Locator = self.frame_left.locator("body")
        self.contenido_right: Locator = self.frame_right.locator("body")
        self.contenido_bottom: Locator = self.frame_bottom.locator("body")
        # Solo el frame del medio tiene su texto envuelto en un #content;
        # left y right lo tienen suelto directo en el <body>.
        self.contenido_middle: Locator = self.frame_middle.locator("#content")

    def frames_hijos_de_top(self) -> Locator:
        return self.frame_top.locator("frame")

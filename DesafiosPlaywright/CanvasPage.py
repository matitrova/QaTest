from base_page import BasePage
from playwright.sync_api import Locator, Page


class CanvasPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.canvas: Locator = page.locator("#canvas")
        self.log: Locator = page.locator("#canvas-log")

    def click_en(self, x: int, y: int) -> None:
        self.canvas.click(position={"x": x, "y": y})

    def presionar(self, tecla: str) -> None:
        self.canvas.press(tecla)

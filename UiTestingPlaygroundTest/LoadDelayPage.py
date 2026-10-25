from base_page import BasePage
from playwright.sync_api import Page


class LoadDelayPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton = page.get_by_role("button", name="Button Appearing After Delay")

    def boton_visible(self) -> bool:
        return self.boton.is_visible()

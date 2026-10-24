from base_page import BasePage
from playwright.sync_api import Page


class FloatingMenuPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.menu = page.locator("#menu")
        self.link_home = page.locator("#menu a[href='#home']")

    def posicion_del_menu(self) -> dict | None:
        return self.menu.bounding_box()

    def estilo_top_del_menu(self) -> str | None:
        return self.menu.get_attribute("style")

    def hacer_scroll(self, cantidad_px: int) -> None:
        self.page.mouse.wheel(0, cantidad_px)
        self.page.wait_for_timeout(400)

    def hacer_clic_en_link_home(self) -> None:
        self.link_home.click()

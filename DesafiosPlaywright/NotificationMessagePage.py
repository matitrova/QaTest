from base_page import BasePage
from playwright.sync_api import Page


class NotificationMessagePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.flash = page.locator("#flash")
        self.cerrar_flash = page.locator("#flash .close")

    def texto_flash(self):
        # El texto incluye el "×" del botón de cierre pegado al final; se
        # recorta para comparar solo el mensaje.
        return self.flash.inner_text().replace("×", "").strip()

    def clase_flash(self):
        return self.flash.get_attribute("class")

    def cerrar(self):
        self.cerrar_flash.click()

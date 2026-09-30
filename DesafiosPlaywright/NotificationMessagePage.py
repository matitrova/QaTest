class NotificationMessagePage:
    def __init__(self, page):
        self.page = page
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

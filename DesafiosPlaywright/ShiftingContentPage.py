from base_page import BasePage
from playwright.sync_api import Page


TARGET_TEXT = "Important Information You're Looking For"

KNOWN_LINES = {
    TARGET_TEXT,
    "Sed deleniti blanditiis odio laudantium.",
    "Vel aliquid dolores veniam enim nesciunt libero quaerat.",
    "Et numquam et aliquam.",
    "Nesciunt autem eum odit fuga tempora deleniti.",
}


class ShiftingContentListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.contenedor = page.locator(".example .large-6.columns.large-centered")

    def locator_exacto_del_registro_fijo(self):
        return self.page.get_by_text(TARGET_TEXT, exact=True)

    def lineas(self):
        texto = self.contenedor.inner_text()
        return [linea.strip() for linea in texto.splitlines() if linea.strip()]

    def posicion_del_registro_fijo(self):
        return self.lineas().index(TARGET_TEXT)

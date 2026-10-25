from base_page import BasePage
from playwright.sync_api import Locator, Page


ESPACIO_NORMAL = " "
ESPACIO_NO_SEPARABLE = " "


class NbspPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Por rol y texto visible: el propio motor de texto de Playwright
        # normaliza el nbsp a un espacio común al comparar, así que este
        # locator encuentra el botón sin que haga falta saber que el
        # espacio real es distinto.
        self.boton = page.get_by_role("button", name="My Button")

    def xpath_con_espacio_normal(self) -> Locator:
        return self.page.locator(f"xpath=//button[text()='My{ESPACIO_NORMAL}Button']")

    def xpath_con_nbsp(self) -> Locator:
        return self.page.locator(f"xpath=//button[text()='My{ESPACIO_NO_SEPARABLE}Button']")

    def texto_crudo(self) -> str | None:
        return self.boton.text_content()

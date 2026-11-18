from base_page import BasePage
from playwright.sync_api import Locator, Page


class BrowserPermissionsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_pedir_notificaciones = page.get_by_role(
            "button", name="Ask to show notifications"
        )
        self.resultado_notificaciones = page.locator("#notifications-result")
        self.campo_texto_clipboard = page.locator("#clipboard-text")
        self.boton_copiar = page.get_by_role("button", name="Copy")
        self.boton_pegar = page.get_by_role("button", name="Paste")
        self.resultado_clipboard = page.locator("#clipboard-result")

    def estado(self, permiso: str) -> Locator:
        return self.page.locator(f"#state-{permiso}")

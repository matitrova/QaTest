from base_page import BasePage
from playwright.sync_api import Locator, Page


class ToastsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.duration_input = page.locator("#duration")
        self.success_button = page.locator("#success-toast")
        self.error_button = page.locator("#error-toast")
        self.info_button = page.locator("#info-toast")
        self.toast_count = page.locator("#toast-count")
        self.toasts_container = page.locator("#toasts")

    def fijar_duracion(self, milisegundos: int) -> None:
        self.duration_input.fill(str(milisegundos))

    def mostrar_toast_exito(self) -> None:
        self.success_button.click()

    def mostrar_toast_error(self) -> None:
        self.error_button.click()

    def mostrar_toast_info(self) -> None:
        self.info_button.click()

    def toast_por_numero(self, numero: int) -> Locator:
        return self.page.locator(f"#toast-{numero}")

    def cerrar_toast(self, numero: int) -> None:
        self.toast_por_numero(numero).locator(".toast-close").click()

    def cantidad_toasts_visibles(self) -> int:
        return self.toasts_container.locator(".toast").count()

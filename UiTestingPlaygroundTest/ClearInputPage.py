from playwright.sync_api import Locator, Page

from base_page import BasePage

# Los ocho primeros son controles de formulario estándar (input/textarea);
# el noveno es un <div contenteditable>, que no tiene .value ni se lee con
# las mismas APIs de Playwright que un control de formulario real.
CAMPOS_ESTANDAR = [
    "clearInput",
    "clearTextarea",
    "clearPassword",
    "clearEmail",
    "clearNumber",
    "clearSearch",
    "clearUrl",
    "clearTel",
]
CAMPO_CONTENTEDITABLE = "clearContentEditable"
TODOS_LOS_CAMPOS = CAMPOS_ESTANDAR + [CAMPO_CONTENTEDITABLE]


class ClearInputPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.estado = page.locator("#opstatus")

    def campo(self, id_campo: str) -> Locator:
        return self.page.locator(f"#{id_campo}")

    def limpiar(self, id_campo: str) -> None:
        # fill("") no distingue entre los ocho controles estándar y el
        # contenteditable: Playwright lo admite en los tres tipos de
        # elemento (input, textarea y [contenteditable]) por igual.
        self.campo(id_campo).fill("")

    def valor_estandar(self, id_campo: str) -> str:
        return self.campo(id_campo).input_value()

    def texto_visible_contenteditable(self) -> str:
        return self.campo(CAMPO_CONTENTEDITABLE).inner_text()

    def contenido_real_contenteditable(self) -> str:
        return self.campo(CAMPO_CONTENTEDITABLE).text_content() or ""

    def texto_estado(self) -> str:
        return self.estado.inner_text()

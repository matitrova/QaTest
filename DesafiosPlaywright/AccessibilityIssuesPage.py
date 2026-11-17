from base_page import BasePage
from playwright.sync_api import Locator, Page


class AccessibilityIssuesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.filas_tabla = page.locator("#known-issues tbody tr")
        self.link_version_alternativa = page.locator("#mode a")
        self.profile_image = page.locator("#profile-image")
        self.search_input = page.locator("#search-input")
        self.size_select = page.locator("#size-select")
        self.icon_button = page.locator("#icon-button")
        self.icon_link = page.locator("#icon-link")
        self.faint_text = page.locator("#faint-text")
        self.bad_role = page.locator("#bad-role")
        self.skipped_heading = page.locator("#skipped-heading")

    def reglas_documentadas(self) -> list[str]:
        return self.filas_tabla.evaluate_all("filas => filas.map(f => f.dataset.rule)")

    def tiene_label_asociado(self, control: Locator) -> bool:
        id_del_control = control.get_attribute("id")
        return self.page.locator(f"label[for='{id_del_control}']").count() > 0

    def etiqueta_del_heading(self) -> str:
        return self.skipped_heading.evaluate("el => el.tagName")

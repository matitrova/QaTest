from base_page import BasePage
from playwright.sync_api import Locator, Page


class JqueryUiMenuPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        items = page.locator("#menu > li")
        item_disabled = items.nth(0)
        item_enabled = items.nth(1)

        self.link_disabled: Locator = item_disabled.locator("> a")
        self.submenu_disabled: Locator = item_disabled.locator("> ul")
        self.link_should_not_see: Locator = self.submenu_disabled.locator("> li > a")

        self.link_enabled: Locator = item_enabled.locator("> a")
        self.submenu_enabled: Locator = item_enabled.locator("> ul")

        enabled_sub_items = self.submenu_enabled.locator("> li")
        item_downloads = enabled_sub_items.nth(0)
        item_volver = enabled_sub_items.nth(1)

        self.link_downloads: Locator = item_downloads.locator("> a")
        self.submenu_downloads: Locator = item_downloads.locator("> ul")
        self.link_volver: Locator = item_volver.locator("> a")

        self.enlace_pdf: Locator = self.submenu_downloads.get_by_text("PDF", exact=True)
        self.enlace_csv: Locator = self.submenu_downloads.get_by_text("CSV", exact=True)
        self.enlace_excel: Locator = self.submenu_downloads.get_by_text(
            "Excel", exact=True
        )

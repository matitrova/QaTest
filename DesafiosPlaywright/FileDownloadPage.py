from base_page import BasePage
from playwright.sync_api import Page


class FileDownloadPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.enlaces_archivo = page.locator("a[href^='download/']")

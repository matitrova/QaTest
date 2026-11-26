from base_page import BasePage
from playwright.sync_api import Page


class ModernFileDownloadPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.boton_blob = page.locator("#blob-download")
        self.boton_fetch = page.locator("#fetch-download")
        self.enlace_data_url = page.locator("#data-url-download")
        self.estado = page.locator("#download-status")
        self.enlace_inline = page.locator("a[href='/download_modern/file/inline']")
        self.enlace_utf8 = page.locator("a[href='/download_modern/file/utf8']")
        self.enlace_spaces = page.locator("a[href='/download_modern/file/spaces']")
        self.enlace_no_name = page.locator("a[href='/download_modern/file/no_name']")

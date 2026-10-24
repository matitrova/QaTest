from base_page import BasePage
from playwright.sync_api import Page


class UploadPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.file_input = page.locator("#file-upload")
        self.submit_button = page.locator("#file-submit")
        self.uploaded_files = page.locator("#uploaded-files")

    def subir_archivo(self, ruta_archivo: str) -> None:
        self.file_input.set_input_files(ruta_archivo)
        self.submit_button.click()

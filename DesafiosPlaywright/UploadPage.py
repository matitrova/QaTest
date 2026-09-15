class UploadPage:
    def __init__(self, page):
        self.page = page
        self.file_input = page.locator("#file-upload")
        self.submit_button = page.locator("#file-submit")
        self.uploaded_files = page.locator("#uploaded-files")

    def subir_archivo(self, ruta_archivo):
        self.file_input.set_input_files(ruta_archivo)
        self.submit_button.click()

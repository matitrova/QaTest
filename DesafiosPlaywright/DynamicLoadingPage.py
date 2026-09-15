class DynamicLoadingPage:
    def __init__(self, page):
        self.page = page
        self.start_button = page.locator("#start button")
        self.finish_text = page.locator("#finish")

    def hacer_clic_en_start(self):
        self.start_button.click()

class ContextMenuPage:
    def __init__(self, page):
        self.page = page
        self.hot_spot = page.locator("#hot-spot")

    def hacer_clic_derecho_en_hot_spot(self):
        self.hot_spot.click(button="right")

    def hacer_clic_izquierdo_en_hot_spot(self):
        self.hot_spot.click()

class DisappearingElementsPage:
    def __init__(self, page):
        self.page = page
        self.items = page.locator(".example ul li a")

    def textos(self):
        return self.items.all_inner_texts()

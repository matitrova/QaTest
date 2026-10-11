class LoadDelayPage:
    def __init__(self, page):
        self.page = page
        self.boton = page.get_by_role("button", name="Button Appearing After Delay")

    def boton_visible(self):
        return self.boton.is_visible()

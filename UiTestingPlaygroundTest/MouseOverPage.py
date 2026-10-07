class MouseOverPage:
    def __init__(self, page):
        self.page = page
        self.contador_click_me = page.locator("#clickCount")
        self.contador_link_button = page.locator("#clickButtonCount")

    def link_click_me(self):
        # El hover reemplaza este nodo por un clon (ver clase) -- por eso
        # cada método lo busca de nuevo en vez de guardar una referencia fija.
        return self.page.locator("a", has_text="Click me")

    def link_button(self):
        return self.page.locator("a", has_text="Link Button")

    def hover_click_me(self):
        self.link_click_me().hover()

    def click_click_me(self):
        self.link_click_me().click()

    def click_link_button(self):
        self.link_button().click()

    def clicks_click_me(self):
        return int(self.contador_click_me.inner_text())

    def clicks_link_button(self):
        return int(self.contador_link_button.inner_text())

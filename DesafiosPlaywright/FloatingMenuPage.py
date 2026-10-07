class FloatingMenuPage:
    def __init__(self, page):
        self.page = page
        self.menu = page.locator("#menu")
        self.link_home = page.locator("#menu a[href='#home']")

    def posicion_del_menu(self):
        return self.menu.bounding_box()

    def estilo_top_del_menu(self):
        return self.menu.get_attribute("style")

    def hacer_scroll(self, cantidad_px):
        self.page.mouse.wheel(0, cantidad_px)
        self.page.wait_for_timeout(400)

    def hacer_clic_en_link_home(self):
        self.link_home.click()

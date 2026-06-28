class InventoryPage:
    def __init__(self, page):
        self.page = page

    def agregar_al_carrito(self, nombre_producto):
        selector = f"#add-to-cart-{nombre_producto}"
        self.page.locator(selector).click()
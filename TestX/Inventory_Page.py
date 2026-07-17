class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.cantidad_carrito = page.locator(".shopping_cart_badge")

    def agregar_al_carrito(self, nombre_producto):
        selector = f"#add-to-cart-{nombre_producto}"
        self.page.locator(selector).click()
    
    def obtener_cantidad_carrito(self):
        return self.cantidad_carrito.inner_text()
        assert self.obtener_cantidad_carrito() == "1"
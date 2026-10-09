class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.cantidad_carrito = page.locator(".shopping_cart_badge")
        self.selector_orden = page.locator(".product_sort_container")
        self.nombres = page.locator(".inventory_item_name")
        self.imagenes = page.locator("img.inventory_item_img")

    def agregar_al_carrito(self, nombre_producto):
        selector = f"#add-to-cart-{nombre_producto}"
        self.page.locator(selector).click()

    def obtener_cantidad_carrito(self):
        return self.cantidad_carrito.inner_text()
        assert self.obtener_cantidad_carrito() == "1"

    def ordenar(self, opcion):
        self.selector_orden.select_option(opcion)

    def nombres_productos(self):
        return self.nombres.all_inner_texts()

    def srcs_imagenes(self):
        count = self.imagenes.count()
        return [self.imagenes.nth(i).get_attribute("src") for i in range(count)]
from base_page import BasePage
from playwright.sync_api import Page


class InventoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cantidad_carrito = page.locator(".shopping_cart_badge")
        self.selector_orden = page.locator(".product_sort_container")
        self.nombres = page.locator(".inventory_item_name")
        self.precios = page.locator(".inventory_item_price")
        self.imagenes = page.locator("img.inventory_item_img")
        self.boton_menu = page.locator("#react-burger-menu-btn")
        self.link_logout = page.locator("#logout_sidebar_link")
        self.mensaje_error = page.locator("[data-test='error']")

    def agregar_al_carrito(self, nombre_producto):
        selector = f"#add-to-cart-{nombre_producto}"
        self.page.locator(selector).click()

    def obtener_cantidad_carrito(self):
        return self.cantidad_carrito.inner_text()

    def ordenar(self, opcion):
        self.selector_orden.select_option(opcion)

    def nombres_productos(self):
        return self.nombres.all_inner_texts()

    def precios_productos(self):
        return [float(p.replace("$", "")) for p in self.precios.all_inner_texts()]

    def srcs_imagenes(self):
        count = self.imagenes.count()
        return [self.imagenes.nth(i).get_attribute("src") for i in range(count)]

    def cerrar_sesion(self):
        self.boton_menu.click()
        self.link_logout.wait_for(state="visible")
        self.link_logout.click()
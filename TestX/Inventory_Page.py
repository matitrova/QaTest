from base_page import BasePage
from playwright.sync_api import Locator, Page


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

    def boton_agregar(self, nombre_producto: str) -> Locator:
        # Selector por atributo, no "#id": el producto
        # "test.allthethings()-t-shirt-(red)" tiene un id con puntos y
        # paréntesis, caracteres que un selector CSS de id ("#...") necesita
        # escapar. Como atributo entre comillas no hace falta escapar nada.
        return self.page.locator(f'[id="add-to-cart-{nombre_producto}"]')

    def agregar_al_carrito(self, nombre_producto: str) -> None:
        self.boton_agregar(nombre_producto).click()

    def obtener_cantidad_carrito(self) -> str:
        return self.cantidad_carrito.inner_text()

    def ordenar(self, opcion: str) -> None:
        self.selector_orden.select_option(opcion)

    def nombres_productos(self) -> list[str]:
        return self.nombres.all_inner_texts()

    def precios_productos(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.precios.all_inner_texts()]

    def srcs_imagenes(self) -> list[str | None]:
        count = self.imagenes.count()
        return [self.imagenes.nth(i).get_attribute("src") for i in range(count)]

    def cerrar_sesion(self) -> None:
        self.boton_menu.click()
        self.link_logout.wait_for(state="visible")
        self.link_logout.click()
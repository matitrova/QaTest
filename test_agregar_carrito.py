from LoginPage import LoginPage
from Inventory_Page import InventoryPage

def test_agregar_carrito(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    inventory.agregar_al_carrito("sauce-labs-backpack")
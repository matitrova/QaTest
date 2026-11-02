from typing import Callable

from TestX.Inventory_Page import InventoryPage


def test_agregar_carrito(inventory_as: Callable[..., InventoryPage]) -> None:
    inventory = inventory_as("standard_user")
    inventory.agregar_al_carrito("sauce-labs-backpack")
    assert inventory.obtener_cantidad_carrito() == "1"

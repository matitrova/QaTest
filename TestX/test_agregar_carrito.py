def test_agregar_carrito(inventory_as):
    inventory = inventory_as("standard_user")
    inventory.agregar_al_carrito("sauce-labs-backpack")
    assert inventory.obtener_cantidad_carrito() == "1"

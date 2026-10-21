from playwright.sync_api import expect


def test_standard_user_ordenar_por_precio_de_menor_a_mayor(inventory_as):
    inventory = inventory_as("standard_user")
    expect(inventory.nombres.first).to_be_visible()
    precios_inicial = inventory.precios_productos()
    inventory.ordenar("lohi")

    precios_lohi = inventory.precios_productos()
    assert precios_lohi == sorted(precios_inicial)


def test_standard_user_ordenar_por_precio_de_mayor_a_menor(inventory_as):
    inventory = inventory_as("standard_user")
    expect(inventory.nombres.first).to_be_visible()
    precios_inicial = inventory.precios_productos()
    inventory.ordenar("hilo")

    precios_hilo = inventory.precios_productos()
    assert precios_hilo == sorted(precios_inicial, reverse=True)


def test_standard_user_el_empate_de_precio_mantiene_el_orden_original(inventory_as):
    # El catálogo tiene dos productos al mismo precio ($15.99): "Sauce Labs
    # Bolt T-Shirt" y "Test.allTheThings() T-Shirt (Red)", en ese orden en
    # el catálogo original. Un sort inestable podría invertirlos entre
    # "lohi" y "hilo" sin que ninguna de las dos asserts de arriba lo note,
    # porque ambas solo comparan la lista de precios, no cuál nombre va con
    # cuál posición cuando hay un empate. Este test confirma explícitamente
    # que los dos productos empatados conservan su orden relativo original
    # en ambos sentidos de orden -- la implementación usa un sort estable,
    # no uno que reordene arbitrariamente a los iguales.
    inventory = inventory_as("standard_user")
    expect(inventory.nombres.first).to_be_visible()

    nombres_inicial = inventory.nombres_productos()
    precios_inicial = inventory.precios_productos()
    empatados = [
        nombre
        for nombre, precio in zip(nombres_inicial, precios_inicial)
        if precios_inicial.count(precio) > 1
    ]
    assert len(empatados) == 2

    for opcion in ("lohi", "hilo"):
        inventory.ordenar(opcion)
        nombres = inventory.nombres_productos()
        orden_resultante = [n for n in nombres if n in empatados]
        assert orden_resultante == empatados


def test_problem_user_el_orden_no_cambia_con_ningun_criterio(inventory_as):
    # test_usuarios_especiales.py ya prueba que a problem_user elegir "Name
    # (Z to A)" no le reordena la lista. Pero el bug real no es específico
    # de ese criterio: el <select> de orden no dispara ningún reordenamiento
    # para NINGUNA opción, tampoco para ordenar por precio. Confirmado
    # contra el sitio real antes de escribir este test: ni "lohi" ni "hilo"
    # cambian ni los nombres ni los precios mostrados, a diferencia de
    # standard_user donde las dos opciones sí reordenan de verdad.
    inventory = inventory_as("problem_user")
    expect(inventory.nombres.first).to_be_visible()
    nombres_inicial = inventory.nombres_productos()
    precios_inicial = inventory.precios_productos()

    for opcion in ("lohi", "hilo"):
        inventory.ordenar(opcion)
        assert inventory.nombres_productos() == nombres_inicial
        assert inventory.precios_productos() == precios_inicial

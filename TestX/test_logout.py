from playwright.sync_api import expect

from TestX.Inventory_Page import InventoryPage


def test_logout_vuelve_a_la_pantalla_de_login(page, login_as):
    login = login_as("standard_user")
    page.wait_for_url("**/inventory.html")

    inventory = InventoryPage(page)
    inventory.cerrar_sesion()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(login.login_button).to_be_visible()
    expect(login.username_input).to_have_value("")


def test_logout_protege_inventory_ante_navegacion_con_atras(page, inventory_as):
    inventory = inventory_as("standard_user")
    inventory.cerrar_sesion()
    expect(page).to_have_url("https://www.saucedemo.com/")

    # go_back() deja la barra de direcciones apuntando otra vez a
    # /inventory.html, pero la sesión ya quedó invalidada del lado cliente:
    # la propia app detecta que no hay sesión y redirige sola a "/". Esa
    # redirección es asíncrona, así que leer la URL o el contenido
    # inmediatamente después de go_back() es flaky -- a veces todavía se ve
    # inventory.html en blanco, sin productos, a mitad de camino de la
    # redirección. Por eso la aserción espera explícitamente a que la URL
    # vuelva a "/" en vez de confiar en que go_back() ya deja todo resuelto.
    page.go_back()
    page.wait_for_url("https://www.saucedemo.com/")

    expect(inventory.mensaje_error).to_have_text(
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )
    assert inventory.nombres.count() == 0


def test_acceso_directo_a_inventory_sin_sesion_muestra_error(page):
    # Ni siquiera hace falta loguearse y desloguearse: entrar directo a
    # /inventory.html sin sesión previa cae en el mismo chequeo del lado
    # cliente que usa logout, y la app redirige la URL a "/" mostrando el
    # mismo mensaje de acceso denegado.
    page.goto("https://www.saucedemo.com/inventory.html")
    page.wait_for_url("https://www.saucedemo.com/")

    error = page.locator("[data-test='error']")
    expect(error).to_have_text(
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )

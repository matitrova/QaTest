from playwright.sync_api import expect

from TestX.LoginPage import LoginPage
from TestX.Inventory_Page import InventoryPage
from TestX.CheckoutPage import CheckoutPage


def test_checkout_completo_con_un_producto(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.agregar_al_carrito("sauce-labs-backpack")

    checkout = CheckoutPage(page)
    checkout.ir_a_carrito()
    page.wait_for_url("**/cart.html")
    checkout.iniciar_checkout()
    page.wait_for_url("**/checkout-step-one.html")

    # La navegación de esta SPA actualiza la URL con un history.pushState
    # antes de montar el componente de la página nueva: un locator
    # consultado apenas se resuelve wait_for_url todavía puede encontrar el
    # DOM de la página anterior (el carrito), no el formulario. Hay que
    # esperar explícitamente a que aparezca un elemento propio de la página
    # nueva antes de interactuar con ella.
    expect(checkout.first_name_input).to_be_visible()
    checkout.completar_datos("Matias", "Trovato", "1000")
    checkout.continuar()
    page.wait_for_url("**/checkout-step-two.html")
    expect(checkout.finish_button).to_be_visible()

    # El impuesto no es un valor fijo: es el 8% del subtotal, redondeado a
    # dos decimales. El test lo recalcula en vez de hardcodear el monto,
    # para seguir siendo válido si cambia el precio del producto.
    subtotal = checkout.subtotal()
    impuesto = checkout.impuesto()
    assert impuesto == round(subtotal * 0.08, 2)
    assert checkout.total() == round(subtotal + impuesto, 2)

    checkout.finalizar()
    page.wait_for_url("**/checkout-complete.html")
    expect(checkout.complete_header).to_have_text("Thank you for your order!")

    # Terminar la compra vacía el carrito del todo: el badge con la
    # cantidad de items deja de existir en el DOM, no queda en "0".
    assert checkout.cart_badge.count() == 0


def test_checkout_sin_completar_datos_muestra_error(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.agregar_al_carrito("sauce-labs-backpack")

    checkout = CheckoutPage(page)
    checkout.ir_a_carrito()
    page.wait_for_url("**/cart.html")
    checkout.iniciar_checkout()
    page.wait_for_url("**/checkout-step-one.html")
    expect(checkout.first_name_input).to_be_visible()

    checkout.continuar()

    expect(checkout.error_message).to_have_text("Error: First Name is required")
    assert page.url.endswith("/checkout-step-one.html")

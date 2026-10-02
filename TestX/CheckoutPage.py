class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.error_message = page.locator("[data-test='error']")
        self.subtotal_label = page.locator("[data-test='subtotal-label']")
        self.tax_label = page.locator("[data-test='tax-label']")
        self.total_label = page.locator("[data-test='total-label']")
        self.complete_header = page.locator("[data-test='complete-header']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    def ir_a_carrito(self):
        self.page.locator(".shopping_cart_link").click()

    def iniciar_checkout(self):
        self.page.locator("[data-test='checkout']").click()

    def completar_datos(self, nombre, apellido, codigo_postal):
        self.first_name_input.fill(nombre)
        self.last_name_input.fill(apellido)
        self.postal_code_input.fill(codigo_postal)

    def continuar(self):
        self.continue_button.click()

    def finalizar(self):
        self.finish_button.click()

    def subtotal(self):
        return float(self.subtotal_label.inner_text().replace("Item total: $", ""))

    def impuesto(self):
        return float(self.tax_label.inner_text().replace("Tax: $", ""))

    def total(self):
        return float(self.total_label.inner_text().replace("Total: $", ""))

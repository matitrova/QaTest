class ForgotPasswordPage:
    def __init__(self, page):
        self.page = page
        self.email = page.locator("#email")
        self.submit = page.locator("#form_submit")
        self.titulo_resultado = page.locator("h1")

    def enviar(self, email=None):
        if email is not None:
            self.email.fill(email)
        with self.page.expect_navigation() as nav_info:
            self.submit.click()
        return nav_info.value

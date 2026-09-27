class BasicAuthPage:
    def __init__(self, page):
        self.page = page
        self.mensaje_exito = page.locator(".example p")

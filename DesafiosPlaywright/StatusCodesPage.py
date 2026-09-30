import re


class StatusCodesPage:
    def __init__(self, page):
        self.page = page
        self.mensaje = page.locator(".example p")

    def texto_esperado(self, codigo):
        return re.compile(rf"This page returned a {codigo} status code")

from base_page import BasePage
from playwright.sync_api import Page


import re


class StatusCodesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.mensaje = page.locator(".example p")

    def texto_esperado(self, codigo):
        return re.compile(rf"This page returned a {codigo} status code")

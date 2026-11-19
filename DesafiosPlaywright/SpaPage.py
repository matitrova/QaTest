from base_page import BasePage
from playwright.sync_api import Page


class SpaPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.titulo_vista = page.locator("#view-title")
        self.texto_vista = page.locator("#view-text")
        self.contador = page.locator("#page-loads")

    def link_de_nav(self, nombre: str):
        return self.page.locator("#spa-nav").get_by_role("link", name=nombre)

    def marcar_carga_actual(self) -> None:
        # Si un click (o un back/forward) terminara disparando una navegación
        # real en vez de pushState/popstate, el contexto de JS se reinicia y
        # esta marca desaparece -- es la única forma de confirmar "no hubo
        # reload" desde afuera, porque la URL y el contenido visual cambian
        # igual en los dos casos.
        self.page.evaluate("window.__sin_reload = true")

    def hubo_reload(self) -> bool:
        return self.page.evaluate("window.__sin_reload !== true")

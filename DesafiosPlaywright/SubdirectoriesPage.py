from base_page import BasePage
from playwright.sync_api import Locator, Page


class SubdirectoriesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.titulo: Locator = page.locator("#content h1")
        # El HTML fuente anida el <pre> de la miga de pan dentro del <p>
        # ("<p>You are here: <pre>...</pre></p>"), pero <pre> es contenido
        # de bloque y el parser HTML5 no permite bloque dentro de <p>: el
        # navegador cierra el <p> antes del <pre> y lo deja como hermano,
        # no como hijo -- "#content p pre" nunca matchea nada en el DOM
        # real, hay que ubicarlo por posición en vez de por anidamiento.
        self.miga_de_pan: Locator = page.locator("#content pre").first
        self.links: Locator = page.locator("#content ol a")

    def link_hacia(self, ruta: str) -> Locator:
        return self.page.locator(f"#content a[href='{ruta}']")

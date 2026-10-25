from base_page import BasePage
from playwright.sync_api import Locator, Page


FRASE_OBJETIVO = "Welcome UserName!"


class VerifyTextPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # El <span> real de la sección "Playground" vive dentro de un único
        # div.bg-primary en toda la página -- es el contenedor que acota la
        # búsqueda al elemento correcto en vez de a cualquier otro lugar de
        # la página que mencione la misma frase.
        self.contenedor_playground = page.locator("div.bg-primary")

    def xpath_igualdad_exacta(self) -> Locator:
        # El propio enunciado de la página lo marca como "Does not work": el
        # span real tiene sangría y salto de línea en su markup (y un <span>
        # anidado alrededor de "UserName"), así que su string-value de XPath
        # nunca es igual, carácter a carácter, a la frase sin espacios de más.
        return self.page.locator(f"xpath=//span[.='{FRASE_OBJETIVO}']")

    def xpath_normalize_space(self) -> Locator:
        # El propio enunciado lo marca como "Works": normalize-space() colapsa
        # los espacios/saltos de línea internos y recorta los extremos antes
        # de comparar.
        return self.page.locator(f"xpath=//span[normalize-space(.)='{FRASE_OBJETIVO}']")

    def get_by_text_exacto_en_toda_la_pagina(self) -> Locator:
        return self.page.get_by_text(FRASE_OBJETIVO, exact=True)

    def get_by_text_parcial_en_toda_la_pagina(self) -> Locator:
        return self.page.get_by_text(FRASE_OBJETIVO, exact=False)

    def get_by_text_acotado_al_playground(self, exact: bool) -> Locator:
        return self.contenedor_playground.get_by_text(FRASE_OBJETIVO, exact=exact)

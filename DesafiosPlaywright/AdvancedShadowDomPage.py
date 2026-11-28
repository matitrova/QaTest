from typing import List, Optional

from base_page import BasePage
from playwright.sync_api import Locator, Page


class AdvancedShadowDomPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # <outer-card> envuelve un <inner-card>, cada uno con su propio shadow
        # root en modo 'open'. El motor de selectores CSS de Playwright
        # atraviesa shadow roots abiertos de forma transparente y encadenada,
        # así que un locator por id solo (sin nombrar ningún host intermedio)
        # llega directo al botón de más adentro, dos niveles abajo.
        self.boton_shadow_anidado: Locator = page.locator("#inner-button")
        self.resultado_anidado: Locator = page.locator("#nested-result")

        # <closed-card> abre su shadow root en modo 'closed'. El propio sitio
        # dice que "page scripts" no pueden entrar ahí pero "WebDriver" sí.
        # Playwright resuelve sus selectores CSS leyendo la propiedad
        # shadowRoot de cada elemento, exactamente como lo haría un script de
        # la página -- así que, para Playwright, un shadow root cerrado es
        # tan inaccesible como para cualquier otro script.
        self.host_cerrado: Locator = page.locator("#closed-card")
        self.texto_cerrado: Locator = page.locator("#closed-text")
        self.input_cerrado: Locator = page.locator("#closed-input")

        self.host_slots: Locator = page.locator("#slot-card")

        self.campo_nombre: Locator = page.locator("#name")
        self.boton_submit: Locator = page.locator("#rating-form button[type='submit']")
        self.resultado_form: Locator = page.locator("#form-result")

    def shadow_root_cerrado_es_null(self) -> bool:
        return self.host_cerrado.evaluate("el => el.shadowRoot === null")

    def texto_asignado_al_slot(self, nombre: str) -> Optional[str]:
        # Lee el nodo que el navegador proyectó de verdad en cada <slot> del
        # shadow root (vía assignedNodes()), no el fallback declarado ahí
        # mismo. Cuando ningún nodo liviano tiene slot=nombre, la lista viene
        # vacía y el método devuelve None -- ahí es donde se ve el fallback.
        return self.host_slots.evaluate(
            "(el, nombre) => { "
            "const slot = el.shadowRoot.querySelector(`slot[name=${nombre}]`); "
            "const nodos = slot.assignedNodes(); "
            "return nodos.length ? nodos[0].textContent : null; }",
            nombre,
        )

    def elegir_estrella(self, numero: int) -> None:
        # <star-rating> es un elemento form-associated (formAssociated = true):
        # participa en el <form> que lo envuelve vía ElementInternals, sin
        # ser un <input> nativo. Cada botón vive dentro de su propio shadow
        # root abierto, así que Playwright lo encuentra igual que cualquier
        # otro elemento de la página.
        self.page.locator(f"#star-{numero}").click()

    def iconos_de_estrellas(self) -> List[str]:
        return self.page.locator("#rating").evaluate(
            "el => Array.from(el.shadowRoot.querySelectorAll('button')).map(b => b.innerHTML)"
        )

    def enviar_formulario(self) -> None:
        self.boton_submit.click()

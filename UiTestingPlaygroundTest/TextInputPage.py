class TextInputPage:
    def __init__(self, page):
        self.page = page
        self.nombre_input = page.locator("#newButtonName")
        self.boton = page.locator("#updatingButton")

    def escribir_con_fill(self, texto):
        self.nombre_input.fill(texto)

    def escribir_con_teclado(self, texto):
        self.nombre_input.click()
        self.nombre_input.press_sequentially(texto)

    def escribir_con_js_sin_eventos(self, texto):
        # Asigna `.value` directo por script, sin disparar ningún evento. El
        # propio navegador no marca el campo como "editado" cuando el valor
        # cambia así, a diferencia de una edición real.
        self.nombre_input.evaluate("(el, v) => { el.value = v; }", texto)

    def escribir_con_evento_input_manual(self, texto):
        # Dispara un evento `input` sintético a mano, sin pasar por ninguna
        # API real de edición de texto (ni `fill()` ni tipeo físico).
        self.nombre_input.evaluate(
            """(el, v) => {
                el.value = v;
                el.dispatchEvent(new Event("input", { bubbles: true }));
            }""",
            texto,
        )

    def escribir_valores_distintos_en_input_y_change(self, valor_input, valor_change):
        self.nombre_input.evaluate(
            """(el, [vi, vc]) => {
                el.value = vi;
                el.dispatchEvent(new Event("input", { bubbles: true }));
                el.value = vc;
                el.dispatchEvent(new Event("change", { bubbles: true }));
            }""",
            [valor_input, valor_change],
        )

    def click_boton(self):
        self.boton.click()

    def texto_boton(self):
        return self.boton.inner_text()

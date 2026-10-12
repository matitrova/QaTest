class OverlappedPage:
    def __init__(self, page):
        self.page = page
        self.id_input = page.locator("#id")
        self.name_input = page.locator("#name")
        self.subject_input = page.locator("#subject")

    def escribir_name_sin_scroll(self, texto):
        # `fill()` no hace scroll del contenedor interno con overflow -- solo
        # garantiza que el input esté "actionable" (visible y no deshabilitado),
        # y este input lo está, aunque un div absoluto lo tape por encima. Por
        # eso el disparo del `input` listener de la propia página sigue
        # funcionando igual que con un usuario real.
        self.name_input.fill(texto)

    def escribir_name_con_scroll(self, texto):
        # `scroll_into_view_if_needed()` de Playwright NO alcanza acá: solo
        # escrolea si el elemento no intersecta el viewport, y este input ya
        # es visible dentro del viewport (lo que lo tapa es el div gris
        # superpuesto, no un recorte de viewport). Hay que forzar el scroll
        # real del contenedor con `overflow-y: scroll` vía `scrollIntoView()`
        # de JS, que sí reubica al input fuera del área que cubre el div.
        self.name_input.evaluate("el => el.scrollIntoView()")
        self.name_input.fill(texto)

    def valor_name(self):
        return self.name_input.input_value()

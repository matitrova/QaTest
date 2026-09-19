class WindowsPage:
    def __init__(self, page):
        self.page = page
        # El <a> de esta página tiene un HTML medio roto (coma suelta entre
        # atributos: href='...', target='_blank'), así que en vez de
        # depender del href literal se ubica por rol + texto visible.
        self.abrir_ventana_link = page.get_by_role("link", name="Click Here")
        self.titulo = page.locator("h3")

    def hacer_clic_en_abrir_ventana(self):
        # target="_blank" abre una pestaña nueva, no navega la actual --
        # hay que engancharse al evento "page" del context ANTES del click
        # para no perder la referencia a esa pestaña nueva.
        with self.page.context.expect_page() as nueva_pagina_info:
            self.abrir_ventana_link.click()
        return nueva_pagina_info.value

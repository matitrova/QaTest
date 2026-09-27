import re

from playwright.sync_api import expect


class TablesPage:
    def __init__(self, page):
        self.page = page
        # Tabla 1: sin class ni id en <td>, hay que ubicar por posición.
        self.apellidos_tabla1 = page.locator("#table1 tbody tr td:nth-child(1)")
        # Tabla 2: con class en cada <td>, se puede ubicar por atributo.
        self.th_apellido_tabla2 = page.locator("#table2 thead th").filter(has=page.locator("span.last-name"))
        self.th_monto_tabla2 = page.locator("#table2 thead th").filter(has=page.locator("span.dues"))
        self.encabezado_apellido_tabla2 = page.locator("#table2 thead span.last-name")
        self.encabezado_monto_tabla2 = page.locator("#table2 thead span.dues")
        self.apellidos_tabla2 = page.locator("#table2 tbody td.last-name")
        self.montos_tabla2 = page.locator("#table2 tbody td.dues")

    def esperar_que_tablesorter_este_listo(self):
        # tablesorter agrega la clase "header" a cada <th> recién cuando
        # termina de inicializarse. Ni el evento "load" ni "networkidle" lo
        # garantizan: con la red lenta, un click podía llegar antes de que
        # el plugin terminara de engancharse y quedaba sin ningún efecto,
        # sin lanzar ningún error.
        expect(self.th_apellido_tabla2).to_have_class(re.compile(r"\bheader\b"))
        expect(self.th_monto_tabla2).to_have_class(re.compile(r"\bheader\b"))

    def montos_como_numeros(self):
        # tablesorter ordena "$100.00" como texto por default (compararía
        # "$51.00" > "$100.00" porque "5" > "1"), a menos que reconozca el
        # formato. El test valida el orden numérico real, no el que
        # tablesorter *diga* que aplicó.
        return [float(texto.strip().lstrip("$")) for texto in self.montos_tabla2.all_inner_texts()]

import re


class DynamicTablePage:
    def __init__(self, page):
        self.page = page
        self.encabezados = page.locator('[role="columnheader"]')
        self.filas = page.locator('[role="rowgroup"]').nth(1).locator('[role="row"]')
        self.label_cpu = page.locator(".bg-warning")

    def cpu_de_chrome(self):
        # El orden de las columnas cambia en cada recarga (la de nombre es
        # la única que siempre queda primera): no se puede asumir que "CPU"
        # está en una posición fija. Hay que preguntarle a los propios
        # encabezados en qué índice está antes de leer la celda.
        indice_cpu = self._indice_columna("CPU")
        for i in range(self.filas.count()):
            fila = self.filas.nth(i)
            celdas = fila.locator('[role="cell"]')
            if celdas.nth(0).inner_text() == "Chrome":
                return self._porcentaje_a_float(celdas.nth(indice_cpu).inner_text())
        raise AssertionError("No se encontró la fila de Chrome")

    def cpu_del_label(self):
        return self._porcentaje_a_float(self.label_cpu.inner_text())

    def nombres_de_columnas(self):
        return self.encabezados.all_inner_texts()

    def nombres_de_procesos_en_orden(self):
        return [
            self.filas.nth(i).locator('[role="cell"]').nth(0).inner_text()
            for i in range(self.filas.count())
        ]

    def _indice_columna(self, nombre):
        return self.encabezados.all_inner_texts().index(nombre)

    @staticmethod
    def _porcentaje_a_float(texto):
        return float(re.search(r"[\d.]+", texto).group())

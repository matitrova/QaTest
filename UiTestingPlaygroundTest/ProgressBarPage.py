import re


class ProgressBarPage:
    def __init__(self, page):
        self.page = page
        self.boton_start = page.locator("#startButton")
        self.boton_stop = page.locator("#stopButton")
        self.barra_progreso = page.locator("#progressBar")
        self.resultado = page.locator("#result")

    def iniciar(self):
        self.boton_start.click()

    def detener(self):
        self.boton_stop.click()

    def porcentaje_actual(self):
        return int(self.barra_progreso.get_attribute("aria-valuenow"))

    def esperar_porcentaje_minimo(self, valor, timeout=35000):
        # El incremento real (ratio += 1) ocurre dentro del propio setTimeout
        # de la página, a un ritmo aleatorio -- no hay forma de calcular de
        # antemano cuándo va a llegar a un valor puntual. Sondear la barra
        # vía wait_for_function (en vez de un sleep fijo) es la única forma
        # de detenerse apenas se cumple la condición, sin pasarse de largo
        # ni quedarse esperando de más.
        #
        # El delay entre pasos no es fijo: se calcula una sola vez por cada
        # click en Start, al azar entre 0 y 499ms, y se reusa en los ~50
        # pasos que faltan hasta el 75%. En el peor caso (delay cercano a
        # 499ms) llegar del 25% al 75% puede tardar más de 24 segundos --
        # un timeout corto confundiría ese caso límite, real y válido, con
        # una falla de la página.
        self.page.wait_for_function(
            f"document.getElementById('progressBar').getAttribute('aria-valuenow') >= {valor}",
            timeout=timeout,
        )

    def resultado_numerico(self):
        texto = self.resultado.inner_text()
        if "n/a" in texto:
            return None
        return int(re.search(r"Result: (-?\d+)", texto).group(1))

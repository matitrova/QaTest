class AboNuevo:
    def __init__(self, page):
        self.page = page 
        self.numero_calle_input = page.locator("#ctl00_ctl00_b_b_ucAlta_txtInstalacionNumero")

    def completar_nro_calle(self, numero):
        self.numero_calle_input.fill(numero)
    
    def obtener_nro_calle(self):
        input_value = self.numero_calle_input.input_value()
        return input_value
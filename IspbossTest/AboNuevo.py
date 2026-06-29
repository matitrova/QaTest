class AboNuevo:
    def __init__(self, page):
        self.page = page 
        self.numero_calle_input = page.locator("#ctl00_ctl00_b_b_ucAlta_txtInstalacionNumero")
        self.calle_seleccionada = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlInstalacionCalle-container")
        self.zona_seleccionada = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlInstalacionZona-container")
        self.locator_Next_paso2 = page.locator("#ctl00_ctl00_b_b_ucAlta_btnGuardar1")

    def completar_nro_calle(self, numero):
        self.numero_calle_input.fill(numero)
    
    def obtener_nro_calle(self):
        input_value = self.numero_calle_input.input_value()
        return input_value
    
    def seleccionar_cualquier_calle(self):
        self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlInstalacionCalle-container").click()
        self.page.locator(".select2-results__option").first.click()
    
    def obtener_calle_seleccionada(self):
        calle_seleccionada = self.calle_seleccionada.inner_text()
        return calle_seleccionada
    
    def obtener_zona_seleccionada(self):
        zona_seleccionada = self.zona_seleccionada.inner_text()
        return zona_seleccionada
    
    def click_next_paso2(self):
        self.locator_Next_paso2.click()
    
    
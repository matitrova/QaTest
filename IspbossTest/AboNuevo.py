class AboNuevo:
    def __init__(self, page):
        self.page = page 
        self.numero_calle_input = page.locator("#ctl00_ctl00_b_b_ucAlta_txtInstalacionNumero")
        self.calle_seleccionada = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlInstalacionCalle-container")
        self.zona_seleccionada = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlInstalacionZona-container")
        self.locator_Next_paso2 = page.locator("#ctl00_ctl00_b_b_ucAlta_btnGuardar1")
        self.abo_alta_Documento = page.locator("#ctl00_ctl00_b_b_ucAlta_txtDocumentoNumero")
        self.abo_alta_Nombre = page.locator("#ctl00_ctl00_b_b_ucAlta_txtNombre")
        self.abo_alta_apellido = page.locator("#ctl00_ctl00_b_b_ucAlta_txtApellido")
        self.abo_alta_categoria = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlCategoria-container")
        self.abo_alta_metod_envio_comp = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlComprobanteMetodoEnvio-container")
        self.cod_area = page.get_by_placeholder("Cód.Area")
        self.abo_alta_telefono = page.get_by_placeholder("Número")
        self.abo_alta_email = page.locator("#ctl00_ctl00_b_b_ucAlta_txtEmail")

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

    def completar_documento(self, documento):
        self.abo_alta_Documento.fill(documento)

    def obtener_documento(self):
        return self.abo_alta_Documento.input_value()

    def completar_nombre(self, nombre):
        self.abo_alta_Nombre.fill(nombre)

    def obtener_nombre(self):
        return self.abo_alta_Nombre.input_value()

    def completar_apellido(self, apellido):
        self.abo_alta_apellido.fill(apellido)

    def obtener_apellido(self):
        return self.abo_alta_apellido.input_value()


    def seleccionar_cualquier_categoria(self):
        self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlCategoria-container").click()
        self.page.locator(".select2-results__option").first.click()
    
    def obtener_categoria_seleccionada(self):
        categoria_seleccionada = self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlCategoria-container").inner_text()
        return categoria_seleccionada
    
    def seleccionar_metodo_envio_comprobante(self):
        self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlComprobanteMetodoEnvio-container").click()
        self.page.locator(".select2-results__option", has_Text="Email").click()

    def completar_cod_area(self, cod_area):
        self.page.get_by_placeholder("Cód.Area").fill(cod_area)

    def obtener_cod_area(self):
        return self.page.get_by_placeholder("Cód.Area").input_value()
    
    def completar_telefono(self, numero):
        self.abo_alta_telefono.fill(numero)
    
    def obtener_telefono(self):
        return self.abo_alta_telefono.input_value()
    
    def completar_email(self, email):
        self.abo_alta_email.fill(email)

    def obtener_email(self):
        return self.abo_alta_email.input_value()
    


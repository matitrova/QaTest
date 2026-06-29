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
        self.cod_area = page.locator('input[name="ctl00$ctl00$b$b$ucAlta$txtCelular$ctl02"]')
        self.abo_alta_celular = page.locator('input[name="ctl00$ctl00$b$b$ucAlta$txtCelular$ctl03"]')
        self.abo_alta_email = page.locator("#ctl00_ctl00_b_b_ucAlta_txtEmail")
        self.locator_Next_paso3 = page.locator("#ctl00_ctl00_b_b_ucAlta_btnGuardar2")
        self.selec_forma_pago_alta_abo = page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlFormaPago-container")
        self.locator_Next_paso4 = page.locator("#ctl00_ctl00_b_b_ucAlta_btnGuardar3")

    # ---------- PASO 1: Domicilio de Instalación ----------

    def seleccionar_cualquier_calle(self):
        self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlInstalacionCalle-container").click()
        self.page.locator(".select2-results__option").first.click()

    def obtener_calle_seleccionada(self):
        return self.calle_seleccionada.inner_text()

    def completar_nro_calle(self, numero):
        self.numero_calle_input.fill(numero)
        self.numero_calle_input.blur()    # ← saca el foco, dispara el cálculo de zona

    def obtener_nro_calle(self):
        return self.numero_calle_input.input_value()

    def obtener_zona_seleccionada(self):
        return self.zona_seleccionada.inner_text()

    def click_next_paso2(self):
        self.locator_Next_paso2.click()

    # ---------- PASO 2: Datos Personales ----------

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
        return self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlCategoria-container").inner_text()

    def seleccionar_metodo_envio_comprobante(self):
        self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlComprobanteMetodoEnvio-container").click()
        self.page.locator(".select2-results__option", has_text="Email").click()

    def completar_cod_area(self, cod_area):
        self.cod_area.fill(cod_area)

    def obtener_cod_area(self):
        return self.cod_area.input_value()

    def completar_telefono(self, numero):
        self.abo_alta_celular.fill(numero)

    def obtener_telefono(self):
        return self.abo_alta_celular.input_value()

    def completar_email(self, email):
        self.abo_alta_email.fill(email)

    def obtener_email(self):
        return self.abo_alta_email.input_value()

    def click_next_paso3(self):
        self.locator_Next_paso3.click()

    # ---------- PASO 3: Datos de Facturación ----------

    def seleccionar_forma_pago(self):
        self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlFormaPago-container").click()
        self.page.locator(".select2-results__option", has_text="Contado").click()

    def obtener_forma_pago(self):
        return self.page.locator("#select2-ctl00_ctl00_b_b_ucAlta_ddlFormaPago-container").inner_text()

    def click_next_paso4(self):
        self.locator_Next_paso4.click()
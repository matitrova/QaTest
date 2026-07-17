class PerfilSegNuevo: 
    def __init__(self, page):
        self.page = page
        self.btn_nuevo = page.locator("#ctl00_ctl00_b_b_btnNuevo")
        self.nombre_input = page.locator("#ctl00_ctl00_b_b_txtNombre")
        self.codigo_input = page.locator("#ctl00_ctl00_b_b_txtCodigo")
        self.btn_guardar = page.locator("#ctl00_ctl00_b_b_btnGrabar")

        # Permisos 
        self.abonado = page.locator("#ctl00_ctl00_b_b_trvFuncionest5")
        self.promotor_abonado = page.locator("#ctl00_ctl00_b_b_trvFuncionest39")
        self.Conf_novedades = page.locator("#ctl00_ctl00_b_b_trvFuncionest57")
        self.comp_facturas = page.locator("#ctl00_ctl00_b_b_trvFuncionest95")
        self.comp_autorizacion = page.locator("#ctl00_ctl00_b_b_trvFuncionest121")
        self.comp_recibos = page.locator("#ctl00_ctl00_b_b_trvFuncionest135")
        self.comp_ing_cobranzas = page.locator("#ctl00_ctl00_b_b_trvFuncionest189")
        self.ordenes_servicio = page.locator("#ctl00_ctl00_b_b_trvFuncionest235")
        self.remitos_internos = page.locator("#ctl00_ctl00_b_b_trvFuncionest383")
        self.tablas_perid_fact = page.locator("#ctl00_ctl00_b_b_trvFuncionest550")
        self.reportes_todo = page.locator("#ctl00_ctl00_b_b_trvFuncionest635")
        self.tipos_reportes = page.locator("#ctl00_ctl00_b_b_trvFuncionest637")
        self.buscador_input = page.locator("#ctl00_ctl00_b_b_txtFiltro")
        self.btn_buscar = page.locator("#ctl00_ctl00_b_b_btnBuscar")


    def click_nuevo(self):
        self.btn_nuevo.click()

    def completar_codigo(self, codigo):
        self.codigo_input.fill(codigo)

    def completar_nombre(self, nombre):
        self.nombre_input.fill(nombre)

    def click_abonado (self):
        self.abonado.click()  

    def click_promotor_abonado(self):
        self.promotor_abonado.click()

    def click_conf_novedades(self):
        self.Conf_novedades.click()

    def click_comp_facturas(self):
        self.comp_facturas.click()

    def click_comp_autorizacion(self):
        self.comp_autorizacion.click()

    def click_comp_recibos(self):
        self.comp_recibos.click()

    def click_comp_ing_cobranzas(self):
        self.comp_ing_cobranzas.click()

    def click_ordenes_servicio(self):
        self.ordenes_servicio.click()

    def click_remitos_internos(self):
        self.remitos_internos.click()

    def click_tablas_perid_fact(self):
        self.tablas_perid_fact.click()

    def click_reportes_todo(self):
        self.reportes_todo.click()

    def click_tipos_reportes(self):
        self.tipos_reportes.click()

    def click_guardar(self):
        self.btn_guardar.click()

    def buscar_perfil(self, nombre):
        self.buscador_input.fill(nombre)
        self.btn_buscar.click()

    def abrir_primer_resultado(self):
        self.page.locator("#ctl00_ctl00_b_b_grdDatos tbody tr").first.click()
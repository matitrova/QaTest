class MenuPage: 
    def __init__(self, page): 
        self.page = page 
        self.BtnAboMenu = self.page.get_by_text("Abonados").first
        self.btnAboGrilla = self.page.locator('a[href="/Abonados/Default.aspx"]')
        self.BtnAboNuevo = self.page.locator("#ctl00_ctl00_b_b_btnNuevo")
        self.btn_seguridad_menu = page.get_by_role("link", name=" Seguridad ")
        self.btn_perfiles_seguridad = page.get_by_role("link", name=" Perfiles de Seguridad")
        self.btn_usuarios = page.get_by_role("link", name=" Usuarios")


        

    def navigate(self):
        self.page.goto("https://beta.test.ispboss.com/usuarios/Default.aspx")
    
    def click_abonados_menu(self):
        self.BtnAboMenu.click()
        self.btnAboGrilla.click()
        self.BtnAboNuevo.wait_for()

    def click_boton_nuevo_abonado(self):
        self.BtnAboNuevo.click()

    def click_perfiles_seguridad_menu(self):
        self.btn_seguridad_menu.click()
        self.btn_perfiles_seguridad.click()
    
    def click_usuarios_menu(self):
        self.btn_seguridad_menu.click()   
        self.btn_usuarios.click()          
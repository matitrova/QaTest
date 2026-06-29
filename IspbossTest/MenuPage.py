class MenuPage: 
    def __init__(self, page): 
        self.page = page 
        self.BtnAboMenu = self.page.get_by_text("Abonados").first
        self.btnAboGrilla = self.page.locator('a[href="/Abonados/Default.aspx"]')
        self.BtnAboNuevo = self.page.locator("#ctl00_ctl00_b_b_btnNuevo")

        

    def navigate(self):
        self.page.goto("https://beta.test.ispboss.com/usuarios/Default.aspx")
    
    def click_abonados_menu(self):
        self.BtnAboMenu.click()
        self.btnAboGrilla.click()
        self.BtnAboNuevo.wait_for()
        self.BtnAboNuevo.click()
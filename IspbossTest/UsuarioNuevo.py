class UsuarioNuevo : 
    def __init__(self, page):
        self.page = page     
        self.BtnNuevo = page.get_by_role("button", name="  Nuevo")
        self.NmbCompleto = page.get_by_role("textbox", name="Nombre Completo")
        self.Usuario = page.get_by_role("textbox", name="Usuario")
        self.Pass = page.get_by_role("textbox", name="Contraseña")
        self.Rol = page.get_by_text("Todos")
        self.QuitRolExt = page.get_by_text("Externo - Externo")
    
    def click_unidad_negocio(self, nombre_unidad):
        self.page.get_by_text(nombre_unidad).click()
        
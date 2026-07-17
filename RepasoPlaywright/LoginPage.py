class LoginPage : 
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login>button")
    
    def completar_usuario(self, username):
        self.username_input.fill(username)
    
    def completar_contraseña(self, password):
        self.password_input.fill(password)
    
    def hacer_clic_en_login(self):
        self.login_button.click()
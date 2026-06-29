class LoginIspBoss: 
    def __init__(self, page):
        self.page = page 
        self.username_input = page.locator("#ctl00_b_txtUsuario")
        self.password_input = page.locator("#ctl00_b_txtPassword")
        self.login_button = page.locator("#ctl00_b_btnSubmit")

    def navigate(self):
        self.page.goto("https://beta.test.ispboss.com")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    

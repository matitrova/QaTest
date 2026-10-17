class SampleAppPage:
    def __init__(self, page):
        self.page = page
        # El HTML que manda el servidor trae id="username"/id="password" en
        # los dos inputs, pero un script inline -- ubicado más abajo en la
        # misma página -- les asigna un GUID al azar como nuevo id apenas
        # termina de parsear el documento, antes de que Playwright devuelva
        # el control tras `goto()`. Ubicarlos por el atributo `name` (que ese
        # script nunca toca) es la única forma de que el locator siga siendo
        # válido de una carga a la siguiente.
        self.usuario = page.locator("input[name='UserName']")
        self.clave = page.locator("input[name='Password']")
        self.boton_login = page.locator("#login")
        self.estado = page.locator("#loginstatus")

    def login(self, usuario, clave):
        self.usuario.fill(usuario)
        self.clave.fill(clave)
        self.boton_login.click()

    def texto_estado(self):
        return self.estado.inner_text()

    def clase_estado(self):
        return self.estado.get_attribute("class")

    def texto_boton(self):
        return self.boton_login.inner_text()

    def id_usuario(self):
        return self.usuario.get_attribute("id")

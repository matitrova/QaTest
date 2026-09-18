class CheckboxesPage:
    def __init__(self, page):
        self.page = page
        # Ninguno de los dos <input> tiene id propio -- solo el <form>
        # que los contiene (#checkboxes) lo tiene. Hay que agarrarlos
        # por posición dentro de ese form.
        self.checkbox_1 = page.locator("#checkboxes input[type='checkbox']").nth(0)
        self.checkbox_2 = page.locator("#checkboxes input[type='checkbox']").nth(1)

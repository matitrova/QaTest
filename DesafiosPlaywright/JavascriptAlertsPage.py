class JavascriptAlertsPage:
    def __init__(self, page):
        self.page = page
        self.alert_button = page.locator('button[onclick="jsAlert()"]')
        self.confirm_button = page.locator('button[onclick="jsConfirm()"]')
        self.prompt_button = page.locator('button[onclick="jsPrompt()"]')
        self.result_text = page.locator("#result")

    def hacer_clic_en_alert(self):
        self.alert_button.click()

    def hacer_clic_en_confirm(self):
        self.confirm_button.click()

    def hacer_clic_en_prompt(self):
        self.prompt_button.click()

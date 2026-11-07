from base_page import BasePage
from playwright.sync_api import Locator, Page


class RadioButtonsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.red: Locator = page.locator("#red")
        self.blue: Locator = page.locator("#blue")
        self.green: Locator = page.locator("#green")
        self.football: Locator = page.locator("input[name='sport'][value='football']")
        self.tennis: Locator = page.locator("input[name='sport'][value='tennis']")
        self.hockey: Locator = page.locator("input[name='sport'][value='hockey']")
        self.resultado: Locator = page.locator("#result")

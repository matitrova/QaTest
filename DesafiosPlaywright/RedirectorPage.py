class RedirectorPage:
    def __init__(self, page):
        self.page = page
        self.link_redirect = page.locator("#redirect")

"""Clase base para todos los Page Objects de esta suite."""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

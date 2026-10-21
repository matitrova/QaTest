from typing import Callable

import pytest
from playwright.sync_api import Page

from TestX.Inventory_Page import InventoryPage
from TestX.LoginPage import LoginPage


@pytest.fixture
def login_as(page: Page) -> Callable[..., LoginPage]:
    """Devuelve una función que navega a /login e inicia sesión con el
    usuario indicado, dejando el LoginPage listo para revisar errores."""

    def _login_as(username: str, password: str = "secret_sauce") -> LoginPage:
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(username, password)
        return login_page

    return _login_as


@pytest.fixture
def inventory_as(login_as: Callable[..., LoginPage]) -> Callable[..., InventoryPage]:
    """Igual que login_as, pero espera a que la sesión quede establecida y
    devuelve el InventoryPage ya en /inventory.html."""

    def _inventory_as(username: str, password: str = "secret_sauce") -> InventoryPage:
        login_page = login_as(username, password)
        login_page.page.wait_for_url("**/inventory.html")
        return InventoryPage(login_page.page)

    return _inventory_as

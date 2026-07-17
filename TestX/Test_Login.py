import pytest 
from TestX.LoginPage import LoginPage

def test_login_exitoso(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    assert page.url == "https://www.saucedemo.com/inventory.html"
    
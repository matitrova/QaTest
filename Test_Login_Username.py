import pytest
from LoginPage import LoginPage 

def test_login_username(page):
    login = LoginPage(page)
    login.navigate()
    login.login("", "") 
    assert login.error_message.inner_text() == "Epic sadface: Username is required"
    assert login.error_message.is_visible() 
    
from config import BASE_URL
from LoginPage import LoginPage

def test_login(page):
    login_page = LoginPage(page)
    page.goto(f"{BASE_URL}/login")
    
    # Completar el nombre de usuario y la contraseña
    login_page.completar_usuario("tomsmith")
    login_page.completar_contraseña("SuperSecretPassword!")
    
    # Hacer clic en el botón de inicio de sesión
    login_page.hacer_clic_en_login()

    assert "You logged into a secure area!" in page.locator("#flash").inner_text()

def test_login_incorrecto(page):
    login_page = LoginPage(page)
    page.goto(f"{BASE_URL}/login")
    
    # Completar el nombre de usuario y la contraseña incorrecta
    login_page.completar_usuario("tomsmith")
    login_page.completar_contraseña("1234")
    
    # Hacer clic en el botón de inicio de sesión
    login_page.hacer_clic_en_login()

    assert "Your password is invalid!" in page.locator("#flash").inner_text()
from IspbossLoginPage import LoginIspBoss 
from MenuPage import MenuPage 

def test_alta_abonado(page): 
    login_page = LoginIspBoss(page) 
    menu_page = MenuPage(page) 

    login_page.navigate() 
    login_page.login("mati", "1234") 
    menu_page.navigate()
    menu_page.click_abonados_menu()
    locator_paso1 = page.get_by_text("Paso 1: Domicilio de Instalación")
    locator_paso1.wait_for()
    assert locator_paso1.is_visible()

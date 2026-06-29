from IspbossLoginPage import LoginIspBoss 
from MenuPage import MenuPage 
from AboNuevo import AboNuevo


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

    abo_nuevo = AboNuevo(page)
    abo_nuevo.completar_nro_calle("123")
    numero_calle_input = abo_nuevo.obtener_nro_calle()
    assert numero_calle_input == "123"

    selec_calle = abo_nuevo.seleccionar_cualquier_calle()
    calle_seleccionada = abo_nuevo.obtener_calle_seleccionada()
    assert calle_seleccionada != "Seleccione"

    abo_nuevo.zona_seleccionada.wait_for()
    zona_seleccionada = abo_nuevo.obtener_zona_seleccionada()
    assert zona_seleccionada != "Seleccione"

    next_paso2 = abo_nuevo.click_next_paso2()
    locator_paso2 = page.get_by_text("Paso 2: Datos Personales")
    locator_paso2.wait_for()
    assert page.get_by_text("Paso 2: Datos Personales").is_visible()

    completar_documento = abo_nuevo.completar_documento("12345678")
    documento_completado = abo_nuevo.obtener_documento()
    assert documento_completado == "12345678"

    completar_nombre = abo_nuevo.completar_nombre("Juan")
    nombre = abo_nuevo.obtener_nombre()
    assert nombre == "Juan"

    completar_apellido = abo_nuevo.completar_apellido("Gomez")
    apellido = abo_nuevo.obtener_apellido()
    assert apellido == "Gomez"

    selec_categoria = abo_nuevo.seleccionar_cualquier_categoria()
    categoria_seleccionada = abo_nuevo.obtener_categoria_seleccionada()
    assert categoria_seleccionada != "Seleccione"

    completar_cod_area = abo_nuevo.completar_cod_area("011")
    cod_area = abo_nuevo.obtener_cod_area()
    assert cod_area == "011"

    completar_telefono = abo_nuevo.completar_telefono("12345678")
    telefono = abo_nuevo.obtener_telefono()
    assert telefono == "12345678"

    completar_email = abo_nuevo.completar_email("matitrova13@gmail.com")
    email = abo_nuevo.obtener_email()
    assert email == "matitrova13@gmail.com"


from IspbossLoginPage import LoginIspBoss
from MenuPage import MenuPage
from AboNuevo import AboNuevo
from playwright.sync_api import expect


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

    # Primero la calle (tu pedido: es más rápido que arrancar por el número)
    abo_nuevo.seleccionar_cualquier_calle()
    calle_seleccionada = abo_nuevo.obtener_calle_seleccionada()
    assert calle_seleccionada != "Seleccione"

    # Después el número
    abo_nuevo.completar_nro_calle("123")
    numero_calle_input = abo_nuevo.obtener_nro_calle()
    assert numero_calle_input == "123"

    # Zona se autocompleta (tarda 1-2 seg): esperamos a que deje de decir "Seleccione"
    expect(abo_nuevo.zona_seleccionada).not_to_have_text("Seleccione")
    zona_seleccionada = abo_nuevo.obtener_zona_seleccionada()
    assert zona_seleccionada != "Seleccione"

    abo_nuevo.click_next_paso2()
    locator_paso2 = page.get_by_text("Paso 2: Datos Personales")
    locator_paso2.wait_for()
    assert locator_paso2.is_visible()

    abo_nuevo.completar_documento("12345678")
    assert abo_nuevo.obtener_documento() == "12345678"

    abo_nuevo.completar_nombre("Juan")
    assert abo_nuevo.obtener_nombre() == "Juan"

    abo_nuevo.completar_apellido("Gomez")
    assert abo_nuevo.obtener_apellido() == "Gomez"

    abo_nuevo.seleccionar_cualquier_categoria()
    assert abo_nuevo.obtener_categoria_seleccionada() != "Seleccione"

    abo_nuevo.seleccionar_metodo_envio_comprobante()

    abo_nuevo.completar_cod_area("11")
    assert abo_nuevo.obtener_cod_area() == "11"

    abo_nuevo.completar_telefono("12345678")
    assert abo_nuevo.obtener_telefono() == "12345678"

    abo_nuevo.completar_email("matitrova13@gmail.com")
    assert abo_nuevo.obtener_email() == "matitrova13@gmail.com"

    abo_nuevo.click_next_paso3()
    locator_paso3 = page.get_by_text("Paso 3: Datos de Facturación")
    locator_paso3.wait_for()
    assert locator_paso3.is_visible()

    abo_nuevo.seleccionar_forma_pago()
    forma_pago = abo_nuevo.obtener_forma_pago()
    assert forma_pago != "Seleccione"

    abo_nuevo.click_next_paso4()
    locator_paso4 = page.get_by_text("Paso 4: Confirmación")
    locator_paso4.wait_for()
    assert locator_paso4.is_visible()
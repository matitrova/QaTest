from IspbossLoginPage import LoginIspBoss
from MenuPage import MenuPage
from AboNuevo import AboNuevo
from playwright.sync_api import expect
from ispboss_config import ISPBOSS_USER, ISPBOSS_PASS
import json


def test_alta_abonado(page):
    login_page = LoginIspBoss(page)
    menu_page = MenuPage(page)

    with open("IspbossTest/abonados.json") as f:
        lista_abonados = json.load(f)

    login_page.navigate()
    login_page.login(ISPBOSS_USER, ISPBOSS_PASS)
    menu_page.navigate()
    menu_page.click_abonados_menu()

    for abonado in lista_abonados:

        menu_page.click_boton_nuevo_abonado()
        locator_paso1 = page.get_by_text("Paso 1: Domicilio de Instalación")
        locator_paso1.wait_for()
        assert locator_paso1.is_visible()

        abo_nuevo = AboNuevo(page)

        # Primero la calle (tu pedido: es más rápido que arrancar por el número)
        abo_nuevo.seleccionar_primer_calle()
        calle_seleccionada = abo_nuevo.obtener_calle_seleccionada()
        assert calle_seleccionada != "Seleccione"

        # Después el número
        abo_nuevo.completar_nro_calle(abonado["numero_calle"])
        numero_calle_input = abo_nuevo.obtener_nro_calle()
        assert numero_calle_input == abonado["numero_calle"]

        # Zona se autocompleta (tarda 1-2 seg): esperamos a que deje de decir "Seleccione"
        expect(abo_nuevo.zona_seleccionada).not_to_have_text("Seleccione")
        zona_seleccionada = abo_nuevo.obtener_zona_seleccionada()
        assert zona_seleccionada != "Seleccione"

        abo_nuevo.click_next_paso2()
        locator_paso2 = page.get_by_text("Paso 2: Datos Personales")
        locator_paso2.wait_for()
        assert locator_paso2.is_visible()

        abo_nuevo.completar_documento(abonado["documento"])
        assert abo_nuevo.obtener_documento() == abonado["documento"]

        abo_nuevo.completar_nombre(abonado["nombre"])
        assert abo_nuevo.obtener_nombre() == abonado["nombre"]

        abo_nuevo.completar_apellido(abonado["apellido"])
        assert abo_nuevo.obtener_apellido() == abonado["apellido"]

        abo_nuevo.seleccionar_cualquier_categoria()
        assert abo_nuevo.obtener_categoria_seleccionada() != "Seleccione"

        abo_nuevo.seleccionar_metodo_envio_comprobante()
        assert abo_nuevo.obtener_metodo_envio_comprobante() != "Seleccione"

        abo_nuevo.completar_cod_area("11")
        assert abo_nuevo.obtener_cod_area() == "11"

        abo_nuevo.completar_telefono(abonado["telefono"])
        assert abo_nuevo.obtener_telefono() == abonado["telefono"]

        abo_nuevo.completar_email(abonado["email"])
        assert abo_nuevo.obtener_email() == abonado["email"]

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

        abo_nuevo.click_guardar_abonado()

        # El texto de la ficha viene con formato "#codigo - Apellido, Nombre"
        # por eso se usa "in" en vez de "==" (comparación exacta)
        nombre_perfil = abo_nuevo.obtener_nombre_perfil_abonado()
        assert abonado["nombre"] in nombre_perfil
        assert abonado["apellido"] in nombre_perfil

        abo_nuevo.click_boton_volver()
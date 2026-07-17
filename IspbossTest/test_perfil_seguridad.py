from IspbossLoginPage import LoginIspBoss
from MenuPage import MenuPage
from perfil_seg_nuevo import PerfilSegNuevo
from ispboss_config import ISPBOSS_USER, ISPBOSS_PASS
import json


def test_crear_perfil_seguridad(page):
    login_page = LoginIspBoss(page)
    menu_page = MenuPage(page)

    login_page.navigate()
    login_page.login(ISPBOSS_USER, ISPBOSS_PASS)

    menu_page.click_perfiles_seguridad_menu()

    perfil = PerfilSegNuevo(page)
    perfil.click_nuevo()
    perfil.completar_codigo("TESTQA")
    perfil.completar_nombre("Perfil de Prueba QA")
    perfil.click_abonado()
    perfil.click_promotor_abonado()
    perfil.click_comp_facturas()
    perfil.click_ordenes_servicio()
    perfil.click_guardar()


def test_editar_perfil_seguridad(page):
    login_page = LoginIspBoss(page)
    menu_page = MenuPage(page)

    login_page.navigate()
    login_page.login(ISPBOSS_USER, ISPBOSS_PASS)

    menu_page.click_perfiles_seguridad_menu()

    perfil = PerfilSegNuevo(page)
    perfil.buscar_perfil("TESTQA")
    perfil.abrir_primer_resultado()

    # Agregar un permiso nuevo
    perfil.click_comp_recibos()

    perfil.click_guardar()
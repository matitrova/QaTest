from config import BASE_URL


def test_los_tres_botones_tienen_el_mismo_nombre_accesible(page):
    page.goto(f"{BASE_URL}/classattr")

    # Los tres botones muestran "Button" a simple vista -- el tercero
    # termina en varios espacios de más en el HTML, pero el nombre accesible
    # que usa get_by_role() normaliza y recorta espacios, así que los tres
    # quedan indistinguibles por texto. La única forma de ubicar el correcto
    # es por clase.
    assert page.get_by_role("button", name="Button").count() == 3


def test_xpath_con_clase_exacta_no_encuentra_nada(page):
    page.goto(f"{BASE_URL}/classattr")

    # El atributo class real del botón es "btn class3 btn-primary btn-test",
    # no "btn-primary" solo. Un XPath que compara el atributo completo
    # contra un único valor -- el ejemplo que la propia página muestra como
    # "esto no funciona" -- nunca encuentra el botón, aunque exista y tenga
    # esa clase entre las suyas.
    assert page.locator("xpath=//button[@class='btn-primary']").count() == 0


def test_selector_css_por_clase_encuentra_un_solo_boton(class_page):
    # Un selector CSS por clase busca dentro de la lista completa de clases
    # del atributo, no una igualdad exacta -- btn-primary matchea sin
    # problema aunque conviva con btn, class3 y btn-test en el mismo botón.
    assert class_page.boton_primary.count() == 1
    assert class_page.boton_success.count() == 1
    assert class_page.boton_warning.count() == 1


def test_click_en_boton_primary_dispara_el_alert(page, class_page):
    # El alert es nativo y sincrónico: el propio JS de la página se queda
    # bloqueado hasta que algo lo resuelve, así que el handler tiene que
    # estar registrado y aceptar el diálogo *antes* de que termine el
    # click -- esperar a que click() retorne para recién ahí mirar el
    # diálogo (como con expect_event) deja todo colgado, porque click()
    # nunca termina de resolver mientras el alert siga abierto.
    mensajes = []

    def registrar_y_aceptar(dialog):
        mensajes.append(dialog.message)
        dialog.accept()

    page.once("dialog", registrar_y_aceptar)
    class_page.hacer_clic_en_primary()

    assert mensajes == ["Primary button pressed"]


def test_click_en_los_otros_dos_botones_no_dispara_ningun_alert(page, class_page):
    # El handler de la página filtra por clase en el propio JS
    # (event.target.className.indexOf("btn-primary")): clickear cualquiera
    # de los otros dos botones no tiene que disparar ningún diálogo. Se
    # registra un listener que descarta y guarda cualquier diálogo que
    # aparezca, en vez de asumir que "no pasó nada" solo porque el test no
    # explotó.
    dialogos = []

    def registrar_y_descartar(dialog):
        dialogos.append(dialog.message)
        dialog.dismiss()

    page.on("dialog", registrar_y_descartar)

    class_page.hacer_clic_en_success()
    class_page.hacer_clic_en_warning()

    assert dialogos == []

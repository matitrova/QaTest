def test_el_id_literal_del_html_no_existe_apenas_carga_la_pagina(page, sample_app_page):
    # El HTML servido por el backend trae id="username" tal cual -- se puede
    # confirmar pidiéndolo crudo con requests, sin ejecutar ningún JS -- pero
    # un script inline lo reemplaza por un GUID al terminar de parsear el
    # documento. Para cuando Playwright devuelve el control tras `goto()`,
    # ese reemplazo ya ocurrió: un locator por el id original no encuentra
    # nada, no porque el campo no exista, sino porque ya no se llama así.
    assert page.locator("#username").count() == 0
    assert page.locator("#password").count() == 0
    assert sample_app_page.usuario.count() == 1
    assert sample_app_page.clave.count() == 1


def test_el_id_de_los_campos_cambia_en_cada_recarga_pero_el_name_no(page, sample_app_page):
    id_primera_carga = sample_app_page.id_usuario()
    assert id_primera_carga != "username"

    page.reload()
    id_segunda_carga = sample_app_page.id_usuario()

    # El GUID se recalcula en cada carga: no es un valor fijo asignado una
    # sola vez en el servidor. Un locator por id, además de empezar roto (el
    # test anterior ya lo confirma), se rompería de nuevo en la próxima
    # recarga aunque alguien lo "arreglara" copiando el id de esta corrida.
    assert id_segunda_carga != id_primera_carga
    # El locator por `name`, en cambio, sigue encontrando exactamente un
    # campo después de la recarga, sin necesitar saber cuál es el id vigente.
    assert sample_app_page.usuario.count() == 1


def test_login_con_password_incorrecta_es_invalido_y_limpia_los_campos(sample_app_page):
    sample_app_page.login("matias", "password_incorrecta")

    assert sample_app_page.texto_estado() == "Invalid username/password"
    assert sample_app_page.clase_estado() == "text-danger"
    # La página borra los dos campos ante un intento fallido, incluida la
    # password -- no solo el usuario, que sería lo más intuitivo de limpiar.
    assert sample_app_page.usuario.input_value() == ""
    assert sample_app_page.clave.input_value() == ""


def test_login_sin_usuario_tambien_es_invalido_aunque_la_password_sea_correcta(sample_app_page):
    # El enunciado de la página pide "any non-empty user name" -- un usuario
    # vacío con la password correcta ("pwd") tiene que fallar igual que una
    # password incorrecta, no alcanza con que uno de los dos campos esté bien.
    sample_app_page.login("", "pwd")

    assert sample_app_page.texto_estado() == "Invalid username/password"
    assert sample_app_page.clase_estado() == "text-danger"


def test_login_exitoso_muestra_bienvenida_y_cambia_el_boton_a_log_out(sample_app_page):
    sample_app_page.login("matias", "pwd")

    assert sample_app_page.texto_estado() == "Welcome, matias!"
    assert sample_app_page.clase_estado() == "text-success"
    # El mismo botón que dispara el login pasa a funcionar como logout: no
    # hay un segundo botón que aparezca, cambia de rol y de texto a la vez.
    assert sample_app_page.texto_boton() == "Log Out"


def test_logout_revierte_el_estado_y_limpia_los_campos(sample_app_page):
    sample_app_page.login("matias", "pwd")
    assert sample_app_page.texto_boton() == "Log Out"

    # Clickear el mismo botón de nuevo, ya logueado, dispara la rama de
    # logout: el texto, la clase y el label del botón vuelven exactamente al
    # estado inicial, sin necesitar recargar la página.
    sample_app_page.boton_login.click()

    assert sample_app_page.texto_estado() == "User logged out."
    assert sample_app_page.clase_estado() == "text-info"
    assert sample_app_page.texto_boton() == "Log In"
    assert sample_app_page.usuario.input_value() == ""
    assert sample_app_page.clave.input_value() == ""

from config import BASE_URL
from ClientDelayPage import ClientDelayPage


def test_no_hay_contenido_cargado_antes_de_hacer_click(page):
    client_delay_page = ClientDelayPage(page)
    page.goto(f"{BASE_URL}/clientDelay")

    assert client_delay_page.contenido.inner_text() == ""
    assert not client_delay_page.spinner.is_visible()


def test_al_hacer_click_el_spinner_aparece_de_inmediato(page):
    client_delay_page = ClientDelayPage(page)
    page.goto(f"{BASE_URL}/clientDelay")

    client_delay_page.disparar_calculo()

    # El propio CreateLabel() muestra el spinner con $('#spinner').show()
    # antes de programar el setTimeout: tiene que estar visible ya, sin
    # esperar nada de los 15 segundos que faltan para el label.
    assert client_delay_page.spinner.is_visible()
    assert client_delay_page.contenido.inner_text() == ""


def test_despues_de_esperar_aparece_el_texto_calculado(page):
    client_delay_page = ClientDelayPage(page)
    page.goto(f"{BASE_URL}/clientDelay")

    client_delay_page.disparar_calculo()
    client_delay_page.esperar_etiqueta()

    assert client_delay_page.texto_etiqueta() == "Data calculated on the client side."
    # El callback del setTimeout oculta el spinner con $('#spinner').hide()
    # en la misma línea en la que inserta el párrafo: para cuando la
    # etiqueta ya está visible, el spinner tiene que haber desaparecido.
    assert not client_delay_page.spinner.is_visible()


def test_la_espera_no_dispara_ningun_pedido_de_red(page):
    # A diferencia de /ajax (AjaxDataPage), donde el botón dispara un
    # $.get("/ajaxdata") real contra el servidor, el de esta página solo
    # programa un setTimeout en el propio navegador: los 15 segundos no
    # deberían generar ningún pedido xhr/fetch, aunque el resultado visible
    # (spinner, espera, texto) sea idéntico.
    pedidos_de_datos = []
    page.on(
        "request",
        lambda request: pedidos_de_datos.append(request)
        if request.resource_type in ("xhr", "fetch")
        else None,
    )

    client_delay_page = ClientDelayPage(page)
    page.goto(f"{BASE_URL}/clientDelay")

    client_delay_page.disparar_calculo()
    client_delay_page.esperar_etiqueta()

    assert pedidos_de_datos == []

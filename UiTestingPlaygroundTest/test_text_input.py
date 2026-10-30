TEXTO_ORIGINAL = "Button That Should Change it's Name Based on Input Value"


def test_fill_cambia_el_nombre_del_boton(text_input_page):
    text_input_page.escribir_con_fill("Hola Fill")
    text_input_page.click_boton()

    # `fill()` deja el campo "sucio" para el navegador aunque no dispare un
    # `change` en el momento: recién al perder foco (el propio click del
    # botón lo hace), Chromium dispara un `change` nativo con el valor
    # cargado, que coincide con el `input` que `fill()` sí disparó al
    # escribir -- la condición del handler (`NewButtonNameC == NewButtonNameI`)
    # se cumple y el botón cambia de nombre.
    assert text_input_page.texto_boton() == "Hola Fill"


def test_teclado_fisico_cambia_el_nombre_del_boton(text_input_page):
    text_input_page.escribir_con_teclado("Hola Teclado")
    text_input_page.click_boton()

    # `press_sequentially()` simula tecla por tecla como un teclado físico,
    # el caso que la propia página pide probar explícitamente. Dispara
    # `input` en cada tecla y deja el campo marcado como editado por el
    # usuario, así que el `change` nativo al perder foco trae el mismo
    # valor y el botón cambia.
    assert text_input_page.texto_boton() == "Hola Teclado"


def test_js_sin_eventos_no_cambia_el_nombre_del_boton(text_input_page):
    text_input_page.escribir_con_js_sin_eventos("Hola JS")
    text_input_page.click_boton()

    # Asignar `.value` por script no dispara ningún evento por sí solo, y
    # tampoco deja al campo "sucio" para el navegador: a diferencia de
    # `fill()`, perder el foco después no dispara ningún `change` nativo.
    # `NewButtonNameI` y `NewButtonNameC` quedan `undefined` y el handler de
    # la página nunca cambia el texto del botón -- el caso de "setear vía
    # eventos del DOM no lleva a ningún lado" que la página advierte.
    assert text_input_page.texto_boton() == TEXTO_ORIGINAL


def test_evento_input_manual_no_alcanza_para_cambiar_el_boton(text_input_page):
    text_input_page.escribir_con_evento_input_manual("Hola Input Manual")
    text_input_page.click_boton()

    # Disparar un `input` sintético a mano sí actualiza `NewButtonNameI` (el
    # handler de la página solo mira el evento, no cómo se originó), pero no
    # pasa por ninguna API real de edición de texto: el navegador no marca
    # el campo como editado por el usuario, así que el `change` nativo al
    # perder foco nunca llega. `NewButtonNameC` queda `undefined` y la
    # condición del handler no se cumple -- confirma que el `change` nativo
    # depende de cómo se edita el campo, no de si algún evento `input` ya
    # disparó.
    assert text_input_page.texto_boton() == TEXTO_ORIGINAL


def test_valores_distintos_en_input_y_change_no_actualiza_el_boton(text_input_page):
    text_input_page.escribir_valores_distintos_en_input_y_change("Primero", "Segundo")
    text_input_page.click_boton()

    # El handler de `/textinput` exige que `NewButtonNameC` (lo que guardó el
    # último `change`) sea igual a `NewButtonNameI` (lo que guardó el último
    # `input`), no solo que ambos existan. Disparando los dos eventos a mano
    # con valores distintos, cada variable guarda lo suyo pero no coinciden
    # entre sí, así que el botón se queda con su texto original aunque los
    # dos eventos sí se dispararon.
    assert text_input_page.texto_boton() == TEXTO_ORIGINAL

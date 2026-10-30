def test_el_boton_queda_fuera_del_area_visible_pero_is_visible_da_true(scrollbars_page):
    cont_box = scrollbars_page.box_contenedor()
    boton_box = scrollbars_page.box_boton()

    # El botón vive dentro de un contenido de 600x300 recortado por un
    # contenedor de 300x150 con scroll propio: su posición real en la página
    # cae afuera del rectángulo visible del contenedor, tanto a la derecha
    # (eje X) como por debajo (eje Y). A diferencia de /overlapped (donde
    # otro elemento tapa el punto central), acá no hay nada encima del botón
    # -- el recorte lo produce el propio `overflow` del contenedor ancestro.
    assert boton_box["x"] >= cont_box["x"] + cont_box["width"]
    assert boton_box["y"] >= cont_box["y"] + cont_box["height"]

    # `is_visible()` solo mira layout y estilos (bounding box, display,
    # visibility) del elemento mismo: no sabe que un ancestro con
    # `overflow: scroll` lo está recortando fuera de su área visible, así
    # que da `True` igual que si el botón estuviera completamente a la
    # vista. Es el mismo tipo de falso positivo que ya se documentó en
    # /overlapped con la superposición, pero con una causa distinta.
    assert scrollbars_page.boton.is_visible()


def test_click_sin_scroll_manual_escrollea_el_contenedor_en_ambos_ejes(scrollbars_page):
    scroll_izq_antes, scroll_arriba_antes = scrollbars_page.scroll_actual()
    assert scroll_izq_antes == 0
    assert scroll_arriba_antes == 0

    # A diferencia de Selenium -- donde clickear un elemento fuera del área
    # visible de un contenedor con scroll requiere un `scrollIntoView()`
    # manual antes del click, o directamente falla --, el paso de
    # "actionability" de Playwright escrolea el contenedor más cercano por
    # su cuenta antes de clickear. No hace falta llamar a
    # `scroll_into_view_if_needed()` a mano, ni acá ni en ningún otro test
    # de esta suite que use `.click()`.
    scrollbars_page.boton.click(timeout=5000)

    scroll_izq_despues, scroll_arriba_despues = scrollbars_page.scroll_actual()
    # El scroll automático mueve el contenedor en los DOS ejes a la vez
    # (izquierda y abajo), porque el botón está desplazado del área visible
    # tanto en X como en Y -- un solo eje de scroll no alcanzaría para
    # dejarlo clickeable.
    assert scroll_izq_despues > 0
    assert scroll_arriba_despues > 0


def test_click_con_force_tambien_escrollea_el_contenedor(scrollbars_page):
    scroll_antes = scrollbars_page.scroll_actual()
    assert scroll_antes == [0, 0]

    # `force=True` bypassea las verificaciones de "actionability" (visible,
    # habilitado, estable, que nada más reciba el evento), pero el scroll
    # del contenedor hacia el elemento es un paso aparte que Playwright
    # ejecuta antes de esas verificaciones -- `force` no lo salta. El click
    # llega igual de "escrolleado" que uno sin `force`.
    scrollbars_page.boton.click(timeout=5000, force=True)

    scroll_despues = scrollbars_page.scroll_actual()
    assert scroll_despues[0] > 0
    assert scroll_despues[1] > 0

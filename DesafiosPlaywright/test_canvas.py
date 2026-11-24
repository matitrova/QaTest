from playwright.sync_api import Page, expect

from config import BASE_URL
from CanvasPage import CanvasPage


def test_al_cargar_el_log_dice_nothing_yet(page: Page) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    expect(canvas_page.log).to_have_text("Nothing yet")


# El canvas tiene 1px de borde (`border: 1px solid #333`), que CSS suma a
# su caja aunque `box-sizing` no esté declarado (el valor por defecto es
# `content-box`, pero el borde se dibuja igual fuera del área de
# contenido). El sitio calcula las coordenadas del click como
# `event.clientX - rect.left`, y `getBoundingClientRect()` sí incluye ese
# borde -- pero la opción `position` de Playwright para `.click()` apunta
# al borde del elemento en sí, no al área de contenido de adentro. El
# resultado es que pedirle a Playwright que clickee en (x, y) termina
# reportado por el sitio como (x+1, y+1): un offset de un píxel por el
# borde, que no aparece si se clickea "a ojo" con el mouse real porque ahí
# no hay ninguna coordenada pedida de antemano para comparar.
def test_click_reporta_la_posicion_corrida_un_pixel_por_el_borde(
    page: Page,
) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.click_en(100, 50)
    expect(canvas_page.log).to_have_text("Clicked at 101, 51")

    canvas_page.click_en(0, 0)
    expect(canvas_page.log).to_have_text("Clicked at 1, 1")


def test_escribir_y_enter_muestra_submitted_con_el_texto(page: Page) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.presionar("h")
    canvas_page.presionar("i")
    canvas_page.presionar("Enter")

    expect(canvas_page.log).to_have_text("Submitted: hi")


# Tipear no toca el log en absoluto -- el sitio guarda cada tecla en una
# variable `typed` que solo se vuelca a `canvas-log` cuando se presiona
# Enter. Mientras tanto el log sigue mostrando lo que haya quedado del
# estado anterior (en este test, el "Nothing yet" inicial), así que no hay
# ninguna señal visible en el DOM de que se está tipeando hasta que se
# confirma con Enter.
def test_tipear_sin_enter_no_cambia_el_log(page: Page) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.presionar("a")
    canvas_page.presionar("b")
    canvas_page.presionar("c")

    expect(canvas_page.log).to_have_text("Nothing yet")


def test_backspace_borra_el_ultimo_caracter_del_buffer_pendiente(
    page: Page,
) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.presionar("a")
    canvas_page.presionar("b")
    canvas_page.presionar("c")
    canvas_page.presionar("Backspace")
    canvas_page.presionar("Enter")

    expect(canvas_page.log).to_have_text("Submitted: ab")


# El handler de teclado filtra por `event.key.length === 1`: cualquier
# tecla cuyo nombre en el estándar de JavaScript tenga más de un
# caracter -- "Shift", "ArrowLeft", "Escape", "Tab" -- entra en el `else`
# y se ignora por completo, sin tocar el buffer `typed` ni el log. La
# espaciadora (`" "`) en cambio tiene nombre de un solo caracter y pasa el
# filtro igual que una letra: es un espacio literal dentro del texto
# tipeado, no una tecla de control.
def test_teclas_de_nombre_largo_se_ignoran_pero_el_espacio_es_texto(
    page: Page,
) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.presionar("a")
    canvas_page.presionar("Shift")
    canvas_page.presionar("ArrowLeft")
    canvas_page.presionar("Escape")
    canvas_page.presionar(" ")
    canvas_page.presionar("b")
    canvas_page.presionar("Enter")

    expect(canvas_page.log).to_have_text("Submitted: a b")


# El click no toca el buffer `typed` -- solo pisa el texto del log con el
# mensaje de "Clicked at...". El texto pendiente sigue ahí, invisible,
# listo para salir completo apenas se presiona Enter.
def test_un_click_en_medio_de_tipear_no_pierde_el_buffer_pendiente(
    page: Page,
) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.presionar("h")
    canvas_page.presionar("i")
    canvas_page.click_en(10, 10)
    expect(canvas_page.log).to_have_text("Clicked at 11, 11")

    canvas_page.presionar("Enter")
    expect(canvas_page.log).to_have_text("Submitted: hi")


def test_enter_con_el_buffer_vacio_envia_un_submitted_vacio(page: Page) -> None:
    canvas_page = CanvasPage(page)
    page.goto(f"{BASE_URL}/canvas")

    canvas_page.presionar("Enter")

    expect(canvas_page.log).to_have_text("Submitted: ")

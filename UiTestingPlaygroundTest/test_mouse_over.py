from config import BASE_URL
from MouseOverPage import MouseOverPage


def test_el_hover_reemplaza_el_link_y_cambia_su_titulo_y_clase(page):
    mouse_over_page = MouseOverPage(page)
    page.goto(f"{BASE_URL}/mouseover")

    link = mouse_over_page.link_click_me()
    assert link.get_attribute("title") == "Click me"
    assert link.get_attribute("class") == "text-primary"

    mouse_over_page.hover_click_me()

    # `linkActive()` no modifica el <a> original: lo clona, le cambia
    # título y clase al clon, y reemplaza el nodo viejo por el nuevo en el
    # DOM. Por eso hay que volver a pedir el locator (no reusar `link`) --
    # un Locator de Playwright se re-resuelve solo en cada acción, así que
    # alcanza con preguntarle de nuevo a la misma variable `link`.
    assert link.get_attribute("title") == "Active Link"
    assert link.get_attribute("class") == "text-warning"


def test_dos_clicks_consecutivos_incrementan_el_contador_en_dos(page):
    mouse_over_page = MouseOverPage(page)
    page.goto(f"{BASE_URL}/mouseover")

    assert mouse_over_page.clicks_click_me() == 0

    # El escenario que plantea la propia página ("record 2 consecutive
    # link clicks, el contador debe subir de a 2") es justamente el caso
    # que falla con Selenium si se guarda una referencia al <a> de antes
    # del primer click: el primer hover automático de Playwright antes de
    # cada click reemplaza el nodo por un clon distinto, y un Locator (a
    # diferencia de un WebElement) se busca de nuevo en cada acción en vez
    # de operar sobre un nodo guardado, así que ninguno de los dos clicks
    # se pierde.
    mouse_over_page.click_click_me()
    mouse_over_page.click_click_me()

    assert mouse_over_page.clicks_click_me() == 2


def test_referencia_obsoleta_al_elemento_no_se_puede_clickear_tras_el_hover(page):
    mouse_over_page = MouseOverPage(page)
    page.goto(f"{BASE_URL}/mouseover")

    # A diferencia de un Locator, un ElementHandle sí apunta a un nodo
    # concreto del DOM, resuelto una sola vez en el momento en que se pide.
    # Es el equivalente de Playwright al WebElement de Selenium, y sirve
    # para reproducir a propósito el "stale element problem" que esta
    # página fue diseñada para enseñar.
    referencia_vieja = page.query_selector("a[title='Click me']")
    assert referencia_vieja is not None

    mouse_over_page.hover_click_me()

    # El hover dispara `linkActive()`, que saca el <a> original del DOM
    # (`removeChild`) y agrega un clon nuevo en su lugar. La referencia
    # vieja sigue siendo un objeto válido en Python, pero el nodo que
    # representa ya no pertenece al documento.
    assert referencia_vieja.evaluate("el => el.isConnected") is False

    try:
        referencia_vieja.click()
        assert False, "se esperaba que el click sobre la referencia obsoleta fallara"
    except Exception as error:
        assert "not attached to the DOM" in str(error)

    # El click sobre la referencia vieja no tuvo ningún efecto en la
    # página: el contador sigue en 0. Recién un Locator pedido de nuevo
    # -- que apunta al clon actual, no al nodo original -- puede clickear
    # de verdad.
    assert mouse_over_page.clicks_click_me() == 0
    mouse_over_page.click_click_me()
    assert mouse_over_page.clicks_click_me() == 1


def test_el_segundo_link_mantiene_su_titulo_pero_tambien_cambia_de_clase(page):
    mouse_over_page = MouseOverPage(page)
    page.goto(f"{BASE_URL}/mouseover")

    link_button = mouse_over_page.link_button()
    assert link_button.get_attribute("title") == "Link Button"
    assert link_button.get_attribute("class") == "text-primary"

    mouse_over_page.click_link_button()

    # La página describe este segundo link como uno que "se reemplaza con
    # uno idéntico" al pasar el mouse, a diferencia del primero (que
    # cambia de título). Pero el código fuente (`linkButtonActive()`) le
    # cambia la clase a "text-warning" igual que al primero -- la única
    # diferencia real es que el título no cambia. "Idéntico" describe el
    # título, no el resto del clon.
    assert link_button.get_attribute("title") == "Link Button"
    assert link_button.get_attribute("class") == "text-warning"
    assert mouse_over_page.clicks_link_button() == 1

    mouse_over_page.click_link_button()
    assert mouse_over_page.clicks_link_button() == 2

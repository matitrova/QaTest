import time

from playwright.sync_api import expect

from TestX.LoginPage import LoginPage
from TestX.Inventory_Page import InventoryPage


def test_problem_user_todas_las_imagenes_son_la_misma(page):
    login = LoginPage(page)
    login.navigate()
    login.login("problem_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")

    # Igual que en el checkout (ver test_checkout_completo.py): la URL de
    # esta SPA cambia antes de que el componente nuevo termine de montarse,
    # así que hay que esperar a un elemento propio de la página de inventario
    # antes de leer nada, en vez de asumir que wait_for_url ya implica que el
    # contenido está listo.
    inventory = InventoryPage(page)
    expect(inventory.imagenes.first).to_be_visible()
    srcs = inventory.srcs_imagenes()

    assert len(srcs) == 6
    # Las seis imágenes apuntan al mismo archivo: no es que falten imágenes
    # (como en /broken_images, cubierto en DesafiosPlaywright), es que el
    # catálogo entero muestra el mismo archivo sin importar el producto. El
    # archivo compartido responde 200 y carga con dimensiones reales -- no es
    # una imagen rota en el sentido de naturalWidth == 0, es la imagen
    # equivocada mostrada para los seis productos.
    assert len(set(srcs)) == 1


def test_standard_user_cada_producto_tiene_su_propia_imagen(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")

    inventory = InventoryPage(page)
    expect(inventory.imagenes.first).to_be_visible()
    srcs = inventory.srcs_imagenes()

    assert len(srcs) == 6
    assert len(set(srcs)) == 6


def test_problem_user_el_orden_no_cambia_al_elegir_otro_criterio(page):
    login = LoginPage(page)
    login.navigate()
    login.login("problem_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")

    inventory = InventoryPage(page)
    expect(inventory.nombres.first).to_be_visible()
    orden_inicial = inventory.nombres_productos()
    inventory.ordenar("za")

    # El <select> sí cambia de valor (el dropdown refleja "za" elegido), pero
    # el handler que debería reordenar la lista no hace nada: la lista queda
    # exactamente en el mismo orden que antes de elegir "Name (Z to A)".
    assert inventory.nombres_productos() == orden_inicial


def test_standard_user_el_orden_si_cambia_al_elegir_otro_criterio(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")

    inventory = InventoryPage(page)
    expect(inventory.nombres.first).to_be_visible()
    orden_inicial = inventory.nombres_productos()
    inventory.ordenar("za")

    orden_za = inventory.nombres_productos()
    assert orden_za != orden_inicial
    assert orden_za == sorted(orden_inicial, reverse=True)


def test_performance_glitch_user_el_delay_es_intermitente_no_constante(browser):
    # El delay no está en la navegación posterior al login, sino en la propia
    # respuesta al click: `locator.click()` de Playwright no retorna hasta
    # que termina de procesar el evento, así que el cronómetro tiene que
    # envolver el click entero, no solo la espera de `wait_for_url()` de
    # después (que para cuando se la llama ya encuentra la URL cambiada).
    #
    # Midiendo 30 logins seguidos contra el sitio real, el delay de ~5
    # segundos apareció en 21 de 30 (70%), no en los 30 -- este usuario no es
    # "siempre lento", es lento la mayoría de las veces pero no todas. Un test
    # que afirmara "siempre tarda más de 2 segundos" sería flaky por diseño en
    # el ~30% de corridas que caen rápidas. Por eso se repite el login varias
    # veces con contextos nuevos (cada uno con su propia sesión) y se afirma
    # solo lo que es reproducible: que aparece al menos un login lento, sin
    # exigir que todos lo sean.
    duraciones = []
    for _ in range(8):
        context = browser.new_context()
        page = context.new_page()
        login = LoginPage(page)
        login.navigate()

        inicio = time.time()
        login.login("performance_glitch_user", "secret_sauce")
        page.wait_for_url("**/inventory.html", timeout=15000)
        duraciones.append(time.time() - inicio)
        context.close()

    assert any(d > 2 for d in duraciones)


def test_standard_user_el_login_es_rapido(page):
    login = LoginPage(page)
    login.navigate()

    inicio = time.time()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html", timeout=15000)
    duracion = time.time() - inicio

    assert duracion < 2

import time

from config import BASE_URL


def test_la_navegacion_tarda_al_menos_lo_que_demora_el_servidor(page):
    # A diferencia de /clientDelay (ClientDelayPage), donde el retraso es un
    # setTimeout en el navegador después de que la página ya terminó de
    # cargar, acá es el servidor el que tarda en mandar la respuesta: el
    # propio page.goto() queda bloqueado hasta que el HTML completo llega.
    inicio = time.monotonic()
    page.goto(f"{BASE_URL}/loaddelay")
    duracion = time.monotonic() - inicio

    assert duracion >= 4


def test_el_boton_ya_esta_visible_apenas_termina_la_navegacion(load_delay_page):
    # goto() ya esperó el evento load del navegador: a diferencia de
    # ClientDelayPage, no hace falta ningún wait_for adicional después para
    # ver el botón -- si la navegación terminó, el botón ya está.
    assert load_delay_page.boton_visible()


def test_la_demora_no_dispara_ningun_pedido_xhr_o_fetch(page):
    # Confirma que los ~5 segundos de espera son el propio documento HTML
    # tardando en llegar, no una página que carga rápido y después dispara
    # una llamada async en segundo plano (el caso de /ajax, por ejemplo).
    pedidos_de_datos = []
    page.on(
        "request",
        lambda request: pedidos_de_datos.append(request)
        if request.resource_type in ("xhr", "fetch")
        else None,
    )

    page.goto(f"{BASE_URL}/loaddelay")

    assert pedidos_de_datos == []

from config import BASE_URL
from DynamicIdPage import DynamicIdPage, ID_DINAMICO


def test_el_id_del_boton_tiene_formato_de_id_dinamico(page):
    dynamic_id_page = DynamicIdPage(page)
    page.goto(f"{BASE_URL}/dynamicid")

    assert ID_DINAMICO.match(dynamic_id_page.id_actual())


def test_el_id_del_boton_cambia_entre_recargas(page):
    dynamic_id_page = DynamicIdPage(page)
    page.goto(f"{BASE_URL}/dynamicid")

    ids = {dynamic_id_page.id_actual()}
    for _ in range(4):
        page.reload()
        ids.add(dynamic_id_page.id_actual())

    # Si todas las recargas dieran el mismo id, el "desafío" de la página no
    # existiría: hace falta ver más de un valor distinto para confirmar que
    # el id de verdad se regenera en cada carga, no solo una vez al azar.
    assert len(ids) > 1


def test_el_id_de_una_carga_anterior_deja_de_existir_tras_recargar(page):
    dynamic_id_page = DynamicIdPage(page)
    page.goto(f"{BASE_URL}/dynamicid")
    id_anterior = dynamic_id_page.id_actual()

    page.reload()

    # Un locator armado con el id de la carga anterior (`#id-viejo`) ya no
    # encuentra nada: es la prueba concreta de por qué fijarse en el id es
    # una mala estrategia de locator para este botón.
    assert not dynamic_id_page.existe_un_elemento_con_id(id_anterior)
    assert dynamic_id_page.id_actual() != id_anterior


def test_el_boton_se_puede_clickear_por_rol_y_texto_sin_depender_del_id(page):
    dynamic_id_page = DynamicIdPage(page)
    page.goto(f"{BASE_URL}/dynamicid")

    # El locator por rol y texto visible nunca cambia, aunque el id sí lo
    # haga en cada recarga -- por eso el click funciona igual las tres veces
    # sin que el test necesite leer ni recordar ningún id.
    for _ in range(3):
        dynamic_id_page.boton.click()
        page.reload()

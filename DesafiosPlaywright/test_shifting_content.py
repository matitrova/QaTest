import pytest

from config import BASE_URL
from ShiftingContentPage import KNOWN_LINES, TARGET_TEXT, ShiftingContentListPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo problema que en test_windows.py y test_disappearing_elements.py: el
    # script externo de Optimizely puede colgar el evento "load" si esa red
    # está lenta o inaccesible.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_las_mismas_cinco_lineas_aparecen_siempre_aunque_cambien_de_orden(page):
    shifting_content_page = ShiftingContentListPage(page)

    for _ in range(5):
        page.goto(f"{BASE_URL}/shifting_content/list")
        lineas = shifting_content_page.lineas()
        assert len(lineas) == 5
        assert set(lineas) == KNOWN_LINES


# El sitio no deja ningún rastro de qué posición le tocó al registro fijo más
# allá del propio orden del texto: no hay ningún atributo, clase ni elemento
# separado para esa línea. Un test que guardara la posición de una sola carga
# y la reusara después encontraría el dato equivocado ni bien recargara la
# página, porque no hay ninguna que se mantenga estable entre pedidos.

def test_la_posicion_del_registro_fijo_varia_entre_recargas(page):
    shifting_content_page = ShiftingContentListPage(page)
    posiciones = set()

    for _ in range(10):
        page.goto(f"{BASE_URL}/shifting_content/list")
        posiciones.add(shifting_content_page.posicion_del_registro_fijo())
        if len(posiciones) > 1:
            break

    assert len(posiciones) > 1


# Las cinco líneas de esta página no son <li> ni ningún elemento individual:
# son texto plano separado por <br><br> dentro de un único <div>. Por eso
# get_by_text(exact=True) -- que sí funciona en casos parecidos de este sitio,
# como /disappearing_elements -- no encuentra nada acá: no existe ningún
# elemento cuyo texto completo sea exactamente esa línea, porque el único
# elemento que la contiene es el <div> entero con las cinco líneas juntas. La
# única forma de ubicar la línea es parsear el texto completo del contenedor y
# partirlo, que es justo lo que hace lineas().

def test_no_existe_un_elemento_propio_para_ubicar_la_linea_por_texto(page):
    shifting_content_page = ShiftingContentListPage(page)
    page.goto(f"{BASE_URL}/shifting_content/list")

    assert TARGET_TEXT in shifting_content_page.lineas()
    assert shifting_content_page.locator_exacto_del_registro_fijo().count() == 0

from playwright.sync_api import Browser, Page, expect

from config import BASE_URL
from ABTestingPage import ABTestingPage

VARIANTES_CONOCIDAS = {
    "A/B Test Control",
    "A/B Test Variation 1",
}

DESCRIPCION_ESPERADA = (
    "Also known as split testing. This is a way in which businesses are able to "
    "simultaneously test and learn different versions of a page to see which text "
    "and/or functionality works best towards a desired outcome (e.g. a user action "
    "such as a click-through)."
)


# /abtest corre un experimento real de Optimizely Classic (un producto que
# Optimizely discontinuó en 2018, pero cuyo script -- /js/vendor/298279967.js --
# sigue cargado y funcionando): el servidor manda siempre el mismo HTML de
# control, y es el script el que reescribe el <h3> del lado del cliente según
# el bucket que Optimizely le asigne a esa sesión. Un cliente sin JavaScript
# (como una request con curl) nunca ve la variación -- solo un browser real
# la dispara, que es justo lo que corre Playwright.

def test_titulo_es_una_de_las_dos_variantes_conocidas(page: Page) -> None:
    ab_page = ABTestingPage(page)
    page.goto(f"{BASE_URL}/abtest")

    expect(ab_page.titulo).not_to_have_text("")
    assert ab_page.titulo.inner_text() in VARIANTES_CONOCIDAS


# Con contextos nuevos e independientes (sin cookies compartidas entre sí, así
# que cada uno es un "visitante" distinto para Optimizely) se recolectan varias
# visitas hasta ver ambas variantes, para confirmar que el split es real y no
# que una de las dos casi nunca aparece.

def test_el_split_muestra_las_dos_variantes_en_visitas_independientes(browser: Browser) -> None:
    variantes_vistas: set[str] = set()

    for _ in range(15):
        context = browser.new_context()
        pagina = context.new_page()
        ab_page = ABTestingPage(pagina)
        pagina.goto(f"{BASE_URL}/abtest")
        variantes_vistas.add(ab_page.titulo.inner_text())
        context.close()
        if variantes_vistas == VARIANTES_CONOCIDAS:
            break

    assert variantes_vistas == VARIANTES_CONOCIDAS


def test_descripcion_explica_que_es_ab_testing(page: Page) -> None:
    ab_page = ABTestingPage(page)
    page.goto(f"{BASE_URL}/abtest")

    texto = " ".join(ab_page.descripcion.inner_text().split())
    assert texto == DESCRIPCION_ESPERADA


# El experimento deja sus propias cookies de tracking (ninguna del dominio
# externo optimizely.com, que la fixture de conftest.py bloquea) -- confirma
# que la asignación a variante corre y persiste del lado del cliente, no que
# el servidor eligiera al azar en cada visita.

def test_el_experimento_deja_cookies_propias_de_optimizely(page: Page) -> None:
    page.goto(f"{BASE_URL}/abtest")

    nombres_cookies = {cookie["name"] for cookie in page.context.cookies()}
    assert {"optimizelyEndUserId", "optimizelyBuckets", "optimizelySegments"} <= nombres_cookies

from config import BASE_URL
from VerifyTextPage import FRASE_OBJETIVO, VerifyTextPage


# El texto visible en pantalla ("Welcome UserName!") no es el mismo string
# que el nodo de texto del DOM: el markup real indenta y separa "Welcome" de
# "UserName" con un <span> anidado alrededor de "UserName" y espacios/saltos
# de línea de sobra, que el navegador normaliza al renderizar pero que un
# XPath literal compara tal cual están en el HTML. Además, la propia tabla
# "Does not work / Works" de la página imprime las dos expresiones XPath del
# enunciado como texto plano dentro de bloques <code>, y ese texto contiene
# la frase completa "Welcome UserName!" -- un locator por texto sin acotar a
# la sección correcta puede confundir el ejemplo documentado con el elemento
# que hay que automatizar.


def test_xpath_con_igualdad_exacta_no_encuentra_nada(page):
    verify_text_page = VerifyTextPage(page)
    page.goto(f"{BASE_URL}/verifytext")

    assert verify_text_page.xpath_igualdad_exacta().count() == 0


def test_xpath_con_normalize_space_encuentra_el_span_del_playground(page):
    verify_text_page = VerifyTextPage(page)
    page.goto(f"{BASE_URL}/verifytext")

    span = verify_text_page.xpath_normalize_space()
    assert span.count() == 1
    assert span.evaluate("el => el.tagName") == "SPAN"

    # El texto visible ya viene recortado y sin espacios de más...
    assert span.inner_text() == FRASE_OBJETIVO
    # ...pero el nodo de texto crudo del DOM conserva la indentación y los
    # saltos de línea del markup original, que es justo lo que hace que la
    # igualdad exacta de más arriba no encuentre nada.
    assert span.text_content() != FRASE_OBJETIVO
    assert span.text_content().strip() == FRASE_OBJETIVO


def test_get_by_text_exacto_coincide_con_el_mismo_span_que_normalize_space(page):
    verify_text_page = VerifyTextPage(page)
    page.goto(f"{BASE_URL}/verifytext")

    # get_by_text(exact=True) de Playwright normaliza espacios igual que
    # normalize-space() de XPath: encuentra un único elemento, el mismo
    # span.badge-secondary de la sección "Playground".
    por_texto = verify_text_page.get_by_text_exacto_en_toda_la_pagina()
    assert por_texto.count() == 1
    assert por_texto.evaluate("el => el.className") == "badge-secondary"
    assert por_texto.inner_text() == FRASE_OBJETIVO


def test_get_by_text_sin_exact_tambien_matchea_los_ejemplos_de_codigo_del_enunciado(page):
    verify_text_page = VerifyTextPage(page)
    page.goto(f"{BASE_URL}/verifytext")

    # exact=False busca la frase como substring en cualquier elemento de la
    # página, no solo en la sección "Playground" -- y la propia tabla
    # "Does not work / Works" imprime, como texto plano dentro de bloques
    # <code>, las dos expresiones XPath del enunciado, cada una con la frase
    # completa "Welcome UserName!" dentro del código. Son 3 coincidencias en
    # total, no 1: el span real más los dos ejemplos de código.
    por_texto_parcial = verify_text_page.get_by_text_parcial_en_toda_la_pagina()
    assert por_texto_parcial.count() == 3

    tags = [por_texto_parcial.nth(i).evaluate("el => el.tagName") for i in range(3)]
    assert tags.count("CODE") == 2
    assert tags.count("SPAN") == 1


def test_acotar_el_locator_al_contenedor_del_playground_evita_el_falso_positivo(page):
    verify_text_page = VerifyTextPage(page)
    page.goto(f"{BASE_URL}/verifytext")

    # Acotar la búsqueda al div.bg-primary de la sección "Playground" -- en
    # vez de buscar la frase en toda la página -- alcanza para que incluso la
    # variante sin exact=True deje de confundirse con los bloques <code> del
    # enunciado, porque esos bloques viven en otra sección del documento.
    acotado_exacto = verify_text_page.get_by_text_acotado_al_playground(exact=True)
    assert acotado_exacto.count() == 1

    acotado_parcial = verify_text_page.get_by_text_acotado_al_playground(exact=False)
    assert acotado_parcial.count() == 1
    assert acotado_parcial.inner_text() == FRASE_OBJETIVO

import pytest
from playwright.sync_api import Page

from config import BASE_URL
from TyposPage import TyposPage

TEXTO_SIN_TYPO = "Sometimes you'll see a typo, other times you won't."
TEXTO_CON_TYPO = "Sometimes you'll see a typo, other times you won,t."
VARIANTES_CONOCIDAS = {TEXTO_SIN_TYPO, TEXTO_CON_TYPO}


def test_titulo_y_parrafo_introductorio_son_fijos(page: Page) -> None:
    typos_page = TyposPage(page)
    page.goto(f"{BASE_URL}/typos")

    assert typos_page.texto_titulo() == "Typos"
    assert typos_page.texto_introductorio() == (
        "This example demonstrates a typo being introduced. "
        "It does it randomly on each page load."
    )


# El HTML real de /typos nunca cierra el primer <p> ni el segundo --
# "<p>...carga.<p>\n  Sometimes...won't.\n</div>", sin ningún </p> --, así
# que a primera vista el texto variable podría terminar como un nodo de
# texto suelto dentro del <div>, fuera de cualquier párrafo. El parser
# HTML5 del navegador autocierra un <p> apenas encuentra otro <p> abierto,
# así que el segundo <p> sí termina conteniendo ese texto, y el </div> final
# autocierra también al segundo -- confirmado contando los <p> reales del
# DOM en vez de confiar en cómo se ve el HTML fuente.

def test_el_html_roto_resuelve_en_dos_parrafos_reales(page: Page) -> None:
    typos_page = TyposPage(page)
    page.goto(f"{BASE_URL}/typos")

    assert typos_page.cantidad_de_parrafos() == 2


def test_el_parrafo_variable_es_uno_de_los_dos_textos_conocidos(page: Page) -> None:
    typos_page = TyposPage(page)
    page.goto(f"{BASE_URL}/typos")

    assert typos_page.texto_variable() in VARIANTES_CONOCIDAS


# El típo no es una palabra distinta ni un carácter de más o de menos: la
# única diferencia entre las dos variantes es el apóstrofo de "won't",
# reemplazado por una coma en "won,t". Mismo largo, mismo texto alrededor --
# el test lo confirma carácter por carácter en vez de solo comparar los dos
# strings completos, para dejar documentada la naturaleza exacta del bug.

def test_la_variante_con_typo_difiere_solo_en_el_apostrofo() -> None:
    assert len(TEXTO_CON_TYPO) == len(TEXTO_SIN_TYPO)

    diferencias = [
        (i, esperado, con_typo)
        for i, (esperado, con_typo) in enumerate(zip(TEXTO_SIN_TYPO, TEXTO_CON_TYPO))
        if esperado != con_typo
    ]

    assert len(diferencias) == 1
    indice, caracter_sin_typo, caracter_con_typo = diferencias[0]
    assert caracter_sin_typo == "'"
    assert caracter_con_typo == ","


# No hay forma de pedir la variante con error a demanda: cada carga de
# /typos la elige al azar, con probabilidad pareja según el propio
# enunciado de la página. El test recarga en un loop hasta encontrarla, en
# vez de asumir que aparece a la primera (el mismo patrón que
# /notification_message y /disappearing_elements en esta suite).

def test_el_typo_aparece_al_azar_en_recargas(page: Page) -> None:
    typos_page = TyposPage(page)

    for _ in range(30):
        page.goto(f"{BASE_URL}/typos")
        if typos_page.texto_variable() == TEXTO_CON_TYPO:
            return

    pytest.skip("El sitio no mostró la variante con typo en 30 intentos al azar")


# Simétrico al test anterior: confirma que la variante correcta también
# aparece, para no asumir que "a veces ves un typo" implica que el typo es
# la opción por default y lo demás es la excepción.

def test_la_variante_sin_typo_tambien_aparece_al_azar(page: Page) -> None:
    typos_page = TyposPage(page)

    for _ in range(30):
        page.goto(f"{BASE_URL}/typos")
        if typos_page.texto_variable() == TEXTO_SIN_TYPO:
            return

    pytest.skip("El sitio no mostró la variante sin typo en 30 intentos al azar")


# Las dos variantes conocidas son las únicas que compiten por aparecer: en
# ninguna recarga debería verse un tercer texto (por ejemplo, si el sitio
# agregara con el tiempo otro tipo de error). Se recolectan varias recargas
# y se confirma que el conjunto de textos vistos es subconjunto de las dos
# variantes conocidas.

def test_no_aparecen_variantes_desconocidas_en_varias_recargas(page: Page) -> None:
    typos_page = TyposPage(page)
    vistas = set()

    for _ in range(15):
        page.goto(f"{BASE_URL}/typos")
        vistas.add(typos_page.texto_variable())

    assert vistas <= VARIANTES_CONOCIDAS

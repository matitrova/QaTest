from typing import Iterator

import pytest
from playwright.sync_api import Browser, Page, expect

from config import BASE_URL
from LocalePage import LocalePage

# (locale del contexto, zona horaria del contexto,
#  idioma que debería detectar el servidor, saludo del servidor,
#  zona horaria que debería mostrar el navegador,
#  fecha/número/precio que Intl debería formatear en el navegador)
CASOS_DE_LOCALE = [
    (
        "en-US",
        "UTC",
        "en",
        "Hello!",
        "UTC",
        "Wednesday, April 15, 2026 at 12:00 PM",
        "1,234,567.891",
        "€1,234.50",
    ),
    (
        "es-AR",
        "America/Argentina/Buenos_Aires",
        "es",
        "¡Hola!",
        "America/Buenos_Aires",
        "miércoles, 15 de abril de 2026, 9:00 a. m.",
        "1.234.567,891",
        "EUR\xa01.234,50",
    ),
    (
        "de-DE",
        "Europe/Berlin",
        "de",
        "Hallo!",
        "Europe/Berlin",
        "Mittwoch, 15. April 2026 um 14:00",
        "1.234.567,891",
        "1.234,50\xa0€",
    ),
    (
        "ja-JP",
        "Asia/Tokyo",
        "ja",
        "こんにちは！",
        "Asia/Tokyo",
        "2026年4月15日水曜日 21:00",
        "1,234,567.891",
        "€1,234.50",
    ),
    (
        "fr-FR",
        "Europe/Paris",
        "fr",
        "Bonjour !",
        "Europe/Paris",
        "mercredi 15 avril 2026 à 14:00",
        "1 234 567,891",
        "1 234,50\xa0€",
    ),
]


@pytest.fixture(params=CASOS_DE_LOCALE, ids=[caso[0] for caso in CASOS_DE_LOCALE])
def caso_de_locale(request: pytest.FixtureRequest) -> tuple:
    return request.param


@pytest.fixture
def pagina_con_locale(browser: Browser, caso_de_locale: tuple) -> Iterator[Page]:
    # Esta suite arma su propio contexto por caso (en vez de pisar el
    # fixture "browser_context_args" de pytest-playwright, como hace
    # test_geolocation.py) porque solo DOS de los cuatro tests de este
    # archivo necesitan variar el locale -- los otros dos fijan uno propio
    # para probar el override de ?lang=. Pisar "browser_context_args" a
    # nivel de módulo arrastra también a esos otros tests, por la fixture
    # autouse de conftest.py que depende de "page": correrían una vez por
    # cada locale de CASOS_DE_LOCALE sin ninguna razón.
    locale, timezone_id, *_resto = caso_de_locale
    context = browser.new_context(locale=locale, timezone_id=timezone_id)
    pagina = context.new_page()
    yield pagina
    context.close()


def test_el_saludo_del_servidor_sigue_el_accept_language_del_contexto(
    pagina_con_locale: Page, caso_de_locale: tuple
) -> None:
    _locale, _tz, idioma_esperado, saludo_esperado, *_resto = caso_de_locale
    locale_page = LocalePage(pagina_con_locale)
    pagina_con_locale.goto(f"{BASE_URL}/locale")

    expect(locale_page.saludo).to_have_text(saludo_esperado)
    expect(locale_page.idioma_del_servidor).to_have_text(idioma_esperado)


def test_el_navegador_formatea_fecha_numero_y_precio_con_su_locale_y_zona(
    pagina_con_locale: Page, caso_de_locale: tuple
) -> None:
    (
        locale,
        _timezone_id,
        _idioma,
        _saludo,
        zona_esperada,
        fecha_esperada,
        numero_esperado,
        precio_esperado,
    ) = caso_de_locale
    locale_page = LocalePage(pagina_con_locale)
    pagina_con_locale.goto(f"{BASE_URL}/locale")

    expect(locale_page.idioma_del_navegador).to_have_text(locale)
    expect(locale_page.zona_horaria_del_navegador).to_have_text(zona_esperada)
    expect(locale_page.fecha_formateada).to_have_text(fecha_esperada)
    expect(locale_page.numero_formateado).to_have_text(numero_esperado)
    expect(locale_page.precio_formateado).to_have_text(precio_esperado)


def test_el_parametro_lang_fuerza_el_idioma_del_servidor_sin_importar_el_contexto(
    browser: Browser,
) -> None:
    # El contexto dice "de-DE" (Accept-Language: de), pero la URL fuerza
    # "ja" con ?lang=. El saludo del servidor sigue a la URL; el lado del
    # navegador (navigator.language, Intl) sigue atado al contexto y no se
    # entera del parámetro -- son dos fuentes de idioma totalmente
    # independientes que conviven en la misma página.
    context = browser.new_context(locale="de-DE", timezone_id="Europe/Berlin")
    pagina_con_override = context.new_page()
    locale_page = LocalePage(pagina_con_override)
    pagina_con_override.goto(f"{BASE_URL}/locale?lang=ja")

    expect(locale_page.saludo).to_have_text("こんにちは！")
    expect(locale_page.idioma_del_servidor).to_have_text("ja")
    expect(locale_page.idioma_del_navegador).to_have_text("de-DE")
    expect(locale_page.zona_horaria_del_navegador).to_have_text("Europe/Berlin")

    context.close()


def test_un_codigo_de_idioma_invalido_en_lang_cae_al_accept_language(
    browser: Browser,
) -> None:
    # ?lang= solo vale si trae uno de los cinco códigos que el servidor
    # reconoce. Con uno que no reconoce, lo ignora por completo y vuelve a
    # decidir por Accept-Language, en vez de devolver un error o un saludo
    # vacío.
    context = browser.new_context(locale="de-DE")
    pagina_con_lang_invalido = context.new_page()
    locale_page = LocalePage(pagina_con_lang_invalido)
    pagina_con_lang_invalido.goto(f"{BASE_URL}/locale?lang=xx")

    expect(locale_page.saludo).to_have_text("Hallo!")
    expect(locale_page.idioma_del_servidor).to_have_text("de")

    context.close()

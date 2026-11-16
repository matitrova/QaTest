import datetime

import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from DatePickersPage import DatePickersPage


@pytest.fixture
def date_pickers_page(page: Page) -> DatePickersPage:
    page.goto(f"{BASE_URL}/date_pickers")
    return DatePickersPage(page)


def test_sin_llenar_nada_el_resultado_dice_no_values_yet(
    date_pickers_page: DatePickersPage,
) -> None:
    expect(date_pickers_page.resultado).to_have_text("No values yet")


# El párrafo de resultado no arma el texto en el orden en que se llenaron los
# campos: recorre el <form> con querySelectorAll en cada evento "input" y
# reconstruye la lista entera en el orden en que los inputs aparecen en el
# DOM (date, time, datetime, month, week). Llenar time antes que date tiene
# que mostrar igual "date: ..., time: ..." y no "time: ..., date: ...".
def test_el_orden_del_resultado_es_el_del_dom_no_el_de_llenado(
    date_pickers_page: DatePickersPage,
) -> None:
    date_pickers_page.time_input.fill("14:30")
    date_pickers_page.date_input.fill("2026-04-15")

    expect(date_pickers_page.resultado).to_have_text("date: 2026-04-15, time: 14:30")


def test_llenar_los_cinco_inputs_nativos_los_lista_completos_en_orden(
    date_pickers_page: DatePickersPage,
) -> None:
    date_pickers_page.date_input.fill("2026-04-15")
    date_pickers_page.time_input.fill("14:30")
    date_pickers_page.datetime_input.fill("2026-04-15T14:30")
    date_pickers_page.month_input.fill("2026-04")
    date_pickers_page.week_input.fill("2026-W15")

    expect(date_pickers_page.resultado).to_have_text(
        "date: 2026-04-15, time: 14:30, datetime: 2026-04-15T14:30, "
        "month: 2026-04, week: 2026-W15"
    )


# El input de fecha declara min="2000-01-01" y max="2099-12-31" en su HTML,
# pero esos atributos solo los haría cumplir una validación de formulario al
# enviarlo -- esta página no tiene ningún botón de submit, así que un valor
# fuera de rango no tiene nada que lo bloquee y el navegador lo acepta igual.
def test_el_input_de_fecha_acepta_un_valor_fuera_del_min_y_max(
    date_pickers_page: DatePickersPage,
) -> None:
    date_pickers_page.date_input.fill("1999-01-01")

    expect(date_pickers_page.date_input).to_have_value("1999-01-01")
    expect(date_pickers_page.resultado).to_have_text("date: 1999-01-01")


def test_el_campo_appointment_es_de_solo_lectura(
    date_pickers_page: DatePickersPage,
) -> None:
    expect(date_pickers_page.campo_appointment).to_have_attribute("readonly", "")


def test_abrir_calendario_cambia_el_texto_y_el_aria_expanded_del_boton(
    date_pickers_page: DatePickersPage,
) -> None:
    expect(date_pickers_page.boton_abrir_calendario).to_have_attribute(
        "aria-expanded", "false"
    )
    expect(date_pickers_page.calendario).to_be_hidden()

    date_pickers_page.abrir_calendario()

    expect(date_pickers_page.boton_abrir_calendario).to_have_text("Close calendar")
    expect(date_pickers_page.boton_abrir_calendario).to_have_attribute(
        "aria-expanded", "true"
    )
    expect(date_pickers_page.calendario).to_be_visible()


# El parámetro ?month=YYYY-MM de la URL fija qué mes abre el calendario --
# usarlo en vez de depender de la fecha real del día en que corre la suite
# es lo que permite afirmar un mes puntual, una cantidad de días puntual y un
# día de la semana inicial puntual sin que el test dependa de "hoy".
def test_month_en_la_url_fija_el_mes_que_abre_el_calendario(page: Page) -> None:
    date_pickers_page = DatePickersPage(page)
    page.goto(f"{BASE_URL}/date_pickers?month=2024-02")

    date_pickers_page.abrir_calendario()

    expect(date_pickers_page.encabezado_mes).to_have_text("February 2024")
    assert date_pickers_page.dias.count() == 29  # 2024 es bisiesto


# El 1° de enero de 2023 cae domingo. La grilla arranca en lunes (los
# encabezados de columna son Mo..Su), así que la primera fila tiene que
# tener seis celdas vacías antes de la primera con el botón "1" -- si el
# calendario tratara al domingo como el primer día de la semana (el default
# de Date.getDay()), esas celdas vacías serían otras y el "1" caería en una
# columna distinta.
def test_la_semana_arranca_en_lunes_no_en_domingo(page: Page) -> None:
    date_pickers_page = DatePickersPage(page)
    page.goto(f"{BASE_URL}/date_pickers?month=2023-01")

    date_pickers_page.abrir_calendario()

    primera_fila = page.locator("#calendar-days tr").first
    celdas_vacias = primera_fila.locator("td:not(:has(button))")
    assert celdas_vacias.count() == 6
    expect(date_pickers_page.dias.first).to_have_text("1")


# Un valor de ?month= con un formato que no matchea el regex que el propio
# script espera (YYYY-MM) se ignora del todo, sin ningún error visible --
# el calendario cae en el mes real del día en que corre la suite, calculado
# acá con datetime.now() en vez de hardcodearlo, porque la suite corre en
# integración continua en una fecha distinta cada vez.
def test_month_invalido_en_la_url_se_ignora_y_usa_el_mes_real(
    page: Page,
) -> None:
    date_pickers_page = DatePickersPage(page)
    page.goto(f"{BASE_URL}/date_pickers?month=no-es-un-mes")

    date_pickers_page.abrir_calendario()

    hoy = datetime.date.today()
    mes_esperado = hoy.strftime("%B %Y")
    expect(date_pickers_page.encabezado_mes).to_have_text(mes_esperado)


def test_elegir_un_dia_lo_escribe_en_el_campo_y_cierra_el_calendario(
    date_pickers_page: DatePickersPage,
) -> None:
    page = date_pickers_page.page
    page.goto(f"{BASE_URL}/date_pickers?month=2024-02")
    date_pickers_page.abrir_calendario()

    date_pickers_page.elegir_dia(15)

    expect(date_pickers_page.campo_appointment).to_have_value("2024-02-15")
    expect(date_pickers_page.calendario).to_be_hidden()
    expect(date_pickers_page.boton_abrir_calendario).to_have_text("Open calendar")


# render() marca con la clase "selected" al botón cuyo data-date coincide con
# el valor actual del campo, cada vez que se vuelve a dibujar la grilla --no
# solo la primera vez. El test lo confirma navegando a otro mes y volviendo:
# el día elegido se desmarca en el mes al que no pertenece y se vuelve a
# marcar solo al volver al suyo, sin haber vuelto a clickearlo.
def test_el_dia_elegido_sigue_marcado_como_selected_tras_navegar_y_volver(
    date_pickers_page: DatePickersPage,
) -> None:
    page = date_pickers_page.page
    page.goto(f"{BASE_URL}/date_pickers?month=2024-02")
    date_pickers_page.abrir_calendario()
    date_pickers_page.elegir_dia(15)

    date_pickers_page.abrir_calendario()
    assert date_pickers_page.dia_seleccionado.count() == 1
    expect(date_pickers_page.dia_seleccionado).to_have_text("15")

    date_pickers_page.boton_mes_siguiente.click()
    assert date_pickers_page.dia_seleccionado.count() == 0

    date_pickers_page.boton_mes_anterior.click()
    expect(date_pickers_page.encabezado_mes).to_have_text("February 2024")
    assert date_pickers_page.dia_seleccionado.count() == 1
    expect(date_pickers_page.dia_seleccionado).to_have_text("15")

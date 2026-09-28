import pytest
from playwright.sync_api import expect

from config import BASE_URL
from InputsPage import InputsPage


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # Mismo motivo que en el resto de la suite: el layout del sitio carga un
    # script de Optimizely ajeno a lo que se prueba, y si esa red está lenta
    # o inaccesible el evento "load" puede colgarse esperándolo.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield


def test_arranca_vacio(page):
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    expect(inputs_page.input_numero).to_have_value("")


def test_acepta_digitos(page):
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("1234")

    expect(inputs_page.input_numero).to_have_value("1234")


def test_rechaza_letras(page):
    # No hay ningún atributo `pattern` ni JS de validación en este input: es
    # el propio navegador el que, por ser type="number", descarta cada tecla
    # que no sea un carácter numérico válido antes de que llegue al valor.
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("abc")

    expect(inputs_page.input_numero).to_have_value("")


def test_acepta_negativos_y_decimales(page):
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("-42")
    expect(inputs_page.input_numero).to_have_value("-42")

    inputs_page.escribir("3.14")
    expect(inputs_page.input_numero).to_have_value("3.14")


def test_descarta_un_segundo_punto_decimal(page):
    # El navegador permite un solo punto decimal por valor: al escribir
    # "5.5.5" el segundo punto se descarta solo, pero el resto de los
    # caracteres sigue entrando -- el resultado es "5.55", no un valor vacío
    # ni un error.
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("5.5.5")

    expect(inputs_page.input_numero).to_have_value("5.55")


def test_descarta_el_signo_mas_suelto(page):
    # Un "+" sin exponente (`e`/`E`) de por medio no es un carácter válido en
    # este input: se descarta igual que una letra, y solo queda el dígito
    # que le sigue.
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("+5")

    expect(inputs_page.input_numero).to_have_value("5")


def test_mantiene_notacion_cientifica_como_texto(page):
    # "1e3" es notación científica válida para un number input, pero el
    # navegador no la normaliza mientras se escribe: input_value() devuelve
    # el texto tal cual se tipeó, no el 1000 que representa.
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("1e3")

    expect(inputs_page.input_numero).to_have_value("1e3")


def test_mantiene_ceros_a_la_izquierda(page):
    # Sin ningún atributo min/max/step que fuerce una normalización, el
    # valor se guarda como el string que se tipeó: "007" no se convierte en
    # "7" hasta que algo (un submit, por ejemplo) lo interprete como número.
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("007")

    expect(inputs_page.input_numero).to_have_value("007")


def test_flecha_arriba_incrementa_de_a_uno(page):
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("0")
    inputs_page.presionar_flecha_arriba(veces=2)

    expect(inputs_page.input_numero).to_have_value("2")


def test_flecha_abajo_no_tiene_piso_sin_atributo_min(page):
    # Este input no tiene atributo `min`: bajar con la flecha por debajo de
    # cero no lo frena en 0, sigue restando y entra en negativos.
    inputs_page = InputsPage(page)
    page.goto(f"{BASE_URL}/inputs")

    inputs_page.escribir("0")
    inputs_page.presionar_flecha_abajo(veces=3)

    expect(inputs_page.input_numero).to_have_value("-3")

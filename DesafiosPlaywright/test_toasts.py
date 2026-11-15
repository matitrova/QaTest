import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from ToastsPage import ToastsPage


@pytest.fixture
def toasts_page(page: Page) -> ToastsPage:
    page.goto(f"{BASE_URL}/toasts")
    return ToastsPage(page)


def test_duracion_inicial_es_3000(toasts_page: ToastsPage) -> None:
    expect(toasts_page.duration_input).to_have_value("3000")


# El valor del input se puede traer de la URL (?duration=1000), pero el script
# solo lo pisa si el parámetro es puramente numérico -- la condición explícita
# (/^\d+$/) es la única garantía de que un valor roto en la URL no termine
# escrito en el campo tal cual.
def test_duracion_desde_la_url_pisa_el_valor_default(page: Page) -> None:
    toasts_page = ToastsPage(page)
    page.goto(f"{BASE_URL}/toasts?duration=1000")

    expect(toasts_page.duration_input).to_have_value("1000")


def test_duracion_invalida_en_la_url_no_pisa_el_default(page: Page) -> None:
    toasts_page = ToastsPage(page)
    page.goto(f"{BASE_URL}/toasts?duration=abc")

    expect(toasts_page.duration_input).to_have_value("3000")


@pytest.mark.parametrize(
    ("metodo", "mensaje_esperado", "rol_esperado"),
    [
        ("mostrar_toast_exito", "Saved successfully", "status"),
        ("mostrar_toast_error", "Something went wrong", "alert"),
        ("mostrar_toast_info", "Here is some information", "status"),
    ],
    ids=["exito", "error", "info"],
)
def test_cada_tipo_de_toast_muestra_su_mensaje_y_su_rol(
    toasts_page: ToastsPage,
    metodo: str,
    mensaje_esperado: str,
    rol_esperado: str,
) -> None:
    getattr(toasts_page, metodo)()

    toast = toasts_page.toast_por_numero(1)
    expect(toast).to_be_visible()
    expect(toast.locator(".toast-message")).to_have_text(mensaje_esperado)
    assert toast.get_attribute("role") == rol_esperado


# El contador "shown" es un único acumulador global, no uno por tipo: pedir
# un toast de éxito y después uno de error no reinicia la numeración, el
# segundo toast es el #2 aunque sea de un tipo distinto al primero.
def test_el_contador_de_toasts_es_global_entre_tipos_distintos(
    toasts_page: ToastsPage,
) -> None:
    toasts_page.mostrar_toast_exito()
    expect(toasts_page.toast_count).to_have_text("Toasts shown: 1")

    toasts_page.mostrar_toast_error()
    expect(toasts_page.toast_count).to_have_text("Toasts shown: 2")

    expect(toasts_page.toast_por_numero(1)).to_be_visible()
    expect(toasts_page.toast_por_numero(2)).to_be_visible()


def test_mostrar_dos_toasts_los_apila_sin_reemplazar_al_anterior(
    toasts_page: ToastsPage,
) -> None:
    toasts_page.mostrar_toast_info()
    toasts_page.mostrar_toast_exito()

    assert toasts_page.cantidad_toasts_visibles() == 2


# Con duracion 0 el toast queda para siempre -- el script nunca llama a
# setTimeout si duration no es mayor a 0 -- así que solo se puede sacar de
# encima con el botón de cierre, nunca por sí solo.
def test_duracion_cero_deja_el_toast_abierto_hasta_cerrarlo_a_mano(
    toasts_page: ToastsPage,
) -> None:
    toasts_page.fijar_duracion(0)
    toasts_page.mostrar_toast_exito()
    toast = toasts_page.toast_por_numero(1)

    toasts_page.page.wait_for_timeout(1500)
    expect(toast).to_be_visible()

    toasts_page.cerrar_toast(1)
    expect(toast).to_be_hidden()


def test_duracion_corta_hace_que_el_toast_se_cierre_solo(
    toasts_page: ToastsPage,
) -> None:
    toasts_page.fijar_duracion(500)
    toasts_page.mostrar_toast_info()
    toast = toasts_page.toast_por_numero(1)

    expect(toast).to_be_visible()
    expect(toast).to_be_hidden(timeout=3000)


# El botón de cierre borra el toast al toque, sin importar qué duración
# tenga configurada -- un cierre manual no depende del setTimeout.
def test_cerrar_a_mano_funciona_aunque_la_duracion_no_haya_vencido(
    toasts_page: ToastsPage,
) -> None:
    toasts_page.fijar_duracion(60000)
    toasts_page.mostrar_toast_exito()
    toast = toasts_page.toast_por_numero(1)
    expect(toast).to_be_visible()

    toasts_page.cerrar_toast(1)

    expect(toast).to_be_hidden()

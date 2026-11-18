import pytest
from playwright.sync_api import Page, expect

from config import BASE_URL
from LargeFormPage import LargeFormPage


@pytest.fixture
def form_page(page: Page) -> LargeFormPage:
    page.goto(f"{BASE_URL}/large_form")
    return LargeFormPage(page)


# A diferencia de la opción inicial de `/dropdown` (un placeholder marcado
# `disabled` en el HTML), la de `/large_form` no lo tiene: sigue siendo un
# placeholder en los hechos (ningún país real tiene valor ""), pero nada le
# impide al usuario volver a elegirla a mano desde el propio `<select>`.
def test_opcion_inicial_del_country_es_un_placeholder_sin_disabled(
    form_page: LargeFormPage,
) -> None:
    expect(form_page.country).to_have_value("")
    opcion_inicial = form_page.country.locator("option").first
    expect(opcion_inicial).to_have_text("Choose a country")
    expect(opcion_inicial).to_be_enabled()


def test_contacto_por_email_viene_marcado_por_default_y_elegir_otro_lo_desmarca(
    form_page: LargeFormPage,
) -> None:
    expect(form_page.contacto("email")).to_be_checked()
    expect(form_page.contacto("phone")).not_to_be_checked()

    form_page.contacto("phone").check()

    expect(form_page.contacto("phone")).to_be_checked()
    expect(form_page.contacto("email")).not_to_be_checked()


@pytest.mark.parametrize("valor", ["0", "15", "30"])
def test_slider_de_experiencia_sincroniza_el_span_en_vivo(
    form_page: LargeFormPage, valor: str
) -> None:
    form_page.experience.fill(valor)
    expect(form_page.experience_valor).to_have_text(valor)


# Bug real del sitio: `oninput` del slider actualiza el span a mano, pero
# resetear un <form> con un botón type="reset" no dispara el evento "input"
# en sus controles (solo "reset" en el propio form, según el estándar) --
# el slider sí vuelve a su valor original (5), pero el span queda pegado al
# último valor que el usuario tipeó, mostrando un número que ya no es el que
# tiene el control real.
def test_reset_revierte_los_controles_pero_el_span_de_experiencia_queda_desactualizado(
    form_page: LargeFormPage,
) -> None:
    form_page.first_name.fill("Juan")
    form_page.contacto("phone").check()
    form_page.experience.fill("25")
    expect(form_page.experience_valor).to_have_text("25")

    form_page.boton_reset.click()

    expect(form_page.first_name).to_have_value("")
    expect(form_page.contacto("email")).to_be_checked()
    expect(form_page.experience).to_have_value("5")
    expect(form_page.experience_valor).to_have_text("25")


# El navegador corre su propia validación (type=email, min/max del input de
# edad) ANTES de disparar el submit -- si algún campo no la pasa, el POST
# nunca sale hacia el servidor. Se confirma con un listener de requests en
# vez de asumirlo por el resultado vacío, igual que en /form_validation.
CASOS_BLOQUEADOS = [
    {"email": "no-es-un-email"},
    {"age": "200"},
]
IDS_CASOS_BLOQUEADOS = ["email_sin_forma_de_email", "edad_por_encima_del_maximo"]


@pytest.mark.parametrize("valores", CASOS_BLOQUEADOS, ids=IDS_CASOS_BLOQUEADOS)
def test_campo_invalido_bloquea_el_envio_sin_pegarle_al_servidor(
    form_page: LargeFormPage, valores: dict
) -> None:
    pedidos_post: list[str] = []
    form_page.page.on(
        "request",
        lambda request: pedidos_post.append(request.url)
        if request.method == "POST"
        else None,
    )

    if "email" in valores:
        form_page.email.fill(valores["email"])
    if "age" in valores:
        form_page.age.fill(valores["age"])
    form_page.terms.check()
    form_page.boton_enviar.click()
    form_page.page.wait_for_timeout(300)

    assert pedidos_post == []
    expect(form_page.tabla_resultado).to_have_count(0)


def test_envio_valido_muestra_tabla_con_los_valores_ingresados(
    form_page: LargeFormPage,
) -> None:
    form_page.first_name.fill("Juan")
    form_page.email.fill("juan@example.com")
    form_page.age.fill("30")
    form_page.contacto("phone").check()
    form_page.terms.check()

    with form_page.page.expect_response(
        lambda response: response.url.endswith("/large_form")
        and response.request.method == "POST"
    ):
        form_page.boton_enviar.click()

    expect(form_page.titulo).to_have_text("Form Submitted")
    expect(form_page.valor_en_tabla("first_name")).to_have_text("Juan")
    expect(form_page.valor_en_tabla("email")).to_have_text("juan@example.com")
    expect(form_page.valor_en_tabla("age")).to_have_text("30")
    expect(form_page.valor_en_tabla("contact")).to_have_text("phone")
    expect(form_page.valor_en_tabla("terms")).to_have_text("accepted")
    expect(form_page.valor_en_tabla("experience")).to_have_text("5")
    expect(form_page.valor_en_tabla("color")).to_have_text("#e2231a")


# `languages[]` e `interests[]` son los únicos dos campos del formulario que
# mandan varios valores bajo el mismo nombre. Sin ninguna opción elegida, el
# servidor no agrega ninguna fila para ellos en la tabla de confirmación --
# a diferencia de un campo escalar vacío (`last_name`, `country`), que sí
# aparece en la tabla con el valor vacío. "Vacío" significa cosas distintas
# según el tipo de campo, y la tabla lo refleja de forma inconsistente.
def test_campos_multivalor_vacios_no_aparecen_en_la_tabla_pero_los_escalares_vacios_si(
    form_page: LargeFormPage,
) -> None:
    form_page.terms.check()

    with form_page.page.expect_response(
        lambda response: response.url.endswith("/large_form")
        and response.request.method == "POST"
    ):
        form_page.boton_enviar.click()

    expect(form_page.fila("last_name")).to_have_count(1)
    expect(form_page.valor_en_tabla("last_name")).to_have_text("")
    expect(form_page.fila("country")).to_have_count(1)
    expect(form_page.valor_en_tabla("country")).to_have_text("")

    expect(form_page.fila("languages")).to_have_count(0)
    expect(form_page.fila("interests")).to_have_count(0)


# El servidor no junta los valores elegidos en el orden en que se los eligió:
# siempre los junta en el orden en que las opciones aparecen en el propio
# <select>/grupo de checkboxes del formulario -- el mismo patrón que ya
# documenta esta suite en /date_pickers con el orden del resumen de texto.
def test_campos_multivalor_se_unen_en_el_orden_del_dom_no_en_el_orden_elegido(
    form_page: LargeFormPage,
) -> None:
    form_page.languages.select_option(["German", "English"])
    form_page.interes("devops").check()
    form_page.interes("testing").check()
    form_page.terms.check()

    with form_page.page.expect_response(
        lambda response: response.url.endswith("/large_form")
        and response.request.method == "POST"
    ):
        form_page.boton_enviar.click()

    expect(form_page.valor_en_tabla("languages")).to_have_text("English, German")
    expect(form_page.valor_en_tabla("interests")).to_have_text("testing, devops")

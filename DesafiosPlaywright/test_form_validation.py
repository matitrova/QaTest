import time

import pytest
import requests
from playwright.sync_api import Page, Route, expect

from config import BASE_URL
from FormValidationPage import FormValidationPage


@pytest.fixture
def form_page(page: Page) -> FormValidationPage:
    page.goto(f"{BASE_URL}/form_validation")
    return FormValidationPage(page)


def test_envio_valido_crea_la_cuenta(form_page: FormValidationPage) -> None:
    form_page.completar(username="zzqatestvalido")
    form_page.enviar()

    expect(form_page.resultado).to_have_text("Account created for zzqatestvalido")
    expect(form_page.boton_enviar).to_be_enabled()


# "tomsmith" y "admin" son los dos únicos usuarios que el servidor rechaza.
@pytest.mark.parametrize("username", ["tomsmith", "admin"])
def test_username_ya_tomado_falla_del_lado_del_servidor(
    form_page: FormValidationPage, username: str
) -> None:
    form_page.completar(username=username)
    form_page.enviar()

    expect(form_page.resultado).to_have_text("Please fix the errors below")
    expect(form_page.error("username")).to_have_text("Username is already taken")
    expect(form_page.username).to_have_attribute("aria-invalid", "true")
    # Ningún otro campo participó de este error -- el servidor solo revisó
    # el username, y el JS de la página solo marca `aria-invalid` en los
    # campos que vienen en el `errors` de la respuesta.
    expect(form_page.email).not_to_have_attribute("aria-invalid", "true")


# El `pattern="[a-z0-9]+"` del input de username es case-sensitive, así que
# una variante en mayúsculas ("TomSmith", "ADMIN") nunca llega a mandarse
# desde el navegador -- el propio formulario le impide a cualquiera probar
# si el chequeo de "usuario ya tomado" del servidor distingue mayúsculas o
# no. Pegándole directo al endpoint (sin pasar por el form) se confirma que
# no distingue: el backend compara en minúsculas antes de buscar en su lista
# de usuarios tomados, así que "TomSmith" y "ADMIN" chocan con el mismo
# error que sus versiones en minúsculas, aunque el navegador jamás deje
# probarlo con un usuario real.
@pytest.mark.parametrize("username", ["TomSmith", "ADMIN"])
def test_el_chequeo_de_username_tomado_es_case_insensitive_en_el_servidor(
    username: str,
) -> None:
    respuesta = requests.post(
        f"{BASE_URL}/form_validation",
        data={
            "username": username,
            "email": "zzqatest@example.com",
            "age": "25",
            "website": "",
            "password": "password123",
            "terms": "on",
        },
    )

    assert respuesta.status_code == 422
    assert respuesta.json() == {
        "errors": {"username": "Username is already taken"}
    }


# El navegador corre su propia validación (required, minlength, maxlength,
# pattern, type=email, type=url, min/max) ANTES de disparar el evento
# "submit" de la página -- si algún campo no la pasa, ni siquiera llega a
# ejecutarse el `preventDefault()` del JS, y por lo tanto nunca sale ningún
# POST hacia el servidor. Se confirma con un listener de requests en vez de
# asumirlo por el resultado vacío: "el navegador no lo mandó" y "el servidor
# lo mandó pero no respondió nada" se ven exactamente igual en pantalla.
CASOS_BLOQUEADOS_POR_EL_NAVEGADOR = [
    {"username": ""},
    {"username": "AB"},
    {"email": "no-es-un-email"},
    {"password": "corta1"},
    {"website": "no-es-una-url"},
    {"age": "5"},
    {"age": "150"},
    {"terms": False},
]

IDS_CASOS_BLOQUEADOS = [
    "username_vacio",
    "username_con_mayusculas_y_muy_corto",
    "email_sin_arroba",
    "password_de_menos_de_8_caracteres",
    "website_sin_forma_de_url",
    "edad_por_debajo_del_minimo",
    "edad_por_encima_del_maximo",
    "terms_sin_tildar",
]


@pytest.mark.parametrize(
    "valores", CASOS_BLOQUEADOS_POR_EL_NAVEGADOR, ids=IDS_CASOS_BLOQUEADOS
)
def test_campo_invalido_el_navegador_bloquea_el_envio_sin_pegarle_al_servidor(
    form_page: FormValidationPage, valores: dict
) -> None:
    pedidos_post = []
    form_page.page.on(
        "request",
        lambda request: pedidos_post.append(request.url)
        if request.method == "POST"
        else None,
    )

    form_page.completar(**valores)
    form_page.enviar()
    form_page.page.wait_for_timeout(300)

    assert pedidos_post == []
    expect(form_page.resultado).to_have_text("")


# El contraste con el test anterior: el mismo username que el navegador
# nunca deja mandar ("AB", viola `pattern` y `minlength`) sí es aceptado por
# el servidor -- junto con una edad fuera de rango y una URL con formato
# inválido en el campo opcional. El backend no valida ninguna de esas tres
# reglas: solo revisa que username, email, password y terms estén
# presentes, que el password tenga 8 caracteres o más, y si el username ya
# está tomado. Confirmado pegándole directo al endpoint con `requests`, sin
# pasar por el formulario -- un `curl` real ignora por completo el pattern,
# el rango de edad y el formato de URL que el navegador exige.
def test_el_servidor_acepta_username_edad_y_url_invalidos_para_el_navegador() -> None:
    respuesta = requests.post(
        f"{BASE_URL}/form_validation",
        data={
            "username": "AB",
            "email": "zzqatest@example.com",
            "age": "5",
            "website": "no-es-una-url",
            "password": "password123",
            "terms": "on",
        },
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == {"message": "Account created for AB"}


# Mientras el `fetch()` está en vuelo, el botón queda deshabilitado y el
# párrafo de resultado muestra "Checking..." -- una ventana demasiado chica
# para capturar contra el servidor real (responde casi al instante), así que
# se intercepta la ruta para retrasar la respuesta a propósito y poder
# observar ese estado intermedio con un `expect()` en vez de una carrera
# contra el tiempo.
def test_boton_se_deshabilita_y_muestra_checking_mientras_espera_la_respuesta(
    form_page: FormValidationPage,
) -> None:
    def demorar_respuesta(route: Route) -> None:
        time.sleep(1)
        route.continue_()

    form_page.page.route(f"{BASE_URL}/form_validation", demorar_respuesta)

    form_page.completar(username="zzqatestdemorado")
    form_page.enviar()

    expect(form_page.resultado).to_have_text("Checking...")
    expect(form_page.boton_enviar).to_be_disabled()

    expect(form_page.resultado).to_have_text("Account created for zzqatestdemorado")
    expect(form_page.boton_enviar).to_be_enabled()

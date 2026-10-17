import jsonschema
import pytest
import requests
from config import BASE_URL

SCHEMA_USUARIO = {
    "type": "object",
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
        "first_name": {"type": "string", "minLength": 1},
        "last_name": {"type": "string", "minLength": 1},
        "avatar": {"type": "string", "pattern": r"^https?://"},
    },
}

SCHEMA_USUARIO_INDIVIDUAL = {
    "type": "object",
    "required": ["data"],
    "properties": {"data": SCHEMA_USUARIO},
}

SCHEMA_LISTA_USUARIOS = {
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {"type": "array", "items": SCHEMA_USUARIO},
    },
}

SCHEMA_USUARIO_CREADO = {
    "type": "object",
    "required": ["name", "job", "id", "createdAt"],
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        # A diferencia del GET, donde "id" es un entero, el POST de creación
        # lo devuelve como string ("649", no 649). Un esquema copiado del de
        # GET rechazaría cada creación exitosa.
        "id": {"type": "string"},
        "createdAt": {"type": "string", "format": "date-time"},
    },
}


def test_usuario_individual_cumple_el_contrato(headers):
    respuesta = requests.get(f"{BASE_URL}/api/users/2", headers=headers)
    assert respuesta.status_code == 200
    jsonschema.validate(respuesta.json(), SCHEMA_USUARIO_INDIVIDUAL)


def test_lista_de_usuarios_cumple_el_contrato(headers):
    respuesta = requests.get(f"{BASE_URL}/api/users?page=1", headers=headers)
    assert respuesta.status_code == 200
    jsonschema.validate(respuesta.json(), SCHEMA_LISTA_USUARIOS)


def test_usuario_creado_cumple_su_propio_contrato_no_el_del_get(headers):
    nuevo_usuario = {"name": "morpheus", "job": "leader"}
    respuesta = requests.post(f"{BASE_URL}/api/users", json=nuevo_usuario, headers=headers)
    assert respuesta.status_code == 201
    jsonschema.validate(respuesta.json(), SCHEMA_USUARIO_CREADO)

    # El "id" es string de verdad, no un número que json.loads() convirtió:
    # si reqres alguna vez lo devolviera como entero, SCHEMA_USUARIO (el del
    # GET) lo aceptaría igual si alguien lo reusara acá por error.
    assert isinstance(respuesta.json()["id"], str)


def test_el_esquema_de_usuario_rechaza_un_id_como_string():
    # Confirma que SCHEMA_USUARIO realmente exige "id" entero: un documento
    # idéntico a un usuario real pero con "id" como string (el mismo tipo
    # que devuelve el POST de creación) tiene que fallar la validación. Sin
    # este test, un esquema roto que aceptara cualquier tipo pasaría igual
    # contra la API real sin que nadie lo notara.
    usuario_con_id_invalido = {
        "id": "2",
        "email": "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "https://reqres.in/img/faces/2-image.jpg",
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(usuario_con_id_invalido, SCHEMA_USUARIO)


def test_el_esquema_de_usuario_rechaza_un_avatar_sin_url():
    usuario_con_avatar_invalido = {
        "id": 2,
        "email": "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "no-es-una-url",
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(usuario_con_avatar_invalido, SCHEMA_USUARIO)

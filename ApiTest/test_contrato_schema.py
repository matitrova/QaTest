import jsonschema
import pytest
import requests

from config import BASE_URL

SCHEMA_GEO = {
    "type": "object",
    "required": ["lat", "lng"],
    "properties": {
        "lat": {"type": "string"},
        "lng": {"type": "string"},
    },
}

SCHEMA_DIRECCION = {
    "type": "object",
    "required": ["street", "suite", "city", "zipcode", "geo"],
    "properties": {
        "street": {"type": "string", "minLength": 1},
        "suite": {"type": "string", "minLength": 1},
        "city": {"type": "string", "minLength": 1},
        "zipcode": {"type": "string", "minLength": 1},
        "geo": SCHEMA_GEO,
    },
}

SCHEMA_COMPANIA = {
    "type": "object",
    "required": ["name", "catchPhrase", "bs"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "catchPhrase": {"type": "string", "minLength": 1},
        "bs": {"type": "string", "minLength": 1},
    },
}

SCHEMA_USUARIO = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string", "minLength": 1},
        "username": {"type": "string", "minLength": 1},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
        "address": SCHEMA_DIRECCION,
        "phone": {"type": "string", "minLength": 1},
        "website": {"type": "string", "minLength": 1},
        "company": SCHEMA_COMPANIA,
    },
}

SCHEMA_POST = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "body": {"type": "string", "minLength": 1},
    },
}


def test_usuario_individual_cumple_el_contrato(session: requests.Session) -> None:
    respuesta = session.get(f"{BASE_URL}/users/2")
    assert respuesta.status_code == 200
    jsonschema.validate(respuesta.json(), SCHEMA_USUARIO)


def test_post_individual_cumple_el_contrato(session: requests.Session) -> None:
    respuesta = session.get(f"{BASE_URL}/posts/1")
    assert respuesta.status_code == 200
    jsonschema.validate(respuesta.json(), SCHEMA_POST)


def test_usuario_inexistente_responde_404_con_cuerpo_vacio(session: requests.Session) -> None:
    # A diferencia de ReqRes (200 con "data": []) y de Restful Booker (404
    # con el mismo cuerpo que un id con forma inválida), JSONPlaceholder
    # devuelve un 404 cuyo cuerpo es un objeto JSON vacío de verdad ({}), no
    # un mensaje de error ni null. Un test que solo mirara el status code
    # no distinguiría esto de un 404 con detalle.
    respuesta = session.get(f"{BASE_URL}/users/9999")
    assert respuesta.status_code == 404
    assert respuesta.json() == {}


def test_post_creado_cumple_el_contrato_y_el_id_es_siempre_101(session: requests.Session) -> None:
    # JSONPlaceholder no persiste nada: simula la creación devolviendo un
    # "id" fijo (101, el siguiente a los 100 posts ya existentes) sin
    # importar qué se mande ni cuántas veces se llame. Dos POSTs con
    # payloads distintos confirman que el id no depende del contenido.
    primero = session.post(
        f"{BASE_URL}/posts",
        json={"title": "Post A", "body": "cuerpo A", "userId": 1},
    )
    segundo = session.post(
        f"{BASE_URL}/posts",
        json={"title": "Post B", "body": "cuerpo B", "userId": 5},
    )
    assert primero.status_code == 201
    assert segundo.status_code == 201

    jsonschema.validate(primero.json(), SCHEMA_POST)
    jsonschema.validate(segundo.json(), SCHEMA_POST)
    assert primero.json()["id"] == 101
    assert segundo.json()["id"] == 101


def test_el_esquema_de_usuario_rechaza_un_id_como_string() -> None:
    # Confirma que SCHEMA_USUARIO realmente exige "id" entero: un documento
    # idéntico a un usuario real pero con "id" como string tiene que fallar
    # la validación, para no confiar en un esquema que por error aceptara
    # cualquier tipo.
    usuario_con_id_invalido = {
        "id": "2",
        "name": "Ervin Howell",
        "username": "Antonette",
        "email": "Shanna@melissa.tv",
        "address": {
            "street": "Victor Plains",
            "suite": "Suite 879",
            "city": "Wisokyburgh",
            "zipcode": "90566-7771",
            "geo": {"lat": "-43.9509", "lng": "-34.4618"},
        },
        "phone": "010-692-6593 x09125",
        "website": "anastasia.net",
        "company": {
            "name": "Deckow-Crist",
            "catchPhrase": "Proactive didactic contingency",
            "bs": "synergize scalable supply-chains",
        },
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(usuario_con_id_invalido, SCHEMA_USUARIO)


def test_el_esquema_de_usuario_rechaza_un_email_invalido() -> None:
    usuario_con_email_invalido = {
        "id": 2,
        "name": "Ervin Howell",
        "username": "Antonette",
        "email": "esto-no-es-un-email",
        "address": {
            "street": "Victor Plains",
            "suite": "Suite 879",
            "city": "Wisokyburgh",
            "zipcode": "90566-7771",
            "geo": {"lat": "-43.9509", "lng": "-34.4618"},
        },
        "phone": "010-692-6593 x09125",
        "website": "anastasia.net",
        "company": {
            "name": "Deckow-Crist",
            "catchPhrase": "Proactive didactic contingency",
            "bs": "synergize scalable supply-chains",
        },
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(usuario_con_email_invalido, SCHEMA_USUARIO)

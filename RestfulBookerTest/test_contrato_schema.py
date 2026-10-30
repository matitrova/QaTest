import jsonschema
import pytest
import requests

from config import BASE_URL

SCHEMA_RESERVA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string", "minLength": 1},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string", "format": "date"},
                "checkout": {"type": "string", "format": "date"},
            },
        },
        # additionalneeds es el único campo que la API omite por completo de la
        # respuesta cuando no se lo envía, en vez de devolverlo vacío o nulo: no
        # va en "required".
        "additionalneeds": {"type": "string"},
    },
}

SCHEMA_RESERVA_CREADA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": SCHEMA_RESERVA,
    },
}

SCHEMA_ITEM_LISTA = {
    "type": "object",
    "required": ["bookingid"],
    "properties": {"bookingid": {"type": "integer"}},
}


def crear_reserva(totalprice, additionalneeds=None):
    reserva = {
        "firstname": "Schema",
        "lastname": "Contract",
        "totalprice": totalprice,
        "depositpaid": True,
        "bookingdates": {"checkin": "2031-01-01", "checkout": "2031-01-05"},
    }
    if additionalneeds is not None:
        reserva["additionalneeds"] = additionalneeds
    respuesta = requests.post(f"{BASE_URL}/booking", json=reserva)
    assert respuesta.status_code == 200
    return respuesta


def test_reserva_creada_cumple_el_contrato(reservas_creadas):
    respuesta = crear_reserva(totalprice=150, additionalneeds="Breakfast")
    jsonschema.validate(respuesta.json(), SCHEMA_RESERVA_CREADA)
    reservas_creadas.append(respuesta.json()["bookingid"])


def test_reserva_creada_sin_additionalneeds_tambien_cumple_el_contrato(reservas_creadas):
    # additionalneeds no es obligatorio en el booking enviado, y la respuesta
    # lo omite directamente en vez de devolverlo como "" o null. El esquema
    # tiene que validar igual sin que el campo esté presente.
    respuesta = crear_reserva(totalprice=150)
    assert "additionalneeds" not in respuesta.json()["booking"]
    jsonschema.validate(respuesta.json(), SCHEMA_RESERVA_CREADA)
    reservas_creadas.append(respuesta.json()["bookingid"])


def test_reserva_individual_cumple_el_contrato(reservas_creadas):
    respuesta_creacion = crear_reserva(totalprice=200)
    booking_id = respuesta_creacion.json()["bookingid"]
    reservas_creadas.append(booking_id)

    respuesta = requests.get(f"{BASE_URL}/booking/{booking_id}")
    assert respuesta.status_code == 200
    jsonschema.validate(respuesta.json(), SCHEMA_RESERVA)


def test_lista_de_reservas_cumple_el_contrato():
    respuesta = requests.get(f"{BASE_URL}/booking")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert len(datos) > 0
    for item in datos[:20]:
        jsonschema.validate(item, SCHEMA_ITEM_LISTA)


def test_totalprice_enviado_como_float_se_trunca_a_entero_no_se_redondea(reservas_creadas):
    # El esquema exige "integer" para totalprice, y la API lo cumple incluso
    # mandando un float: pero no redondeando, sino truncando hacia abajo.
    # 111.9 vuelve como 111, no como 112 ni como el 111.9 original. Un test
    # que solo chequeara el tipo del resultado (int) no detectaría que el
    # valor en sí se perdió.
    respuesta = crear_reserva(totalprice=111.9)
    datos = respuesta.json()
    jsonschema.validate(datos, SCHEMA_RESERVA_CREADA)
    assert datos["booking"]["totalprice"] == 111
    reservas_creadas.append(datos["bookingid"])


def test_el_esquema_de_reserva_rechaza_totalprice_como_string():
    # Confirma que SCHEMA_RESERVA realmente exige "totalprice" entero: un
    # documento idéntico a una reserva real pero con el precio como string
    # tiene que fallar la validación, para no confiar en un esquema que por
    # error aceptara cualquier tipo.
    reserva_con_precio_invalido = {
        "firstname": "Schema",
        "lastname": "Contract",
        "totalprice": "150",
        "depositpaid": True,
        "bookingdates": {"checkin": "2031-01-01", "checkout": "2031-01-05"},
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(reserva_con_precio_invalido, SCHEMA_RESERVA)


def test_el_esquema_de_reserva_rechaza_bookingdates_sin_checkout():
    reserva_sin_checkout = {
        "firstname": "Schema",
        "lastname": "Contract",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2031-01-01"},
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(reserva_sin_checkout, SCHEMA_RESERVA)

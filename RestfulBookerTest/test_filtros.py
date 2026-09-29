import uuid

import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def crear_reserva(firstname, lastname, checkin, checkout):
    respuesta = requests.post(
        f"{BASE_URL}/booking",
        json={
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": checkin, "checkout": checkout},
            "additionalneeds": "",
        },
    )
    assert respuesta.status_code == 200
    return respuesta.json()["bookingid"]


def eliminar_reserva(booking_id, token):
    requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={token}"},
    )


def ids_filtrados(**params):
    respuesta = requests.get(f"{BASE_URL}/booking", params=params)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert isinstance(datos, list)
    return {reserva["bookingid"] for reserva in datos}


def test_filtrar_por_firstname_trae_todas_las_reservas_con_ese_nombre(token):
    # Un mismo firstname con apellidos distintos: filtrar solo por firstname
    # tiene que traer las dos, no solo la primera que encuentre.
    nombre = f"Zzqatest{uuid.uuid4().hex[:8]}"
    id_uno = crear_reserva(nombre, "Uno", "2030-01-01", "2030-01-05")
    id_dos = crear_reserva(nombre, "Dos", "2030-02-01", "2030-02-05")

    try:
        encontrados = ids_filtrados(firstname=nombre)
        assert {id_uno, id_dos} <= encontrados
    finally:
        eliminar_reserva(id_uno, token)
        eliminar_reserva(id_dos, token)


def test_filtrar_por_firstname_y_lastname_juntos_acota_a_una_sola(token):
    nombre = f"Zzqatest{uuid.uuid4().hex[:8]}"
    id_uno = crear_reserva(nombre, "Uno", "2030-03-01", "2030-03-05")
    id_dos = crear_reserva(nombre, "Dos", "2030-04-01", "2030-04-05")

    try:
        encontrados = ids_filtrados(firstname=nombre, lastname="Dos")
        assert encontrados == {id_dos}
    finally:
        eliminar_reserva(id_uno, token)
        eliminar_reserva(id_dos, token)


def test_firstname_no_es_case_insensitive_ni_busca_por_substring(token):
    # El filtro exige coincidencia exacta, sensible a mayúsculas: ni una
    # variante en minúsculas ni un substring del nombre real encuentran la
    # reserva. Quien asuma un LIKE de SQL se lleva una sorpresa.
    nombre = f"Zzqatest{uuid.uuid4().hex[:8]}"
    id_reserva = crear_reserva(nombre, "Exacto", "2030-05-01", "2030-05-05")

    try:
        assert ids_filtrados(firstname=nombre.lower()) == set()
        assert ids_filtrados(firstname=nombre[:-3]) == set()
        assert id_reserva in ids_filtrados(firstname=nombre)
    finally:
        eliminar_reserva(id_reserva, token)


def test_filtrar_sin_coincidencias_devuelve_200_con_lista_vacia():
    # No es un 404: como con la paginación de ReqRes, "no hay resultados"
    # sigue siendo una respuesta exitosa con una lista vacía en el cuerpo.
    respuesta = requests.get(
        f"{BASE_URL}/booking", params={"firstname": "NombreQueNuncaExistio999"}
    )
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_filtrar_por_rango_de_fechas_incluye_solo_lo_que_cae_adentro(token):
    # checkin/checkout como filtro no buscan una fecha exacta: delimitan un
    # rango, y la reserva entra si sus fechas caen dentro de ese rango.
    nombre = f"Zzqatest{uuid.uuid4().hex[:8]}"
    id_reserva = crear_reserva(nombre, "Fechas", "2030-06-10", "2030-06-15")

    try:
        adentro = ids_filtrados(checkin="2030-06-01", checkout="2030-06-30")
        afuera = ids_filtrados(checkin="2031-01-01", checkout="2031-01-31")

        assert id_reserva in adentro
        assert id_reserva not in afuera
    finally:
        eliminar_reserva(id_reserva, token)

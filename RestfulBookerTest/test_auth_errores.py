import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def crear_reserva():
    respuesta = requests.post(
        f"{BASE_URL}/booking",
        json={
            "firstname": "ErrorTest",
            "lastname": "QA",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2030-07-01", "checkout": "2030-07-05"},
            "additionalneeds": "",
        },
    )
    assert respuesta.status_code == 200
    return respuesta.json()["bookingid"]


def test_auth_con_password_incorrecta_responde_200_sin_token():
    # Un 200 no significa éxito: con la contraseña mal, /auth sigue
    # respondiendo 200, y el único indicio del fallo está en el cuerpo
    # ("reason": "Bad credentials"), sin ningún "token". Un test que
    # solo mirara el status code daría este login por bueno.
    respuesta = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "contraseña-incorrecta"},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" not in datos
    assert datos["reason"] == "Bad credentials"


def test_auth_con_username_incorrecto_responde_200_sin_token():
    respuesta = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "usuario-que-no-existe", "password": "password123"},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" not in datos
    assert datos["reason"] == "Bad credentials"


def test_auth_sin_credenciales_responde_200_sin_token():
    # Ni siquiera un cuerpo vacío devuelve un 400: la API trata la
    # ausencia total de credenciales igual que una combinación
    # incorrecta, con la misma respuesta 200 + "reason".
    respuesta = requests.post(f"{BASE_URL}/auth", json={})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" not in datos
    assert datos["reason"] == "Bad credentials"


def test_put_sin_token_responde_403():
    booking_id = crear_reserva()
    respuesta = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json={
            "firstname": "Sin",
            "lastname": "Token",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {"checkin": "2030-08-01", "checkout": "2030-08-05"},
            "additionalneeds": "",
        },
    )
    assert respuesta.status_code == 403


def test_put_con_token_invalido_responde_403_igual_que_sin_token():
    # Mandar una cookie "token" con un valor cualquiera no es lo mismo
    # que no mandar ninguna: acá se confirma que la API de verdad valida
    # el contenido del token (no solo que la cookie exista), rechazando
    # un valor inventado con el mismo 403 que la ausencia total.
    booking_id = crear_reserva()
    respuesta = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json={
            "firstname": "Token",
            "lastname": "Invalido",
            "totalprice": 999,
            "depositpaid": False,
            "bookingdates": {"checkin": "2030-08-01", "checkout": "2030-08-05"},
            "additionalneeds": "",
        },
        headers={"Cookie": "token=esto-no-es-un-token-valido"},
    )
    assert respuesta.status_code == 403


def test_obtener_reserva_con_id_no_numerico_responde_404():
    # El id de una reserva es siempre numérico; pedir uno que ni
    # siquiera tiene esa forma no distingue el caso con un 400 propio,
    # cae en el mismo 404 genérico que un id numérico inexistente.
    respuesta = requests.get(f"{BASE_URL}/booking/no-es-un-id")
    assert respuesta.status_code == 404

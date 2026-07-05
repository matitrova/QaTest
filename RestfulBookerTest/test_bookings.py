import requests

def test_obtener_token():
    credenciales = {
        "username": "admin",
        "password": "password123"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json=credenciales
    )
    print(respuesta.json())

    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" in datos
    assert isinstance(datos["token"], str)
    assert len(datos["token"]) > 0

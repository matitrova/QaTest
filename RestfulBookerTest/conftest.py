import pytest
import requests

@pytest.fixture
def token():
    credenciales = {
        "username": "admin",
        "password": "password123"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json=credenciales
    )
    return respuesta.json()["token"]
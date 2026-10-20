import pytest
import requests

from config import BASE_URL

@pytest.fixture
def token():
    credenciales = {
        "username": "admin",
        "password": "password123"
    }
    respuesta = requests.post(
        f"{BASE_URL}/auth",
        json=credenciales
    )
    return respuesta.json()["token"]
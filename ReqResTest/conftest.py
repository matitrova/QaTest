import requests
import pytest
from config import BASE_URL

@pytest.fixture
def obtener_token(headers: dict[str, str]) -> str:
    credenciales = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    respuesta = requests.post(
        f"{BASE_URL}/api/login",
        json=credenciales,
        headers=headers
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" in datos
    return datos["token"]

@pytest.fixture
def headers() -> dict[str, str]:
    return {
        "x-api-key": "pub_6a1e68915ef0cc65140fe1734bff08cba5902de72982365452e30482f9ac7ac8"
    }
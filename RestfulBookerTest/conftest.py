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


@pytest.fixture
def reservas_creadas(token):
    # Varios tests de test_bookings.py creaban reservas con POST y nunca las
    # borraban: quedaban acumulandose para siempre en la API publica
    # compartida (a diferencia de test_filtros.py, que ya las borra con un
    # try/finally propio). Este fixture centraliza esa limpieza: el test
    # registra cada booking_id que crea y el fixture los borra al terminar,
    # se haya o no el test cumplido con exito.
    ids = []
    yield ids
    for booking_id in ids:
        requests.delete(
            f"{BASE_URL}/booking/{booking_id}",
            headers={"Cookie": f"token={token}"},
        )
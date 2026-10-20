import pytest
import requests

from config import BASE_URL

USUARIOS_REALES = [
    (1, "Leanne Graham", "Sincere@april.biz"),
    (2, "Ervin Howell", "Shanna@melissa.tv"),
    (3, "Clementine Bauch", "Nathan@yesenia.net"),
]


@pytest.mark.parametrize("user_id, nombre, email", USUARIOS_REALES)
def test_obtener_usuario(session: requests.Session, user_id: int, nombre: str, email: str) -> None:
    respuesta = session.get(f"{BASE_URL}/users/{user_id}")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert datos["name"] == nombre
    assert datos["email"] == email


@pytest.mark.parametrize("user_id", [9999, 0, -1])
def test_usuario_inexistente(session: requests.Session, user_id: int) -> None:
    respuesta = session.get(f"{BASE_URL}/users/{user_id}")
    assert respuesta.status_code == 404

import requests

from config import BASE_URL


def test_crear_post(session: requests.Session) -> None:
    nuevo_post = {
        "title": "Mi primer post",
        "body": "Estoy aprendiendo API testing",
        "userId": 1
    }
    respuesta = session.post(
        f"{BASE_URL}/posts",
        json=nuevo_post)
    assert respuesta.status_code == 201

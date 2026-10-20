import requests

from config import BASE_URL


def test_modificar_post(session: requests.Session) -> None:
    post_actualizado = {
        "title": "Título modificado",
        "body": "Contenido actualizado",
        "userId": 1
    }

    respuesta = session.put(
        f"{BASE_URL}/posts/1",
        json=post_actualizado)
    assert respuesta.status_code == 200

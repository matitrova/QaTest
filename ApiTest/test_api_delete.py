import requests

from config import BASE_URL


def test_eliminar_post(session: requests.Session) -> None:
    respuesta = session.delete(f"{BASE_URL}/posts/1")
    assert respuesta.status_code == 200

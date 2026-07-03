import requests

def test_crear_post():
    nuevo_post = {
        "title": "Mi primer post",
        "body": "Estoy aprendiendo API testing",
        "userId": 1
    }
    respuesta = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=nuevo_post)
    assert respuesta.status_code == 201
    
import requests

def test_eliminar_post(): 
    respuesta = requests.delete(
        "https://jsonplaceholder.typicode.com/posts/1")
    assert respuesta.status_code == 200

    
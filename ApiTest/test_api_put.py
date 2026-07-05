import requests

def test_modificar_post():
    post_actualizado = {
        "title": "Título modificado",
        "body": "Contenido actualizado",
        "userId": 1
    }
 
    respuesta = requests.put(
        "https://jsonplaceholder.typicode.com/posts/1",
        json=post_actualizado)
    assert respuesta.status_code == 200
    
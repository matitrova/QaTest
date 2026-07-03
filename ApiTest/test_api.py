import requests

def test_obtener_usuario():
    respuesta = requests.get("https://jsonplaceholder.typicode.com/users/1")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert datos["name"] == "Leanne Graham"
    assert datos["email"] == "Sincere@april.biz"

def test_usuario_inexistente():
    respuesta = requests.get("https://jsonplaceholder.typicode.com/users/9999")
    assert respuesta.status_code == 404
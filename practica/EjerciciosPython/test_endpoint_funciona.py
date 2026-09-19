import requests
import pytest
 
def test_obtener_usuario():
    respuesta = requests.get("https://jsonplaceholder.typicode.com/users/1")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert datos["name"] == "Leanne Graham"
    assert datos["email"] == "Sincere@april.biz"
    assert datos["username"] == "Bret"

def test_id_usuario():
    respuesta = requests.get("https://jsonplaceholder.typicode.com/users/1")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert isinstance(datos["id"], int)
    assert isinstance(datos["name"], str)
    assert isinstance(datos["email"], str)
    assert '@' in datos["email"]

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_obtener_usuario_parametrizado(user_id):
    respuesta = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert isinstance(datos["name"], str)

def test_usuario_inexistente():
    respuesta = requests.get("https://jsonplaceholder.typicode.com/users/9999")
    assert respuesta.status_code == 404

def test_lista_completa():
    respuesta = requests.get("https://jsonplaceholder.typicode.com/users")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert isinstance(datos, list)
    assert len(datos) == 10 
    assert len(set(user["id"] for user in datos)) == len(datos)  # Verifica que los IDs sean únicos
    

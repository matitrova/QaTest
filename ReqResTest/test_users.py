from typing import Any

import requests
import pytest
from config import BASE_URL

def test_obtener_token(headers: dict[str, str]) -> None:
    credenciales = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    respuesta = requests.post(
        f"{BASE_URL}/api/login",
        json=credenciales,
        headers=headers
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" in datos
    print(f"Token recibido: {datos['token']}")

def test_usar_token(obtener_token: Any) -> None:
    assert isinstance(obtener_token, str)
    assert len(obtener_token) > 0
    print(f"Token recibido: {obtener_token}")

@pytest.mark.parametrize(
    "credenciales",
    [
        {"password": "cityslicka"},
        {"email": "eve.holt@reqres.in"},
    ],
    ids=["sin_email", "sin_password"],
)
def test_login_con_campo_faltante_devuelve_400(
    credenciales: dict[str, str], headers: dict[str, str]
) -> None:
    respuesta = requests.post(
        f"{BASE_URL}/api/login",
        json=credenciales,
        headers=headers
    )
    assert respuesta.status_code == 400
    assert "error" in respuesta.json()

def test_registro_exitoso(headers: dict[str, str]) -> None:
    nuevo_usuario = {
        "email": "charles.morris@reqres.in",
        "password": "pistol"
    }
    respuesta = requests.post(
        f"{BASE_URL}/api/register",
        json=nuevo_usuario,
        headers=headers
    )
    assert respuesta.status_code == 200

@pytest.mark.parametrize(
    "nuevo_usuario",
    [
        {"password": "pistol"},
        {"email": "charles.morris@reqres.in"},
    ],
    ids=["sin_email", "sin_password"],
)
def test_registro_con_campo_faltante_devuelve_400(
    nuevo_usuario: dict[str, str], headers: dict[str, str]
) -> None:
    respuesta = requests.post(
        f"{BASE_URL}/api/register",
        json=nuevo_usuario,
        headers=headers
    )
    assert respuesta.status_code == 400
    assert "error" in respuesta.json()

def test_obtener_lista_usuarios(headers: dict[str, str]) -> None:
    respuesta = requests.get(f"{BASE_URL}/api/users?page=2", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "data" in datos
    assert isinstance(datos["data"], list)
    assert len(datos["data"]) > 0


def test_usuario_especifico(headers: dict[str, str]) -> None:
    user_id = 2
    respuesta = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "data" in datos
    assert isinstance(datos["data"], dict)
    assert datos["data"]["id"] == user_id

def test_usuario_no_encontrado(headers: dict[str, str]) -> None:
    user_id = 23
    respuesta = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    assert respuesta.status_code == 404

def test_crear_usuario(headers: dict[str, str]) -> None:
    nuevo_usuario = {
        "name": "morpheus",
        "job": "leader"
    }    
    respuesta = requests.post(f"{BASE_URL}/api/users", json=nuevo_usuario, headers=headers)
    assert respuesta.status_code == 201 

def test_usuario_sin_nombre(headers: dict[str, str]) -> None:
    nuevo_usuario = {
        "job": "leader"
    }
    respuesta = requests.post(f"{BASE_URL}/api/users", json=nuevo_usuario, headers=headers)
    assert respuesta.status_code == 201

def test_put_exitoso(headers: dict[str, str]) -> None:
    user_id = 2
    respuesta = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "data" in datos
    assert isinstance(datos["data"], dict)
    assert datos["data"]["id"] == user_id

    # ReqRes es una API simulada: responde como si guardara el cambio, pero no lo
    # persiste. Si despues se vuelve a pedir el usuario, llega el original, sin
    # "name". Por eso el resultado se valida en la respuesta del PUT mismo, que es
    # lo unico que esta API promete.
    usuario_modificado = {
        "name": "morpheus",
        "job": "zion resident"
    }
    respuesta = requests.put(f"{BASE_URL}/api/users/{user_id}", json=usuario_modificado, headers=headers)
    assert respuesta.status_code == 200

    datos_nuevos = respuesta.json()
    assert datos_nuevos["name"] == "morpheus"
    assert datos_nuevos["job"] == "zion resident"
    assert "updatedAt" in datos_nuevos

def test_patch_trabajo(headers: dict[str, str]) -> None:
    user_id = 2
    respuesta = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "data" in datos
    assert isinstance(datos["data"], dict)
    assert datos["data"]["id"] == user_id

    # Mismo caso que el PUT: ReqRes no persiste, asi que se valida la respuesta
    # del PATCH y no un GET posterior.
    patch_data = {
        "job": "zion resident"
    }
    respuesta = requests.patch(f"{BASE_URL}/api/users/{user_id}", json=patch_data, headers=headers)
    assert respuesta.status_code == 200

    datos_nuevos = respuesta.json()
    assert datos_nuevos["job"] == "zion resident"
    assert "updatedAt" in datos_nuevos

def test_eliminar_usuario(headers: dict[str, str]) -> None:
    user_id = 2
    respuesta = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "data" in datos
    assert isinstance(datos["data"], dict)
    assert datos["data"]["id"] == user_id

    # ReqRes responde 204 al DELETE pero no borra nada: un GET posterior sigue
    # devolviendo 200. Esperar un 404 ahi seria validar algo que esta API nunca
    # promete. Lo que si garantiza es el 204 sin cuerpo.
    respuesta = requests.delete(f"{BASE_URL}/api/users/{user_id}", headers=headers)
    assert respuesta.status_code == 204
    assert respuesta.text == ""

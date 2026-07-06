import requests
import pytest

def test_obtener_token():
    credenciales = {
        "username": "admin",
        "password": "password123"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/auth",
        json=credenciales
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "token" in datos
    assert isinstance(datos["token"], str)
    assert len(datos["token"]) > 0

def test_usar_token(token):
    assert isinstance(token, str)
    assert len(token) > 0
    print(f"Token recibido: {token}")

def test_obtener_reservas(token):
    respuesta = requests.get(
        "https://restful-booker.herokuapp.com/booking")
    datos = respuesta.json()
    assert respuesta.status_code == 200
    assert isinstance(datos, list)

def test_crear_reserva(token):
    nueva_reserva = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-10"
        },
        "additionalneeds": "Breakfast"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json=nueva_reserva
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "bookingid" in datos
    assert isinstance(datos["bookingid"], int)
    booking_id = datos["bookingid"]
    
    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    datos = respuesta.json()    
    assert respuesta.status_code == 200


def test_modificar_reserva(token):
    nueva_reserva = {
        "firstname": "Jane",
        "lastname": "Smith",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2024-02-01",
            "checkout": "2024-02-10"
        },
        "additionalneeds": "Lunch"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json=nueva_reserva
    )
    booking_id = respuesta.json()["bookingid"]
    
    reserva_modificada = {
        "firstname": "Jane",
        "lastname": "Doe",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-02-05",
            "checkout": "2024-02-15"
        },
        "additionalneeds": "Dinner"
    }
    respuesta = requests.put(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=reserva_modificada,
        headers={"Cookie": f"token={token}"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["lastname"] == "Doe"
    assert datos["totalprice"] == 250

    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    datos = respuesta.json()
    assert datos["lastname"] == "Doe"
    assert datos["totalprice"] == 250

def test_flujo_completo(token):
    nueva_reserva = {
        "firstname": "Alice",
        "lastname": "Johnson",
        "totalprice": 300,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-03-01",
            "checkout": "2024-03-10"
        },
        "additionalneeds": "Breakfast"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json=nueva_reserva
    )
    assert respuesta.status_code == 200
    booking_id = respuesta.json()["bookingid"]
    
    reserva_modificada = {
        "firstname": "Alice",
        "lastname": "Williams",
        "totalprice": 350,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2024-03-05",
            "checkout": "2024-03-15"
        },
        "additionalneeds": "Lunch"
    }
    respuesta = requests.put(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=reserva_modificada,
        headers={"Cookie": f"token={token}"}
    )
    assert respuesta.status_code == 200
    
    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    datos = respuesta.json()
    assert datos["lastname"] == "Williams"
    assert datos["totalprice"] == 350

    respuesta = requests.delete(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        headers={"Cookie": f"token={token}"}
    )
    assert respuesta.status_code == 201
    
    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert respuesta.status_code == 404

def test_patch_reserva(token):
    nueva_reserva = {
        "firstname": "Bob",
        "lastname": "Brown",
        "totalprice": 400,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-01",
            "checkout": "2024-04-10"
        },
        "additionalneeds": "Breakfast"
    }
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json=nueva_reserva
    )
    booking_id = respuesta.json()["bookingid"]
    
    patch_data = {
        "totalprice": 450,
        "additionalneeds": "Dinner"
    }
    respuesta = requests.patch(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=patch_data,
        headers={"Cookie": f"token={token}"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["totalprice"] == 450
    assert datos["additionalneeds"] == "Dinner"

    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    datos = respuesta.json()
    assert datos["totalprice"] == 450
    assert datos["additionalneeds"] == "Dinner"

    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["totalprice"] == 450
  
def test_reserva_patch(token):
    respuesta = requests.post(
        "https://restful-booker.herokuapp.com/booking",
        json={
            "firstname": "Charlie",
            "lastname": "Davis",
            "totalprice": 500,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-05-01",
                "checkout": "2024-05-10"
            },
            "additionalneeds": "Breakfast"
        }
    )
    booking_id = respuesta.json()["bookingid"]
    assert respuesta.status_code == 200

    patch_data = {
        "firstname": "Charli3",
        "lastname": "Evans",
        "totalprice": -100,
    }

    respuesta = requests.patch(
        f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=patch_data,
        
    )
    assert respuesta.status_code == 403

def test_booking_inexists(token):
    respuesta = requests.get(
        f"https://restful-booker.herokuapp.com/booking/999999")
    assert respuesta.status_code == 404

def test_delete_booking_exists_sin_token():
    respuesta = requests.delete(
        f"https://restful-booker.herokuapp.com/booking/1",

    )
    assert respuesta.status_code == 403
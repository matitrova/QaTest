import math

import requests
from config import BASE_URL


def test_pagina_1_trae_los_primeros_seis(headers):
    respuesta = requests.get(f"{BASE_URL}/api/users?page=1", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()

    assert datos["page"] == 1
    assert datos["per_page"] == 6
    assert datos["total"] == 12
    assert datos["total_pages"] == 2
    assert [usuario["id"] for usuario in datos["data"]] == [1, 2, 3, 4, 5, 6]


def test_pagina_2_no_repite_usuarios_de_la_1(headers):
    ids_pagina_1 = requests.get(f"{BASE_URL}/api/users?page=1", headers=headers).json()
    ids_pagina_1 = {usuario["id"] for usuario in ids_pagina_1["data"]}

    respuesta = requests.get(f"{BASE_URL}/api/users?page=2", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    ids_pagina_2 = {usuario["id"] for usuario in datos["data"]}

    assert datos["page"] == 2
    # Las dos páginas cubren el total entre las dos, sin superponerse.
    assert ids_pagina_1.isdisjoint(ids_pagina_2)
    assert ids_pagina_1 | ids_pagina_2 == set(range(1, datos["total"] + 1))


def test_sin_parametro_page_devuelve_la_primera_pagina(headers):
    # El endpoint no exige "page": sin él, se comporta igual que page=1.
    respuesta = requests.get(f"{BASE_URL}/api/users", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()

    assert datos["page"] == 1
    assert [usuario["id"] for usuario in datos["data"]] == [1, 2, 3, 4, 5, 6]


def test_per_page_cambia_el_tamano_y_recalcula_total_pages(headers):
    respuesta = requests.get(f"{BASE_URL}/api/users?per_page=3", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()

    assert datos["per_page"] == 3
    assert len(datos["data"]) == 3
    # total_pages depende de per_page, no es un valor fijo: con 12
    # usuarios y 3 por página son 4 páginas, no las 2 de siempre.
    assert datos["total_pages"] == math.ceil(datos["total"] / datos["per_page"])


def test_pagina_fuera_de_rango_devuelve_200_con_lista_vacia(headers):
    # No es un 404: ReqRes responde 200 igual, con el número de página
    # que se pidió reflejado en el cuerpo aunque no exista, y "data"
    # vacío en vez de un error. Un test que solo mirara el status code
    # daría esto por una página más, cuando en realidad no hay datos.
    respuesta = requests.get(f"{BASE_URL}/api/users?page=999", headers=headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()

    assert datos["page"] == 999
    assert datos["total_pages"] == 2
    assert datos["data"] == []

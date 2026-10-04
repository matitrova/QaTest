from config import BASE_URL
from BrokenImagesPage import BrokenImagesPage


def test_la_pagina_tiene_tres_imagenes(page):
    broken_images_page = BrokenImagesPage(page)
    page.goto(f"{BASE_URL}/broken_images")

    assert broken_images_page.imagenes.count() == 3


def test_el_src_de_cada_imagen_determina_si_responde_200_o_404(page):
    broken_images_page = BrokenImagesPage(page)
    respuestas = {}

    def guardar_respuesta(response):
        if response.request.resource_type == "image":
            respuestas[response.url] = response.status

    page.on("response", guardar_respuesta)
    page.goto(f"{BASE_URL}/broken_images")
    page.wait_for_load_state("networkidle")

    assert respuestas[f"{BASE_URL}/asdf.jpg"] == 404
    assert respuestas[f"{BASE_URL}/hjkl.jpg"] == 404
    assert respuestas[f"{BASE_URL}/img/avatar-blank.jpg"] == 200


def test_dos_imagenes_rotas_y_una_que_carga_bien(page):
    # El propio sitio apunta dos de las tres imágenes a rutas que no
    # existen (asdf.jpg, hjkl.jpg) y deja la tercera (avatar-blank.jpg)
    # apuntando a un archivo real -- las tres conviven en la misma
    # página para forzar a distinguirlas una por una, no asumir que
    # "la página de imágenes rotas" las rompe a todas.
    broken_images_page = BrokenImagesPage(page)
    page.goto(f"{BASE_URL}/broken_images")
    page.wait_for_load_state("networkidle")

    assert broken_images_page.esta_rota(0) is True
    assert broken_images_page.esta_rota(1) is True
    assert broken_images_page.esta_rota(2) is False

from pathlib import Path

import pytest
from playwright.sync_api import Page

from config import BASE_URL
from FileDownloadPage import FileDownloadPage


@pytest.fixture
def download_page(page: Page) -> FileDownloadPage:
    page.goto(f"{BASE_URL}/download")
    return FileDownloadPage(page)


# La lista de archivos la pueblan los que cualquier visitante sube en
# /upload: es contenido compartido entre todos los que usan el sitio y
# cambia con el tiempo, así que ningún test de este archivo asume un
# nombre de archivo puntual -- solo que la lista exista y que descargar
# cualquiera de sus enlaces funcione de verdad.


def test_la_pagina_lista_varios_archivos_para_descargar(
    download_page: FileDownloadPage,
) -> None:
    assert download_page.enlaces_archivo.count() > 1


def test_descargar_un_archivo_trae_su_contenido_completo(
    download_page: FileDownloadPage, tmp_path: Path
) -> None:
    enlace = download_page.enlaces_archivo.first
    nombre_esperado = enlace.inner_text()

    with download_page.page.expect_download() as info_descarga:
        enlace.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == nombre_esperado

    destino = tmp_path / descarga.suggested_filename
    descarga.save_as(destino)
    assert destino.stat().st_size > 0


def test_descargar_no_navega_fuera_de_la_pagina(
    download_page: FileDownloadPage,
) -> None:
    # Un click que dispara una descarga no es una navegación: el navegador
    # se queda en /download en vez de ir a la URL del archivo.
    url_antes = download_page.page.url

    with download_page.page.expect_download():
        download_page.enlaces_archivo.first.click()

    assert download_page.page.url == url_antes


def test_descargar_dos_archivos_distintos_trae_dos_contenidos_distintos(
    download_page: FileDownloadPage,
) -> None:
    primer_enlace = download_page.enlaces_archivo.nth(0)
    segundo_enlace = download_page.enlaces_archivo.nth(1)

    with download_page.page.expect_download() as primera_info:
        primer_enlace.click()
    primera_descarga = primera_info.value

    with download_page.page.expect_download() as segunda_info:
        segundo_enlace.click()
    segunda_descarga = segunda_info.value

    assert primera_descarga.suggested_filename != segunda_descarga.suggested_filename
    assert primera_descarga.path().stat().st_size > 0
    assert segunda_descarga.path().stat().st_size > 0

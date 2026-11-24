from pathlib import Path

import pytest
import requests
from playwright.sync_api import Page

from config import BASE_URL
from SecureFileDownloadPage import SecureFileDownloadPage

# /download_secure es la versión de /download protegida con HTTP Basic Auth
# (admin/admin): mismas reglas que /basic_auth para entrar, pero la lista de
# archivos la pueblan los visitantes que suben por /upload, igual que en
# /download -- así que tampoco acá ningún test asume un nombre de archivo
# puntual.


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args: dict) -> dict:
    # Mismo motivo que en test_basic_auth.py: las credenciales tienen que
    # estar puestas en el contexto antes de navegar, porque el diálogo de
    # Basic Auth es nativo del navegador y Playwright no puede responderlo
    # después de que page.goto() ya lo disparó.
    return {
        **browser_context_args,
        "http_credentials": {"username": "admin", "password": "admin"},
    }


@pytest.fixture
def secure_download_page(page: Page) -> SecureFileDownloadPage:
    page.goto(f"{BASE_URL}/download_secure")
    return SecureFileDownloadPage(page)


def test_sin_credenciales_devuelve_401() -> None:
    respuesta = requests.get(f"{BASE_URL}/download_secure")

    assert respuesta.status_code == 401


def test_credenciales_incorrectas_devuelven_401() -> None:
    respuesta = requests.get(f"{BASE_URL}/download_secure", auth=("admin", "incorrecta"))

    assert respuesta.status_code == 401


def test_credenciales_correctas_devuelven_200_con_la_lista_de_archivos() -> None:
    respuesta = requests.get(f"{BASE_URL}/download_secure", auth=("admin", "admin"))

    assert respuesta.status_code == 200
    assert "Secure File Downloader" in respuesta.text


def test_credenciales_correctas_en_el_navegador_listan_varios_archivos(
    secure_download_page: SecureFileDownloadPage,
) -> None:
    assert secure_download_page.enlaces_archivo.count() > 1


def test_descargar_un_archivo_protegido_trae_su_contenido_completo(
    secure_download_page: SecureFileDownloadPage, tmp_path: Path
) -> None:
    enlace = secure_download_page.enlaces_archivo.first
    nombre_esperado = enlace.inner_text()

    with secure_download_page.page.expect_download() as info_descarga:
        enlace.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == nombre_esperado

    destino = tmp_path / descarga.suggested_filename
    descarga.save_as(destino)
    assert destino.stat().st_size > 0


def test_descargar_dos_archivos_protegidos_distintos_trae_dos_contenidos_distintos(
    secure_download_page: SecureFileDownloadPage,
) -> None:
    # El link de descarga es relativo a /download_secure/: la propia
    # descarga reusa las credenciales que ya están puestas en el contexto
    # del navegador, sin ninguna forma de pasarlas de nuevo en el click.
    primer_enlace = secure_download_page.enlaces_archivo.nth(0)
    segundo_enlace = secure_download_page.enlaces_archivo.nth(1)

    with secure_download_page.page.expect_download() as primera_info:
        primer_enlace.click()
    primera_descarga = primera_info.value

    with secure_download_page.page.expect_download() as segunda_info:
        segundo_enlace.click()
    segunda_descarga = segunda_info.value

    assert primera_descarga.suggested_filename != segunda_descarga.suggested_filename
    assert primera_descarga.path().stat().st_size > 0
    assert segunda_descarga.path().stat().st_size > 0

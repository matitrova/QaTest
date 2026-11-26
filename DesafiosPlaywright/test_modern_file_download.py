from pathlib import Path

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from config import BASE_URL
from ModernFileDownloadPage import ModernFileDownloadPage

# /download_modern no tiene links a archivos estáticos como /download y
# /download_secure: cada descarga la arma el propio navegador (Blob, fetch,
# data URL) o depende de cómo el servidor manda el header
# Content-Disposition, así que a diferencia de esas dos suites, acá sí vale
# la pena fijar nombres y contenidos puntuales -- son el objeto del test.


@pytest.fixture
def modern_download_page(page: Page) -> ModernFileDownloadPage:
    page.goto(f"{BASE_URL}/download_modern")
    return ModernFileDownloadPage(page)


def test_arranca_sin_ninguna_descarga_hecha(
    modern_download_page: ModernFileDownloadPage,
) -> None:
    assert modern_download_page.estado.inner_text() == "Nothing downloaded yet"


def test_blob_download_guarda_el_csv_armado_en_el_navegador(
    modern_download_page: ModernFileDownloadPage, tmp_path: Path
) -> None:
    # El botón no pide nada al servidor: arma un Blob con JavaScript, lo
    # vuelca a una URL blob: y clickea un <a download> creado al vuelo.
    with modern_download_page.page.expect_download() as info_descarga:
        modern_download_page.boton_blob.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "report.csv"
    assert descarga.url.startswith("blob:")

    destino = tmp_path / descarga.suggested_filename
    descarga.save_as(destino)
    assert destino.read_text() == "name,count\napple,3\nbanana,5\n"
    assert "Saved report.csv" in modern_download_page.estado.inner_text()


def test_fetch_download_usa_el_nombre_del_content_disposition_de_la_respuesta(
    modern_download_page: ModernFileDownloadPage, tmp_path: Path
) -> None:
    # Este botón sí pide algo al servidor (fetch a /download_modern/file/
    # report.json), pero la descarga en sí vuelve a ser un Blob local: el
    # nombre con el que se guarda no sale de la URL pedida sino de parsear
    # a mano el header Content-Disposition de la respuesta, en el propio
    # JavaScript de la página.
    with modern_download_page.page.expect_download() as info_descarga:
        modern_download_page.boton_fetch.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "report.json"
    assert descarga.url.startswith("blob:")

    destino = tmp_path / descarga.suggested_filename
    descarga.save_as(destino)
    assert destino.read_text().strip().startswith("{")


def test_data_url_download_no_pide_nada_al_servidor(
    modern_download_page: ModernFileDownloadPage, tmp_path: Path
) -> None:
    # Este link ni siquiera usa JavaScript: es un <a> común con un href
    # data: y un atributo download fijo en el HTML. El archivo entero viaja
    # codificado en la propia URL, así que el contenido ya se sabe de
    # antemano sin tener que leerlo después de descargarlo.
    with modern_download_page.page.expect_download() as info_descarga:
        modern_download_page.enlace_data_url.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "hello.txt"

    destino = tmp_path / descarga.suggested_filename
    descarga.save_as(destino)
    assert destino.read_text() == "Hello from a data URL\n"


def test_content_disposition_inline_abre_el_archivo_en_vez_de_descargarlo(
    modern_download_page: ModernFileDownloadPage,
) -> None:
    # Mismo servidor, mismo tipo de link, pero el header que manda esta
    # URL puntual dice "inline" en vez de "attachment": el navegador la
    # trata como una navegación común y no dispara ningún evento de
    # descarga -- por eso la página sí cambia de URL, a diferencia de
    # cualquier otro link de esta suite.
    with pytest.raises(PlaywrightTimeoutError):
        with modern_download_page.page.expect_download(timeout=2000):
            modern_download_page.enlace_inline.click()

    assert modern_download_page.page.url == f"{BASE_URL}/download_modern/file/inline"
    assert "opens in the browser" in modern_download_page.page.locator("body").inner_text()


def test_content_disposition_con_filename_estrella_usa_el_nombre_utf8_no_el_ascii(
    modern_download_page: ModernFileDownloadPage,
) -> None:
    # El servidor manda las dos variantes a la vez: filename="resume.txt"
    # (ASCII, para navegadores viejos) y filename*=UTF-8''r%C3%A9sum%C3%A9.txt
    # (RFC 5987/6266, con los acentos). Chromium prioriza la segunda.
    with modern_download_page.page.expect_download() as info_descarga:
        modern_download_page.enlace_utf8.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "résumé.txt"


def test_content_disposition_con_espacios_en_el_nombre_los_conserva(
    modern_download_page: ModernFileDownloadPage,
) -> None:
    with modern_download_page.page.expect_download() as info_descarga:
        modern_download_page.enlace_spaces.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "my report 2026.txt"


def test_content_disposition_sin_nombre_el_navegador_inventa_uno_de_la_url(
    modern_download_page: ModernFileDownloadPage,
) -> None:
    # El header de esta URL es apenas "attachment", sin filename. Sin nada
    # que leer ahí, Chromium no se queda sin nombre: lo arma a partir del
    # último segmento de la URL ("no_name") más la extensión que le suma
    # mirando el Content-Type de la respuesta (text/plain -> .txt).
    with modern_download_page.page.expect_download() as info_descarga:
        modern_download_page.enlace_no_name.click()
    descarga = info_descarga.value

    assert descarga.suggested_filename == "no_name.txt"

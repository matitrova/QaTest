from pathlib import Path

from config import BASE_URL
from UploadPage import UploadPage

ARCHIVO_DE_PRUEBA = Path(__file__).parent / "archivo_prueba.txt"


def test_subir_archivo(page):
    upload_page = UploadPage(page)
    page.goto(f"{BASE_URL}/upload")

    upload_page.subir_archivo(str(ARCHIVO_DE_PRUEBA))

    assert upload_page.uploaded_files.inner_text() == ARCHIVO_DE_PRUEBA.name

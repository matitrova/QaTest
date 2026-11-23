"""Reexporta la clase base compartida en shared/base_page.py.

Esta suite corre con su propia carpeta en `sys.path` (ver
.github/workflows/tests.yml), así que no puede hacer simplemente
`from shared.base_page import BasePage` sin arriesgar colisiones de nombres
con las otras suites. Se carga el archivo por ruta absoluta con
`importlib`, que no depende de `sys.path` ni del directorio desde el que se
invoque pytest.
"""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "_shared_base_page",
    Path(__file__).resolve().parent.parent / "shared" / "base_page.py",
)
_shared_base_page = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_shared_base_page)

BasePage = _shared_base_page.BasePage

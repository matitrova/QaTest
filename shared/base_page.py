"""Clase base compartida por los Page Objects de las suites de UI.

Antes `DesafiosPlaywright`, `UiTestingPlaygroundTest` y `TestX` tenían cada
una su propia copia idéntica de esta misma clase de tres líneas. Cada suite
sigue teniendo su propio `base_page.py` (lo necesitan: cada una corre con su
propia carpeta en `sys.path` y no son un paquete común), pero ese archivo
ahora reexporta esta única implementación en vez de repetirla.
"""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

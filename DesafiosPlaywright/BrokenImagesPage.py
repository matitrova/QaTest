class BrokenImagesPage:
    def __init__(self, page):
        self.page = page
        self.imagenes = page.locator(".example img")

    def esta_rota(self, indice):
        # `complete` da True en los tres <img> apenas el navegador termina
        # de intentar cargarlos, se hayan roto o no -- no sirve para
        # distinguir una imagen rota de una que cargó bien. naturalWidth/
        # naturalHeight sí: quedan en 0 cuando la respuesta no trajo una
        # imagen válida (404, acá), y reflejan el tamaño real del archivo
        # en cualquier otro caso.
        imagen = self.imagenes.nth(indice)
        ancho = imagen.evaluate("img => img.naturalWidth")
        alto = imagen.evaluate("img => img.naturalHeight")
        return ancho == 0 and alto == 0

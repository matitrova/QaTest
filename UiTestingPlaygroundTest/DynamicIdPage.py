import re

ID_DINAMICO = re.compile(r"^[0-9a-f-]{36}$")


class DynamicIdPage:
    def __init__(self, page):
        self.page = page
        # Por nombre y rol, no por id: es justamente lo que esta página pide
        # verificar ("make sure that ID is not used for button identification").
        self.boton = page.get_by_role("button", name="Button with Dynamic ID")

    def id_actual(self):
        return self.boton.get_attribute("id")

    def existe_un_elemento_con_id(self, id_buscado):
        # No sirve interpolar el id en un selector `#id`: al ser un UUID,
        # suele empezar con un dígito, y un selector CSS de id no puede
        # arrancar con un dígito sin escaparlo -- `#3b35...` tira
        # directamente un SyntaxError en vez de simplemente no encontrar
        # nada. El selector de atributo (`[id="..."]`) no tiene esa
        # restricción.
        return self.page.locator(f'[id="{id_buscado}"]').count() > 0

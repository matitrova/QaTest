abonado1 = {"nombre": "Juan", "dni": "12345678", "estado": "Activo"}
abonado2 = {"nombre": "Maria", "dni": "123", "estado": "baja"}

def validar_abonado_dni(abonado):
    if len(abonado["dni"]) == 8 and abonado["dni"].isdigit():
        return True
    return False
def validar_abonado_estado(abonado):
    if abonado["estado"] == "Activo":
        return "El abonado tiene acceso."
    elif abonado["estado"] == "suspendido":
        return "El abonado no tiene acceso."
    else:
        return "El estado del abonado es desconocido."
    
def verificar_abonado(abonado):
    if validar_abonado_dni(abonado):
        return validar_abonado_estado(abonado)
    return "El DNI del abonado es inválido."


print (verificar_abonado(abonado1))
print (verificar_abonado(abonado2))
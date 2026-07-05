abonados = [
    {"nombre": "Juan", "dni": "12345678", "estado": "Activo"},
    {"nombre": "Maria", "dni": "123", "estado": "Activo"},
    {"nombre": "Pedro", "dni": "87654321", "estado": "Suspendido"},
    {"nombre": "Ana", "dni": "11111111", "estado": "Activo"}
] 

for abonado in abonados: 
    if len(abonado["dni"]) == 8 and abonado["dni"].isdigit():
        if abonado["estado"] == "Activo":
            print(f'El abonado {abonado["nombre"]} tiene acceso.')
        elif abonado["estado"] == "Suspendido":
            print(f'El abonado {abonado["nombre"]} no tiene acceso.')
        else:
            print(f'El estado del abonado {abonado["nombre"]} es desconocido.')
    else:
        print(f'El DNI del abonado {abonado["nombre"]} es inválido.')
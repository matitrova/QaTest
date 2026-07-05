abonado = {
    "nombre": "Juan",
    "apellido": "Gomez",
    "dni": "12345678",
    "estado": "Activo"
}

print (f'El abonado: {abonado["nombre"]}' )
       
print (f'tiene estado: {abonado["estado"]}')

if abonado["estado"] == "Activo":
    print("El abonado tiene acceso.")
elif abonado["estado"] == "suspendido":
    print("El abonado no tiene acceso.")
else:
    print("El estado del abonado es desconocido.")
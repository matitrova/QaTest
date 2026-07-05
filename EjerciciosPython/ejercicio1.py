abonado_estado = "baja"  # Cambia este valor a "Activo", "suspendido" o cualquier otro estado para probar diferentes escenarios

if abonado_estado == "Activo":
    print("El abonado tiene acceso.")
elif abonado_estado == "suspendido":
    print("El abonado no tiene acceso.") 
else :
    print("El estado del abonado es desconocido.")    
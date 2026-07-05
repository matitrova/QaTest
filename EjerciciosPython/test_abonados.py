from ejercicio6 import SistemaAbonados

def test_abonados_validos ():
    abonados = [
        {"nombre": "Juan", "dni": "12345678", "estado": "Activo"},
        {"nombre": "Maria", "dni": "87654321", "estado": "Activo"},
        {"nombre": "Pedro", "dni": "11111111", "estado": "Suspendido"}
    ]
    sistema = SistemaAbonados(abonados)
    sistema.verificar_todos()
    assert sistema.validar_dni(abonados[0]) == True
def validar_dni(dni):
    if len(dni) == 8 and dni.isdigit():
        return True
    return False

print(validar_dni("12345678"))
print(validar_dni("123"))
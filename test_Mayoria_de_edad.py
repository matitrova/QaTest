import pytest 

def es_mayor_de_edad(edad):
    if edad >= 18:
        return True
    else:
        return False
    
@pytest.mark.parametrize("edad, esperado", [
    (18, True),
    (17, False),
    (20, True),
    (15, False),
]) 
def test_es_mayor_de_edad(edad, esperado):
    assert es_mayor_de_edad(edad) == esperado
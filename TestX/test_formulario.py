import pytest

def puede_enviar_formulario(nombre_completo: str, email_valido: bool, acepta_terminos: bool) -> bool:
    if nombre_completo and email_valido and acepta_terminos:
        return True
    else:
        return False

@pytest.mark.parametrize("nombre_completo, email_valido, acepta_terminos, esperado", [
    ("Juan Pérez", True, True, True),
    ("", True, True, False),
    ("Ana Gómez", False, True, False),
    ("Carlos López", True, False, False),
])
def test_puede_enviar_formulario(
    nombre_completo: str, email_valido: bool, acepta_terminos: bool, esperado: bool
) -> None:
    assert puede_enviar_formulario(nombre_completo, email_valido, acepta_terminos) == esperado
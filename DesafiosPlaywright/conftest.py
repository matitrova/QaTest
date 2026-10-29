import pytest


@pytest.fixture(autouse=True)
def bloquear_analitica_externa(page):
    # El layout de the-internet.herokuapp.com carga un script de Optimizely
    # (dominio externo, ajeno a lo que se está probando). Si esa red está
    # lenta o inaccesible, el evento "load" puede colgarse esperándolo y
    # la navegación se vuelve flaky -- se aborta ese pedido explícitamente
    # para que cada test de la suite dependa solo del sitio bajo prueba.
    # Antes esta misma fixture estaba copiada y pegada en 15 archivos.
    page.route("**/*.optimizely.com/**", lambda route: route.abort())
    yield

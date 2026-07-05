# QaTest — Portfolio de QA Automation

Proyecto de automatización de pruebas desarrollado con Python, Playwright y Pytest.
Cubre testing de UI (interfaz web) y testing de API REST.

## Tecnologías

- **Python 3.12+**
- **Playwright** — automatización de navegador
- **Pytest** — framework de testing
- **Requests** — testing de APIs REST

## Estructura del proyecto
QaTest/
├── IspbossTest/        # Tests E2E sobre ISPBoss (sistema real de gestión de ISPs)
├── ApiTest/            # Tests de API REST (CRUD completo)
├── EjerciciosPython/   # Ejercicios progresivos de Python aplicados a QA
├── LoginPage.py        # Page Object — login SauceDemo
├── Inventory_Page.py   # Page Object — inventario SauceDemo
└── test_*.py           # Tests de SauceDemo

## Proyectos

### ISPBoss — Alta de Abonado (E2E)
Automatización del flujo completo de alta de un abonado en un sistema real de gestión de ISPs (ASP.NET WebForms).

**Cubre:**
- Login con credenciales reales
- Navegación por menú con submenús anidados
- Paso 1: Domicilio de Instalación (Select2, autocompletado de Zona)
- Paso 2: Datos Personales (validaciones de DNI, Cód. Área, email)
- Paso 3: Datos de Facturación (Forma de Pago)
- Paso 4: Confirmación

**Desafíos técnicos resueltos:**
- Select2 (desplegables avanzados) con manejo de ambigüedad
- Autocompletado con evento blur (ISPBoss calcula la Zona cuando el campo pierde el foco)
- Race conditions en modo headless → solución con `wait_for()` y `expect()`
- IDs largos de ASP.NET y selectores con atributo `name`

```bash
python3 -m pytest IspbossTest/test_alta_abonado.py -v
```

---

### API Testing — CRUD completo
Suite de tests sobre la API pública JSONPlaceholder, cubriendo los 4 verbos HTTP.

**Cubre:**
- GET con verificación de status code, tipos de datos y estructura JSON
- POST con creación de recursos y verificación de status 201
- PUT para modificación de recursos existentes
- DELETE para eliminación
- Casos negativos (404 para recursos inexistentes)
- `pytest.mark.parametrize` para correr el mismo test con múltiples inputs
- Verificación de unicidad de IDs con `set()`

```bash
python3 -m pytest ApiTest/ -v
```

---

### Ejercicios Python progresivos
7 ejercicios que van de condicionales simples hasta una clase con pytest, usando contexto de ISPBoss.

```bash
python3 -m pytest EjerciciosPython/test_abonados.py -v
```

---

### SauceDemo — Login y Carrito
Tests de login (casos exitosos, errores, validaciones) y agregar productos al carrito.

```bash
python3 -m pytest test_Login.py test_agregar_carrito.py -v
```

## Instalación

```bash
# Clonar el repo
git clone https://github.com/matitrova/QaTest.git
cd QaTest

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
python3 -m playwright install chromium
```

## Correr todos los tests

```bash
python3 -m pytest -v
```

## Autor

**Matias Trovato** — Manual QA Tester en transición a QA Automation  
[GitHub](https://github.com/matitrova)
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

---

### Desafíos de Playwright — carga dinámica, upload, diálogos JS y checkboxes
Suite sobre the-internet.herokuapp.com enfocada en problemas clásicos de automatización de UI.

**Cubre:**
- Carga dinámica con elemento oculto (`display:none`) vs. elemento que directamente no existe en el DOM hasta terminar la carga — dos formas distintas de la misma espera, cada una necesita su propio manejo
- Espera explícita con `expect().to_be_visible(timeout=...)` en vez de un `sleep()` a ciegas
- Upload de archivos con `set_input_files()` y verificación del nombre subido
- Diálogos nativos del navegador (`alert`, `confirm`, `prompt`) aceptados, cancelados y con texto ingresado
- Checkboxes sin `id` propio, ubicados por posición dentro de su contenedor con `.nth()`, y toggle con `.check()` / `.uncheck()`

**Desafíos técnicos resueltos:**
- El timeout default de `expect()` (5000ms) quedaba corto contra la demora simulada del sitio (~5s) y hacía flaky el test — ajustado explícitamente en vez de agrandarlo a ciegas, confirmado corriendo la suite varias veces seguidas.
- Playwright descarta los diálogos JS automáticamente si no hay un listener registrado antes de que aparezcan (a diferencia de Selenium, que permite engancharlos después con `switch_to.alert`) — el handler se registra con `page.once("dialog", ...)` justo antes del click que dispara el diálogo, y con `once` en vez de `on` para no dejarlo pegado y afectar otros tests.
- Los checkboxes de esta página no tienen `id` individual, solo el `<form>` que los contiene — hubo que ubicarlos por posición (`.nth(0)`, `.nth(1)`) en vez de por atributo, y verificar que tildar uno no afecte al otro (son independientes).

```bash
python3 -m pytest DesafiosPlaywright/ -v
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
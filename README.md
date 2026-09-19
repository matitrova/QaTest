# QaTest — Portfolio de QA Automation

[![Tests](https://github.com/matitrova/QaTest/actions/workflows/tests.yml/badge.svg)](https://github.com/matitrova/QaTest/actions/workflows/tests.yml)

Automatización de pruebas con **Python, Pytest y Playwright**, sobre interfaces web y
APIs REST. **66 casos de prueba** organizados con el patrón **Page Object Model**, que
corren en integración continua con **GitHub Actions** en cada push.

Incluye automatización sobre **ISPBoss**, un sistema real de gestión y facturación para
proveedores de internet en el que trabajé cuatro años como responsable de calidad.

## Qué cubre

| Suite | Sobre qué | Tests | Tipo |
|---|---|---|---|
| [`IspbossTest`](IspbossTest) | ISPBoss, sistema real (entorno beta) | 3 | UI · E2E |
| [`DesafiosPlaywright`](DesafiosPlaywright) | the-internet.herokuapp.com | 14 | UI |
| [`TestX`](TestX) | SauceDemo (e-commerce) | 9 | UI |
| [`ReqResTest`](ReqResTest) | API de ReqRes | 15 | API |
| [`RestfulBookerTest`](RestfulBookerTest) | API de Restful Booker, con autenticación | 10 | API |
| [`ApiTest`](ApiTest) | API de JSONPlaceholder | 5 | API |
| [`practica/`](practica) | Ejercicios de Python y repaso de Playwright | 10 | Práctica |

## Tecnologías

- **Python 3.12+**
- **Playwright** — automatización de navegador
- **Pytest** — framework de testing, con fixtures en `conftest.py` y `parametrize`
- **Requests** — testing de APIs REST
- **GitHub Actions** — integración continua

---

## ISPBoss — Alta de Abonado (E2E)

Automatización del flujo completo de alta de un abonado en un sistema real de gestión
de ISPs (ASP.NET WebForms). Los datos de prueba viven en JSON aparte y las
credenciales se leen de variables de entorno: no hay ninguna escrita en el código.

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

Esta suite **no corre en la integración continua**: necesita credenciales del entorno
beta de ISPBoss, que no pertenecen a este repositorio.

```bash
export ISPBOSS_USER=...  ISPBOSS_PASS=...
python3 -m pytest IspbossTest -v
```

---

## Desafíos de Playwright — carga dinámica, upload, diálogos JS, checkboxes y dropdown

Suite sobre the-internet.herokuapp.com enfocada en problemas clásicos de automatización de UI.

**Cubre:**
- Carga dinámica con elemento oculto (`display:none`) vs. elemento que directamente no existe en el DOM hasta terminar la carga — dos formas distintas de la misma espera, cada una necesita su propio manejo
- Espera explícita con `expect().to_be_visible(timeout=...)` en vez de un `sleep()` a ciegas
- Upload de archivos con `set_input_files()` y verificación del nombre subido
- Diálogos nativos del navegador (`alert`, `confirm`, `prompt`) aceptados, cancelados y con texto ingresado
- Checkboxes sin `id` propio, ubicados por posición dentro de su contenedor con `.nth()`, y toggle con `.check()` / `.uncheck()`
- Dropdown (`<select>`) con `.select_option(value=...)`, incluyendo que la opción inicial es un placeholder disabled, no una opción real

**Desafíos técnicos resueltos:**
- El timeout default de `expect()` (5000ms) quedaba corto contra la demora simulada del sitio (~5s) y hacía flaky el test — ajustado explícitamente en vez de agrandarlo a ciegas, confirmado corriendo la suite varias veces seguidas.
- Playwright descarta los diálogos JS automáticamente si no hay un listener registrado antes de que aparezcan (a diferencia de Selenium, que permite engancharlos después con `switch_to.alert`) — el handler se registra con `page.once("dialog", ...)` justo antes del click que dispara el diálogo, y con `once` en vez de `on` para no dejarlo pegado y afectar otros tests.
- Los checkboxes de esta página no tienen `id` individual, solo el `<form>` que los contiene — hubo que ubicarlos por posición (`.nth(0)`, `.nth(1)`) en vez de por atributo, y verificar que tildar uno no afecte al otro (son independientes).
- El `<option>` inicial del dropdown tiene `disabled` en el HTML: es un placeholder, no una tercera opción real. El test lo verifica explícitamente (valor `""`) en vez de asumirlo.

```bash
cd DesafiosPlaywright && python3 -m pytest -v
```

---

## SauceDemo — Login y carrito

Tests de login (casos exitosos, errores y validaciones) y agregado de productos al
carrito, con Page Objects para el login y el inventario.

```bash
python3 -m pytest TestX -v
```

---

## API — ReqRes, Restful Booker y JSONPlaceholder

Tres APIs públicas con comportamientos distintos, que obligan a probar cosas distintas.

**ReqRes** — registro, login, creación, modificación y borrado de usuarios, con casos
negativos (registro sin email, sin contraseña).

**Restful Booker** — reservas con **autenticación por token**: el token se obtiene en un
fixture y se envía en la cookie de las operaciones que lo requieren.

**JSONPlaceholder** — CRUD completo.

**Cubre:**
- GET con verificación de status code, tipos de datos y estructura JSON
- POST con creación de recursos y verificación de status 201
- PUT para modificación de recursos existentes
- DELETE para eliminación
- Casos negativos (404 para recursos inexistentes)
- `pytest.mark.parametrize` para correr el mismo test con múltiples inputs
- Verificación de unicidad de IDs con `set()`

```bash
cd ReqResTest && python3 -m pytest -v
cd RestfulBookerTest && python3 -m pytest -v
cd ApiTest && python3 -m pytest -v
```

---

## Decisiones y bugs encontrados

**Probar una API simulada no es probar una API real.** Tres tests de ReqRes fallaban:
hacían un PUT, PATCH o DELETE y después volvían a pedir el usuario esperando verlo
modificado o borrado. Pero ReqRes es una API simulada: responde como si guardara el
cambio y no persiste nada, así que el GET siempre devolvía el usuario original. El test
validaba algo que esa API nunca promete. Ahora se valida la respuesta de la operación
misma, que es lo único que ReqRes garantiza.

**Cada suite corre desde su propia carpeta.** Varias carpetas tienen módulos con el
mismo nombre (`config.py` en tres de ellas). Corriendo todo junto desde la raíz, Python
importa el primero que encuentra y las demás suites usan la configuración equivocada:
los tests de ReqRes le pegaban a otro sitio y daban 404. La integración continua corre
cada suite como un trabajo aparte, desde su carpeta, sin tocar el código de los tests.

**Mayúsculas en nombres de archivo.** El módulo de configuración de ISPBoss estaba
guardado en el repositorio como `IspBoss_config.py`, pero se importaba como
`ispboss_config`. Python distingue mayúsculas al importar, así que en cualquier máquina
que clonara el repo el test ni siquiera cargaba. El origen probable es un renombre que
solo cambió mayúsculas: macOS no las distingue en los nombres de archivo y, por eso, git
no siempre registra ese tipo de cambio. El archivo se renombró a minúsculas, que además
es la convención de Python.

## Instalación

```bash
git clone https://github.com/matitrova/QaTest.git
cd QaTest

python3 -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
python3 -m playwright install chromium
```

Cada suite se corre desde su carpeta, como muestran los comandos de arriba. La
integración continua hace lo mismo: ver [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

## Autor

**Matías Trovato** — QA con cuatro años como responsable de calidad de un sistema de
facturación en producción, hoy automatizando con Python, Playwright y Pytest.
[GitHub](https://github.com/matitrova)

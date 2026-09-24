# QaTest — Portfolio de QA Automation

[![Tests](https://github.com/matitrova/QaTest/actions/workflows/tests.yml/badge.svg)](https://github.com/matitrova/QaTest/actions/workflows/tests.yml)

Automatización de pruebas con **Python, Pytest y Playwright**, sobre interfaces web y
APIs REST. **76 casos de prueba** organizados con el patrón **Page Object Model**, que
corren en integración continua con **GitHub Actions** en cada push.

Incluye automatización sobre **ISPBoss**, un sistema real de gestión y facturación para
proveedores de internet en el que trabajé cuatro años como responsable de calidad.

## Qué cubre

| Suite | Sobre qué | Tests | Tipo |
|---|---|---|---|
| [`IspbossTest`](IspbossTest) | ISPBoss, sistema real (entorno beta) | 3 | UI · E2E |
| [`DesafiosPlaywright`](DesafiosPlaywright) | the-internet.herokuapp.com | 24 | UI |
| [`TestX`](TestX) | SauceDemo (e-commerce) | 9 | UI |
| [`ReqResTest`](ReqResTest) | API de ReqRes | 15 | API |
| [`RestfulBookerTest`](RestfulBookerTest) | API de Restful Booker, con autenticación | 10 | API |
| [`ApiTest`](ApiTest) | API de JSONPlaceholder | 5 | API |
| [`postman/`](postman) | API de Restful Booker, en Postman + Newman | 22 | API |
| [`practica/`](practica) | Ejercicios de Python y repaso de Playwright | 10 | Práctica |

## Tecnologías

- **Python 3.12+**
- **Playwright** — automatización de navegador
- **Pytest** — framework de testing, con fixtures en `conftest.py` y `parametrize`
- **Requests** — testing de APIs REST
- **Postman + Newman** — colecciones de API corriendo en integración continua
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

## Desafíos de Playwright — carga dinámica, upload, diálogos JS, checkboxes, dropdown, ventanas, hovers, slider y drag and drop

Suite sobre the-internet.herokuapp.com enfocada en problemas clásicos de automatización de UI.

**Cubre:**
- Carga dinámica con elemento oculto (`display:none`) vs. elemento que directamente no existe en el DOM hasta terminar la carga — dos formas distintas de la misma espera, cada una necesita su propio manejo
- Espera explícita con `expect().to_be_visible(timeout=...)` en vez de un `sleep()` a ciegas
- Upload de archivos con `set_input_files()` y verificación del nombre subido
- Diálogos nativos del navegador (`alert`, `confirm`, `prompt`) aceptados, cancelados y con texto ingresado
- Checkboxes sin `id` propio, ubicados por posición dentro de su contenedor con `.nth()`, y toggle con `.check()` / `.uncheck()`
- Dropdown (`<select>`) con `.select_option(value=...)`, incluyendo que la opción inicial es un placeholder disabled, no una opción real
- Apertura de pestañas nuevas (`target="_blank"`) y verificación de que la pestaña original no se ve afectada
- Hover sobre una de tres figuras iguales, verificando que solo se muestra la información de la que tiene el mouse encima, no las otras dos
- Slider horizontal (`<input type="range">`) movido con flechas del teclado, verificando que respeta el `step` de 0.5 y no se pasa de los límites `min`/`max`
- Drag and drop entre dos columnas que intercambian su contenido, verificando el resultado del intercambio y que arrastrar dos veces vuelve al estado original

**Desafíos técnicos resueltos:**
- El timeout default de `expect()` (5000ms) quedaba corto contra la demora simulada del sitio (~5s) y hacía flaky el test — ajustado explícitamente en vez de agrandarlo a ciegas, confirmado corriendo la suite varias veces seguidas.
- Playwright descarta los diálogos JS automáticamente si no hay un listener registrado antes de que aparezcan (a diferencia de Selenium, que permite engancharlos después con `switch_to.alert`) — el handler se registra con `page.once("dialog", ...)` justo antes del click que dispara el diálogo, y con `once` en vez de `on` para no dejarlo pegado y afectar otros tests.
- Los checkboxes de esta página no tienen `id` individual, solo el `<form>` que los contiene — hubo que ubicarlos por posición (`.nth(0)`, `.nth(1)`) en vez de por atributo, y verificar que tildar uno no afecte al otro (son independientes).
- El `<option>` inicial del dropdown tiene `disabled` en el HTML: es un placeholder, no una tercera opción real. El test lo verifica explícitamente (valor `""`) en vez de asumirlo.
- `target="_blank"` no navega la página actual: hay que engancharse a `context.expect_page()` **antes** del click para capturar la pestaña nueva, si el listener se registra después ya es tarde y se pierde la referencia. El `<a>` de esa página además tiene HTML mal formado (una coma suelta entre atributos), así que el link se ubica por rol y texto visible en vez de por `href`.
- El layout de este sitio carga un script de analítica de un dominio externo (Optimizely) ajeno a lo que se prueba; si esa red está lenta o inaccesible, el evento `load` puede colgarse esperándolo. Se aborta ese pedido puntual con `page.route()` para que el test de ventanas dependa solo del sitio bajo prueba.
- Las tres figuras de `/hovers` son visualmente idénticas en el HTML (misma clase `.figure`), así que hubo que ubicarlas por posición con `.nth()` y confirmar, al pasar el mouse por la del medio, que las otras dos siguen ocultas — no alcanza con probar que "una" caption aparece, hay que probar que aparece la correcta y ninguna otra.
- Clickear el slider no lo mueve de a un paso: salta directo al valor que corresponde a la posición del click (clickear cerca del borde derecho lo manda directo al máximo), a diferencia de las flechas del teclado que sí respetan el `step`. El test lo usa a favor: clickear el extremo izquierdo del track deja el valor en el mínimo conocido (0) para arrancar cada caso.
- `page.keyboard.press()` depende del foco global de la página, que en modo headless no siempre queda asentado justo después de un `click()` — a veces la tecla no tenía ningún efecto. Se reemplazó por `locator.press()`, que reenfoca el elemento puntual antes de cada tecla, y quedó estable en corridas repetidas.
- La página de drag and drop no usa una librería como jQuery UI, sino los eventos nativos de HTML5 Drag and Drop (`dragstart`, `dragover`, `drop`) implementados a mano en JavaScript, que además intercambian el `innerHTML` de las columnas en vez de mover los nodos. Un `dispatchEvent` manual de esos eventos suele quedar incompleto (falta simular `dataTransfer` correctamente) y es la razón por la que este caso es históricamente flaky con Selenium; `locator.drag_to()` de Playwright dispara la secuencia completa vía CDP, así que el test verifica el intercambio de contenido en vez de asumir que "no tira error" es suficiente.

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

## Postman — Restful Booker con Newman

La misma suite de Restful Booker que está en Python, hecha en Postman para comparar las
dos herramientas: **11 pedidos y 22 pruebas** que corren en integración continua con
**Newman**, que es Postman desde la terminal.

**Cubre:**
- Autenticación: el token se obtiene en el primer pedido y queda en una variable de la
  colección, que usan después los pedidos que lo necesitan.
- El id de la reserva creada también se guarda en una variable, y encadena el resto del
  recorrido: consultar, modificar, borrar y verificar que se borró.
- Valores por defecto en la colección, así que corre sin configurar nada; el environment
  es opcional y los pisa si se elige. La integración continua prueba las dos formas.
- Pruebas con `pm.test` y `pm.expect` sobre status code y contenido del JSON.

**Lo que esta API enseña, validado contra la API real:**

- **Un 200 no significa éxito.** Un login con la clave incorrecta responde 200, con el
  error solo en el cuerpo (`"reason": "Bad credentials"`). Un test que solo mirara el
  status code daría ese login por bueno. Por eso se valida que no haya token.
- **Borrar responde 201 "Created"**, no 200 ni 204 como indica la convención. El test
  valida lo que la API hace de verdad: si algún día cambiara, avisaría.
- **Restful Booker sí guarda los cambios, ReqRes no.** Acá tiene sentido consultar una
  reserva después de crearla, o verificar un 404 después de borrarla. En ReqRes ese
  mismo test está mal planteado, porque es una API simulada que no persiste nada — ver
  "Decisiones y bugs encontrados".

```bash
npm install -g newman
newman run postman/restful-booker.postman_collection.json \
  -e postman/restful-booker.postman_environment.json
```

O desde la app de Postman: *Import* → `restful-booker.postman_collection.json` →
*Run collection*. **Funciona recién importada, sin elegir environment:** la URL y las
credenciales de demo tienen un valor por defecto en la propia colección. El
environment de `postman/` es opcional y, si se elige, sus valores tienen prioridad.

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

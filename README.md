# QaTest — Portfolio de QA Automation

[![Tests](https://github.com/matitrova/QaTest/actions/workflows/tests.yml/badge.svg)](https://github.com/matitrova/QaTest/actions/workflows/tests.yml)

Automatización de pruebas con **Python, Pytest y Playwright**, sobre interfaces web y
APIs REST. **307 casos de prueba** organizados con el patrón **Page Object Model**, que
corren en integración continua con **GitHub Actions** en cada push.

Incluye automatización sobre **ISPBoss**, un sistema real de gestión y facturación para
proveedores de internet en el que trabajé cuatro años como responsable de calidad.

## Qué cubre

| Suite | Sobre qué | Tests | Tipo |
|---|---|---|---|
| [`IspbossTest`](IspbossTest) | ISPBoss, sistema real (entorno beta) | 3 | UI · E2E |
| [`DesafiosPlaywright`](DesafiosPlaywright) | the-internet.herokuapp.com | 118 | UI |
| [`UiTestingPlaygroundTest`](UiTestingPlaygroundTest) | uitestingplayground.com | 80 | UI |
| [`TestX`](TestX) | SauceDemo (e-commerce) | 24 | UI |
| [`ReqResTest`](ReqResTest) | API de ReqRes | 20 | API |
| [`RestfulBookerTest`](RestfulBookerTest) | API de Restful Booker, con autenticación | 21 | API |
| [`ApiTest`](ApiTest) | API de JSONPlaceholder | 9 | API |
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

## Desafíos de Playwright — carga dinámica, upload, diálogos JS, checkboxes, dropdown, ventanas, hovers, slider, drag and drop, add/remove elements, basic auth, tablas, inputs numéricos, teclas, menú contextual, mensajes de notificación, códigos de status HTTP, elementos que aparecen y desaparecen, contenido que cambia de posición, recuperar contraseña, anuncio de entrada, imágenes rotas, intención de salida, menú flotante, scroll infinito, un link cuya URL relativa redirige a otra página, un DOM enorme anidado 50 niveles de profundidad, un formulario de login con sesión real de servidor y controles que se habilitan o eliminan de forma asíncrona

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
- Agregar y quitar elementos dinámicamente, verificando que el contador de botones sube y baja de a uno y que la lista puede volver a quedar vacía
- HTTP Basic Auth: acceso con credenciales correctas por navegador, y verificación por API de que sin credenciales o con credenciales incorrectas la respuesta es 401
- Tablas ordenables: dos tablas con los mismos datos, una sin ningún atributo para
  agrupar filas o columnas y otra con clases en cada celda, ordenadas por columna de
  texto (apellido) y por columna numérica con formato de moneda (`$100.00`), en ambos
  sentidos
- Input numérico (`<input type="number">`) sin ningún atributo `min`/`max`/`step`:
  qué caracteres acepta y cuáles descarta el propio navegador al tipear, y cómo
  responde a las flechas del teclado sin ningún piso ni techo que lo frene
- Teclas presionadas sobre un input, verificando el nombre que devuelve cada una
  (letra, dígito, espacio, Escape, Backspace, flecha) y que Enter no se comporta
  como las demás
- Menú contextual: clic derecho sobre un cuadro dispara un `window.alert` nativo,
  verificando el mensaje exacto y que un clic izquierdo sobre el mismo cuadro no
  dispara nada
- Mensajes de notificación: cada visita a la página elige al azar uno de dos mensajes
  ("éxito" o "error"), verificando que el mensaje mostrado sea uno de los dos conocidos,
  que ambos usen exactamente la misma clase CSS (no hay forma de distinguirlos por
  estilo) y que el botón de cierre oculte el mensaje
- Códigos de status HTTP (200, 301, 404, 500): que el status real de la respuesta
  coincida con el texto que la propia página imprime en su body, que la página
  principal linkee a los cuatro, y un caso aparte para el 301 que confirma que la
  navegación no termina en ninguna otra URL
- Elementos que aparecen y desaparecen: un menú de navegación donde cuatro items
  están siempre presentes y en el mismo orden, y un quinto ("Gallery") que el
  servidor decide al azar si incluir o no en cada carga, verificando ambos
  estados y que, cuando aparece, siempre queda último
- Contenido que cambia de posición: una lista de cinco líneas de texto donde
  una de ellas ("Important Information You're Looking For") aparece en una
  posición distinta en cada carga de la página, verificando que las cinco
  líneas siguen siendo las mismas (sin importar el orden), que la posición de
  esa línea varía entre recargas y que no existe ningún elemento individual
  para ubicarla por locator, solo texto plano dentro de un contenedor común
- Recuperar contraseña: el formulario de `/forgot_password` responde
  **500 Internal Server Error** con cualquier input -- un email con formato
  válido, un campo vacío y un texto sin forma de email dan exactamente el
  mismo resultado, lo que descarta que el error dependa de una validación de
  formato
- Anuncio de entrada (`/entry_ad`): un modal que aparece 500ms después de
  cargar la página, se cierra al tocar el fondo o el botón "Close" pero no al
  tocar su propio contenido, y queda cerrado para el resto de la sesión --
  una nueva visita a la página ni siquiera recibe el script que lo muestra.
  El sitio promete "to re-enable it, click here", pero ese link nunca
  reactiva nada
- Imágenes rotas (`/broken_images`): de tres `<img>` en la página, dos
  apuntan a rutas que no existen (404) y una carga bien, verificando cada
  una por separado con el status real de la respuesta y con
  `naturalWidth`/`naturalHeight` del elemento
- Intención de salida (`/exit_intent`): un modal que aparece cuando el mouse
  sale del viewport por el borde superior (y no por moverse dentro de la
  página, ni por salir por abajo o los costados), que un click dentro del
  modal no lo cierra pero un click en su botón "Close" sí, y que una vez
  mostrado no vuelve a dispararse dentro de la misma carga de página aunque
  el mouse vuelva a salir por arriba
- Scroll infinito (`/infinite_scroll`): la página carga al menos un párrafo
  sin que haga falta scrollear, y cada scroll hasta el fondo del documento
  agrega exactamente un párrafo más, mientras que un scroll que no llega al
  fondo no agrega nada
- Menú flotante (`/floating_menu`): un menú que arranca en una posición fija
  dentro del documento y, al hacer scroll, se recalcula para quedar pegado
  cerca del borde superior del viewport en vez de desplazarse fuera de
  vista, verificando tanto la posición resultante tras un scroll largo como
  que vuelve exactamente a su posición original al volver arriba, y que los
  links del menú siguen siendo clickeables mientras está "flotando"
- Redirector (`/redirector`): un link cuyo `href` es la URL relativa
  `redirect`, sin barra inicial -- verificando contra la API real que esa
  URL relativa resuelve contra la raíz del sitio (`/redirect`, un 302 con
  header `Location` hacia `/status_codes`) y no contra la carpeta que
  sugiere el nombre de la página (`/redirector/redirect`, que da 404), y
  que un click en el navegador efectivamente termina en `/status_codes`
- Formulario de login (`/login`): credenciales correctas redirigen a
  `/secure` con un mensaje de éxito y el botón de logout visible; usuario
  inválido y contraseña inválida muestran cada uno su propio mensaje de
  error puntual sin redirigir, y cuando los dos están mal el servidor
  informa solo el del usuario, nunca los dos juntos; logout termina la
  sesión y vuelve a `/login`; y entrar directo a `/secure` sin haber
  iniciado sesión en ese mismo browser context redirige a `/login` en vez
  de mostrar la página
- Controles dinámicos (`/dynamic_controls`): un checkbox que un botón
  elimina del DOM y luego reinserta, y un input que otro botón habilita y
  deshabilita, ambos con un delay real de 3 segundos simulado con
  `setTimeout`, verificando que el checkbox desaparece y reaparece del todo
  (no se oculta con CSS), que el input pasa de no poder tipearse a poder
  hacerlo y viceversa, que el botón queda deshabilitado mientras dura el
  delay -- bloqueando un segundo click en vez de ignorarlo en silencio -- y
  que cada mensaje de resultado ("It's gone!", "It's back!", "It's
  enabled!", "It's disabled!") reemplaza al anterior en vez de acumularse

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
- Los botones "Delete" que agrega `/add_remove_elements` son todos idénticos: mismo texto, misma clase, sin `id` ni ningún atributo que los distinga entre sí. No hay forma de verificar "cuál" se eliminó puntualmente, así que el test se apoya en un invariante que sí es verificable: la cantidad total de botones sube y baja de a uno por click. Además, el propio JS de la página elimina siempre `button:first-child` (el primero agregado), no el último — un comportamiento FIFO que contradice la intuición de "deshacer lo último", y que quedó documentado en el código en vez de asumido.
- HTTP Basic Auth es un diálogo nativo del navegador, no un `dialog` de JavaScript como los de `/javascript_alerts`: no hay ningún `page.on("dialog")` que lo capture, y si `page.goto()` navega sin credenciales ya puestas, el test se queda colgado esperando una interacción que Playwright no puede dar. Tampoco alcanza con pasarlas embebidas en la URL (`https://usuario:clave@...`), porque Chromium las ignora en navegación de primer nivel. La solución es extender el fixture `browser_context_args` de `pytest-playwright` para fijar `http_credentials` en el contexto **antes** de crear la página. Para probar el camino negativo (sin credenciales, o con credenciales incorrectas) sin arriesgarse a colgar el navegador, esos dos casos se verifican con `requests` en vez de con `page`, contra el mismo endpoint.
- La tabla ordenable usa el plugin jQuery `tablesorter`, que ordena `$100.00` como texto por default: alfabéticamente, `"$100.00"` queda antes que `"$51.00"` porque compara carácter a carácter (`"1" < "5"`). El test no confía en que el plugin haya interpretado el monto como número: parsea cada celda a `float` y compara ese resultado contra `sorted()`, que es la única forma de confirmar que el orden es numérico y no textual.
- El CSS de la propia página sugiere que el plugin marca la columna ordenada con las clases `tablesorter-headerAsc` / `tablesorter-headerDesc`, pero la versión que corre en producción usa otras: `headerSortDown` para ascendente y `headerSortUp` para descendente. Guiarse por el CSS en vez de inspeccionar el DOM real hubiera hecho fallar el test silenciosamente ni bien se esperara la clase.
- Ni el evento `load` ni `networkidle` garantizan que `tablesorter` ya haya enganchado sus listeners de click: bajo latencia de red, un click podía llegar justo antes de que el plugin terminara de inicializarse y no tenía ningún efecto, sin lanzar ningún error que lo delatara. La solución es esperar explícitamente a que cada `<th>` tenga la clase `header` que el plugin agrega al terminar de inicializarse, antes de clickear.
- El input de `/inputs` no tiene ningún atributo `min`, `max`, `step` ni `pattern`: toda la validación es del propio navegador, por ser `type="number"`. Escribir letras no deja rastro (el valor queda vacío), un `+` suelto sin exponente de por medio se descarta igual que una letra, y un segundo punto decimal se descarta solo pero deja pasar el resto de los caracteres (`"5.5.5"` termina en `"5.55"`, no en un valor vacío). La notación científica (`"1e3"`) y los ceros a la izquierda (`"007"`) quedan tal cual se tipearon: el navegador no los normaliza a menos que algo — un submit, por ejemplo — los interprete como número. Y sin `min`, las flechas de teclado no tienen piso: bajar desde 0 sigue restando y entra en negativos.
- `/key_presses` traduce el `keyCode` de cada tecla con una tabla propia (`keyboardMap`) que no siempre coincide con lo intuitivo: Backspace se muestra como `BACK_SPACE` (con guión bajo) y una flecha se muestra solo como `LEFT`, `RIGHT`, etc., sin la palabra "ARROW". Nada de eso se puede asumir por el nombre de la tecla en Playwright — hubo que confirmar cada texto contra el sitio real antes de escribirlo en una aserción. El caso más interesante fue Enter: el `<input>` vive solo dentro de un `<form>` sin botón de submit, así que el propio navegador dispara ahí el submit implícito del formulario (el comportamiento estándar cuando hay un único campo de texto). Como el form no tiene `action` ni el input tiene `name`, el submit sólo recarga la misma URL sin enviar nada — Enter nunca llega a mostrar "You entered: ENTER" como cualquier otra tecla, sino que recarga la página entera y borra lo que había escrito. El test lo verifica con `page.expect_navigation()` en vez de asumir que Enter es una tecla más.
- `/context_menu` engancha su diálogo al evento `oncontextmenu` del elemento, no a un `onclick`: el disparador es específicamente el botón derecho del mouse. El test no se conforma con probar que el clic derecho abre el diálogo — también verifica que un clic izquierdo sobre el mismo cuadro no dispara nada, para no confundir "cualquier clic" con "el botón derecho puntualmente". Es el mismo mecanismo de `page.once("dialog", ...)` que `javascript_alerts`, pero disparado con `locator.click(button="right")` en vez de un `onclick` común.
- `/notification_message` no tiene forma de pedir "el mensaje de éxito" o "el de error" a demanda: cada visita a la página redirige con uno de los dos elegido al azar por el servidor. Un test no puede afirmar cuál va a aparecer, así que primero verifica solamente que sea uno de los dos conocidos, y para los casos que necesitan un mensaje puntual (el del error, y juntar ambas variantes para comparar su clase) visita la página en un loop hasta encontrarlo, en vez de asumir que aparece a la primera. El mensaje de error además tiene un typo publicado en el sitio real ("unsuccesful", sin la segunda "s"), que el test verifica tal cual está y no con la ortografía correcta. El bug más interesante es que los dos mensajes comparten exactamente la misma clase CSS (`flash notice`), sin ningún atributo que distinga éxito de error — un test que confiara en la clase para saber el resultado de la acción siempre daría el mismo veredicto, sin importar cuál de los dos mensajes se haya mostrado en realidad. El cierre del mensaje tampoco es instantáneo (Foundation le aplica un `fadeOut` de 300ms antes de sacarlo del DOM), así que se verifica con `expect().to_be_hidden()` en vez de comprobar la visibilidad apenas se hace clic.
- `/status_codes/301` responde con el status HTTP 301 de verdad (`response.status`
  lo confirma), pero no trae ningún header `Location` -- se puede confirmar
  inspeccionando la respuesta cruda de la navegación. Un 301 real de un servidor
  siempre viene acompañado de a dónde redirigir; este es un 301 "de mentira" que
  sirve su propio contenido en vez de redirigir a ningún lado. El test no se
  conforma con el status code: confirma también que `page.url` después de la
  navegación sigue siendo la misma URL pedida, porque un navegador real sí
  seguiría un 301 legítimo y terminaría en otra parte. Esto obliga a distinguir
  dos fuentes de verdad independientes para el mismo dato: el status code de la
  respuesta HTTP (`response.status`, lo que ve el navegador) y el texto que el
  body imprime ("This page returned a 301 status code", lo que el servidor dice
  de sí mismo) -- las dos tienen que coincidir, pero son cosas distintas y el
  test las verifica por separado.
- `/disappearing_elements` no oculta "Gallery" con CSS: el servidor decide en
  cada pedido si lo incluye en el HTML, así que cuando no aparece no hay
  ningún `<li>` oculto esperando en el DOM -- no existe. Un test que buscara
  el elemento con `is_hidden()` nunca encontraría nada que afirmar, porque no
  hay nada que mirar. La única forma de probar las dos ramas es recargar en un
  loop hasta verlas ambas, igual que con `/notification_message`, pero acá la
  variable es la *cantidad* de items (4 o 5), no su contenido. Los primeros
  cuatro items (Home, About, Contact Us, Portfolio) están siempre presentes y
  en el mismo orden -- el test lo confirma por separado del quinto, para no
  mezclar "qué es estable" con "qué es aleatorio" en la misma aserción.
- `/shifting_content/list` no tiene ningún `<li>` ni elemento individual por
  línea: las cinco líneas son texto plano separado por `<br><br>` dentro de un
  único `<div>`. Por eso `get_by_text(exact=True)` -- que sí funciona en casos
  parecidos de este mismo sitio, como `/disappearing_elements` -- no encuentra
  nada acá: no existe ningún elemento cuyo texto completo sea exactamente esa
  línea, porque el único elemento que la contiene es el `<div>` entero con las
  cinco líneas juntas (`get_by_text()` sin `exact` sí "encuentra" algo, pero
  devuelve ese mismo `<div>` completo, no la línea puntual). La única forma de
  ubicar la línea es parsear el texto completo del contenedor con
  `inner_text()` y partirlo por salto de línea, que es lo que hace
  `ShiftingContentListPage.lineas()`. El test lo verifica explícitamente
  comprobando que ese locator exacto da `count() == 0`, en vez de asumir que
  "no funciona" sin probarlo.
- `/forgot_password` tiene un bug real en el servidor: enviar el formulario
  devuelve **500 Internal Server Error** sin importar qué se escriba en el
  campo de email. El propio HTML no ayuda a sospecharlo de entrada: el input
  es `type="text"`, no `type="email"`, así que el navegador no aplica ninguna
  validación de formato antes de mandar el POST -- cualquier string llega
  igual al servidor. Para confirmar que el 500 es un bug del backend y no el
  resultado esperable de una validación que falla distinto según el input, el
  test prueba tres casos (`usuario@example.com`, campo vacío y un texto sin
  forma de email) y verifica que los tres dan la misma respuesta: si el error
  dependiera de la validación del email, el campo vacío o el texto sin
  arroba deberían fallar antes o distinto que un email con formato válido, y
  no es así.
- `/entry_ad` promete "to re-enable it, click here" en un link que llama a
  `$.post('/entry-ad')` -- con GUION. El único endpoint que el servidor usa
  de verdad para marcar la sesión como "ya cerrado" es `/entry_ad`, con GUION
  BAJO (el mismo que dispara el botón "Close"). El típo hace que el POST de
  "reiniciar" pegue a una ruta que no existe (**404**) y la sesión nunca se
  actualiza: el anuncio queda cerrado para siempre, sin ningún error visible
  para quien hace click. El propio `<a href="">` del link, sin
  `preventDefault()`, dispara además una navegación real del navegador que
  en una corrida real puede cancelar ese POST a mitad de camino -- probar el
  404 clickeando el link es inherentemente flaky, así que ese chequeo se
  hace con `page.request.post()` directo al endpoint, y por separado se
  confirma el síntoma (clickear "reiniciar" y revisitar la página sigue sin
  mostrar el anuncio). Además, el click del body que cierra el anuncio en
  cualquier parte de la página (`$('body').on('click', dismissedAd)`) se
  corta con `e.stopPropagation()` únicamente dentro de la caja del modal, así
  que clickear el texto del anuncio no lo cierra pero clickear su fondo sí.
- `/broken_images` no deja ningún rastro en el DOM de qué imagen rompió y
  cuál no: las tres etiquetas `<img>` son indistinguibles por HTML, y la
  propiedad `complete` del elemento da `True` en las tres apenas el
  navegador termina de intentar cargarlas, se hayan roto o no -- no sirve
  para distinguir una imagen rota de una que cargó bien. La única señal
  confiable es `naturalWidth`/`naturalHeight`: quedan en `0` cuando la
  respuesta no trajo una imagen válida, y reflejan el tamaño real del
  archivo en cualquier otro caso. El test cruza esa señal contra el
  status HTTP real de cada request (dos 404 y un 200) para confirmar que
  ambas fuentes coinciden, en vez de confiar en una sola.
- `/exit_intent` usa la librería `ouibounce`, inicializada con
  `aggressive: true` y `sensitivity` en su valor por default (20px): solo
  cuenta como "salida" un `mouseleave` del `documentElement` con
  `clientY <= 20`, el borde superior puntualmente -- moverse dentro de la
  página, incluso hasta el borde inferior, no dispara ese evento. En
  Playwright no hay forma de que el mouse "salga de verdad" de un
  navegador headless, pero `page.mouse.move()` sí puede posicionarlo en
  coordenadas negativas, y eso alcanza para que Chromium dispare el
  `mouseleave` real con el `clientY` que la librería necesita -- no hizo
  falta simular el evento a mano con `dispatchEvent`. La hipótesis inicial
  sobre `aggressive: true` era que permitía que el modal se repitiera cada
  vez que el mouse volviera a salir por arriba, pero probándolo quedó claro
  que no: esa opción solo hace que la librería ignore la cookie que evitaría
  mostrarlo de nuevo en una **visita futura** a la página. Dentro de la
  misma carga, el propio callback interno que muestra el modal desconecta
  los listeners de `mouseleave`/`mouseenter`/`keydown` apenas se dispara una
  vez, sin excepción -- una segunda salida por arriba en la misma carga no
  reabre nada, y el test que lo asume quedó escrito después de confirmarlo
  contra el sitio real, no antes.
- `/floating_menu` usa la librería `stickyfloat`, que **no** cambia el menú a
  `position: fixed` (lo que el navegador resolvería solo, sin ningún
  JavaScript en cada scroll): el elemento se queda `position: absolute`
  todo el tiempo, y es la propia librería la que, en cada evento de scroll,
  recalcula a mano el `top` inline para que la caja siga pareciendo clavada
  cerca del borde superior. Por eso el test no afirma nada sobre el valor de
  `top` en sí (que crece sin límite junto con el scroll) sino sobre la
  posición resultante en pantalla (`bounding_box()`): sin esta librería, un
  elemento `position: absolute` ubicado a 32px del tope del documento
  terminaría en `y = 32 - 2000 = -1968` (bien afuera del viewport) después
  de un scroll de 2000px, y que siga apareciendo pegado arriba es la prueba
  de que algo lo está reposicionando activamente en cada frame.
- `/infinite_scroll` usa la librería `jscroll`, que no agrega contenido ante
  "cualquier" scroll sino solo cuando el scroll deja el final del documento
  lo bastante cerca del borde inferior del viewport -- por eso el contenido
  nuevo no aparece envuelto en `<p>` (no hay ningún `<p>` en toda la página,
  el texto se agrega como texto plano dentro de un `<div class="jscroll-added">`)
  y el test lo ubica por esa clase en vez de por una etiqueta semántica que
  no existe. El primer párrafo se carga solo, sin ningún scroll de por
  medio, y cuánto más contenido aparece así depende de la altura del
  viewport: con uno chico alcanza y sobra un solo párrafo para llenarlo, con
  uno más alto (como el default de 1280x720 de este repo) ya entran dos
  antes de tocar nada. Afirmar un número fijo de párrafos "al cargar" sería
  asumir un viewport puntual que nada garantiza -- el test solo pide que
  haya como mínimo uno, y mide todo lo demás por la diferencia entre el
  conteo de antes y de después de cada scroll, no por un valor absoluto.
  Para confirmar que el umbral importa de verdad, un scroll corto que no
  llega al fondo (`window.scrollTo(0, 50)`) se prueba por separado contra
  uno que sí llega (`document.body.scrollHeight`): solo el segundo agrega
  contenido.
- `/redirector` linkea con `href='redirect'`, una URL relativa sin barra
  inicial. La regla de resolución de URLs relativas no toma el nombre de
  la página actual como si fuera una carpeta: como `/redirector` no
  termina en `/`, su "directorio" es la raíz del sitio, así que el link
  resuelve a `{BASE_URL}/redirect`, no a `{BASE_URL}/redirector/redirect`
  como sugeriría intuitivamente el nombre de la página (esa URL ni
  siquiera existe, devuelve 404). El test lo verifica con `requests`
  contra las dos URLs antes de tocar el navegador, para separar la
  resolución de la URL del comportamiento del click, y después confirma
  con `page.expect_navigation()` que clickear el link real termina en
  `/status_codes`.
- DOM enorme y anidado (`/large`): un elemento sin hermanos envuelto en 50
  `<div>` sin class ni id, uno dentro del otro, que se ubica por id tan
  directo como si estuviera en la raíz del documento. La sección "Siblings"
  resulta no ser tan plana como su nombre sugiere: item-2 e item-3 de cada
  tier sí son hermanos reales entre sí, pero item-1 no es su hermano sino su
  padre, y ese mismo `<div>` se queda abierto hasta contener completo al
  tier siguiente -- el item-1 del tier 1 termina siendo ancestro de los 49
  tiers restantes. Por último, la tabla de la página es una grilla completa
  de 50 filas por 50 columnas (2500 celdas) con un `<thead>` propio, no las
  6 columnas visibles sin hacer scroll horizontal -- contar `tr` sin
  filtrar por `tbody` da 51 filas en vez de 50.
- `/login` mantiene sesión real del lado del servidor (una cookie
  `rack.session`, no un token en `localStorage` ni un router de puro
  cliente): la prueba de que `/secure` está protegida de verdad no es
  afirmar un `expect()` sobre un mensaje en pantalla, sino navegar
  directo a `/secure` en un `page` nuevo, sin haber llamado a `login()`
  antes, y confirmar que el propio servidor redirige a `/login` --
  reproduciendo con curl el mismo POST a `/authenticate` confirmó antes de
  escribir el test que el error de usuario inválido y el de contraseña
  inválida son mensajes de texto distintos (`"Your username is invalid!"`
  vs. `"Your password is invalid!"`), y que mandar los dos mal a la vez
  prioriza siempre el de usuario, sin mezclar ambos mensajes en una sola
  aserción genérica de "hubo un error".
- `/dynamic_controls` no deshabilita el botón con un atributo CSS ni con
  una clase: `disableButton()` hace `$(locator).attr("disabled", true)`
  de forma sincrónica, dentro del mismo handler de click, antes de arrancar
  el `setTimeout` de 3 segundos. Eso significa que un segundo click
  disparado mientras el primero todavía está en el delay nunca llega a
  ejecutar nada -- Playwright rechaza clickear un botón disabled y tira
  timeout de "actionability" en vez de silenciosamente no hacer nada, y el
  test usa ese mismo timeout como la prueba de que el bloqueo es real.
- El checkbox que `toggleCheckboxControls()` reinserta no es el mismo HTML
  que el original: la página arranca con `<div id="checkbox"><input></div>`
  (el id vive en el div contenedor, el input no tiene ninguno), pero al
  agregarlo de nuevo el script inserta
  `<div><input id='checkbox'></div>` -- el id se mudó del div al input. Un
  locator que dependiera de "el input dentro de `#checkbox`" encontraría el
  checkbox inicial pero no el que vuelve tras un ciclo de quitar/agregar.
  La solución es ubicarlo por `#checkbox-example input[type='checkbox']`,
  que no le importa en qué elemento quedó el id en cada estado.

```bash
cd DesafiosPlaywright && python3 -m pytest -v
```

---

## UI Testing Playground — ocho formas distintas de estar "oculto", un botón que ignora clicks de JS, una tabla que se reordena sola, una barra de progreso al azar, un link que se reemplaza a sí mismo al pasarle el mouse, un botón cuyo id cambia en cada carga, un dato que tarda 15 segundos reales en llegar por AJAX, otro que tarda los mismos 15 segundos sin tocar la red, una página cuya propia carga tarda 5 segundos reales de servidor, un espacio invisible que rompe un XPath aparentemente correcto, tres botones idénticos a simple vista que solo se distinguen por una clase CSS entre varias, un input que un div superpuesto vacía solo si se escribe sin escrollarlo antes a la vista, un botón verde que queda tapado por uno azul idéntico en posición al clickearlo, un botón que solo cambia de nombre si el campo se edita de una forma que el navegador reconoce como real, un segundo diálogo nativo que aparece recién un segundo después de responder al primero, un generador de GUID escondido dentro de un shadow root que el DOM global ni siquiera puede ver, un botón que un contenedor con scroll recorta fuera de su área visible sin que `is_visible()` se dé cuenta, un texto visible en pantalla que no es igual, carácter a carácter, al nodo de texto crudo del DOM que lo contiene, y un formulario de login cuyos campos empiezan con id="username"/id="password" en el HTML real pero quedan con un GUID al azar apenas termina de cargar la página

Suite sobre uitestingplayground.com, un sitio diseñado a propósito para casos difíciles
de automatización (a diferencia de the-internet, acá el desafío es cada página puntual,
no el sitio completo).

**Cubre:**
- `/visibility`: un botón "Hide" oculta otros siete, cada uno con una técnica CSS/DOM
  distinta -- `display: none`, `visibility: hidden`, `opacity: 0`, ancho 0, posición
  fuera de pantalla, superposición con otro elemento y eliminación directa del DOM --
  verificando con qué técnicas `is_visible()` de Playwright coincide con lo que ve un
  usuario real y con cuáles no.
- `/click`: un botón que ignora clicks disparados por JavaScript y solo reacciona a un
  click físico de mouse, verificando ambos caminos -- `locator.click()` de Playwright sí
  lo activa, `element.click()` ejecutado vía `page.evaluate()` no.
- `/dynamictable`: una tabla de procesos (Name, CPU, Disk, Memory, Network) que en cada
  recarga cambia al azar tanto el orden de sus columnas como el de sus filas,
  verificando que el valor de CPU de Chrome ubicado por nombre de columna coincida con
  el que muestra el label de abajo, y que tanto las columnas como la posición de la
  fila de Chrome efectivamente cambien de orden entre recargas (no solo que el test
  "no falle" con un orden fijo).
- `/progressbar`: una barra que sube de 25% a 100% a un ritmo aleatorio y que hay que
  frenar lo más cerca posible del 75%, verificando el caso límite de frenarla antes de
  que arranque a moverse, el caso general de frenarla al llegar al 75%, que el label de
  resultado coincida con el valor real de la barra, y que `Stop` efectivamente corte el
  avance en vez de solo dejar de leerlo.
- `/mouseover`: dos links que, al pasarles el mouse por encima, se reemplazan a sí
  mismos por un clon con otro título y otra clase, verificando que el título y la clase
  cambian de verdad tras el hover, que dos clicks consecutivos suben el contador en 2 (el
  escenario que la propia página pide probar), que una referencia al nodo tomada *antes*
  del hover queda inválida y no se puede clickear, y que el segundo link -- descrito por
  la página como "idéntico" tras el reemplazo -- en realidad solo mantiene el título, no
  la clase.
- `/dynamicid`: un botón cuyo único atributo `id` es un UUID distinto en cada carga de
  página, verificando que el id efectivamente cambia entre recargas, que el id de una
  carga anterior deja de existir en el DOM tras recargar (la prueba concreta de por qué
  ubicarlo por ese atributo rompería el test a la primera recarga) y que un locator por
  rol y texto visible -- que no depende del id -- puede clickear el botón sin problema
  en tres recargas seguidas.
- `/ajax`: un botón que dispara un pedido real al servidor (`$.get("/ajaxdata")`) que
  tarda 15 segundos en responder antes de que aparezca un `<p>` con el texto cargado,
  verificando que no hay contenido antes del click, que el spinner aparece de inmediato
  al clickear (lo muestra el propio handler, no la respuesta) y que, tras esperar
  explícitamente a que la etiqueta aparezca, el texto es el esperado y el spinner ya
  no está visible.
- `/clientDelay`: un botón casi idéntico al de `/ajax` -- mismo spinner, mismos 15
  segundos de espera -- pero que calcula el resultado íntegramente en el navegador
  con un `setTimeout`, verificando que el contenido y el spinner arrancan igual que
  en `/ajax` (vacío y oculto), que tras esperar aparece el texto correcto y el
  spinner se oculta, y -- la diferencia real entre ambos casos -- que ningún pedido
  `xhr`/`fetch` se dispara entre el click y que el texto aparece.
- `/loaddelay`: una página cuyo servidor tarda ~5 segundos reales en mandar la
  respuesta antes de que el navegador termine de cargarla -- a diferencia de
  `/ajax` y `/clientDelay`, donde la página carga al toque y el retraso aparece
  recién después de un click -- verificando que la propia navegación
  (`page.goto()`) queda bloqueada al menos esos segundos, que el botón ya está
  visible apenas termina de cargar sin necesitar ningún wait_for adicional, y
  que esa demora no dispara ningún pedido `xhr`/`fetch` de por sí.
- `/nbsp`: un botón cuyo texto visible es idéntico a simple vista a "My Button", pero
  el espacio real entre las dos palabras es un carácter non-breaking space (`\xa0`), no
  un espacio común, verificando que un XPath con `text()='My Button'` (espacio normal)
  no encuentra nada, que el mismo XPath con un nbsp sí encuentra el botón, que el texto
  crudo del elemento efectivamente contiene ese carácter, y que un locator por rol y
  texto visible encuentra y clickea el botón sin que haga falta saber nada de esto.
- `/classattr`: tres botones con el mismo texto visible ("Button"), cada uno con varias
  clases CSS a la vez (`btn class1 btn-success btn-test`, `btn class2 btn-warning
  btn-test`, `btn class3 btn-primary btn-test`), verificando que un XPath que compara el
  atributo `class` completo contra un único valor no encuentra ninguno de los tres, que
  un selector CSS por clase sí encuentra exactamente el botón correcto, que clickearlo
  dispara un `alert` nativo con el texto exacto que distingue a ese botón de los otros
  dos, y que clickear cualquiera de los otros dos no dispara ningún diálogo.
- `/alerts`: tres botones (Alert, Confirm, Prompt) que abren diálogos nativos del
  navegador, verificando el mensaje exacto de cada uno, que aceptar o cancelar el
  Confirm dispare, un segundo después, un SEGUNDO `alert` con "Yes" o "No" según la
  respuesta, que aceptar el Prompt con un texto dispare ese mismo texto en el segundo
  alert ("User value: ..."), y que cancelarlo lo reemplace por "no answer" en vez de un
  valor vacío.
- `/shadowdom`: un componente `<guid-generator>` (Custom Element con
  `attachShadow({mode: "open"})`) que vive en un shadow root propio, fuera
  del documento principal, verificando que `page.locator("#editField")` lo
  encuentra igual que a cualquier otro elemento mientras que
  `document.querySelector("#editField")` desde el documento global no ve
  nada, que el botón de generar carga un valor con formato de GUID válido en
  el input, que dos clicks seguidos dan dos GUIDs distintos, y que el botón
  de copiar al clipboard dispara un error real de la página en este deploy
  puntual en vez de copiar nada.
- `/scrollbars`: un botón ubicado dentro de un contenido de 600x300 recortado
  por un contenedor de 300x150 con scroll propio, verificando que la posición
  real del botón cae afuera del rectángulo visible del contenedor en los dos
  ejes a la vez, que `is_visible()` de Playwright no detecta ese recorte y
  sigue dando `True`, que clickearlo sin ningún scroll manual previo escrolea
  el contenedor automáticamente en ambos ejes antes de clickear, y que
  `force=True` -- que bypassea otras verificaciones de "actionability" --
  sigue escrolleando igual, porque ese paso no depende de `force`.
- `/verifytext`: un `<span>` cuyo texto visible en pantalla ("Welcome
  UserName!") no es el mismo string que su nodo de texto crudo del DOM --
  tiene un `<span>` anidado alrededor de "UserName" y espacios/saltos de
  línea de más que el navegador normaliza al renderizar --, verificando que
  un XPath de igualdad exacta (`//span[.='Welcome UserName!']`) no encuentra
  nada, que la misma comparación con `normalize-space()` sí encuentra
  exactamente ese span, que `get_by_text(exact=True)` de Playwright coincide
  con el mismo elemento, y que la variante sin `exact` -- que busca la frase
  como substring en toda la página -- también matchea, sin ninguna relación
  con lo que hay que automatizar, los dos bloques `<code>` de la propia
  tabla "Does not work / Works" que imprimen el enunciado de la página como
  texto plano.
- `/sampleapp`: un formulario de login donde cualquier nombre de usuario no
  vacío junto con la password `pwd` loguea con éxito, verificando el mensaje
  de bienvenida con el nombre ingresado, que una password incorrecta y un
  usuario vacío (con la password correcta) dan el mismo mensaje de error y
  limpian los dos campos, que el mismo botón pasa de "Log In" a "Log Out" al
  loguearse y que clickearlo de nuevo ya logueado revierte todo el estado al
  original, y que el id real de los campos de usuario y contraseña no es un
  valor fijo: no existe apenas carga la página y cambia otra vez en cada
  recarga.

**Desafíos técnicos resueltos:**
- `is_visible()` de Playwright no es un sinónimo de "el usuario lo ve": solo mira el
  layout (bounding box) y los estilos `visibility`/`display`. Un botón con
  `opacity: 0` o movido a `position: absolute; left: -9999px` sigue dando
  `is_visible() == True`, porque conserva tamaño y `visibility: visible` -- son
  técnicas que esconden algo a simple vista sin que Playwright las detecte. El único
  caso que de verdad lo engaña es el que no toca ningún estilo del botón: superponerle
  otro elemento encima. `is_visible()` no mira qué hay delante, así que también da
  `True`, pero ahí un click real sí choca con esa capa y termina en timeout de
  "actionability" en vez de llegar al botón -- la única forma de confirmar la
  superposición no es leer un estado, es intentar clickear y ver que falla.
- `display: none` sí saca al elemento del flujo de layout (`bounding_box()` devuelve
  `None`); `visibility: hidden` y ancho 0, en cambio, conservan un bounding box pero
  Playwright los trata igual como no visibles -- dos resultados iguales
  (`is_visible() == False`) por razones de DOM distintas.
- El botón "Hide" depende de un handler de jQuery cargado desde un CDN externo
  (`code.jquery.com`). Si esa descarga no llega a tiempo, el click no dispara nada y
  `$` queda indefinido sin ningún error visible en el test -- solo se nota después,
  esperando en vano un cambio que nunca iba a pasar. La solución espera explícitamente
  a que `$` esté definido antes de clickear, y recarga la página si no llega a
  tiempo, en vez de asumir que la carga de scripts externos nunca falla.
- La capa que tapa al botón superpuesto se posiciona con jQuery `.position()` dentro
  del mismo handler de click: justo después del click, ese cálculo a veces todavía no
  corrió y la capa queda en su estado inicial (altura 0) por un instante. El test
  espera explícitamente a que la capa tenga altura real antes de afirmar nada sobre
  la superposición, en vez de asumir que el click ya dejó todo listo.
- `/click` filtra el evento de click en su propio handler con la condición
  `event.screenX > 0`: un click sintético disparado desde JavaScript
  (`elemento.click()`) no trae coordenadas de pantalla reales -- queda en
  `screenX == 0` -- y el handler lo descarta en silencio, sin lanzar ningún
  error que delate que "no pasó nada". `locator.click()` de Playwright, en
  cambio, dispara el click a través del protocolo de DevTools como un evento
  de mouse físico de verdad, con coordenadas reales, y sí pasa el filtro. El
  test prueba las dos formas sobre el mismo botón para dejar esa diferencia
  documentada en código, no solo en la descripción de la página.
- `/dynamictable` no usa un `<table>` HTML ni un plugin de JS como la tabla
  ordenable de `/tables`: son `<div>` con atributos ARIA (`role="row"`,
  `role="columnheader"`, `role="cell"`), y tanto el orden de las columnas
  como el de las filas se vuelve a tirar al azar en cada recarga, salvo la
  columna del nombre de proceso, que siempre queda primera. Un locator por
  índice fijo (`.nth(1)` para "la columna de CPU") funciona en la primera
  carga y falla en la siguiente sin ningún aviso, porque sigue devolviendo
  una celda real, solo que de otra columna. La solución es preguntarle a los
  propios encabezados en qué posición está "CPU" antes de leer la celda, en
  vez de asumir una posición. Dos tests aparte confirman que el supuesto que
  obliga a esa solución es real: hacen varias recargas y verifican que el
  orden efectivamente cambió al menos una vez, para no quedarse validando
  contra una sola distribución posible por casualidad.
- `/progressbar` calcula el delay entre pasos una sola vez por cada click en
  Start (al azar entre 0 y 499ms) y lo reusa en los ~50 pasos que faltan
  hasta el 75% -- en el peor caso, llegar del 25% al 75% puede tardar más de
  24 segundos. Un timeout corto confundiría ese caso límite, real y válido,
  con una falla de la página, así que el test espera con un margen generoso
  en vez de asumir un ritmo fijo. Además, el primer incremento no sigue ese
  delay random: está programado con un `setTimeout` fijo de 1000ms, separado
  del resto -- eso permite un test 100% determinístico (Start seguido de
  Stop sin ninguna espera siempre cae en esa ventana fija) en un desafío que
  por diseño es aleatorio. Por último, el propio label de resultado de la
  página trata el 25% como "todavía no arrancó" (`ratio == 25 ? "n/a" :
  ratio - 75`) en vez de mostrar `-50`: asumir la resta sin leer el código
  fuente hubiera hecho fallar ese test determinístico contra el sitio real.
- `/mouseover` está diseñada a propósito para reproducir el "stale element
  problem" de Selenium: el handler de `onmouseenter` no modifica el `<a>`
  original, lo clona (`cloneNode`), le cambia atributos al clon y reemplaza
  el nodo viejo por el nuevo con `removeChild`/`appendChild`. Guardar una
  referencia al elemento con `page.query_selector()` (el equivalente de
  Playwright a un `WebElement`) y clickearla después del hover falla con
  "Element is not attached to the DOM", porque esa referencia sigue
  apuntando al nodo que ya no existe en el documento -- confirmado
  explícitamente leyendo `el.isConnected` antes de intentar el click, no
  solo capturando la excepción. Un `Locator` no tiene este problema porque
  no guarda un nodo: se vuelve a resolver contra el DOM actual en cada
  acción, así que dos `.click()` seguidos sobre el mismo `Locator` -- el
  escenario que la página pide probar explícitamente -- siempre encuentran
  el clon vigente y suben el contador de a uno por click, sin perder
  ninguno.
- La página describe el segundo link ("Link Button") como uno que "se
  reemplaza con uno idéntico" al pasarle el mouse, a diferencia del primero
  (que cambia de título). Leyendo el código fuente, `linkButtonActive()` le
  cambia la clase a `text-warning` igual que al primero -- la única
  diferencia real contra el primer link es que el título no cambia
  (`title="Link Button"` se mantiene en las dos versiones). "Idéntico"
  describe el título, no el resto del clon, y el test lo verifica
  explícitamente en vez de asumir la descripción de la página al pie de la
  letra.
- El id de `/dynamicid` es un UUID (`4e044870-4ee7-...`), que casi siempre
  arranca con un dígito. Un selector CSS de id no puede empezar con un
  dígito sin escaparlo: interpolar el id crudo en un locator tipo
  `page.locator(f"#{id}")` no "no encuentra nada" cuando ese id ya no
  existe tras recargar -- tira directamente un `SyntaxError` de selector
  inválido, porque `#4e04...` ni siquiera es CSS válido. El test confirma
  esa ausencia con un selector de atributo (`[id="..."]`) en su lugar, que
  no tiene esa restricción.
- `/ajax` no simula el delay en el cliente: el botón llama a `/ajaxdata`, un endpoint
  real del servidor que tarda 15 segundos exactos en responder antes de que el
  callback de `$.get()` inserte el `<p>` con el resultado -- confirmado midiendo la
  respuesta directamente con `curl` antes de escribir el test. Un timeout por
  defecto de Playwright (5 segundos) falla ahí siempre, no por flaky: el test espera
  la etiqueta con un timeout explícito por encima de esos 15 segundos reales, en vez
  de asumir que todo delay de AJAX es cosa del cliente.
- `/clientDelay` y `/ajax` se ven y se comportan idéntico desde afuera: mismo
  botón, mismo spinner, los mismos 15 segundos de espera antes de que aparezca el
  texto. La diferencia está en qué pasa por detrás. `/ajax` dispara un
  `$.get("/ajaxdata")` real, un pedido de red que un servidor tarda 15 segundos en
  responder. `/clientDelay`, en cambio, llama a `CreateLabel()`, que no pide nada a
  ningún servidor: programa el mismo texto con un `setTimeout(fn, 15000)` del propio
  navegador. Confirmado capturando los eventos `request` de Playwright durante la
  espera: en `/clientDelay` el único pedido que se dispara es el de una fuente de
  ícono ya en caché, ninguno de tipo `xhr` ni `fetch` -- a diferencia de lo que
  pasaría en `/ajax`, donde el pedido a `/ajaxdata` sí aparecería en esa misma
  lista. Dos páginas que un test visual no podría distinguir, pero que son dos
  problemas de automatización distintos: esperar una respuesta de servidor no es lo
  mismo que esperar a que el navegador termine de ejecutar su propio JavaScript.
- `/loaddelay` no simula nada en el navegador: medido directamente con
  `curl -w "%{time_total}"` antes de escribir el test, el servidor tarda
  ~5 segundos exactos en mandar el documento HTML completo, así que
  `page.goto()` queda bloqueado todo ese tiempo y recién devuelve el control
  cuando la página ya terminó de cargar -- por eso el botón ya está visible
  apenas vuelve `goto()`, sin ningún `wait_for` extra. Es el mismo síntoma
  visible que `/clientDelay` (una espera de varios segundos antes de ver
  contenido) pero por una causa opuesta a las de `/ajax` y `/clientDelay`:
  ahí la página carga instantánea y el delay llega recién después de un
  click (vía red real o `setTimeout` del navegador); acá el delay es previo
  a que la página exista para el navegador. Confirmado también capturando
  eventos `request` durante la navegación: ninguno es `xhr` ni `fetch`,
  porque no hace falta ninguna llamada aparte -- todo el retraso va en la
  respuesta del propio documento.
- El HTML de `/nbsp` escribe el texto del botón como `My&nbsp;Button`, que un
  navegador renderiza exactamente igual que "My Button" con espacio normal -- no hay
  ninguna diferencia visual que delate el problema. Un XPath `//button[text()='My
  Button']` escrito con el espacio que se ve en pantalla compara contra el string
  literal `"My Button"` carácter por carácter, y `\xa0 != 0x20`, así que no encuentra
  nada aunque el botón esté ahí. `locator.text_content()` confirma la causa exacta:
  el string real devuelto es `'My\xa0Button'`. El motor de texto propio de Playwright
  (el que usan `get_by_text()` y `get_by_role(name=...)`), a diferencia de XPath,
  normaliza nbsp a espacio común antes de comparar -- por eso un locator por rol y
  texto visible encuentra el mismo botón sin que el test necesite saber que ese
  espacio es distinto, mientras que el XPath literal del enunciado de la página sigue
  fallando tal como está escrito.
- `scroll_into_view_if_needed()` de Playwright no resuelve el caso de
  `/overlapped`: confirmado con `bounding_box()` antes y después de llamarlo,
  no mueve el scroll del contenedor interno un solo píxel, porque Playwright
  solo escrolea si el elemento no intersecta el viewport -- y `#name` ya es
  parte del viewport visible, lo que lo tapa es otro elemento encima, no un
  recorte de pantalla. `fill()` sobre ese input "funciona" sin error ninguno
  (el campo pasa el chequeo de actionability de Playwright, que no mira qué
  hay delante), pero la propia página detecta la superposición por su
  cuenta: un listener de `input` calcula el punto central del campo con
  `getBoundingClientRect()` y pregunta con `elementFromPoint()` qué elemento
  hay ahí, y mientras la respuesta sea el `<div>` gris en vez del input, borra
  el valor que se acababa de escribir. La solución real es forzar el scroll
  del contenedor con JavaScript (`el.evaluate("el => el.scrollIntoView()")`),
  que sí reubica al input fuera del área que tapa el div -- un caso donde el
  método de Playwright pensado justamente para esto no alcanza, y hay que
  bajar un nivel más.
- El atributo `class` de `/classattr` no es un valor único: es una lista de tokens
  separados por espacio (`btn class3 btn-primary btn-test`). Un XPath que compara el
  atributo completo con `@class='btn-primary'` -- el propio ejemplo que la página
  muestra como "esto no funciona" -- exige una igualdad exacta de todo el string, así
  que nunca encuentra el botón aunque `btn-primary` sea una de sus clases reales. Un
  selector CSS por clase (`button.btn-primary`), en cambio, busca dentro de la lista
  completa de tokens, no un match exacto del atributo entero. El `get_by_role()` por
  nombre visible tampoco sirve para distinguir el botón correcto acá: los tres
  muestran "Button" (el nombre accesible normaliza y recorta los espacios de más que
  tiene el tercero en el HTML), así que el único diferenciador real es la clase. El
  handler de la página (`event.target.className.indexOf("btn-primary")`) confirma que
  el criterio del propio sitio también es por clase, no por texto ni por posición: el
  test lo verifica clickeando los tres botones por separado y comprobando que solo uno
  dispara el `alert`.
- `/overlapped`: un input (`#name`) dentro de un contenedor con scroll interno
  (`overflow-y: scroll`), parcialmente tapado por un `<div>` gris posicionado de forma
  absoluta encima suyo, verificando que escribir en el campo sin escrollarlo antes a la
  vista termina con el campo vacío, que escrollarlo primero hace que el texto quede
  cargado, y que ese mismo scroll también libera a `#subject` (que arranca más abajo
  en el contenedor).
- `/hiddenlayers`: un botón verde que, al clickearlo, hace aparecer un botón azul
  superpuesto exactamente en el mismo lugar (mismo `bounding_box()`), confirmado por
  `ClickEventHandler` agregando un nuevo `.spa-view` con z-index más alto dentro del
  mismo contenedor `position: relative`. Un segundo click normal de Playwright sobre
  el locator del botón verde ya tapado no clickea a ciegas lo que haya debajo: el
  chequeo de actionability exige que el punto reciba eventos de puntero, y como el
  azul está encima, el click reintenta hasta el timeout sin dispararse nunca. Forzar
  ese click (`force=True`) tampoco "engaña" a la página para tratarlo como un click en
  el verde: el evento se dispara en esas coordenadas, pero el navegador resuelve el
  `target` real por hit-testing contra lo que hay ahí en ese momento, y el propio
  handler de la página lo confirma logueando "Blue button pressed", no "Green button
  pressed". La forma correcta de automatizar el escenario -- el que la propia página
  describe como "make sure that green button can not be hit twice" -- no es forzar el
  locator viejo, sino clickear el locator del elemento vigente (`#blueButton`), que
  pasa el chequeo de actionability sin problema porque de verdad es el tope del stack.
- `/textinput`: un botón cuyo texto cambia al valor escrito en un input, pero solo si
  el navegador considera que el campo fue editado de verdad, no por cualquier forma de
  llenarlo. Depende de dos variables globales que la página actualiza por separado
  (`document.NewButtonNameI` en cada evento `input`, `document.NewButtonNameC` en cada
  evento `change`) y solo cambia el botón cuando, al clickearlo, las dos coinciden.
  `fill()` no dispara `change` por sí mismo -- confirmado leyendo
  `document.NewButtonNameC` justo después de un `fill()` sin haber clickeado nada
  todavía, que da `None` -- pero sí deja el campo marcado como "editado" para el
  navegador, así que el `change` real llega recién al perder el foco, que es lo que
  hace el propio click del botón, y con el valor correcto. El tipeo físico
  (`press_sequentially()`) llega al mismo resultado por el mismo motivo. Asignar
  `.value` por script en vez de con `fill()` no deja al campo marcado como "editado":
  perder el foco después no dispara ningún `change` nativo, y el botón se queda con su
  texto original. Un evento `input` disparado a mano con `dispatchEvent()` sí
  actualiza `NewButtonNameI` (el handler no distingue de dónde vino el evento), pero
  tampoco pasa por ninguna API real de edición de texto: el `change` nativo al perder
  foco nunca llega y `NewButtonNameC` queda `undefined`. Esto separa dos cosas que a
  simple vista parecen la misma: si un evento `input`/`change` se disparó, y si el
  navegador considera que el campo fue editado por el usuario a los fines de un
  `change` nativo posterior -- lo primero no implica lo segundo. Por último, disparar
  `input` y `change` a mano pero con valores distintos entre sí tampoco actualiza el
  botón: el handler exige que ambas variables coincidan, no solo que existan.
- `/alerts` no deja ningún rastro en el DOM de qué pasó: a diferencia de
  `/javascript_alerts` (DesafiosPlaywright), acá Confirm y Prompt no escriben ningún
  resultado en una página -- lo único que producen es un SEGUNDO `alert()` que la
  propia página dispara con `setTimeout(fn, 1000)` recién después de responder al
  primero. Un `page.once("dialog", ...)` como el que alcanza para `/javascript_alerts`
  se queda corto acá: hay dos diálogos por interacción, no uno, así que el test
  registra el handler con `page.on()` (no `once`) para capturar ambos, y lo saca
  explícitamente con `page.remove_listener()` al final de cada caso para no dejarlo
  pegado. Como el segundo diálogo llega después de que el primer `click()` ya
  retornó, hace falta un `page.wait_for_timeout()` posterior antes de poder leer la
  lista de diálogos capturados -- no hay ningún elemento al que hacerle `expect()`
  que resuelva la espera por sí solo. El valor del Prompt cancelado tampoco es un
  string vacío: el propio JS de la página reemplaza el `null` que devuelve
  `dialog.dismiss()` por el string `"no answer"` antes de mostrar el segundo alert,
  así que cancelar y aceptar con un campo vacío no dan el mismo resultado.
- `/shadowdom` mete el input y los dos botones dentro de un shadow root
  abierto (`attachShadow({mode: "open"})`) de un Custom Element
  (`<guid-generator>`), no en el `<body>` del documento. Confirmado con
  `document.querySelector("#editField")` ejecutado por `page.evaluate()`
  desde el documento principal: devuelve `null`, porque las APIs nativas del
  DOM no atraviesan el límite de un shadow root por default. `page.locator()`
  de Playwright sí lo encuentra con el mismo selector CSS de toda la vida
  (`#editField`), sin ninguna sintaxis especial ni tener que pedir
  `shadowRoot` a mano -- a diferencia de Selenium clásico, donde hay que
  resolver el `shadow-root` como un paso explícito antes de poder buscar
  dentro. El enunciado de la propia página pide comparar el valor del
  clipboard contra el input después de clickear "copiar", pero contra este
  deploy puntual (servido por `http://`, no `https://`) eso no se puede
  cumplir: la Clipboard API ni siquiera existe ahí, confirmado con
  `typeof navigator.clipboard === "undefined"` antes de clickear nada -- no
  es un permiso denegado (`context.grant_permissions()` no cambia nada,
  probado explícitamente), es que el navegador no expone esa API fuera de un
  contexto seguro (https o localhost). El handler de la página llama a
  `navigator.clipboard.writeText(...)` sin ningún `try/catch` alrededor, así
  que el click no falla en silencio: dispara un error real de la página,
  capturado con `page.on("pageerror")`, con "writeText" en el mensaje. El
  test verifica ese error real en vez de simular el escenario completo que
  la página describe, que en este deploy es directamente imposible de
  automatizar tal como está escrito.
- `/scrollbars` recorta un botón fuera del área visible de un contenedor de
  300x150 con scroll propio (su contenido real mide 600x300), así que su
  posición de página cae afuera del rectángulo visible en los dos ejes a la
  vez -- y aun así `is_visible()` sigue dando `True`, porque solo mira
  layout y estilos del elemento mismo, no si un ancestro con `overflow`
  lo está recortando. A diferencia de Selenium, donde este caso clásico
  exige un `scrollIntoView()` manual antes de clickear (o falla
  directamente), el paso de "actionability" de `locator.click()` de
  Playwright escrolea el contenedor más cercano por su cuenta, en ambos
  ejes, antes de clickear -- confirmado leyendo `scrollLeft`/`scrollTop`
  del contenedor antes y después del click, sin ningún scroll manual de
  por medio. Ese scroll además es un paso aparte de las demás
  verificaciones de "actionability" (visible, habilitado, estable, que
  nada más reciba el evento): `force=True`, que sí bypassea esas otras,
  sigue escrollando igual.
- `/verifytext` tiene, dentro de `div.bg-primary`, un único
  `span.badge-secondary` con el markup `Welcome <span>UserName</span>!`
  envuelto en indentación y saltos de línea propios del HTML fuente. El
  string-value de XPath de ese span (`.`) concatena el texto de todos sus
  nodos descendientes tal cual están en el markup, así que
  `//span[.='Welcome UserName!']` no es igual, carácter a carácter, al
  resultado -- confirmado leyendo `text_content()` del propio elemento,
  que devuelve la frase rodeada de espacios y saltos de línea en vez del
  string limpio. `normalize-space()` colapsa ese espacio en blanco interno
  y recorta los extremos antes de comparar, y encuentra el span sin
  ambigüedad porque es el único elemento de toda la página cuyo texto
  normalizado es exactamente esa frase. `get_by_text(exact=True)` de
  Playwright se comporta igual que `normalize-space()` -- normaliza
  espacios antes de comparar -- y coincide con el mismo span, sin que el
  test necesite escribir ningún XPath. La variante sin `exact` (substring,
  sin acotar a ninguna sección) es la que expone el caso más interesante:
  la propia tabla "Does not work / Works" de la página imprime las dos
  expresiones XPath del enunciado como texto plano dentro de bloques
  `<code>`, y ese texto también contiene, de forma literal, la frase
  "Welcome UserName!" -- un locator por texto flexible sin acotar a la
  sección correcta encuentra 3 elementos en vez de 1, confirmado leyendo
  el `tagName` de cada coincidencia (`CODE`, `CODE`, `SPAN`), y dos de
  ellos son justamente el enunciado que describe el problema, no el
  elemento a automatizar. Acotar el locator al contenedor `div.bg-primary`
  de la sección "Playground" -- en vez de perseguir una condición de texto
  más estricta -- alcanza para que incluso la variante sin `exact=True`
  vuelva a dar 1 sola coincidencia.
- `/sampleapp` manda un HTML donde los inputs de usuario y contraseña tienen
  literalmente `id="username"` e `id="password"` -- confirmado pidiendo la
  página con `requests`, sin ejecutar ningún JavaScript. Pero un `<script>`
  inline, ubicado más abajo en el mismo documento, le asigna a cada uno un
  GUID al azar como nuevo id apenas el parser llega a esa línea -- antes de
  que Playwright termine de cargar la página y devuelva el control tras
  `goto()`. Un locator por `#username` no encuentra nada desde el primer
  momento, y ni copiando el GUID vigente alcanzaría para el día siguiente:
  se recalcula en cada recarga, confirmado comparando el id antes y después
  de un `page.reload()`. El atributo `name` (`UserName`/`Password`), que ese
  script nunca toca, es el único identificador estable entre cargas. El
  botón de login tampoco distingue entre dos elementos: es el mismo
  `<button id="login">` el que pasa a actuar como logout con solo cambiar
  una variable interna (`loggedIn`) y su propio texto visible, así que el
  test clickea ese mismo locator en los dos sentidos en vez de buscar un
  botón de logout que no existe como tal.

```bash
cd UiTestingPlaygroundTest && python3 -m pytest -v
```

---

## SauceDemo — Login, carrito, checkout completo, logout, ordenar productos y usuarios especiales

Tests de login (casos exitosos, errores y validaciones), agregado de productos al
carrito, el flujo completo de compra, el cierre de sesión, el ordenamiento del
catálogo y los usuarios de prueba que SauceDemo ofrece a propósito con bugs y
comportamientos distintos, con Page Objects para el login, el inventario y el
checkout.

**Cubre:**
- Ordenar el catálogo por precio (`lohi`, de menor a mayor, y `hilo`, de mayor a
  menor) con `standard_user`, verificando que el resultado coincide con la lista de
  precios ordenada numéricamente, y que dos productos con el mismo precio
  ($15.99) mantienen su orden relativo original en ambos sentidos
- Checkout de principio a fin: agregar un producto, ir al carrito, completar los tres
  pasos del checkout y llegar a la pantalla de confirmación
- Verificación de que el impuesto (8% del subtotal) y el total se calculan de verdad, no
  son un texto fijo en la página
- Que el carrito queda vacío después de confirmar la compra
- Validación del formulario de checkout: continuar sin completar los datos personales
  muestra un error y no avanza de pantalla
- `problem_user`: las seis imágenes del catálogo apuntan al mismo archivo (contra
  `standard_user`, donde las seis son distintas), y el selector de orden no reordena
  la lista para **ningún** criterio -- ni "Name (Z to A)" ni ninguno de los dos
  órdenes por precio (contra `standard_user`, donde los tres sí reordenan
  correctamente)
- `performance_glitch_user`: el login se repite varias veces con sesiones nuevas para
  confirmar que el delay artificial de ~5 segundos es intermitente, no constante
- Logout desde el menú hamburguesa: vuelve a la pantalla de login con el campo de
  usuario vacío, y la sesión queda realmente invalidada del lado cliente, no solo
  "oculta" -- ni volviendo con el botón atrás del navegador ni entrando de nuevo a
  `/inventory.html` a mano se puede ver el catálogo sin loguearse otra vez

**Desafíos técnicos resueltos:**
- El test que ya existía para `problem_user` solo probaba que "Name (Z to A)" no
  reordenaba el catálogo, y la descripción original del bug hablaba de ese criterio
  puntual. Probando los otros tres contra el sitio real antes de escribir el test de
  ordenar por precio, el `<select>` de orden tampoco reordena nada al elegir "Price
  (low to high)" ni "Price (high to low)": el bug no es específico de un criterio, es
  que el handler de cambio de orden no hace nada para ningún valor del `<select>` con
  este usuario. El test nuevo generaliza esa cobertura a los dos criterios de precio en
  vez de dar por sentado que solo afecta al que ya estaba probado.
- El catálogo tiene dos productos al mismo precio ($15.99: "Sauce Labs Bolt T-Shirt" y
  "Test.allTheThings() T-Shirt (Red)"), confirmado leyendo los precios reales antes de
  escribir el test. Comparar solo la lista de precios ordenada no alcanza para detectar
  un sort inestable que invirtiera el orden de los empatados entre `lohi` y `hilo` --
  numéricamente seguiría dando la lista correcta igual. El test de empate verifica por
  separado que esos dos nombres puntuales mantienen su orden relativo original en
  ambos sentidos, confirmando que el sort es estable y no solo numéricamente correcto.
- La versión actual de SauceDemo es una SPA (bundle servido con Vite): al hacer clic en
  "Checkout" o en "Continue", la URL cambia primero (`history.pushState`) y el
  componente de la página nueva recién se monta un instante después. Un locator
  consultado apenas se resuelve `wait_for_url()` a veces todavía encuentra el DOM de la
  página anterior -- por ejemplo, el formulario de datos personales devolvía `count()
  == 0` justo después de navegar a `/checkout-step-one.html`, porque el carrito
  seguía siendo lo único montado. La solución es esperar con `expect().to_be_visible()`
  sobre un elemento propio de la página nueva antes de interactuar con ella, en vez de
  confiar en que la URL ya implica que el contenido está listo. El mismo problema
  aparece al entrar al inventario con cualquier usuario: `wait_for_url()` por sí solo no
  alcanza, hace falta esperar a que el primer producto esté visible antes de leer nada.
- El impuesto que muestra el resumen de compra no es un 8% redondeado a ojo: es
  `round(subtotal * 0.08, 2)`. El test recalcula ese valor a partir del subtotal real
  que muestra la página en cada corrida, en vez de hardcodear un monto fijo, para que
  siga siendo válido si cambia el precio del producto usado en la prueba.
- Las imágenes "rotas" de `problem_user` no son imágenes caídas: las seis responden
  **200** y cargan con dimensiones reales (`naturalWidth`/`naturalHeight` distintos de
  cero), a diferencia del caso de `/broken_images` ya cubierto en DesafiosPlaywright. El
  bug es otro: el catálogo entero muestra el mismo archivo sin importar qué producto es,
  así que el test no verifica "que la imagen cargue" sino que las seis sean
  exactamente la misma, contra `standard_user` donde las seis son distintas entre sí.
- El delay de `performance_glitch_user` resultó no ser determinístico: midiendo 30
  logins seguidos contra el sitio real, el delay de ~5 segundos apareció en 21 de 30
  (70%), no en los 30. Un test que afirmara "este usuario siempre tarda más de 2
  segundos" sería flaky por diseño en el ~30% de corridas que caen rápidas. La solución
  es repetir el login varias veces con contextos nuevos (una sesión limpia por intento)
  y afirmar solo lo reproducible: que aparece al menos un login lento en varios
  intentos, sin exigir que todos lo sean. El cronómetro además tiene que envolver el
  `click()` del login entero, no solo el `wait_for_url()` posterior -- el delay ocurre
  durante la propia respuesta al click, así que medir después de que `login()` ya
  retornó siempre da un tiempo casi nulo, aunque el login en sí haya tardado 5 segundos.
- Después de hacer logout, pulsar atrás en el navegador deja la barra de direcciones
  apuntando de nuevo a `/inventory.html`, pero eso no es que la sesión haya quedado
  "viva" en caché: la propia app detecta que no hay sesión y redirige sola a `/`, solo
  que esa redirección es asíncrona. Leer la URL o el contenido del DOM justo después de
  `go_back()` es flaky -- a veces se llega a ver `/inventory.html` en blanco, sin
  productos, a mitad de camino de la redirección todavía no terminada. La solución es
  esperar explícitamente con `wait_for_url()` a que la URL vuelva a `/` antes de afirmar
  nada, en vez de confiar en que `go_back()` ya deja todo resuelto.
- Entrar directo a `/inventory.html` sin haber hecho login nunca dispara el mismo
  chequeo del lado cliente que usa logout: no hace falta loguearse y desloguearse para
  probar la protección de la ruta, alcanza con navegar directo a la URL protegida.
- Trece tests repetían a mano el mismo bloque de tres líneas (crear el `LoginPage`,
  navegar y loguearse) para después operar sobre el inventario. Ahora `TestX/conftest.py`
  suma dos fixtures, `login_as` y `inventory_as`, que reciben el usuario y devuelven el
  Page Object ya logueado -- `inventory_as` además espera a que la navegación a
  `/inventory.html` termine antes de devolver el `InventoryPage`. Los dos tests que
  miden cuánto tarda el login en sí (`performance_glitch_user` y la aserción de
  velocidad de `standard_user`) se dejaron sin tocar porque necesitan cronometrar el
  `login()` directamente, no un helper que ya incluye la espera.

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
- Paginación: metadata (`page`, `per_page`, `total`, `total_pages`), que las páginas no
  se superpongan, que `per_page` recalcule `total_pages`, y qué devuelve pedir una
  página fuera de rango
- Filtros de Restful Booker (`GET /booking?firstname=...&lastname=...&checkin=...&checkout=...`):
  por nombre solo, por nombre y apellido combinados, sin coincidencias, y por rango de
  fechas de estadía
- Códigos de error específicos de Restful Booker: `/auth` con password incorrecta, con
  username incorrecto y sin credenciales (los tres casos devuelven 200, no 401/403), un
  `PUT` sin token y uno con un token inventado (ambos 403, confirmando que la API valida
  el contenido del token y no solo que la cookie exista), y una reserva pedida con un id
  no numérico (404, el mismo que un id numérico inexistente)
- Contrato de schema de ReqRes (`jsonschema`): valida que `GET /users/<id>`, la lista de
  `GET /users` y el `POST /users` de creación cumplan la forma exacta del JSON que
  prometen (tipos, campos obligatorios, formato de `email` y de `avatar`), más dos tests
  que confirman que el propio esquema rechaza un documento inválido, para no confiar en
  un esquema que por error aceptara cualquier cosa
- JSONPlaceholder, parametrizado contra datos reales: tres usuarios conocidos
  (`id`, `name`, `email` verificados contra la API antes de escribirlos en el
  test, no copiados de memoria) y tres ids inexistentes (`9999`, `0`, `-1`),
  cada grupo corriendo como un solo `test_...[caso]` por `pytest.mark.parametrize`
  en vez de una función por caso

**Desafíos técnicos resueltos:**
- El `id` de un usuario es un entero en el `GET` (`"id": 2`) pero un **string** en la
  respuesta del `POST` de creación (`"id": "649"`). Son dos contratos distintos aunque
  el campo se llame igual: el esquema de creación no puede reusar el del `GET`, y el test
  de contrato lo deja explícito en vez de descubrirlo por un fallo críptico de tipos.
- Pedir una página que no existe (`?page=999`) no da 404: ReqRes responde **200** con
  `data: []`, y encima refleja el número de página pedido en el cuerpo aunque no exista.
  Un test que solo mirara el status code daría esa respuesta por una página más. El caso
  valida el cuerpo completo, no solo que la request "no falló".
- `total_pages` no es un valor fijo: depende de `per_page`. El test lo verifica
  calculándolo (`ceil(total / per_page)`) en vez de hardcodear el número que da con el
  `per_page` por defecto, para que siga siendo válido si el default cambia.
- El filtro `firstname` de Restful Booker exige coincidencia **exacta y sensible a
  mayúsculas**: ni una variante en minúsculas ni un substring del nombre real encuentran
  la reserva, a diferencia de un `LIKE` de SQL. `checkin`/`checkout` como filtro no
  buscan una fecha exacta, sino que delimitan un rango: una reserva entra si sus fechas
  caen dentro de ese rango, no si coinciden con los parámetros. Como es una API pública
  compartida con reservas de otros tests corriendo en paralelo, los casos identifican sus
  propias reservas con un `firstname` único por corrida (`uuid4`) y verifican pertenencia
  al resultado en vez de igualdad exacta de listas, para no depender de qué otros datos
  haya en ese momento en el sandbox — y las borran al terminar.
- `ApiTest` era la única suite de API sin `conftest.py`: cada test llamaba a
  `requests.get/post/put/delete` suelto, abriendo y cerrando una conexión TCP
  nueva por request en vez de reusarla como sí hacen `ReqResTest` y
  `RestfulBookerTest` con sus propios fixtures. Se agregó un fixture
  `session` (`requests.Session`, cerrada al terminar cada test) que ahora
  usan los cuatro archivos, y los dos tests de usuarios se migraron a
  `pytest.mark.parametrize` — antes eran tres funciones fijas (un usuario
  conocido y un único id inexistente, `9999`), ahora son dos listas de casos
  que se leen como datos, no como código repetido.
- `RestfulBookerTest` era la única de las tres suites de API sin `config.py`:
  `conftest.py` y `test_bookings.py` tenían la URL base escrita a mano en cada
  request (`test_bookings.py` la repetía 21 veces), mientras que
  `test_auth_errores.py` y `test_filtros.py` ya la habían extraído cada uno a
  su propia constante local, duplicada entre los dos archivos. Se agregó un
  `config.py` con el mismo patrón que `ApiTest`/`ReqResTest`
  (`BASE_URL = os.environ.get('BASE_URL', ...)`, así se puede apuntar a otro
  entorno sin tocar código) y los cuatro archivos ahora importan la misma
  constante en vez de tener cada uno su copia.

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
mismo nombre (`config.py` en cuatro de ellas). Corriendo todo junto desde la raíz, Python
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

**Un `__init__` idéntico repetido en 49 Page Objects.** `DesafiosPlaywright`,
`UiTestingPlaygroundTest` y `TestX` tenían exactamente el mismo patrón en cada Page
Object: `def __init__(self, page): self.page = page`, sin ningún type hint, copiado y
pegado 49 veces. Cada carpeta suma ahora un `base_page.py` con una clase `BasePage`
tipada (`page: Page`) de la que heredan todos sus Page Objects, que llaman a
`super().__init__(page)` en vez de repetir la asignación. El cambio es mecánico (no
toca ningún locator ni ninguna aserción) y se verificó corriendo las tres suites
completas, dos veces seguidas cada una, antes de commitear — mismos tests, mismos
resultados, con menos código repetido y con tipado explícito en el único punto que
todas comparten.

**La URL de JSONPlaceholder repetida a mano en los cuatro tests de `ApiTest`.** A
diferencia de `ReqResTest`, `RestfulBookerTest` y `UiTestingPlaygroundTest`, que ya
leen su URL base desde un `config.py` con `os.environ.get(...)`, `ApiTest` tenía
`"https://jsonplaceholder.typicode.com"` escrito literalmente en los cuatro archivos
de test. Cambiar de ambiente significaba editar cuatro strings sueltos en vez de una
sola constante, y nada impedía que alguno quedara desactualizado. Se sumó
`ApiTest/config.py` con el mismo patrón que las otras suites (`BASE_URL` con default y
override por variable de entorno) y los cuatro tests pasaron a importar `BASE_URL` en
vez de repetir la URL. Las aserciones y el comportamiento de cada test quedaron
idénticos: se corrió la suite dos veces seguidas antes de commitear, mismos 5 tests,
mismo resultado.

**Una línea muerta disfrazada de verificación, en `TestX/Inventory_Page.py`.**
`obtener_cantidad_carrito()` tenía un `assert self.obtener_cantidad_carrito() == "1"`
escrito *después* del `return` del método -- nunca se ejecutaba, y si por algún cambio
hubiera pasado a ejecutarse habría sido una llamada recursiva infinita. Probablemente
un `assert` de depuración que quedó pegado al método en vez de borrarse. Se eliminó al
sumar las fixtures `login_as`/`inventory_as` de `TestX/conftest.py` (ver SauceDemo más
arriba), que es lo que de verdad reduce la duplicación que el `assert` fallido
pretendía cubrir.

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

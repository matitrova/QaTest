# QaTest — Portfolio de QA Automation

[![Tests](https://github.com/matitrova/QaTest/actions/workflows/tests.yml/badge.svg)](https://github.com/matitrova/QaTest/actions/workflows/tests.yml)

Automatización de pruebas con **Python, Pytest y Playwright**, sobre interfaces web y
APIs REST. **178 casos de prueba** organizados con el patrón **Page Object Model**, que
corren en integración continua con **GitHub Actions** en cada push.

Incluye automatización sobre **ISPBoss**, un sistema real de gestión y facturación para
proveedores de internet en el que trabajé cuatro años como responsable de calidad.

## Qué cubre

| Suite | Sobre qué | Tests | Tipo |
|---|---|---|---|
| [`IspbossTest`](IspbossTest) | ISPBoss, sistema real (entorno beta) | 3 | UI · E2E |
| [`DesafiosPlaywright`](DesafiosPlaywright) | the-internet.herokuapp.com | 96 | UI |
| [`UiTestingPlaygroundTest`](UiTestingPlaygroundTest) | uitestingplayground.com | 21 | UI |
| [`TestX`](TestX) | SauceDemo (e-commerce) | 11 | UI |
| [`ReqResTest`](ReqResTest) | API de ReqRes | 20 | API |
| [`RestfulBookerTest`](RestfulBookerTest) | API de Restful Booker, con autenticación | 15 | API |
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

## Desafíos de Playwright — carga dinámica, upload, diálogos JS, checkboxes, dropdown, ventanas, hovers, slider, drag and drop, add/remove elements, basic auth, tablas, inputs numéricos, teclas, menú contextual, mensajes de notificación, códigos de status HTTP, elementos que aparecen y desaparecen, contenido que cambia de posición, recuperar contraseña, anuncio de entrada, imágenes rotas, intención de salida, menú flotante y scroll infinito

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

```bash
cd DesafiosPlaywright && python3 -m pytest -v
```

---

## UI Testing Playground — ocho formas distintas de estar "oculto", un botón que ignora clicks de JS, una tabla que se reordena sola, una barra de progreso al azar y un link que se reemplaza a sí mismo al pasarle el mouse

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

```bash
cd UiTestingPlaygroundTest && python3 -m pytest -v
```

---

## SauceDemo — Login, carrito y checkout completo

Tests de login (casos exitosos, errores y validaciones), agregado de productos al
carrito y el flujo completo de compra, con Page Objects para el login, el inventario y
el checkout.

**Cubre:**
- Checkout de principio a fin: agregar un producto, ir al carrito, completar los tres
  pasos del checkout y llegar a la pantalla de confirmación
- Verificación de que el impuesto (8% del subtotal) y el total se calculan de verdad, no
  son un texto fijo en la página
- Que el carrito queda vacío después de confirmar la compra
- Validación del formulario de checkout: continuar sin completar los datos personales
  muestra un error y no avanza de pantalla

**Desafíos técnicos resueltos:**
- La versión actual de SauceDemo es una SPA (bundle servido con Vite): al hacer clic en
  "Checkout" o en "Continue", la URL cambia primero (`history.pushState`) y el
  componente de la página nueva recién se monta un instante después. Un locator
  consultado apenas se resuelve `wait_for_url()` a veces todavía encuentra el DOM de la
  página anterior -- por ejemplo, el formulario de datos personales devolvía `count()
  == 0` justo después de navegar a `/checkout-step-one.html`, porque el carrito
  seguía siendo lo único montado. La solución es esperar con `expect().to_be_visible()`
  sobre un elemento propio de la página nueva antes de interactuar con ella, en vez de
  confiar en que la URL ya implica que el contenido está listo.
- El impuesto que muestra el resumen de compra no es un 8% redondeado a ojo: es
  `round(subtotal * 0.08, 2)`. El test recalcula ese valor a partir del subtotal real
  que muestra la página en cada corrida, en vez de hardcodear un monto fijo, para que
  siga siendo válido si cambia el precio del producto usado en la prueba.

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

**Desafíos técnicos resueltos:**
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

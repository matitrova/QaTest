<!-- tema: qatest -->

# Diálogos JS: por qué Playwright y Selenium no se manejan igual

Esta semana sumé al portfolio un caso que en Selenium se resuelve distinto que en Playwright, y la diferencia no es cosmética.

En Selenium, un alert/confirm/prompt se maneja después de que aparece: switch_to.alert. En Playwright no existe ese "después": si no registrás un listener de diálogo ANTES de disparar la acción que lo abre, Playwright lo descarta automáticamente y el test sigue como si nada.

La solución fue usar page.once("dialog", ...) justo antes del click, no page.on(...) fijo — así el handler no queda pegado a la page y no contamina los tests siguientes con un comportamiento pensado para un solo diálogo.

Terminé con 5 tests: alert simple, confirm aceptado y cancelado, prompt con texto y prompt cancelado. Los corrí varias veces seguidas antes de subirlos para descartar que fueran flaky.

Código acá: github.com/matitrova/QaTest

#Playwright #QAAutomation

---

**Para publicar:** copiá el texto de arriba, después abrí este link — te abre el compositor de LinkedIn con el repo ya adjunto como tarjeta (necesitás estar logueado en LinkedIn en el navegador que uses):
https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fgithub.com%2Fmatitrova%2FQaTest

Pegá el texto copiado en el cuadro de comentario ANTES de la tarjeta del link, después publicá. LinkedIn no permite precargar el texto por URL (lo sacó hace años para frenar spam), así que el pegado sigue siendo manual — este link solo evita tener que buscar "crear post" y pegar el link del repo a mano.

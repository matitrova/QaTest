<!-- tema: qatest -->

# Diálogos JS: por qué Playwright y Selenium no se manejan igual

Esta semana sumé al portfolio un caso que en Selenium se resuelve distinto que en Playwright, y la diferencia no es cosmética.

En Selenium, un alert/confirm/prompt se maneja después de que aparece: switch_to.alert. En Playwright no existe ese "después": si no registrás un listener de diálogo ANTES de disparar la acción que lo abre, Playwright lo descarta automáticamente y el test sigue como si nada.

La solución fue usar page.once("dialog", ...) justo antes del click, no page.on(...) fijo — así el handler no queda pegado a la page y no contamina los tests siguientes con un comportamiento pensado para un solo diálogo.

Terminé con 5 tests: alert simple, confirm aceptado y cancelado, prompt con texto y prompt cancelado. Los corrí varias veces seguidas antes de subirlos para descartar que fueran flaky.

Código acá: github.com/matitrova/QaTest

#Playwright #QAAutomation

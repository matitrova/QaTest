<!-- tema: mojonapp -->

# Cloudflare Pages: cuando el archivo de configuración es el que rompe las rutas

Esta semana encontré un bug de esos que solo aparecen en producción.

En mojonapp (mi app real, con Cloudflare Pages) había agregado un archivo `_redirects` para que las rutas del router no dieran 404 al recargar. Pero en vez de arreglarlas, las rompía: Pages no lo interpreta como un rewrite sino como un redirect 308 al destino "canonizado", así que entrar directo a `/contactos` rebotaba al mapa.

Lo verifiqué con curl contra la URL real:

```
HTTP/2 308
location: /
```

La solución fue sacar el archivo y entender el comportamiento nativo de Pages: ya devuelve `index.html` con 200 en cualquier ruta sin extensión, sin configurar nada. A veces la config de más rompe lo que ya andaba solo.

https://github.com/matitrova/mojonapp/commit/d9cf3a27246deaead215a9ad45bd1a7aa66f6cad

#WebDev #Debugging

---

**Para publicar:** copia el texto de arriba, despues abri este link -- te abre el compositor de LinkedIn con el repo ya adjunto como tarjeta (necesitas estar logueado en LinkedIn en el navegador que uses):
https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fgithub.com%2Fmatitrova%2Fmojonapp%2Fcommit%2Fd9cf3a27246deaead215a9ad45bd1a7aa66f6cad

Pega el texto copiado en el cuadro de comentario ANTES de la tarjeta del link, despues publicá. LinkedIn no permite precargar el texto por URL (lo sacó hace anios para frenar spam), así que el pegado sigue siendo manual -- este link solo evita tener que buscar "crear post" y pegar el link del repo a mano.

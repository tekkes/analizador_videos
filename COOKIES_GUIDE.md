# Cómo Arreglar el Error de "Sign in" en Render

YouTube bloquea a veces las descargas desde servidores en la nube (como Render). Para solucionarlo, necesitamos darle tus "cookies" (credenciales) para que se identifique como un usuario real.

## Paso 1: Obtener tus Cookies de YouTube

1.  Instala la extensión **"Get cookies.txt LOCALLY"** en tu navegador:
    *   [Chrome/Edge](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflccjobjhccjbm)
    *   [Firefox](https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/)
2.  Ve a [YouTube.com](https://www.youtube.com).
3.  Haz clic en el icono de la extensión.
4.  Haz clic en **"Export"** (o "Download"). Se descargará un archivo `cookies.txt` (o similar).
5.  Abre ese archivo con el Bloc de Notas.
6.  **Copia todo el texto** que hay dentro.

## Paso 2: Configurar Render

1.  Ve a tu Dashboard en [render.com](https://render.com).
2.  Entra en tu servicio **`analizador-videos-backend`**.
3.  Ve a la pestaña **"Environment"**.
4.  Haz clic en **"Add Environment Variable"**.
5.  Rellena los campos:
    *   **Key**: `YOUTUBE_COOKIES`
    *   **Value**: *(Pega aquí todo el texto que copiaste del archivo de cookies)*.
6.  Si el texto es muy largo, no te preocupes, pégalo entero.
7.  Haz clic en **"Save Changes"**.

## Método Alternativo (más fiable): "Secret Files"

Si el método anterior falla (a veces el texto es demasiado largo para Render), usa este:

1.  En tu Dashboard de Render, ve a la pestaña **"Environment"**.
2.  Haz clic en **"Secret Files"** (debajo de Environment Variables).
3.  Haz clic en **"Add Secret File"**.
4.  Configura:
    *   **Filename**: `cookies.txt`
    *   **File Content**: *(Pega aquí todo el texto de tus cookies)*.
5.  Haz clic en **"Save Changes"**.

Esto guardará el archivo en `/etc/secrets/cookies.txt`, y mi código lo detectará automáticamente.


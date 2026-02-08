# Guía de Despliegue en la Nube (Gratis)

Sigue estos pasos para tener tu aplicación disponible en internet.

## Parte 1: El Backend (Render)
El "cerebro" de la app necesita un servidor que soporte Python y FFmpeg.

1.  Crea una cuenta en [render.com](https://render.com/).
2.  Haz clic en **"New +"** y selecciona **"Web Service"**.
3.  Conecta tu cuenta de GitHub y selecciona el repositorio `analizador_videos`.
4.  Configura lo siguiente:
    *   **Name**: `analizador-videos-backend` (o lo que quieras).
    *   **Region**: `Frankfurt` (o la más cercana).
    *   **Branch**: `main`.
    *   **Root Directory**: `backend` (¡Importante!).
    *   **Runtime**: **Docker**.
    *   **Instance Type**: Free.
5.  **Variables de Entorno (Environment Variables)**:
    *   Añade una llamada `GOOGLE_API_KEY` con tu clave de Gemini.
6.  Haz clic en **"Create Web Service"**.

Render tardará unos minutos. Cuando termine, te dará una URL (ej. `https://analizador-videos-backend.onrender.com`). **Copia esa URL.**

## Parte 2: El Frontend (GitHub Pages)
La parte visual se alojará gratis en GitHub.

1.  Ve a tu repositorio en GitHub.
2.  Entra en **Settings** > **Pages**.
3.  En "Source", asegura que esté seleccionado **GitHub Actions**.
4.  Esto activará el despliegue automático que acabo de programar.

## Parte 3: Conectar Frontend y Backend
Ahora debemos decirle al Frontend dónde está el Backend de Render.

1.  En tu ordenador, ve a la carpeta `frontend`.
2.  Crea (o edita) el archivo `.env.production`:
    ```env
    VITE_API_URL=https://TU-APP-EN-RENDER.onrender.com
    ```
    *(Reemplaza la URL con la que copiaste de Render)*.
3.  Guarda, haz commit y push:
    ```bash
    git add .
    git commit -m "Configure production URL"
    git push
    ```

¡Listo! En unos minutos, tu app estará visible en `https://tekkes.github.io/analizador_videos/`.

# YouTube Video Analysis Tool

Este proyecto es una herramienta para analizar videos de YouTube, generando resúmenes, transcripciones y guías didácticas.

## Estructura del Proyecto

- `backend/`: Servidor API construido con FastAPI (Python).
- `frontend/`: Interfaz de usuario construida con React y Vite (JavaScript).
- `output/`: Directorio donde se guardan los archivos generados.

## Requisitos Previos

Asegúrate de tener instalados:
- [Python](https://www.python.org/downloads/) (3.8 o superior)
- [Node.js](https://nodejs.org/) (versión LTS recomendada)
- [Git](https://git-scm.com/)

## Instrucciones de Instalación y Ejecución

### 1. Configuración del Backend

1.  Abre una terminal y navega a la carpeta `backend`:
    ```bash
    cd backend
    ```

2.  (Opcional pero recomendado) Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configura las variables de entorno:
    - Asegúrate de tener un archivo `.env` basado en `.env.example` si es necesario (especialmente para claves de API como Gemini).

5.  Inicia el servidor:
    ```bash
    python main.py
    ```
    O alternativamente con uvicorn para recarga automática:
    ```bash
    uvicorn main:app --reload
    ```
    El backend correrá en `http://localhost:8000`.

### 2. Configuración del Frontend

1.  Abre una nueva terminal y navega a la carpeta `frontend`:
    ```bash
    cd frontend
    ```

2.  Instala las dependencias de Node.js:
    ```bash
    npm install
    ```

3.  Inicia el servidor de desarrollo:
    ```bash
    npm run dev
    ```
    El frontend estará disponible generalmente en `http://localhost:5173`.

## Uso

1.  Abre el navegador en la URL del frontend (`http://localhost:5173`).
2.  Ingresa una URL de un video de YouTube.
3.  Selecciona las opciones de análisis deseadas (Resumen, Transcripción, Guía, etc.).
4.  Haz clic en "Analizar".

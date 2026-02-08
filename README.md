# YouTube Video Analysis Tool

Herramienta profesional para analizar videos de YouTube, generar resúmenes extensos, transcripciones y guías didácticas utilizando IA (Gemini).

## Características

- **Análisis de Video**: Extrae audio y metadatos de YouTube.
- **Inteligencia Artificial**: Usa Google Gemini para generar resúmenes detallados y guías.
- **Múltiples Formatos**: Exporta resultados en Markdown, PDF y más.
- **Historial**: Guarda un registro de todos los análisis realizados.
- **Interfaz Moderna**: Frontend en React con modo oscuro y diseño responsive.

## Requisitos Previos

- [Python](https://www.python.org/downloads/) (3.8 o superior)
- [Node.js](https://nodejs.org/) (v16 o superior)
- [FFmpeg](https://ffmpeg.org/download.html) (Debe estar instalado y en el PATH del sistema)
- Una [API Key de Google Gemini](https://aistudio.google.com/app/apikey)

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tekkes/analizador_videos.git
cd analizador_videos
```

### 2. Configurar el Backend (Python)

```bash
cd backend
# (Opcional) Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # En Windows
# source venv/bin/activate # En Mac/Linux

# Instalar dependencias
pip install -r requirements.txt
```

**Configuración de Variables de Entorno:**
1.  En la carpeta `backend`, crea un archivo llamado `.env`.
2.  Añade tu API Key de Google:
    ```env
    GOOGLE_API_KEY=tu_clave_de_api_aqui
    ```

### 3. Configurar el Frontend (React)

Abrir una nueva terminal en la carpeta principal del proyecto:

```bash
cd frontend
npm install
```

## Ejecución

### Opción A: Script Automático (Windows)
Simplemente haz doble clic en el archivo `start_app.bat` en la carpeta raíz.
Esto abrirá dos ventanas (Backend y Frontend) y te indicará la URL a usar.

### Opción B: Ejecución Manual

**Backend:**
```bash
cd backend
python main.py
# Corre en http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm run dev -- --host
# Corre en http://localhost:5173 (o 5174, 5175...)
```

## Uso

1.  Abre la URL que te muestra el frontend (ej. `http://localhost:5173`).
2.  Pega el enlace de un video de YouTube.
3.  Selecciona "Analizar".
4.  Espera a que la IA procese el contenido y descarga los resultados.

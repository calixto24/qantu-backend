# Qantu Backend

Backend local y asíncrono para **Qantu**. Este servidor se ejecuta 100% de manera **offline** sobre infraestructura local, proporcionando procesamiento de lenguaje (LLM), transcripción de voz (STT), síntesis de voz (TTS) y comunicación en tiempo real por WebSockets.

---

## Requisitos Previos e Instalación del Sistema

Antes de clonar e iniciar el proyecto, asegúrate de contar con los siguientes componentes en el equipo host:

1. **Python 3.10+**: [Descargar Python](https://www.python.org/) _(Asegúrate de marcar "Add Python to PATH" durante la instalación)._
2. **Ollama**: Motor local de LLM. [Descargar Ollama](https://ollama.com/).
3. **FFmpeg**: Necesario para el procesamiento y conversión de archivos de audio (STT).
   - **Windows:** `winget install ffmpeg` o `choco install ffmpeg`

---

## Guía de Configuración e Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone https://github.com/calixto24/qantu-backend.git
```

### 2. Configurar y Activar el Entorno Virtual

Crear un enorno virtual

```bash
python -m venv venv
```

Activar el entorno virtual, En Windows (CMD / PowerShell):

```bash
.\venv\Scripts\activate
```

### 3. Instalar las Dependencias

Instalar las dependencias del proyecto:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Descargar modelos offline

Modelo de Lenguaje (Ollama), Abre una terminal y descarga el modelo optimizado para CPU:

```bash
ollama pull llama3.2:3b
```

(Verifica que esté listo ejecutando).

```bash
ollama list
```

### 5. Ejecutar el Servidor

Con Ollama corriendo en segundo plano y el entorno virtual activo, ejecuta Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Documentación Interactive (Swagger UI): http://localhost:8000/docs

- Salud del Servidor: http://localhost:8000/

- Canal WebSocket en Tiempo Real: ws://localhost:8000/ws/chat

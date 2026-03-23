# texto-to-path 🚀

**texto-to-path** es un motor de generación de proyectos automatizado que utiliza la potencia de **Gemini AI** y **Docker** para transformar descripciones de texto en estructuras de código funcionales y completas, entregándolas directamente en tu escritorio de Windows.

---

## 🛠️ Stack Tecnológico

* **Core:** Python 3.11+ (Pydantic, Typer)
* **AI:** Google Gemini API (Generative AI)
* **Infraestructura:** Docker & Docker Compose
* **Cache:** Redis

---

## 🚀 Inicio Rápido

### 1. Requisitos Previos
* Docker Desktop instalado y corriendo.
* Una API Key de Google Gemini.

### 2. Configuración del Env
Crea un archivo `.env` en la raíz del proyecto:
GEMINI_API_KEY=tu_api_key_aquí
REDIS_HOST=redis

### 3. Construir e Iniciar
docker-compose build

### 4. Generar un Proyecto
Ejecuta el comando `build` seguido de tu idea entre comillas. El resultado aparecerá en tu **Escritorio de Windows**:
docker-compose run --rm app build "Un microservicio con FastAPI y Redis"

---

## 📁 Estructura del Repositorio

.
├── src/
│   ├── core/           # Lógica del ProjectEngine (Generación de archivos)
│   ├── cli/            # Comandos de Typer (Interfaz de terminal)
│   └── schemas/        # Validaciones Pydantic y modelos de datos
├── Dockerfile          # Configuración de la imagen de Python 3.11
├── docker-compose.yml  # Orquestación de servicios (App + Redis)
├── main.py             # Punto de entrada principal del CLI
├── requirements.txt    # Dependencias del proyecto
└── .gitignore          # Archivos y carpetas excluidos de Git

---

## ⚙️ Funcionamiento Interno

1.  **Prompt:** El usuario envía una descripción desde la terminal de WSL o PowerShell.
2.  **Engine:** El sistema procesa la solicitud y consulta a Gemini para definir la arquitectura de archivos y el contenido de cada uno.
3.  **Mapeo de Volúmenes:** Gracias a la configuración de Docker, el contenedor escribe en la ruta interna `/app/output`. Esta carpeta está vinculada directamente a tu ruta de Windows: `/mnt/c/Users/User/Desktop`.
4.  **Resultado:** Obtienes una carpeta lista para abrir en VS Code directamente en tu escritorio, sin pasos intermedios de copiado.

---

## 🛠️ Desarrollo en Local (Sin Docker)

Si prefieres ejecutar el motor nativamente en tu entorno de WSL:

1.  **Activar entorno virtual:**
    python -m venv .venv && source .venv/bin/activate
2.  **Instalar dependencias:**
    pip install -r requirements.txt
3.  **Configurar el Path y Ejecutar:**
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    python main.py build "tu prompt aquí"

---

*Desarrollado con ❤️ para automatizar el boilerplate aburrido y acelerar el inicio de nuevos proyectos.*
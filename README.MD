# Agente de Búsqueda de Empleo con IA

Un agente autónomo en Python diseñado para buscar, filtrar y evaluar ofertas de trabajo de manera inteligente utilizando Inteligencia Artificial. El agente cruza tu currículum vítae (CV) contra vacantes reales obtenidas de Google Jobs y te devuelve un análisis estructurado de tu nivel de compatibilidad con cada una.

## Características Principales

- **Extracción Automatizada**: Obtiene vacantes en tiempo real utilizando [SerpApi](https://serpapi.com/) (Google Jobs engine).
- **Evaluación Inteligente**: Utiliza **Google Gemini 1.5 Pro** para actuar como un Headhunter Experto, analizando cada vacante contra tu perfil.
- **Análisis de Brechas (Gap Analysis)**: Te indica qué requisitos cumples, cuáles te faltan, y te da recomendaciones clave para optimizar tu perfil (ATS).
- **Prevención de Duplicados**: Incorpora una base de datos local (SQLite) que recuerda qué vacantes ya han sido procesadas para ahorrar tokens y tiempo en ejecuciones futuras.
- **Altamente Configurable**: Permite definir criterios estrictos (salario, años de experiencia, habilidades obligatorias) mediante un archivo de configuración.
- **Interfaz Web Intuitiva**: Cuenta con una aplicación gráfica desarrollada en **Streamlit** (`app.py`) para modificar tu CV, ajustar parámetros y visualizar los resultados de forma amigable.
- **Instalación y Uso Automatizado**: Incluye scripts diseñados para facilitar la instalación de Python y el despliegue del proyecto con un solo clic.

## Estructura del Proyecto

```text
Agente_V0/
├── data/                       # Archivos de entrada y salida
│   ├── cv.json                 # Tu información profesional
│   ├── parametros.json         # Configuración de búsqueda y reglas de la IA
│   ├── vacantes.db             # Base de datos SQLite generada automáticamente
│   └── resultados_evaluacion.json # Análisis final devuelto por la IA
├── src/
│   ├── ai_agent/               # Lógica de Inteligencia Artificial (Prompts y Gemini)
│   ├── db/                     # Gestión de base de datos local
│   ├── extractor/              # Conexión con SerpApi para buscar empleos
│   └── main.py                 # Orquestador principal del agente por CLI
├── app.py                      # Interfaz gráfica principal (Streamlit)
├── iniciar_proyecto.bat        # Ejecutable para iniciar el proyecto en Windows (Doble clic)
├── iniciar_proyecto.ps1        # Script para iniciar en Windows (PowerShell)
├── iniciar_proyecto.sh         # Script para iniciar en Linux/Mac (Terminal)
├── scrip_for_python.ps1        # Script de instalación y actualización de Python para Windows
├── .env                        # Variables de entorno (API Keys)
├── requirements.txt            # Dependencias del proyecto
└── README.MD                   # Este archivo
```

## Requisitos Previos

- **Python 3.8+** (Si estás en Windows y no lo tienes, puedes usar el script `scrip_for_python.ps1`).
- Una API Key de [SerpApi](https://serpapi.com/) (Para extraer las vacantes).
- Una API Key de [Google Gemini](https://aistudio.google.com/app/apikey) (Para evaluar las vacantes).

## Instalación y Uso Simplificado

Hemos integrado scripts automáticos para que no tengas que lidiar con comandos complicados. El script se encargará de crear el entorno virtual, instalar las dependencias e iniciar la aplicación visual.

### Paso 1: Configurar las API Keys
1. Crea un archivo `.env` en la raíz del proyecto (puedes basarte en `.env_example`).
2. Agrega tus claves de esta forma:
   ```env
   SERAPI_API_KEY=tu_llave_de_serpapi_aqui
   GOOGLE_API_KEY=tu_llave_de_gemini_aqui
   ```

### Paso 2: Iniciar el Proyecto
Dependiendo de tu sistema operativo, elige el script adecuado para arrancar todo automáticamente:

- **Windows**: Haz doble clic en el archivo `iniciar_proyecto.bat`.
  - *(Nota: Si prefieres la consola de PowerShell, puedes usar `.\iniciar_proyecto.ps1`)*.
- **Linux / Mac**: Abre tu terminal y ejecuta `./iniciar_proyecto.sh`.

¡Listo! Esto abrirá automáticamente una ventana en tu navegador web con la interfaz gráfica donde podrás:
1. Modificar y cargar tu CV.
2. Definir tus parámetros de búsqueda.
3. Iniciar el agente y visualizar las recomendaciones de las vacantes analizadas.

---
*(Nota avanzada: Si deseas ejecutar el agente directamente por consola sin la interfaz web, puedes seguir usando `python src/main.py` previa activación manual del entorno virtual)*.

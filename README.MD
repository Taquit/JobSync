#  Agente de Búsqueda de Empleo con IA

Un agente autónomo en Python diseñado para buscar, filtrar y evaluar ofertas de trabajo de manera inteligente utilizando Inteligencia Artificial. El agente cruza tu currículum vítae (CV) contra vacantes reales obtenidas de Google Jobs y te devuelve un análisis estructurado de tu nivel de compatibilidad con cada una.

##  Características Principales

- **Extracción Automatizada**: Obtiene vacantes en tiempo real utilizando [SerpApi](https://serpapi.com/) (Google Jobs engine).
- **Evaluación Inteligente**: Utiliza **Google Gemini 1.5 Pro** para actuar como un Headhunter Experto, analizando cada vacante contra tu perfil.
- **Análisis de Brechas (Gap Analysis)**: Te indica qué requisitos cumples, cuáles te faltan, y te da recomendaciones clave para optimizar tu perfil (ATS).
- **Prevención de Duplicados**: Incorpora una base de datos local (SQLite) que recuerda qué vacantes ya han sido procesadas para ahorrar tokens y tiempo en ejecuciones futuras.
- **Altamente Configurable**: Permite definir criterios estrictos (salario, años de experiencia, habilidades obligatorias) mediante un archivo de configuración.

##  Estructura del Proyecto

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
│   └── main.py                 # Orquestador principal del agente
├── .env                        # Variables de entorno (API Keys)
├── requirements.txt            # Dependencias del proyecto
└── README.MD                   # Este archivo
```

##  Requisitos Previos

- **Python 3.8+**
- Una API Key de [SerpApi](https://serpapi.com/) (Para extraer las vacantes).
- Una API Key de [Google Gemini](https://aistudio.google.com/app/apikey) (Para evaluar las vacantes).

##  Instalación y Configuración

1. **Clona o descarga este repositorio.**
2. **Crea y activa un entorno virtual** (Recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configura tus API Keys**:
   Crea un archivo `.env` en la raíz del proyecto (al mismo nivel que `README.MD`) con el siguiente contenido:
   ```env
   SERAPI_API_KEY=tu_llave_de_serpapi_aqui
   GOOGLE_API_KEY=tu_llave_de_gemini_aqui
   ```

##  Preparando tus Datos

Antes de ejecutar el agente, debes configurar dos archivos en la carpeta `data/`:

1. **`cv.json`**: Llena este archivo con tu información real. Incluye tu educación, experiencia, habilidades técnicas y blandas.
2. **`parametros.json`**: Define qué estás buscando.
   - `busqueda_api`: Las palabras clave y ubicación que se enviarán a Google Jobs.
   - `criterios_evaluacion_ia`: Reglas estrictas para el Headhunter (salario mínimo, habilidades indispensables).
   - `configuracion_ranking`: Reglas de descarte.

##  Uso

Para iniciar la búsqueda y evaluación, simplemente ejecuta el orquestador principal:

```bash
python src/main.py
```

El script hará lo siguiente:
1. Buscará vacantes.
2. Descartará las que ya analizó en días anteriores (usando SQLite).
3. Enviará las nuevas a Gemini.
4. Generará un archivo `data/resultados_evaluacion.json` con las recomendaciones ATS y el porcentaje de compatibilidad.

¡Revisa el archivo JSON resultante para ver a qué vacantes te conviene aplicar!

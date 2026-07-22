#!/bin/bash

echo "==================================================="
echo "  Iniciando JobSync IA - Headhunter (Linux/Mac)"
echo "==================================================="
echo ""

# 1. Verificar si existe Python
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 no está instalado o no está en el PATH."
    exit 1
fi

# 2. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "[INFO] Creando entorno virtual local (venv)..."
    python3 -m venv venv
fi

# 3. Activar el entorno virtual
echo "[INFO] Activando entorno virtual..."
source venv/bin/activate

# 4. Instalar dependencias
echo "[INFO] Verificando e instalando dependencias..."
pip install -r requirements.txt -q

# 5. Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "[ADVERTENCIA] No se encontró el archivo .env."
    echo "Copiando plantilla desde .env_example..."
    cp .env_example .env
    echo ""
    echo "==================================================="
    echo "  ATENCIÓN: Se ha creado el archivo .env"
    echo "  Por favor, edita el archivo .env en esta carpeta"
    echo "  y coloca tus API Keys (SerpApi y Google Gemini)"
    echo "  antes de realizar evaluaciones con IA."
    echo "==================================================="
    read -p "Presiona Enter cuando hayas configurado tus API Keys o para continuar de todos modos"
fi

# 6. Iniciar la aplicación
echo ""
echo "[INFO] Iniciando la aplicación web..."
echo "Se abrirá en tu navegador automáticamente (si el sistema lo permite)."
echo "Para cerrar el servidor, presiona Ctrl+C en esta ventana."
echo ""
streamlit run app.py

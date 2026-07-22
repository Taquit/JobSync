Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Iniciando JobSync IA - Headhunter" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar si existe Python
$pythonCmd = Get-Command "python" -ErrorAction SilentlyContinue
if (-Not $pythonCmd) {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH." -ForegroundColor Red
    Write-Host "Por favor, ejecuta primero el script de instalación de Python (scrip_for_python.ps1)." -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    Exit
}

# 2. Crear entorno virtual si no existe
if (-Not (Test-Path "venv")) {
    Write-Host "[INFO] Creando entorno virtual local (venv)..." -ForegroundColor Yellow
    python -m venv venv
}

# 3. Activar el entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Yellow
$activatePath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $activatePath) {
    . $activatePath
} else {
    Write-Host "[ERROR] No se pudo encontrar el script de activación del entorno virtual." -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    Exit
}

# 4. Instalar dependencias
Write-Host "[INFO] Verificando e instalando dependencias (esto puede tomar unos segundos)..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# 5. Verificar archivo .env
if (-Not (Test-Path ".env")) {
    Write-Host "[ADVERTENCIA] No se encontró el archivo .env." -ForegroundColor Magenta
    Write-Host "Copiando plantilla desde .env_example..." -ForegroundColor Yellow
    Copy-Item ".env_example" -Destination ".env"
    
    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Red
    Write-Host "  ATENCIÓN: Se ha creado el archivo .env" -ForegroundColor Red
    Write-Host "  Por favor, edita el archivo .env en esta carpeta" -ForegroundColor Red
    Write-Host "  y coloca tus API Keys (SerpApi y Google Gemini)" -ForegroundColor Red
    Write-Host "  antes de realizar evaluaciones con IA." -ForegroundColor Red
    Write-Host "===================================================" -ForegroundColor Red
    Read-Host -Prompt "Presiona Enter cuando hayas configurado tus API Keys o para continuar de todos modos"
}

# 6. Iniciar la aplicación
Write-Host ""
Write-Host "[INFO] Iniciando la aplicación web..." -ForegroundColor Green
Write-Host "Se abrirá en tu navegador automáticamente." -ForegroundColor Green
Write-Host "Para cerrar el servidor, presiona Ctrl+C en esta ventana." -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

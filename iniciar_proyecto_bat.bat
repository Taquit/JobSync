@echo off
cd /d "%~dp0"
echo ===================================================
echo   Iniciando JobSync IA - Headhunter
echo ===================================================
echo.

:: 1. Verificar si existe Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Python no esta instalado o no esta en el PATH.
    echo [INFO] Iniciando instalacion automatica de Python...
    
    :: Mandamos a llamar tu script de PowerShell saltando la restriccion de seguridad
    powershell.exe -ExecutionPolicy Bypass -File ".\scrip_for_python.ps1"
    
    echo [INFO] Por favor, reinicia esta ventana despues de la instalacion.
    pause
    exit /b
)

:: 2. Crear entorno virtual si no existe
if not exist venv\ (
    echo [INFO] Creando entorno virtual local ^(venv^)...
    python -m venv venv
)

:: 3. Activar el entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

:: 4. Instalar dependencias
echo [INFO] Verificando e instalando dependencias...
pip install -r requirements.txt -q

:: 5. Verificar archivo .env
if not exist .env (
    echo [ADVERTENCIA] No se encontro el archivo .env.
    echo Copiando plantilla desde .env_example...
    copy .env_example .env >nul
    echo.
    echo ===================================================
    echo   ATENCION: Se ha creado el archivo .env
    echo   Por favor, edita el archivo .env en esta carpeta
    echo   y coloca tus API Keys ^(SerpApi y Google Gemini^)
    echo   antes de realizar evaluaciones con IA.
    echo ===================================================
    pause
)

:: 6. Iniciar la aplicacion
echo.
echo [INFO] Iniciando la aplicacion web...
echo Se abrira en tu navegador automaticamente.
echo Para cerrar el servidor, cierra esta ventana.
echo.
python -m streamlit run app.py

pause

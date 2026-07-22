# Requerir permisos de administrador (opcional pero recomendado)
# #Requires -RunAsAdministrator

# Definir la versión objetivo y la URL de descarga oficial
$targetVersionStr = "3.14.6"
$targetVersion = [version]$targetVersionStr
$downloadUrl = "https://www.python.org/ftp/python/$targetVersionStr/python-$targetVersionStr-amd64.exe"
$installerPath = "$env:TEMP\python_installer.exe"

$installNeeded = $true

Write-Host "Verificando si Python está instalado..." -ForegroundColor Cyan

# Comprobar si Python ya está en el PATH
$pythonCmd = Get-Command "python" -ErrorAction SilentlyContinue

if ($pythonCmd) {
    # Extraer la versión actual de Python
    $versionOutput = & python --version 2>&1
    
    if ($versionOutput -match "Python\s+([0-9]+\.[0-9]+\.[0-9]+)") {
        $currentVersionStr = $matches[1]
        $currentVersion = [version]$currentVersionStr
        
        if ($currentVersion -ge $targetVersion) {
            Write-Host "¡Genial! Ya tienes la versión $currentVersion instalada (igual o superior a la $targetVersionStr)." -ForegroundColor Green
            Write-Host "No se requiere ninguna actualización." -ForegroundColor Green
            $installNeeded = $false
        } else {
            Write-Host "Se encontró la versión antigua $currentVersionStr." -ForegroundColor Yellow
            Write-Host "Iniciando actualización a la versión $targetVersionStr..." -ForegroundColor Cyan
        }
    } else {
        Write-Host "Python está instalado, pero no se pudo leer la versión exacta. Se forzará la instalación de $targetVersionStr." -ForegroundColor Yellow
    }
} else {
    Write-Host "Python no está instalado en este sistema. Procediendo con una instalación limpia." -ForegroundColor Cyan
}

# Ejecutar instalación solo si es necesario
if ($installNeeded) {
    Write-Host "Descargando Python $targetVersionStr..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath

    Write-Host "Instalando Python silenciosamente (esto puede tomar un minuto)..." -ForegroundColor Cyan
    
    # Argumentos: Instalación silenciosa, para todos los usuarios y agregando Python al PATH
    # Nota: Si es una actualización de la misma versión principal (ej. 3.12.3 a 3.12.4), el instalador la actualiza.
    # Si es un salto grande (ej. 3.11 a 3.12), instala ambas pero 'PrependPath=1' hace que la nueva sea la predeterminada.
    $installArgs = "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0"

    $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru

    if ($process.ExitCode -eq 0) {
        Write-Host "¡Python $targetVersionStr se ha instalado/actualizado correctamente!" -ForegroundColor Green
    } else {
        Write-Host "Hubo un error durante la instalación. Código de salida: $($process.ExitCode)" -ForegroundColor Red
    }

    # Limpiar el instalador descargado
    if (Test-Path $installerPath) {
        Remove-Item -Path $installerPath -Force
        Write-Host "Archivo de instalación temporal eliminado." -ForegroundColor DarkGray
    }
}

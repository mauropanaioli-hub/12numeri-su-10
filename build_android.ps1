# Build APK da PowerShell - avvia WSL e lancia la build
# Esegui: .\build_android.ps1

$projectPath = "/mnt/c/Users/mauro/Desktop/mauro/12numeri su 10"

Write-Host "=== Build APK 12 numeri su 10 ===" -ForegroundColor Cyan
Write-Host "Percorso in WSL: $projectPath"
Write-Host ""

# Usa sh -c con comando tra virgolette (evita errori "execvpe bash failed")
Write-Host "Avvio WSL..." -ForegroundColor Yellow
wsl sh -c "cd '$projectPath' && buildozer android debug"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Se vedi ancora errori, apri WSL a mano e lancia i comandi da li:" -ForegroundColor Yellow
    Write-Host "  wsl"
    Write-Host "  cd `"$projectPath`""
    Write-Host "  buildozer android debug"
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "APK in: bin\ (nella cartella del progetto)" -ForegroundColor Green

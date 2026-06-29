# gear_system startup script
$BASE_DIR = $PSScriptRoot
$BACKEND_DIR = "$BASE_DIR\backend"
$FRONTEND_DIR = "$BASE_DIR\frontend"
$LOG_DIR = "$BASE_DIR\logs"
$BACKEND_PORT = 8000
$FRONTEND_PORT = 5173

# Resolve the real python.exe (skip Microsoft Store stub)
$PYTHON = (Get-Command python -All -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike "*WindowsApps*" } | Select-Object -First 1).Source
if (-not $PYTHON) { $PYTHON = "python" }

if (-not (Test-Path $LOG_DIR)) { New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null }

switch ($args[0]) {
    "start" {
        Write-Host "Starting backend..." -ForegroundColor Cyan
        $p1 = Start-Process -FilePath $PYTHON -ArgumentList "-m","uvicorn","app.main:app","--host","0.0.0.0","--port","$BACKEND_PORT","--reload" -WorkingDirectory $BACKEND_DIR -WindowStyle Hidden -RedirectStandardOutput "$LOG_DIR\backend.log" -PassThru

        Write-Host "Starting frontend..." -ForegroundColor Cyan
        $p2 = Start-Process -FilePath "cmd" -ArgumentList "/c","npx","vite","--host","0.0.0.0","--port","$FRONTEND_PORT" -WorkingDirectory $FRONTEND_DIR -WindowStyle Hidden -RedirectStandardOutput "$LOG_DIR\frontend.log" -PassThru

        @{ "backend_pid" = $p1.Id; "frontend_pid" = $p2.Id } | ConvertTo-Json | Out-File "$BASE_DIR\.run_pids.json" -Encoding utf8
        Write-Host "Done!" -ForegroundColor Green
        Write-Host "Backend: http://localhost:$BACKEND_PORT"
        Write-Host "Frontend: http://localhost:$FRONTEND_PORT"
        Write-Host "Logs: $LOG_DIR"
    }
    "stop" {
        Write-Host "Stopping..." -ForegroundColor Yellow
        $pidFile = "$BASE_DIR\.run_pids.json"
        if (Test-Path $pidFile) {
            $pids = Get-Content $pidFile | ConvertFrom-Json
            try { Stop-Process -Id $pids.backend_pid -Force -ErrorAction SilentlyContinue } catch {}
            try { Stop-Process -Id $pids.frontend_pid -Force -ErrorAction SilentlyContinue } catch {}
            Remove-Item $pidFile
        }
        Write-Host "Stopped." -ForegroundColor Green
    }
    "status" {
        $pidFile = "$BASE_DIR\.run_pids.json"
        if (Test-Path $pidFile) {
            $pids = Get-Content $pidFile | ConvertFrom-Json
            $bp = Get-Process -Id $pids.backend_pid -ErrorAction SilentlyContinue
            $fp = Get-Process -Id $pids.frontend_pid -ErrorAction SilentlyContinue
            if ($bp) { Write-Host "Backend running (PID: $($bp.Id))" -ForegroundColor Green } else { Write-Host "Backend not running" -ForegroundColor Red }
            if ($fp) { Write-Host "Frontend running (PID: $($fp.Id))" -ForegroundColor Green } else { Write-Host "Frontend not running" -ForegroundColor Red }
        } else {
            Write-Host "No service record found" -ForegroundColor Red
        }
    }
    default { Write-Host "Usage: start.ps1 {start|stop|status}" }
}

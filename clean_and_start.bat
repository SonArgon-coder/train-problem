@echo off
echo ===================================================
echo Resetting Cache and Starting Passenger Portal...
echo ===================================================
cd /d %~dp0frontend

if exist .next (
    echo Clearing stale .next build cache...
    rd /s /q .next
)

echo.
echo Starting fresh dev server on http://localhost:3000 ...
echo Opening your web browser in 5 seconds...
start /b cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:3000"

call npm run dev
pause

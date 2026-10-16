@echo off
echo ===================================================
echo Starting Indian Railways Passenger Travel Portal...
echo ===================================================
cd /d %~dp0frontend

echo.
echo Server is launching on: http://localhost:3000
echo Opening http://localhost:3000 in your default browser in 5 seconds...
start /b cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:3000"

call npm run dev
pause

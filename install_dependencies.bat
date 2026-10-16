@echo off
echo ===================================================
echo Installing Frontend Dependencies...
echo ===================================================
cd /d %~dp0frontend
call npm install
echo.
echo Dependencies installed successfully!
echo You can now run start_frontend.bat to open the portal.
pause

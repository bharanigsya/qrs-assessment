@echo off
setlocal
title QRS Assessment - One Click Start
color 0B
cd /d "%~dp0"

echo.
echo  ================================================
echo    QRS Assessment - ONE CLICK START
echo  ================================================
echo.
echo  Folder: %CD%
echo.

REM ---- Check required files ----
if not exist "%~dp0backend.py" (
  echo  ERROR: backend.py not found in this folder.
  echo  Copy backend.py, admin.html, test.html, questions.js here first.
  echo.
  dir /b "%~dp0"
  echo.
  pause
  exit /b 1
)

echo  Admin login: use your admin account
echo.
pause

REM ---- 1) Backend ----
echo  Starting backend...
start "QRS-Backend" /D "%~dp0" cmd /k "title QRS-Backend && color 0A && echo Backend folder: %CD% && python backend.py && echo. && echo Backend stopped. && pause"

timeout /t 4 /nobreak >nul

REM ---- 2) Cloudflare tunnel ----
set "CF="
if exist "%ProgramFiles(x86)%\cloudflared\cloudflared.exe" set "CF=%ProgramFiles(x86)%\cloudflared\cloudflared.exe"
if exist "%ProgramFiles%\cloudflared\cloudflared.exe" set "CF=%ProgramFiles%\cloudflared\cloudflared.exe"
if exist "%LOCALAPPDATA%\cloudflared\cloudflared.exe" set "CF=%LOCALAPPDATA%\cloudflared\cloudflared.exe"

if not defined CF (
  echo.
  echo  cloudflared NOT FOUND.
  echo  Install once:
  echo    winget install --id Cloudflare.cloudflared
  echo.
  echo  Local only: http://localhost:5000/admin.html
  start "" "http://localhost:5000/admin.html"
  pause
  exit /b 0
)

echo  Starting tunnel...
start "QRS-Tunnel" cmd /k "title QRS-Tunnel && color 0E && echo. && echo === Copy the https://....trycloudflare.com URL below === && echo. && "%CF%" tunnel --protocol http2 --url http://localhost:5000"

echo.
echo  ================================================
echo   NEXT STEPS
echo  ================================================
echo.
echo  1. Yellow window "QRS-Tunnel" - copy:
echo        https://xxxxx.trycloudflare.com
echo  2. Open:
echo        https://xxxxx.trycloudflare.com/admin.html
echo  3. Log in with your admin account
echo  4. Create assessment AFTER tunnel is running
echo.
echo  Keep BOTH windows open while candidates test.
echo  Do NOT restart the tunnel or let this PC sleep during a test:
echo  the address changes and every link already sent stops working.
echo.
timeout /t 5 /nobreak >nul
start "" "http://localhost:5000/admin.html"

echo  Done. You can close this window.
pause

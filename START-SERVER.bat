@echo off
title QRS Assessment Server
color 0B
echo.
echo  ========================================
echo    QRS Second Round Assessment Platform
echo  ========================================
echo.
cd /d "%~dp0"

echo  Trying free backend (Flask)...
python backend.py
if errorlevel 1 (
  echo.
  echo  Flask not found or failed. Using simple server...
  echo  Install Flask with:  pip install flask
  echo.
  python -m http.server 8080
  if errorlevel 1 (
    python3 -m http.server 8080
  )
)

pause

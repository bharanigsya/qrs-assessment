@echo off
setlocal
title QRS Assessment Server
color 0B
echo.
echo  ========================================
echo    QRS Second Round Assessment Platform
echo  ========================================
echo.
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
  echo  Python was not found. Install Python 3 from python.org
  echo  and tick "Add Python to PATH", then run this again.
  pause
  exit /b 1
)

python -c "import flask, flask_cors" >nul 2>&1
if errorlevel 1 (
  echo  Installing required packages...
  python -m pip install -r requirements.txt
)

echo  Starting backend on http://localhost:5000  (keep this window open)
echo.
python backend.py

echo.
echo  Backend stopped. If this was unexpected, read the error above.
pause

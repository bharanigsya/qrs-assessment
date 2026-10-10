@echo off
setlocal
title QRS Public Link (Cloudflare Tunnel)
echo.
echo  Keep START-SERVER.bat running in its own window first.
echo  Copy the https://....trycloudflare.com address shown below,
echo  then open  THAT-ADDRESS/admin.html  to create candidate links.
echo.
echo  WARNING: if you close/restart this window or the PC sleeps, the address
echo  changes and every link already sent stops working.
echo.

set "CF="
if exist "%ProgramFiles(x86)%\cloudflared\cloudflared.exe" set "CF=%ProgramFiles(x86)%\cloudflared\cloudflared.exe"
if exist "%ProgramFiles%\cloudflared\cloudflared.exe" set "CF=%ProgramFiles%\cloudflared\cloudflared.exe"
if exist "%LOCALAPPDATA%\cloudflared\cloudflared.exe" set "CF=%LOCALAPPDATA%\cloudflared\cloudflared.exe"
if not defined CF (
  where cloudflared >nul 2>&1
  if not errorlevel 1 set "CF=cloudflared"
)
if not defined CF (
  echo  cloudflared NOT FOUND. Install once:
  echo    winget install --id Cloudflare.cloudflared
  pause
  exit /b 1
)

"%CF%" tunnel --protocol http2 --url http://localhost:5000
pause

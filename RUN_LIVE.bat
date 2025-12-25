@echo off
title JUMP0X1 - LIVE TRADING
cd /d "%~dp0"
echo.
echo ============================================================
echo   JUMP0X1 - LIVE TRADING MODE
echo ============================================================
echo.
echo   WARNING: Real orders may be placed!
echo   Check .env settings before proceeding.
echo.
python run_live.py
pause

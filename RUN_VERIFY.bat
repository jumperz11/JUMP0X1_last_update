@echo off
title JUMP0X1 - Pre-Live Verification
cd /d "%~dp0"
echo.
echo ============================================================
echo   JUMP0X1 - PRE-LIVE VERIFICATION SUITE
echo ============================================================
echo.
echo   Running all safety checks before going live...
echo.
python scripts/verify_pre_live.py
pause

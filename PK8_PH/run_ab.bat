@echo off
set PATH=C:\msys64\mingw64\bin;%PATH%
set LOG_DIR=C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH\logs\runs\100_session_run
set AB_TEST=1
set ENABLE_ORDERS_JSONL=1
set MAX_TRADES_PER_SESSION=1
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
cd /d C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH
target\release\live_console.exe

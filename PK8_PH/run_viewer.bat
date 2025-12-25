@echo off
set PATH=C:\msys64\mingw64\bin;%PATH%
set LOG_DIR=C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH\logs\runs\100_session_run
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
cd /d C:\Users\Mega-PC\Desktop\JUMP0X1\PK8_PH
target\release\multi_signal_recorder.exe --live BTC

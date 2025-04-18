@echo off
cd /d "%~dp0"
call ..\venv\Scripts\activate
python ../backend/main.py
call ..\venv\Scripts\deactivate
pause
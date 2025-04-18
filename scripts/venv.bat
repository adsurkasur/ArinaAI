@echo off
cd..

REM Check if the venv directory exists
if not exist venv (
    echo Error: Virtual environment not found. Please create it first.
    pause
    exit /b 1
)

call venv\Scripts\activate
cmd

@echo off
echo ============================================================
echo Loading ArinaAI...
echo ============================================================

REM Navigate to the root directory
cd..

REM Check if the virtual environment exists
if not exist venv (
    echo ============================================================
    echo Error: Virtual environment not found. Please create it first.
    echo ============================================================
    pause
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ============================================================
    echo Error: Failed to activate the virtual environment.
    echo ============================================================
    pause
    exit /b 1
)

REM Run the ArinaAI script
echo ============================================================
echo Running ArinaAI...
echo ============================================================
python backend\scripts\arina.py
if %errorlevel% neq 0 (
    echo ============================================================
    echo Error: Failed to run ArinaAI. Python error message is shown above.
    echo ============================================================
    pause
    exit /b 1
)

echo ============================================================
echo ArinaAI has finished running successfully.
echo ============================================================
pause
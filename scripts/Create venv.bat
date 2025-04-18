@echo off
REM Define the name of the virtual environment folder in the root directory
set ROOT_DIR=%~dp0..
set VENV_NAME=%ROOT_DIR%\venv

REM Check if the virtual environment already exists
if exist %VENV_NAME% (
    echo ============================================================
    echo Virtual environment already exists in:
    echo %VENV_NAME%
    echo ============================================================
    echo Please delete the existing virtual environment if you want to recreate it.
    echo ============================================================
    pause
    exit /b 1
)

REM Find all available Python executables
echo ============================================================
echo Searching for available Python versions...
echo ============================================================
setlocal enabledelayedexpansion
set count=1
for /f "delims=" %%P in ('where python') do (
    echo !count!. %%P
    set "PYTHON_!count!=%%P"
    set /a count+=1
)

REM Check if any Python executables were found
if %count%==1 (
    echo ============================================================
    echo No Python executables found on the system.
    echo Ensure Python is installed and added to PATH.
    echo ============================================================
    pause
    exit /b 1
)

REM Prompt the user to choose a Python version
set /a MAX_CHOICE=%count%-1
echo ============================================================
set /p CHOICE="Enter the number corresponding to the Python version you want to use: "

REM Validate the user's choice
if %CHOICE% lss 1 if %CHOICE% gtr %MAX_CHOICE% (
    echo ============================================================
    echo Invalid choice. Exiting.
    echo ============================================================
    pause
    exit /b 1
)

REM Get the selected Python executable
for /f "tokens=2 delims==" %%P in ('set PYTHON_%CHOICE%') do set SELECTED_PYTHON=%%P

REM Check if the selected Python executable is valid
%SELECTED_PYTHON% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ============================================================
    echo The selected Python executable is not valid or not found.
    echo ============================================================
    pause
    exit /b 1
)

REM Create the virtual environment
echo ============================================================
echo Creating virtual environment in root directory using %SELECTED_PYTHON%...
echo ============================================================
%SELECTED_PYTHON% -m venv %VENV_NAME%

REM Check if the virtual environment was created successfully
if exist %VENV_NAME% (
    echo ============================================================
    echo Virtual environment created successfully in:
    echo %VENV_NAME%
    echo ============================================================
) else (
    echo ============================================================
    echo Failed to create virtual environment.
    echo Please check for errors and try again.
    echo ============================================================
    pause
    exit /b 1
)

REM Activate the virtual environment for testing
echo ============================================================
echo Activating virtual environment for testing...
echo ============================================================
call %VENV_NAME%\Scripts\activate.bat

REM Confirm activation
if "%VIRTUAL_ENV%"=="" (
    echo ============================================================
    echo Failed to activate virtual environment.
    echo Please check for errors and try again.
    echo ============================================================
    pause
    exit /b 1
) else (
    echo ============================================================
    echo Virtual environment activated successfully for testing.
    echo Running a test command inside the virtual environment...
    echo ============================================================
    python --version
    echo ============================================================
    echo Deactivating virtual environment after testing...
    echo ============================================================
    deactivate
)

REM Allow the user to read the success or failure message
echo ============================================================
echo Process completed. Press any key to exit.
echo ============================================================
pause
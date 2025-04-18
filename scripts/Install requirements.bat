@echo off
cd ..
call venv\Scripts\activate

echo Installing requirements...
pip install -r config\requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements. Please check the error messages above.
    call venv\Scripts\deactivate
    pause
    exit /b %ERRORLEVEL%
)

echo Requirements installed successfully.
call venv\Scripts\deactivate
pause
@echo off
REM Watchtower Installation Script (Windows)

echo ==========================================
echo   WATCHTOWER INSTALLATION
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is required but not installed.
    exit /b 1
)

echo [OK] Python found

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

echo [OK] Dependencies installed

REM Create batch wrapper
echo.
echo Setting up Watchtower CLI...

set SCRIPT_DIR=%~dp0
set CLI_PATH=%SCRIPT_DIR%watchtower_cli.py

echo @echo off > watchtower.bat
echo python "%CLI_PATH%" %%* >> watchtower.bat

echo [OK] CLI wrapper created: watchtower.bat

REM Initialize field
echo.
set /p INIT="Do you want to initialize your field now? (y/n): "

if /i "%INIT%"=="y" (
    python "%CLI_PATH%" init
)

echo.
echo ==========================================
echo   [OK] WATCHTOWER INSTALLED
echo ==========================================
echo.
echo Next steps:
echo   1. Run: watchtower status
echo   2. Start daemon: watchtower daemon start
echo   3. View glyphs: watchtower glyphs list
echo.
echo For help: watchtower --help
echo.
echo NOTE: Add %SCRIPT_DIR% to your PATH to use 'watchtower' from anywhere
echo.

pause

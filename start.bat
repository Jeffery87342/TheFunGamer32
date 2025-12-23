@echo off
REM Roblox Auto-Group Joiner - Launcher
REM This batch file launches the Roblox Group Joiner application

echo ================================================================================
echo   Roblox Auto-Group Joiner
echo   Powered by FunBypass.com
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
echo.

REM Check if dependencies are installed
echo [2/3] Checking dependencies...
python -c "import requests, cryptography, colorama" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
) else (
    echo Dependencies OK
)
echo.

REM Try to launch GUI version first
echo [3/3] Launching application...
echo Attempting to start GUI version...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo Tkinter not available. Launching console version...
    echo.
    python main_console.py
) else (
    echo Starting GUI version...
    echo.
    python main.py
)

REM If we get here, the program exited
echo.
echo Program closed.
pause

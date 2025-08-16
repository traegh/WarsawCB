@echo off
title Colorbot Launcher

echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9+ and make sure to check "Add Python to PATH".
    pause
    exit /b
)

echo Checking for virtual environment...
if not exist ".\venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment and installing dependencies...
call ".\venv\Scripts\activate.bat"
pip install -r requirements.txt --quiet

echo Starting the application...
python main.py

echo Application finished. Press any key to exit.
pause
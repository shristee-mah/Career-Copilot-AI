@echo off
REM Career Copilot AI - Streamlit App Launcher
echo.
echo ================================================
echo  Career Copilot AI - Streamlit Application
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo Warning: .env file not found!
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env and add your Google API Key
    echo Then run this script again
    pause
    exit /b 0
)

REM Run the Streamlit app
echo.
echo Starting Career Copilot AI...
echo.
python -m streamlit run app.py

pause

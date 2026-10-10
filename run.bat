@echo off
REM =========================================================================
REM  run.bat — CareerPilot one-click launcher for Windows
REM  1. Checks Python is installed
REM  2. Copies .env.example → .env if .env is missing
REM  3. Creates a virtual environment (venv/) if it doesn't exist
REM  4. Installs / upgrades dependencies from requirements.txt
REM  5. Launches the Streamlit app
REM =========================================================================
setlocal enabledelayedexpansion

echo.
echo  =========================================
echo   CareerPilot ^– AI Career Mentor
echo  =========================================
echo.

REM ── 1. Check Python ───────────────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not on PATH.
    echo         Download it from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% found.

REM ── 2. Create .env if missing ─────────────────────────────────────────────
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [INFO] .env created from .env.example.
        echo        ^> Open .env and replace "your_key_here" with your Groq API key.
        echo        ^> Then re-run this script.
        pause
        exit /b 0
    ) else (
        echo [WARN] Neither .env nor .env.example found.
        echo        Create a .env file with:  GROQ_API_KEY=your_key_here
    )
) else (
    echo [OK] .env file found.
)

REM ── 3. Create virtual environment ─────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

REM ── 4. Install dependencies ───────────────────────────────────────────────
echo [INFO] Installing / updating dependencies...
call venv\Scripts\activate.bat
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] Dependencies ready.

REM ── 5. Launch Streamlit ───────────────────────────────────────────────────
echo.
echo [INFO] Starting CareerPilot...
echo        Open http://localhost:8501 in your browser.
echo        Press Ctrl+C here to stop the server.
echo.
streamlit run app.py

endlocal

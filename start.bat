@echo off
echo ========================================
echo ChatSphere - Splinter Cell Edition
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

echo [3/4] Setting up directories...
if not exist "static\uploads\profiles" mkdir static\uploads\profiles
if not exist "static\uploads\media" mkdir static\uploads\media
if not exist "static\uploads\status" mkdir static\uploads\status
echo Directories created!
echo.

echo [4/4] Starting application...
echo.
echo ========================================
echo Application running on http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python run.py

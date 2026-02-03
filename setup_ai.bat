@echo off
echo ===============================================
echo   ChatSphere AI Setup - Quick Start
echo ===============================================
echo.

REM Check if .env exists
if not exist .env (
    echo [1/4] Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your Groq API key!
    echo     Get your FREE key at: https://console.groq.com/
    echo.
    pause
) else (
    echo [1/4] .env file already exists ✓
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [3/4] Installing/Updating dependencies...
pip install -q -r requirements.txt

echo.
echo [4/4] Initializing AI Bot...
python setup_ai_bot.py

echo.
echo ===============================================
echo   Setup Complete! 🎉
echo ===============================================
echo.
echo Next steps:
echo   1. Make sure your Groq API key is in .env
echo   2. Run: start.bat
echo   3. Visit: http://localhost:5000
echo   4. Chat with 'chatsphere_ai' to test AI features!
echo.
echo For detailed instructions, read SETUP_GUIDE.md
echo For AI features info, read AI_FEATURES.md
echo.
pause

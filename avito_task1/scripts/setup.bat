@echo off
REM Setup script for Windows

echo Setting up URL Shortener...

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    (
        echo DATABASE_URL=postgresql://urlshortener:urlshortener@localhost:5432/urlshortener
        echo BASE_URL=http://localhost:8000
        echo SHORT_CODE_LENGTH=6
    ) > .env
)

echo Setup complete!
echo To start the application:
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload

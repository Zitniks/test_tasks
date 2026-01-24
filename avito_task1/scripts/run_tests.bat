@echo off
REM Run tests script for Windows

echo Running tests...

REM Activate virtual environment if it exists
if exist "venv" (
    call venv\Scripts\activate.bat
)

REM Run tests with coverage
pytest

echo Tests completed!

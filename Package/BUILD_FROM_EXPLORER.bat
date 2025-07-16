@echo off
title Pladria v2.5 - Build from File Explorer
color 0A

echo.
echo ============================================================
echo    PLADRIA v2.5 - BUILD FROM FILE EXPLORER
echo ============================================================
echo.
echo This script ensures the build works correctly when
echo double-clicked from Windows File Explorer.
echo.
echo ============================================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Show current directory for debugging
echo Current directory: %CD%
echo.

REM Check if Python is available
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo SOLUTION:
    echo 1. Install Python 3.8+ from https://python.org
    echo 2. Make sure "Add Python to PATH" is checked during installation
    echo 3. Restart your computer
    echo 4. Try again
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python found
echo.

REM Check if required files exist
echo Checking required files...
if not exist "build_pladria_improved.py" (
    echo ❌ ERROR: build_pladria_improved.py not found
    echo Make sure you're running this from the Package directory
    pause
    exit /b 1
)

if not exist "..\src\main.py" (
    echo ❌ ERROR: Main script not found at ..\src\main.py
    echo Make sure the Pladria project structure is intact
    pause
    exit /b 1
)

echo ✅ Required files found
echo.

REM Run the build script
echo Starting build process...
echo.
python build_pladria_improved.py

REM Check if build was successful
if errorlevel 1 (
    echo.
    echo ❌ BUILD FAILED
    echo Check the error messages above
    echo.
) else (
    echo.
    echo ✅ BUILD COMPLETED
    echo Check the dist\ folder for your executable
    echo.
)

echo.
echo Press any key to close this window...
pause >nul

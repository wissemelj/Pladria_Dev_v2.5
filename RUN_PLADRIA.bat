@echo off
title Pladria v2.5 - Direct Python Launch
color 0A

echo.
echo ============================================================
echo    PLADRIA v2.5 - DIRECT LAUNCH
echo ============================================================
echo.
echo Running Pladria directly with Python (no build needed)
echo.

cd /d "%~dp0"
cd src

echo Starting Pladria...
python main.py

if errorlevel 1 (
    echo.
    echo ❌ Error running Pladria
    echo Check that all dependencies are installed
    pause
) else (
    echo.
    echo ✅ Pladria closed normally
)

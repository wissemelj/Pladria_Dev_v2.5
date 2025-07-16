@echo off
title Pladria v2.5 - Quick Build
echo ============================================================
echo    PLADRIA v2.5 - QUICK BUILD
echo ============================================================
echo.

REM Change to Package directory
cd /d "%~dp0"

echo Starting improved build script...
echo.

python build_pladria_improved.py

echo.
echo Build completed. Check the dist\ folder for results.
echo.
pause

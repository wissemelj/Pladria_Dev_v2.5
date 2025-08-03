@echo off
title Pladria - Streamlined Build System
color 0A

echo.
echo ============================================================
echo    PLADRIA - STREAMLINED BUILD SYSTEM
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting streamlined build system...
echo.

python build_pladria.py

echo.
echo ============================================================
echo    BUILD SYSTEM CLOSED
echo ============================================================
pause

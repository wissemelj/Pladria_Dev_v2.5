@echo off
title Pladria - Unified Build System
color 0A

echo.
echo ============================================================
echo    PLADRIA - UNIFIED BUILD SYSTEM
echo ============================================================
echo.

cd /d "%~dp0"

echo Starting unified build system...
echo.

python build_and_package.py

echo.
echo ============================================================
echo    BUILD SYSTEM CLOSED
echo ============================================================
pause

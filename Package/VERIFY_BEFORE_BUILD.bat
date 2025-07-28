@echo off
title Pladria v2.5 - Pre-Build Verification
color 0B

echo.
echo ============================================================
echo    PLADRIA v2.5 - PRE-BUILD VERIFICATION
echo ============================================================
echo.
echo This script verifies all files and dependencies before building
echo.

cd /d "%~dp0"

echo [1/4] File Structure Verification...
echo.

echo Checking main application file:
if exist "..\src\main.py" (
    echo ✅ ..\src\main.py - EXISTS
) else (
    echo ❌ ..\src\main.py - MISSING
    set ERROR_FOUND=1
)

echo.
echo Checking icon and image files:
if exist "..\Icone_App_Sharp.ico" (
    echo ✅ ..\Icone_App_Sharp.ico - EXISTS
) else (
    echo ❌ ..\Icone_App_Sharp.ico - MISSING
    set ERROR_FOUND=1
)

if exist "..\Icone_App.png" (
    echo ✅ ..\Icone_App.png - EXISTS
) else (
    echo ❌ ..\Icone_App.png - MISSING
    set ERROR_FOUND=1
)

if exist "..\logo_Sofrecom.png" (
    echo ✅ ..\logo_Sofrecom.png - EXISTS
) else (
    echo ❌ ..\logo_Sofrecom.png - MISSING
    set ERROR_FOUND=1
)

echo.
echo Checking Package directory files:
if exist "requirements.txt" (
    echo ✅ requirements.txt - EXISTS
) else (
    echo ❌ requirements.txt - MISSING
    set ERROR_FOUND=1
)

if exist "BUILD_QUICK.bat" (
    echo ✅ BUILD_QUICK.bat - EXISTS
) else (
    echo ❌ BUILD_QUICK.bat - MISSING
    set ERROR_FOUND=1
)

echo.
echo [2/4] Source Code Structure Verification...
echo.

echo Checking core modules:
if exist "..\src\config\__init__.py" (
    echo ✅ config module - EXISTS
) else (
    echo ❌ config module - MISSING
    set ERROR_FOUND=1
)

if exist "..\src\core\__init__.py" (
    echo ✅ core module - EXISTS
) else (
    echo ❌ core module - MISSING
    set ERROR_FOUND=1
)

if exist "..\src\ui\__init__.py" (
    echo ✅ ui module - EXISTS
) else (
    echo ❌ ui module - MISSING
    set ERROR_FOUND=1
)

if exist "..\src\utils\__init__.py" (
    echo ✅ utils module - EXISTS
) else (
    echo ❌ utils module - MISSING
    set ERROR_FOUND=1
)

echo.
echo [3/4] Python Environment Check...
echo.

python --version
if errorlevel 1 (
    echo ❌ Python not found or not in PATH
    set ERROR_FOUND=1
) else (
    echo ✅ Python is available
)

echo.
echo Checking pip:
pip --version
if errorlevel 1 (
    echo ❌ pip not found
    set ERROR_FOUND=1
) else (
    echo ✅ pip is available
)

echo.
echo [4/4] Dependency Check...
echo.

echo Testing critical imports:

echo Testing pandas...
python -c "import pandas; print('✅ pandas:', pandas.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ pandas - NOT AVAILABLE
    set MISSING_DEPS=1
) else (
    echo ✅ pandas - OK
)

echo Testing openpyxl...
python -c "import openpyxl; print('✅ openpyxl:', openpyxl.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ openpyxl - NOT AVAILABLE
    set MISSING_DEPS=1
) else (
    echo ✅ openpyxl - OK
)

echo Testing PIL/Pillow...
python -c "import PIL; print('✅ PIL/Pillow:', PIL.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ PIL/Pillow - NOT AVAILABLE
    set MISSING_DEPS=1
) else (
    echo ✅ PIL/Pillow - OK
)

echo Testing tkcalendar...
python -c "import tkcalendar; print('✅ tkcalendar - OK')" 2>nul
if errorlevel 1 (
    echo ❌ tkcalendar - NOT AVAILABLE
    set MISSING_DEPS=1
) else (
    echo ✅ tkcalendar - OK
)

echo Testing tkinter...
python -c "import tkinter; print('✅ tkinter - OK')" 2>nul
if errorlevel 1 (
    echo ❌ tkinter - NOT AVAILABLE
    set MISSING_DEPS=1
) else (
    echo ✅ tkinter - OK
)

if defined MISSING_DEPS (
    echo.
    echo ❌ Some dependencies are missing
    echo Run: pip install -r requirements.txt
    set ERROR_FOUND=1
) else (
    echo.
    echo ✅ All dependencies are available
)

echo.
echo ============================================================
echo VERIFICATION RESULTS
echo ============================================================

if defined ERROR_FOUND (
    echo.
    echo ❌ ERRORS FOUND - BUILD WILL LIKELY FAIL
    echo.
    echo Please fix the issues above before running BUILD_QUICK.bat
    echo.
    echo Common solutions:
    echo 1. Install dependencies: pip install -r requirements.txt
    echo 2. Check file paths and directory structure
    echo 3. Ensure you're in the correct directory
) else (
    echo.
    echo ✅ ALL CHECKS PASSED - READY TO BUILD
    echo.
    echo You can now run BUILD_QUICK.bat safely
)

echo.
pause

@echo off
title Pladria v2.5 - Simple Build
color 0A

echo.
echo ============================================================
echo    PLADRIA v2.5 - SIMPLE BUILD (NO VERIFICATION)
echo ============================================================
echo.
echo This script skips verification and builds directly
echo.

cd /d "%~dp0"

echo [1/4] Installing dependencies...
pip install -r requirements.txt --quiet
echo ✅ Dependencies installed

echo.
echo [2/4] Installing PyInstaller (Python 3.13 compatible)...
pip uninstall pyinstaller -y >nul 2>&1
echo Installing latest PyInstaller compatible with Python 3.13...
pip install --no-cache-dir pyinstaller --quiet
if errorlevel 1 (
    echo ❌ Failed to install PyInstaller
    echo Trying with --user flag...
    pip install --user pyinstaller --quiet
)
echo ✅ PyInstaller ready

echo.
echo [3/4] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist" >nul 2>&1
if exist "build" rmdir /s /q "build" >nul 2>&1
echo ✅ Cleanup complete

echo.
echo [4/4] Building application...
echo This may take several minutes...

python -m PyInstaller ^
    --name=Pladria ^
    --onedir ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --icon=../Icone_App_Sharp.ico ^
    --add-data="../Icone_App.png;." ^
    --add-data="../Icone_App_Sharp.ico;." ^
    --add-data="../logo_Sofrecom.png;." ^
    --hidden-import=pandas ^
    --hidden-import=openpyxl ^
    --hidden-import=PIL ^
    --hidden-import=tkcalendar ^
    --exclude-module=matplotlib ^
    --exclude-module=scipy ^
    --exclude-module=pytest ^
    ../src/main.py

if errorlevel 1 (
    echo ❌ Build failed
    echo Try running as administrator or check antivirus settings
    goto :end
)

echo.
echo ✅ BUILD COMPLETED!
if exist "dist\Pladria\Pladria.exe" (
    echo.
    echo Executable created: dist\Pladria\Pladria.exe
    dir "dist\Pladria\Pladria.exe" | find "Pladria.exe"
    echo.
    echo To test: cd dist\Pladria && Pladria.exe
) else (
    echo ❌ Executable not found
)

:end
pause

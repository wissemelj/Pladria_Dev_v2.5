@echo off
title Pladria v2.5 - Quick Build (Fixed)
color 0A

echo.
echo ============================================================
echo    PLADRIA v2.5 - QUICK BUILD (DEPENDENCY CONFLICT FIX)
echo ============================================================
echo.

REM Change to Package directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo [0/6] Verifying all required files exist...
if not exist "..\src\main.py" (
    echo ❌ ERROR: main.py not found at ..\src\main.py
    echo Current directory: %CD%
    goto :error
)
echo ✅ main.py found

if not exist "..\Icone_App_Sharp.ico" (
    echo ❌ ERROR: Icon file not found at ..\Icone_App_Sharp.ico
    goto :error
)
echo ✅ Icon files found

if not exist "..\Icone_App.png" (
    echo ❌ ERROR: PNG icon not found at ..\Icone_App.png
    goto :error
)
echo ✅ PNG icon found

if not exist "..\logo_Sofrecom.png" (
    echo ❌ ERROR: Logo not found at ..\logo_Sofrecom.png
    goto :error
)
echo ✅ Logo found

if not exist "requirements.txt" (
    echo ❌ ERROR: requirements.txt not found in Package directory
    goto :error
)
echo ✅ requirements.txt found

echo ✅ All required files verified
echo.

echo [1/6] Installing/updating dependencies from requirements.txt...
pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    goto :error
)
echo ✅ Dependencies installed

echo.
echo [2/6] Cleaning PyInstaller cache and conflicts...
pip uninstall pyinstaller -y >nul 2>&1
pip uninstall setuptools -y >nul 2>&1
pip install setuptools==68.2.2
pip install --no-cache-dir pyinstaller==5.13.2
if errorlevel 1 (
    echo ❌ Failed to install PyInstaller
    goto :error
)
echo ✅ PyInstaller refreshed with compatible version

echo.
echo [3/6] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist" >nul 2>&1
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "*.spec" del "*.spec" >nul 2>&1
echo ✅ Cleanup complete

echo.
echo [4/6] Building with minimal dependencies (avoiding conflicts)...
echo This may take several minutes...
echo.

REM Use direct PyInstaller command with minimal options to avoid dependency hell
pyinstaller ^
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
    --hidden-import=tkinter ^
    --exclude-module=matplotlib ^
    --exclude-module=scipy ^
    --exclude-module=pytest ^
    --exclude-module=setuptools ^
    --exclude-module=wheel ^
    --exclude-module=pip ^
    ../src/main.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed. Trying ultra-minimal approach...
    echo.

    REM Clean again
    if exist "dist" rmdir /s /q "dist" >nul 2>&1
    if exist "build" rmdir /s /q "build" >nul 2>&1

    REM Ultra-minimal build
    pyinstaller ^
        --name=Pladria_Minimal ^
        --onedir ^
        --windowed ^
        --noconfirm ^
        --clean ^
        --icon=../Icone_App_Sharp.ico ^
        ../src/main.py

    if errorlevel 1 (
        echo ❌ Even minimal build failed
        echo Check Python environment and dependencies
        goto :error
    )

    echo ✅ Minimal build completed
    set BUILD_NAME=Pladria_Minimal
) else (
    echo ✅ Standard build completed
    set BUILD_NAME=Pladria
)

echo.
echo [5/6] Copying additional files...
if exist "dist\%BUILD_NAME%" (
    copy "..\Icone_App.png" "dist\%BUILD_NAME%\" >nul 2>&1
    copy "..\Icone_App_Sharp.ico" "dist\%BUILD_NAME%\" >nul 2>&1
    copy "..\logo_Sofrecom.png" "dist\%BUILD_NAME%\" >nul 2>&1
    echo ✅ Additional files copied
)

echo.
echo [6/6] Verifying build...
if exist "dist\%BUILD_NAME%\%BUILD_NAME%.exe" (
    echo ✅ Executable found: dist\%BUILD_NAME%\%BUILD_NAME%.exe
    dir "dist\%BUILD_NAME%\%BUILD_NAME%.exe" | find "%BUILD_NAME%.exe"
    echo.
    echo ✅ BUILD SUCCESSFUL!
    echo.
    echo To test the application:
    echo   cd dist\%BUILD_NAME%
    echo   %BUILD_NAME%.exe
) else (
    echo ❌ Executable not found
    goto :error
)

echo.
echo ============================================================
echo BUILD COMPLETED SUCCESSFULLY
echo ============================================================
goto :end

:error
echo.
echo ============================================================
echo BUILD FAILED
echo ============================================================
echo.
echo Try these solutions:
echo 1. Run as administrator
echo 2. Disable antivirus temporarily
echo 3. Check that all source files exist in ../src/
echo 4. Try: pip install --force-reinstall pandas openpyxl pillow tkcalendar

:end
pause

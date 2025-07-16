@echo off
title Pladria v2.5 - Simple Build (Fallback)
color 0A

echo.
echo ============================================================
echo    PLADRIA v2.5 - SIMPLE BUILD (FALLBACK METHOD)
echo ============================================================
echo.
echo This is a simplified build method that bypasses complex
echo PyInstaller features and should work even with antivirus.
echo.

REM Change to Package directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist build_temp rmdir /s /q build_temp
if exist dist_temp rmdir /s /q dist_temp
echo ✅ Cleanup complete
echo.

REM Install/update dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul
python -m pip uninstall pyinstaller -y >nul 2>&1
python -m pip install --no-cache-dir pyinstaller>=6.0.0
python -m pip install -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Simple PyInstaller command (no spec file)
echo Building executable with simple method...
echo This may take several minutes...
echo.

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
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkcalendar ^
    --workpath=./build_simple ^
    --distpath=./dist_simple ^
    ../src/main.py

if errorlevel 1 (
    echo.
    echo ❌ Simple build failed
    echo Try running DIAGNOSE_BUILD_ISSUE.bat first
    echo.
    goto :end
)

echo.
echo ✅ Simple build completed!
echo.

REM Move to standard locations
if exist dist rmdir /s /q dist
if exist dist_simple\Pladria (
    move dist_simple dist
    echo ✅ Moved to standard dist directory
)

REM Create portable package
echo Creating portable package...
if exist dist\Pladria_v2.5_Portable rmdir /s /q dist\Pladria_v2.5_Portable
mkdir dist\Pladria_v2.5_Portable

REM Copy all files
xcopy /E /I /Q dist\Pladria\* dist\Pladria_v2.5_Portable\

REM Create launcher
echo @echo off > dist\Pladria_v2.5_Portable\Launch_Pladria.bat
echo title Pladria v2.5 >> dist\Pladria_v2.5_Portable\Launch_Pladria.bat
echo echo Starting Pladria... >> dist\Pladria_v2.5_Portable\Launch_Pladria.bat
echo "Pladria.exe" >> dist\Pladria_v2.5_Portable\Launch_Pladria.bat

REM Create README
echo # Pladria v2.5 > dist\Pladria_v2.5_Portable\README.txt
echo. >> dist\Pladria_v2.5_Portable\README.txt
echo Double-click Pladria.exe to run the application >> dist\Pladria_v2.5_Portable\README.txt
echo Or use Launch_Pladria.bat for convenience >> dist\Pladria_v2.5_Portable\README.txt

echo ✅ Portable package created!
echo.

REM Test the executable
echo Testing executable...
start /wait /min dist\Pladria_v2.5_Portable\Pladria.exe
timeout /t 3 >nul
taskkill /f /im Pladria.exe >nul 2>&1

echo.
echo ============================================================
echo BUILD COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Your application is ready in:
echo dist\Pladria_v2.5_Portable\
echo.
echo Files created:
dir /b dist\Pladria_v2.5_Portable\
echo.

:end
echo Press any key to close...
pause >nul

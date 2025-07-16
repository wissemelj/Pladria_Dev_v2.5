@echo off
title Pladria v2.5 - Build Issue Diagnosis
color 0E

echo.
echo ============================================================
echo    PLADRIA v2.5 - BUILD ISSUE DIAGNOSIS
echo ============================================================
echo.
echo This script will help diagnose PyInstaller build issues.
echo.

REM Change to Package directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo [1/6] Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found
    goto :end
)
echo ✅ Python OK
echo.

echo [2/6] Checking PyInstaller...
pyinstaller --version
if errorlevel 1 (
    echo ❌ PyInstaller not found or corrupted
    echo Installing fresh PyInstaller...
    python -m pip uninstall pyinstaller -y >nul 2>&1
    python -m pip install --no-cache-dir pyinstaller>=6.0.0
    echo ✅ PyInstaller reinstalled
) else (
    echo ✅ PyInstaller OK
)
echo.

echo [3/6] Checking file permissions...
echo test > test_write.tmp
if exist test_write.tmp (
    del test_write.tmp
    echo ✅ Write permissions OK
) else (
    echo ❌ Write permission issue
    echo Try running as administrator
)
echo.

echo [4/6] Checking antivirus interference...
echo This is a test file for antivirus detection > pyinstaller_test.py
timeout /t 2 >nul
if exist pyinstaller_test.py (
    del pyinstaller_test.py
    echo ✅ No immediate antivirus blocking
) else (
    echo ❌ File was deleted - antivirus interference detected
    echo Add this folder to antivirus exclusions
)
echo.

echo [5/6] Checking available disk space...
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do set free=%%a
echo Available space: %free% bytes
echo ✅ Disk space check complete
echo.

echo [6/6] Testing simple PyInstaller build...
echo print("Hello World") > simple_test.py
echo Testing PyInstaller with simple script...
pyinstaller --onefile --clean --noconfirm simple_test.py >nul 2>&1
if exist dist\simple_test.exe (
    echo ✅ PyInstaller basic test PASSED
    rmdir /s /q build >nul 2>&1
    rmdir /s /q dist >nul 2>&1
    del simple_test.py >nul 2>&1
    del simple_test.spec >nul 2>&1
) else (
    echo ❌ PyInstaller basic test FAILED
    echo This indicates a fundamental PyInstaller issue
)
echo.

echo ============================================================
echo DIAGNOSIS COMPLETE
echo ============================================================
echo.
echo If all tests passed, try the build again.
echo If tests failed, follow the suggestions above.
echo.
echo Common solutions:
echo 1. Add this folder to antivirus exclusions
echo 2. Run as administrator
echo 3. Close file managers/editors in this directory
echo 4. Restart your computer
echo.

:end
pause

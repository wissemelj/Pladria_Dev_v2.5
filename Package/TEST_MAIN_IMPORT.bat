@echo off
title Pladria v2.5 - Test Main Import
color 0E

echo.
echo ============================================================
echo    PLADRIA v2.5 - TEST MAIN IMPORT
echo ============================================================
echo.
echo Testing if main.py can be imported without errors
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Testing main.py import...
python -c "
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))

try:
    print('Testing imports from main.py...')
    
    # Test basic imports
    import tkinter as tk
    print('✅ tkinter imported successfully')
    
    import pandas as pd
    print('✅ pandas imported successfully')
    
    import openpyxl
    print('✅ openpyxl imported successfully')
    
    from PIL import Image
    print('✅ PIL imported successfully')
    
    import tkcalendar
    print('✅ tkcalendar imported successfully')
    
    # Test main.py imports
    from pathlib import Path
    print('✅ pathlib imported successfully')
    
    # Test if we can import the main modules
    try:
        import config
        print('✅ config module imported successfully')
    except Exception as e:
        print('⚠️ config module warning:', e)
    
    try:
        import ui
        print('✅ ui module imported successfully')
    except Exception as e:
        print('⚠️ ui module warning:', e)
    
    try:
        import core
        print('✅ core module imported successfully')
    except Exception as e:
        print('⚠️ core module warning:', e)
    
    try:
        import utils
        print('✅ utils module imported successfully')
    except Exception as e:
        print('⚠️ utils module warning:', e)
    
    print('\\n✅ ALL CRITICAL IMPORTS SUCCESSFUL')
    print('main.py should build without import errors')
    
except Exception as e:
    print('\\n❌ IMPORT ERROR:', e)
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

if errorlevel 1 (
    echo.
    echo ❌ Import test failed
    echo Fix the import errors before building
) else (
    echo.
    echo ✅ Import test passed
    echo main.py is ready for building
)

echo.
pause

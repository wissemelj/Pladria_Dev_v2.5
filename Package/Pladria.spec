# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\Pladria_Dev_v2.5\\src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('../Icone_App.png', '.'), ('../Icone_App_Sharp.ico', '.'), ('../logo_Sofrecom.png', '.'), ('../Background.png', '.')],
    hiddenimports=['pandas', 'openpyxl', 'PIL', 'tkcalendar', 'requests', 'packaging', 'pandas._libs.tslibs.base', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pytest', 'numpy.testing', 'IPython', 'jupyter', 'setuptools', 'wheel', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx', 'sqlite3', 'unittest', 'doctest'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    exclude_binaries=True,
    name='Pladria',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Pladria_Dev_v2.5\\Icone_App_Sharp.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='Pladria',
)

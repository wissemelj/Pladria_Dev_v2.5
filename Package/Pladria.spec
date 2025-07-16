# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('../Icone_App.png', '.'), ('../Icone_App_Sharp.ico', '.'), ('../logo_Sofrecom.png', '.')],
    hiddenimports=['pandas', 'openpyxl', 'PIL', 'PIL.Image', 'PIL.ImageTk', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkcalendar'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pladria',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['..\\Icone_App_Sharp.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Pladria',
)

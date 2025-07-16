# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pladria v2.5 (One-file mode)
Generates a single executable file with all dependencies embedded.
Slower startup time but easier distribution.
"""

import os
import sys
from pathlib import Path

# Configuration
APP_NAME = 'Pladria_onefile'
APP_VERSION = '2.5'
MAIN_SCRIPT = '../src/main.py'
ICON_PATH = '../Icone_App_Sharp.ico'

# Paths
current_dir = Path('.')
src_dir = current_dir.parent / 'src'
root_dir = current_dir.parent

# Data files to include (images, icons, etc.)
datas = [
    ('../Icone_App.png', '.'),
    ('../Icone_App_Sharp.ico', '.'),
    ('../logo_Sofrecom.png', '.'),
]

# Hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    # Core dependencies
    'pandas',
    'openpyxl',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',

    # Tkinter and UI
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    'tkcalendar',
    'tkcalendar.calendar_',
    'tkcalendar.dateentry',

    # Standard library
    'datetime',
    'calendar',
    'pathlib',
    'json',
    'logging',
    'logging.handlers',
    'threading',
    'concurrent.futures',
    'queue',
    'subprocess',
    'getpass',
    'platform',
    'psutil',
    'time',
    'os',
    'sys',
    're',
    'functools',
    'typing',
    'collections',
    'itertools',
    'shutil',
    'tempfile',
    'uuid',
    'hashlib',
    'base64',

    # Application modules
    'config',
    'config.constants',
    'core',
    'core.file_processor',
    'core.data_validator',
    'core.excel_generator',
    'utils',
    'utils.lazy_imports',
    'utils.file_utils',
    'utils.logging_config',
    'utils.performance',
    'utils.session_manager',
    'ui',
    'ui.main_window',
    'ui.splash_screen',
    'ui.navigation',
    'ui.home_screen',
    'ui.settings_screen',
    'ui.styles',
    'ui.keyboard_shortcuts',
    'ui.modules',
    'ui.modules.suivi_generator_module',
    'ui.modules.suivi_global_module',
    'ui.modules.team_stats_module',
    'ui.modules.data_viewer_module',
    'ui.modules.quality_control_module',
    'ui.components',
    'ui.components.file_import',
    'ui.components.project_info',
    'ui.components.generation',
    'ui.components.header_footer',
]

# Binaries (none needed for this app)
binaries = []

# Analysis
a = Analysis(
    [MAIN_SCRIPT],
    pathex=[str(current_dir.absolute()), str(src_dir.absolute())],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude only clearly unused modules to reduce size
        'matplotlib',
        'scipy',
        'numpy.testing',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'test',
        'tests',
        '_pytest',
        'py.test',
        'pluggy',
        'iniconfig',
        'tomli',
        'exceptiongroup',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate files
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Single file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
    version_file=None,
)

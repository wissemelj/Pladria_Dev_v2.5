#!/usr/bin/env python3
"""
Unified Build Configuration for Pladria
Single source of truth for all build settings, dependencies, and configurations
"""

from pathlib import Path
from typing import List, Dict, Any

class BuildConfig:
    """Centralized configuration for Pladria build system"""
    
    # Version info
    VERSION = "2.5.0"  # Will be read from constants.py if available
    
    # Core dependencies (must be installed)
    CORE_DEPENDENCIES = [
        "pandas>=1.5.0,<2.3.0",
        "openpyxl>=3.0.0,<3.2.0", 
        "Pillow>=9.0.0,<11.0.0",
        "tkcalendar>=1.6.0,<2.0.0",
        "requests>=2.25.0,<3.0.0",
        "packaging>=21.0,<25.0"
    ]
    
    # Build dependencies
    BUILD_DEPENDENCIES = [
        "setuptools>=75.8.2",
        "wheel>=0.37.0",
        "pyinstaller"
    ]
    
    # PyInstaller hidden imports
    HIDDEN_IMPORTS = [
        "pandas",
        "openpyxl", 
        "PIL",
        "tkcalendar",
        "requests",
        "packaging",
        # Essential sub-dependencies
        "pandas._libs.tslibs.base",
        "PIL._tkinter_finder"
    ]
    
    # Packages to exclude from build (reduces size)
    EXCLUDED_MODULES = [
        "matplotlib", "scipy", "pytest", "numpy.testing", "IPython",
        "jupyter", "setuptools", "wheel", "PyQt5", "PyQt6", 
        "PySide2", "PySide6", "wx", "sqlite3", "unittest", "doctest"
    ]
    
    # Asset files to include
    ASSETS = [
        "Icone_App.png",
        "Icone_App_Sharp.ico", 
        "logo_Sofrecom.png",
        "Background.png"
    ]
    
    @classmethod
    def get_version(cls) -> str:
        """Get version from constants.py or fallback to default"""
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            from config.constants import AppInfo
            return AppInfo.VERSION
        except Exception:
            return cls.VERSION
    
    @classmethod
    def get_all_dependencies(cls) -> List[str]:
        """Get all dependencies (core + build)"""
        return cls.CORE_DEPENDENCIES + cls.BUILD_DEPENDENCIES
    
    @classmethod
    def get_pyinstaller_args(cls, src_dir: Path, icon_path: Path) -> List[str]:
        """Generate PyInstaller command arguments"""
        args = [
            "pyinstaller",
            "--name=Pladria",
            "--onedir", 
            "--windowed",
            "--noconfirm",
            "--clean",
            f"--icon={icon_path}",
            "--optimize=2",
            "--strip"
        ]
        
        # Add asset data
        for asset in cls.ASSETS:
            args.append(f"--add-data=../{asset};.")
        
        # Add hidden imports
        for imp in cls.HIDDEN_IMPORTS:
            args.append(f"--hidden-import={imp}")
        
        # Add exclusions
        for exc in cls.EXCLUDED_MODULES:
            args.append(f"--exclude-module={exc}")
        
        # Add main script
        args.append(str(src_dir / "main.py"))
        
        return args
    
    @classmethod
    def get_import_tests(cls) -> List[tuple]:
        """Get list of import tests to verify dependencies"""
        return [
            ("tkinter", "import tkinter"),
            ("pandas", "import pandas"),
            ("openpyxl", "import openpyxl"), 
            ("PIL", "from PIL import Image"),
            ("tkcalendar", "from tkcalendar import Calendar"),
            ("requests", "import requests"),
            ("packaging", "from packaging import version")
        ]

class SimpleProgress:
    """Simplified progress tracking without complex animations"""
    
    def __init__(self, total_steps: int = 100):
        self.total_steps = total_steps
        self.current_step = 0
        self.current_desc = ""
    
    def update(self, step: int, description: str = ""):
        """Update progress"""
        self.current_step = min(step, self.total_steps)
        if description:
            self.current_desc = description
        
        percentage = (self.current_step / self.total_steps) * 100
        bar_length = 30
        filled = int((self.current_step / self.total_steps) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"\r[{bar}] {percentage:5.1f}% - {self.current_desc}", end="", flush=True)
    
    def finish(self, message: str = "Complete"):
        """Finish progress tracking"""
        bar = "█" * 30
        print(f"\r[{bar}] 100.0% - {message}")
        print()  # New line

class PathConfig:
    """Path configuration helper"""
    
    def __init__(self, package_dir: Path = None):
        self.package_dir = package_dir or Path(__file__).parent
        self.src_dir = self.package_dir.parent / "src"
        self.dist_dir = self.package_dir / "dist"
        self.build_dir = self.package_dir / "build"
        self.icon_path = self.package_dir.parent / "Icone_App_Sharp.ico"
    
    def get_asset_paths(self) -> List[Path]:
        """Get paths to all asset files"""
        return [self.package_dir.parent / asset for asset in BuildConfig.ASSETS]

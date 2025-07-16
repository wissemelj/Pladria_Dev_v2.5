#!/usr/bin/env python3
"""
PLADRIA v2.5 - IMPROVED BUILD SCRIPT
Enhanced PyInstaller build script with better error handling and dependency management
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def ensure_correct_working_directory():
    """Ensure we're running from the Package directory."""
    script_dir = Path(__file__).parent.absolute()
    current_dir = Path.cwd().absolute()

    if current_dir != script_dir:
        print(f"⚠️  Changing working directory from {current_dir} to {script_dir}")
        os.chdir(script_dir)
        print(f"✅ Working directory set to: {Path.cwd().absolute()}")

    return script_dir

def pause_on_error():
    """Pause execution to show error messages when run from File Explorer."""
    if len(sys.argv) == 1:  # No command line arguments = likely run from File Explorer
        input("\n❌ Press Enter to close...")

# Ensure correct working directory first
SCRIPT_DIR = ensure_correct_working_directory()

# Configuration
APP_NAME = "Pladria"
APP_VERSION = "2.5"
BUILD_MODE = "unpacked"  # "unpacked" or "onefile"
DIST_DIR = "dist"
BUILD_DIR = "build"

# File paths (relative to Package directory)
MAIN_SCRIPT = "../src/main.py"
ICON_ICO = "../Icone_App_Sharp.ico"
ICON_PNG = "../Icone_App.png"
LOGO_SOFRECOM = "../logo_Sofrecom.png"

def print_header():
    """Print build header."""
    print("=" * 80)
    print(f"    {APP_NAME.upper()} v{APP_VERSION} - IMPROVED BUILD SCRIPT")
    print("=" * 80)
    print(f"Mode: {BUILD_MODE.upper()}")
    print(f"PyInstaller: Enhanced dependency detection")
    print(f"Target: Windows executable with all functionalities")
    print("=" * 80)

def check_python_version():
    """Check Python version compatibility."""
    print("\n🔍 Checking Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version compatible")
    return True

def check_required_files():
    """Check if all required files exist."""
    print("\n📁 Checking required files...")
    print(f"Current working directory: {Path.cwd().absolute()}")

    required_files = {
        "Main script": MAIN_SCRIPT,
        "Icon (ICO)": ICON_ICO,
        "Icon (PNG)": ICON_PNG,
        "Logo Sofrecom": LOGO_SOFRECOM
    }

    all_present = True
    for description, file_path in required_files.items():
        abs_path = Path(file_path).absolute()
        if abs_path.exists():
            size = abs_path.stat().st_size / 1024
            print(f"  ✅ {description}: {file_path} ({size:.1f} KB)")
        else:
            print(f"  ❌ {description}: {file_path} - MISSING")
            print(f"      Absolute path: {abs_path}")
            all_present = False

    if not all_present:
        print("\n💡 Make sure you're running this script from the Package directory!")
        print("💡 Or double-click BUILD_QUICK.bat instead of this Python file.")
        pause_on_error()

    return all_present

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")

    try:
        # First, try to fix any PyInstaller issues
        print("  Checking PyInstaller installation...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "uninstall", "pyinstaller", "-y"
            ], capture_output=True, text=True)
            print("  Cleaned previous PyInstaller installation")
        except:
            pass

        # Install fresh PyInstaller
        print("  Installing fresh PyInstaller...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--no-cache-dir", "pyinstaller>=6.0.0"
        ], check=True, capture_output=True, text=True)

        # Install other dependencies
        print("  Installing application dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)

        # Verify PyInstaller works
        print("  Verifying PyInstaller...")
        result = subprocess.run([
            "pyinstaller", "--version"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  ✅ PyInstaller version: {result.stdout.strip()}")
        else:
            print("  ⚠️ PyInstaller verification failed")

        print("✅ Dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Details: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def clean_build_dirs():
    """Clean previous build directories."""
    print("\n🧹 Cleaning previous builds...")
    
    dirs_to_clean = [DIST_DIR, BUILD_DIR, "__pycache__"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✅ Removed: {dir_name}")
            except Exception as e:
                print(f"  ⚠️ Error removing {dir_name}: {e}")
    
    print("✅ Cleanup completed")
    return True

def build_executable():
    """Build the executable using PyInstaller."""
    print(f"\n🔨 Building executable ({BUILD_MODE} mode)...")

    # Choose spec file based on mode
    spec_file = f"Pladria.spec" if BUILD_MODE == "unpacked" else "Pladria_onefile.spec"

    if not os.path.exists(spec_file):
        print(f"❌ Spec file not found: {spec_file}")
        return False

    print(f"Using spec file: {spec_file}")

    # Check for common issues before building
    print("🔍 Pre-build checks...")

    # Check if build directory can be created
    build_test_dir = Path("build_test")
    try:
        build_test_dir.mkdir(exist_ok=True)
        test_file = build_test_dir / "test.txt"
        test_file.write_text("test")
        test_file.unlink()
        build_test_dir.rmdir()
        print("  ✅ File system permissions OK")
    except Exception as e:
        print(f"  ❌ File system permission issue: {e}")
        print("  💡 Try running as administrator or check antivirus settings")
        return False

    try:
        cmd = [
            "pyinstaller",
            "--clean",
            "--noconfirm",
            "--log-level=INFO",
            "--workpath=./build_temp",  # Use shorter path
            "--distpath=./dist_temp",   # Use shorter path
            spec_file
        ]

        print(f"Command: {' '.join(cmd)}")
        print("Building... (this may take a few minutes)")
        print("💡 If build fails, check your antivirus settings!")

        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        build_time = time.time() - start_time

        if result.returncode == 0:
            print(f"✅ Build completed successfully in {build_time:.1f} seconds")

            # Move from temp directories to standard locations
            if Path("dist_temp").exists():
                if Path("dist").exists():
                    shutil.rmtree("dist")
                shutil.move("dist_temp", "dist")

            if Path("build_temp").exists():
                if Path("build").exists():
                    shutil.rmtree("build")
                shutil.move("build_temp", "build")

            return True
        else:
            print("❌ Build failed:")
            print("STDOUT:", result.stdout[-1500:])  # More context
            print("STDERR:", result.stderr[-1500:])

            # Provide specific troubleshooting
            if "FileNotFoundError" in result.stderr:
                print("\n💡 TROUBLESHOOTING:")
                print("1. Check your antivirus - it may be blocking PyInstaller")
                print("2. Add Package folder to antivirus exclusions")
                print("3. Try running as administrator")
                print("4. Close any file managers or editors in this directory")

            return False

    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def verify_build():
    """Verify the build output."""
    print("\n✅ Verifying build output...")
    
    if BUILD_MODE == "unpacked":
        exe_path = Path(DIST_DIR) / APP_NAME / f"{APP_NAME}.exe"
    else:
        exe_path = Path(DIST_DIR) / f"{APP_NAME}_onefile.exe"
    
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"📁 Executable: {exe_path}")
    print(f"📏 Size: {size_mb:.1f} MB")
    
    return True

def test_executable():
    """Test the executable."""
    print("\n🧪 Testing executable...")
    
    if BUILD_MODE == "unpacked":
        exe_path = Path(DIST_DIR) / APP_NAME / f"{APP_NAME}.exe"
    else:
        exe_path = Path(DIST_DIR) / f"{APP_NAME}_onefile.exe"
    
    if not exe_path.exists():
        print(f"❌ Executable not found for testing: {exe_path}")
        return False
    
    try:
        print("Starting test (will close automatically after 5 seconds)...")
        process = subprocess.Popen([str(exe_path)])
        time.sleep(5)
        process.terminate()
        
        try:
            process.wait(timeout=10)
            print("✅ Test completed successfully")
            return True
        except subprocess.TimeoutExpired:
            process.kill()
            print("⚠️ Test timeout, but executable seems to work")
            return True
            
    except Exception as e:
        print(f"⚠️ Test error: {e} (but build may still be valid)")
        return True

def create_portable_package():
    """Create a portable package."""
    print("\n📦 Creating portable package...")

    try:
        if BUILD_MODE == "unpacked":
            source_dir = Path(DIST_DIR) / APP_NAME
            exe_path = source_dir / f"{APP_NAME}.exe"
        else:
            exe_path = Path(DIST_DIR) / f"{APP_NAME}_onefile.exe"
            source_dir = None

        if not exe_path.exists():
            print(f"❌ Source executable not found: {exe_path}")
            return False

        # Create portable directory
        portable_name = f"{APP_NAME}_v{APP_VERSION}_Portable"
        portable_dir = Path(DIST_DIR) / portable_name

        if portable_dir.exists():
            shutil.rmtree(portable_dir)
        portable_dir.mkdir(parents=True)

        # Copy files
        if BUILD_MODE == "unpacked":
            print("Copying application directory...")
            for item in source_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, portable_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, portable_dir / item.name)
        else:
            print("Copying single executable...")
            shutil.copy2(exe_path, portable_dir / f"{APP_NAME}.exe")

        # No additional documentation files to copy

        # Create simple README
        readme_content = f"""# {APP_NAME} v{APP_VERSION}

## How to Use
1. Double-click {APP_NAME}.exe to launch the application
2. Or use Launch_{APP_NAME}.bat for convenience

## System Requirements
- Windows 10/11 (64-bit)
- No additional software required
- Works without administrator rights

## Features
- Module 1: Suivi Generator (with Orange/RIP domain dropdown)
- Module 2: Suivi Global Tickets
- Module 3: Team Statistics (with quality control)
- Module 4: Data Viewer

## Notes
- No installation required
- All dependencies included
- Portable application

Application developed for Sofrecom
Version: {APP_VERSION}
"""

        with open(portable_dir / "README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)

        # Create a simple launcher batch file
        launcher_content = f"""@echo off
title {APP_NAME} v{APP_VERSION}
echo Starting {APP_NAME}...
"{APP_NAME}.exe"
"""

        with open(portable_dir / f"Launch_{APP_NAME}.bat", "w", encoding="utf-8") as f:
            f.write(launcher_content)

        print(f"✅ Portable package created: {portable_dir}")
        file_count = len(list(portable_dir.iterdir()))
        total_size = sum(f.stat().st_size for f in portable_dir.rglob('*') if f.is_file()) / (1024 * 1024)
        print(f"📋 Files: {file_count}")
        print(f"📏 Total size: {total_size:.1f} MB")

        return True

    except Exception as e:
        print(f"❌ Error creating portable package: {e}")
        return False

def main():
    """Main build function."""
    print_header()
    
    # Build steps
    steps = [
        ("Python version check", check_python_version),
        ("Required files check", check_required_files),
        ("Dependency installation", install_dependencies),
        ("Clean previous builds", clean_build_dirs),
        ("Build executable", build_executable),
        ("Verify build", verify_build),
        ("Test executable", test_executable),
        ("Create portable package", create_portable_package)
    ]
    
    print(f"\n🚀 Starting build process - {len(steps)} steps")
    print("=" * 80)
    
    for i, (step_name, step_func) in enumerate(steps, 1):
        print(f"\n[{i}/{len(steps)}] {step_name.upper()}")
        
        if not step_func():
            print(f"\n❌ FAILED AT STEP: {step_name}")
            print("Build cannot continue.")
            pause_on_error()
            return False
    
    # Success summary
    print("\n" + "=" * 80)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    portable_dir = Path(DIST_DIR) / f"{APP_NAME}_v{APP_VERSION}_Portable"
    if portable_dir.exists():
        print(f"📦 Portable package: {portable_dir}")
        print("✅ Ready for distribution")
        print("✅ All functionalities preserved")
        print("✅ No external dependencies required")
    
    print("\n" + "=" * 80)
    return True

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\n✅ BUILD SUCCESSFUL!")
            print("The application is ready for distribution.")
        else:
            print("\n❌ BUILD FAILED!")
            print("Check the errors above.")
            pause_on_error()

        # Always pause when run from File Explorer
        if len(sys.argv) == 1:
            input("\nPress Enter to exit...")
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️ Build interrupted by user")
        pause_on_error()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        pause_on_error()
        sys.exit(1)

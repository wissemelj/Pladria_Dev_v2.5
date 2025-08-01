#!/usr/bin/env python3
"""
Unified Build & Package Script for Pladria
Combines all packaging functionality in one script
"""

import os
import sys
import subprocess
import zipfile
import shutil
import hashlib
import tempfile
import glob
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta

class ProgressBar:
    """Advanced progress bar with time estimation and visual feedback"""

    def __init__(self, total_steps=100, width=40):
        self.total_steps = total_steps
        self.current_step = 0
        self.width = width
        self.start_time = None
        self.step_times = []
        self.current_description = ""
        self.is_running = False
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.spinner_index = 0
        self.spinner_thread = None
        self.last_update_time = 0

    def start(self, description="Starting..."):
        """Start the progress bar"""
        self.start_time = time.time()
        self.current_description = description
        self.is_running = True
        self.update(0, description)

    def update(self, step, description=""):
        """Update progress bar with current step and description"""
        if not self.is_running:
            return

        self.current_step = min(step, self.total_steps)
        if description:
            self.current_description = description

        # Record step time for estimation
        current_time = time.time()
        if self.start_time:
            self.step_times.append(current_time - self.start_time)

        # Throttle updates to avoid flickering (max 10 updates per second)
        if current_time - self.last_update_time < 0.1:
            return
        self.last_update_time = current_time

        self._render()

    def _render(self):
        """Render the progress bar"""
        if not self.is_running:
            return

        # Calculate percentage
        percentage = (self.current_step / self.total_steps) * 100

        # Calculate filled blocks
        filled_blocks = int((self.current_step / self.total_steps) * self.width)
        empty_blocks = self.width - filled_blocks

        # Create visual bar
        bar = "█" * filled_blocks + "░" * empty_blocks

        # Calculate time estimation
        time_info = self._get_time_estimation()

        # Format output
        output = f"\r🔄 [{bar}] {percentage:5.1f}% {time_info} - {self.current_description}"

        # Ensure we don't exceed terminal width
        if len(output) > 120:
            output = output[:117] + "..."

        print(output, end="", flush=True)

    def _get_time_estimation(self):
        """Calculate estimated time remaining"""
        if not self.step_times or self.current_step == 0:
            return "⏱️ --:--"

        # Calculate average time per step
        avg_time_per_step = sum(self.step_times[-10:]) / len(self.step_times[-10:])  # Use last 10 for better accuracy

        # Estimate remaining time
        remaining_steps = self.total_steps - self.current_step
        estimated_remaining = remaining_steps * (avg_time_per_step / max(1, self.current_step))

        if estimated_remaining < 60:
            return f"⏱️ {estimated_remaining:.0f}s"
        elif estimated_remaining < 3600:
            minutes = int(estimated_remaining // 60)
            seconds = int(estimated_remaining % 60)
            return f"⏱️ {minutes}:{seconds:02d}"
        else:
            hours = int(estimated_remaining // 3600)
            minutes = int((estimated_remaining % 3600) // 60)
            return f"⏱️ {hours}:{minutes:02d}h"

    def spinner_start(self, description="Processing..."):
        """Start an indeterminate spinner for unknown duration tasks"""
        self.current_description = description
        self.is_running = True
        self.spinner_thread = threading.Thread(target=self._spinner_loop, daemon=True)
        self.spinner_thread.start()

    def _spinner_loop(self):
        """Run the spinner animation"""
        while self.is_running:
            spinner_char = self.spinner_chars[self.spinner_index % len(self.spinner_chars)]
            output = f"\r{spinner_char} {self.current_description}"
            print(output, end="", flush=True)
            self.spinner_index += 1
            time.sleep(0.1)

    def finish(self, description="Complete!"):
        """Finish the progress bar"""
        self.is_running = False
        if self.spinner_thread:
            self.spinner_thread.join(timeout=0.5)

        # Show final completed bar
        bar = "█" * self.width
        elapsed_time = time.time() - self.start_time if self.start_time else 0

        if elapsed_time < 60:
            time_str = f"⏱️ {elapsed_time:.1f}s"
        else:
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_str = f"⏱️ {minutes}:{seconds:02d}"

        output = f"\r✅ [{bar}] 100.0% {time_str} - {description}"
        print(output)
        print()  # New line after completion

class PladriaBuilder:
    def __init__(self):
        self.version = self.get_version()
        self.package_dir = Path(__file__).parent
        self.src_dir = self.package_dir.parent / "src"
        self.dist_dir = self.package_dir / "dist"
        self.build_dir = self.package_dir / "build"
        
    def get_version(self):
        """Get version from constants.py"""
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            from config.constants import AppInfo
            return AppInfo.VERSION
        except Exception as e:
            print(f"❌ Error reading version: {e}")
            return input("Enter version (e.g., 2.6.0): ").strip()
    
    def run_cmd(self, cmd, desc, capture=False, progress_bar=None, step_weight=1):
        """Run command with error handling and optional progress tracking"""
        if progress_bar:
            progress_bar.current_description = desc
        else:
            print(f"⏳ {desc}...")

        try:
            if capture:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(cmd, shell=True)

            if result.returncode == 0:
                if not progress_bar:
                    print(f"✅ {desc} success")
                return True, result.stdout if capture else ""
            else:
                if progress_bar:
                    progress_bar.finish(f"❌ {desc} failed")
                else:
                    print(f"❌ {desc} failed")
                if capture and result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                return False, result.stderr if capture else ""
        except Exception as e:
            if progress_bar:
                progress_bar.finish(f"❌ Error {desc}: {e}")
            else:
                print(f"❌ Error {desc}: {e}")
            return False, str(e)
    
    def fix_dependencies(self, progress_bar=None):
        """Fix Python dependencies with progress tracking"""
        if not progress_bar:
            print("\n🔧 Fixing dependencies...")

        # Calculate total steps for progress
        core_packages = ["setuptools", "wheel", "pyinstaller"]
        total_steps = 1 + len(core_packages) + 1 + 7  # pip + core packages + requirements + imports
        current_step = 0

        if progress_bar:
            progress_bar.start("Updating pip...")

        # Update pip
        current_step += 1
        if progress_bar:
            progress_bar.update(current_step, "Updating pip...")
        success, _ = self.run_cmd("python -m pip install --upgrade pip", "Update pip", progress_bar=progress_bar)

        # Update core packages
        for pkg in core_packages:
            current_step += 1
            if progress_bar:
                progress_bar.update(current_step, f"Updating {pkg}...")
            self.run_cmd(f"pip install --upgrade {pkg}", f"Update {pkg}", progress_bar=progress_bar)

        # Install requirements
        current_step += 1
        if progress_bar:
            progress_bar.update(current_step, "Installing requirements...")
        if (self.package_dir / "requirements.txt").exists():
            self.run_cmd("pip install --upgrade -r requirements.txt", "Install requirements", progress_bar=progress_bar)

        # Test critical imports
        if not progress_bar:
            print("\n🧪 Testing imports...")

        imports = [
            ("tkinter", "import tkinter"),
            ("pandas", "import pandas"),
            ("openpyxl", "import openpyxl"),
            ("PIL", "from PIL import Image"),
            ("tkcalendar", "from tkcalendar import Calendar"),
            ("requests", "import requests"),
            ("packaging", "from packaging import version")
        ]

        all_ok = True
        for name, import_stmt in imports:
            current_step += 1
            if progress_bar:
                progress_bar.update(current_step, f"Testing {name} import...")
            try:
                exec(import_stmt)
                if not progress_bar:
                    print(f"   ✅ {name}")
            except ImportError:
                if not progress_bar:
                    print(f"   ❌ {name}")
                all_ok = False

            # Small delay to show progress
            if progress_bar:
                time.sleep(0.2)

        if progress_bar:
            progress_bar.finish("Dependencies check complete")

        return all_ok
    
    def cleanup_build(self):
        """Clean previous builds"""
        print("\n🧹 Cleaning previous builds...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        files_to_clean = list(self.package_dir.glob("*.spec"))
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✅ Removed {dir_path.name}/")
        
        for file_path in files_to_clean:
            file_path.unlink()
            print(f"   ✅ Removed {file_path.name}")
    
    def build_app(self, progress_bar=None):
        """Build application with PyInstaller and progress tracking"""
        if not progress_bar:
            print(f"\n📦 Building Pladria v{self.version}...")

        # PyInstaller command
        cmd = [
            "pyinstaller",
            "--name=Pladria",
            "--onedir",
            "--windowed",
            "--noconfirm",
            "--clean",
            f"--icon=../Icone_App_Sharp.ico",
            "--add-data=../Icone_App.png;.",
            "--add-data=../Icone_App_Sharp.ico;.",
            "--add-data=../logo_Sofrecom.png;.",
            "--add-data=../Background.png;.",
            "--hidden-import=pandas",
            "--hidden-import=openpyxl",
            "--hidden-import=PIL",
            "--hidden-import=tkcalendar",
            "--hidden-import=requests",
            "--hidden-import=packaging",
            "--exclude-module=matplotlib",
            "--exclude-module=scipy",
            "--exclude-module=pytest",
            "../src/main.py"
        ]

        if progress_bar:
            progress_bar.current_description = "Compiling with PyInstaller..."

        success, _ = self.run_cmd(" ".join(cmd), "PyInstaller build", progress_bar=progress_bar)

        if not success:
            if progress_bar:
                progress_bar.current_description = "Standard build failed, trying minimal build..."
            else:
                print("\n⚠️ Standard build failed, trying minimal build...")

            minimal_cmd = [
                "pyinstaller",
                "--name=Pladria_Minimal",
                "--onedir",
                "--windowed",
                "--noconfirm",
                "--clean",
                f"--icon=../Icone_App_Sharp.ico",
                "../src/main.py"
            ]
            success, _ = self.run_cmd(" ".join(minimal_cmd), "Minimal build", progress_bar=progress_bar)
            if success:
                if progress_bar:
                    progress_bar.current_description = "Renaming minimal build..."
                # Rename minimal build
                minimal_path = self.dist_dir / "Pladria_Minimal"
                target_path = self.dist_dir / "Pladria"
                if minimal_path.exists():
                    minimal_path.rename(target_path)

        # Copy additional files
        if success:
            if progress_bar:
                progress_bar.current_description = "Copying additional assets..."
            app_dir = self.dist_dir / "Pladria"
            if app_dir.exists():
                assets = ["Icone_App.png", "Icone_App_Sharp.ico", "logo_Sofrecom.png", "Background.png"]
                for i, asset in enumerate(assets):
                    if progress_bar:
                        progress_bar.current_description = f"Copying {asset}..."
                    src = self.package_dir.parent / asset
                    if src.exists():
                        shutil.copy2(src, app_dir)
                        if not progress_bar:
                            print(f"   ✅ Copied {asset}")
                    # Small delay to show progress
                    if progress_bar:
                        time.sleep(0.1)

        return success and (self.dist_dir / "Pladria" / "Pladria.exe").exists()

    def create_update_package(self, progress_bar=None):
        """Create update package ZIP with progress tracking"""
        if not progress_bar:
            print(f"\n📦 Creating update package v{self.version}...")

        build_path = self.dist_dir / "Pladria"
        if not build_path.exists():
            error_msg = "❌ Build directory not found"
            if progress_bar:
                progress_bar.finish(error_msg)
            else:
                print(error_msg)
            return None

        package_name = f"pladria-v{self.version}-update.zip"
        package_path = self.package_dir / package_name

        # Essential files to include
        essential_files = [
            "Pladria.exe",
            "Background.png",
            "Icone_App.png",
            "Icone_App_Sharp.ico",
            "logo_Sofrecom.png"
        ]

        # Essential directories
        essential_dirs = ["_internal"]

        try:
            if progress_bar:
                progress_bar.current_description = "Creating ZIP archive..."

            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:

                # Add files
                if not progress_bar:
                    print("\n📄 Adding files:")

                for i, file_name in enumerate(essential_files):
                    if progress_bar:
                        progress_bar.current_description = f"Adding {file_name}..."

                    file_path = build_path / file_name
                    if file_path.exists():
                        zipf.write(file_path, file_name)
                        size = file_path.stat().st_size
                        if not progress_bar:
                            print(f"   ✅ {file_name} ({size:,} bytes)")
                    else:
                        if not progress_bar:
                            print(f"   ⚠️ {file_name} not found")

                    # Small delay to show progress
                    if progress_bar:
                        time.sleep(0.1)

                # Add directories
                if not progress_bar:
                    print("\n📁 Adding directories:")

                for dir_name in essential_dirs:
                    if progress_bar:
                        progress_bar.current_description = f"Adding {dir_name} directory..."

                    dir_path = build_path / dir_name
                    if dir_path.exists():
                        file_count = 0
                        total_size = 0

                        # Count files first for progress tracking
                        all_files = []
                        for root, _, files in os.walk(dir_path):
                            for file in files:
                                all_files.append((root, file))

                        for i, (root, file) in enumerate(all_files):
                            if progress_bar and i % 10 == 0:  # Update every 10 files
                                progress_bar.current_description = f"Adding {dir_name}... ({i+1}/{len(all_files)} files)"

                            file_path = Path(root) / file
                            arc_name = file_path.relative_to(build_path)
                            zipf.write(file_path, str(arc_name))
                            file_count += 1
                            total_size += file_path.stat().st_size

                        if not progress_bar:
                            print(f"   ✅ {dir_name}/ ({file_count} files, {total_size:,} bytes)")
                    else:
                        if not progress_bar:
                            print(f"   ⚠️ {dir_name}/ not found")

                # Add metadata
                if progress_bar:
                    progress_bar.current_description = "Adding metadata..."

                metadata = f"""# Pladria Update Package
Version: {self.version}
Created: {datetime.now().isoformat()}
Package Type: Full Update

## Files Included:
"""
                for file_name in essential_files:
                    metadata += f"- {file_name}\n"
                for dir_name in essential_dirs:
                    metadata += f"- {dir_name}/\n"

                zipf.writestr("UPDATE_INFO.txt", metadata)
                if not progress_bar:
                    print(f"   ✅ UPDATE_INFO.txt (metadata)")

            # Calculate stats
            package_size = package_path.stat().st_size
            package_size_mb = package_size / (1024 * 1024)

            # Calculate SHA256
            if progress_bar:
                progress_bar.current_description = "Calculating SHA256 checksum..."
            else:
                print(f"\n🔐 Calculating SHA256...")

            sha256_hash = hashlib.sha256()
            with open(package_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            checksum = sha256_hash.hexdigest()

            if not progress_bar:
                print(f"\n✅ Package created successfully!")
                print(f"📁 File: {package_name}")
                print(f"📊 Size: {package_size_mb:.2f} MB ({package_size:,} bytes)")
                print(f"🔐 SHA256: {checksum}")

            # Create release notes template
            if progress_bar:
                progress_bar.current_description = "Creating release notes template..."
            self.create_release_notes(package_size_mb, checksum)

            return {
                'package_path': package_path,
                'package_name': package_name,
                'version': self.version,
                'size': package_size,
                'checksum': checksum
            }

        except Exception as e:
            error_msg = f"❌ Error creating package: {e}"
            if progress_bar:
                progress_bar.finish(error_msg)
            else:
                print(error_msg)
            return None

    def create_release_notes(self, package_size_mb, checksum):
        """Create release notes template"""
        release_notes_file = self.package_dir / f"release_notes_v{self.version}.md"

        template = f"""# Pladria v{self.version}

## 🆕 New Features
- [ ] Add your new features here

## 🔧 Improvements
- [ ] List improvements made

## 🐛 Bug Fixes
- [ ] Describe bugs fixed

## ⚠️ Important Notes
- This version requires application restart
- Automatic backup of previous version
- Rollback capability in case of issues

## 📊 Technical Information
- **Package Size**: {package_size_mb:.2f} MB
- **SHA256**: `{checksum}`
- **Files Included**: Essential files + _internal directory

---
**Version released on {datetime.now().strftime('%Y-%m-%d')}**
"""

        with open(release_notes_file, 'w', encoding='utf-8') as f:
            f.write(template)

        print(f"📝 Release notes template: {release_notes_file.name}")

    def test_ota_detection(self, use_spinner=False):
        """Test OTA update detection with optional spinner"""
        if use_spinner:
            spinner = ProgressBar()
            spinner.spinner_start("Testing OTA detection...")
        else:
            print(f"\n🧪 Testing OTA detection...")

        try:
            # Import update manager
            sys.path.insert(0, str(self.src_dir))
            from core.update_manager import UpdateManager, UpdateConfig

            # Initialize
            if use_spinner:
                spinner.current_description = "Initializing update manager..."
            update_manager = UpdateManager()

            if not use_spinner:
                print(f"📱 Current version: {update_manager.current_version}")
                print(f"🔗 Repository: {UpdateConfig.GITHUB_OWNER}/{UpdateConfig.GITHUB_REPO}")

            # Check dependencies
            if use_spinner:
                spinner.current_description = "Checking dependencies..."
            if not update_manager.check_dependencies():
                if use_spinner:
                    spinner.finish("❌ Missing dependencies!")
                else:
                    print("❌ Missing dependencies!")
                return False

            if not use_spinner:
                print("✅ Dependencies OK")

            # Check for updates
            if use_spinner:
                spinner.current_description = "Checking for updates..."
            else:
                print("\n🔍 Checking for updates...")

            update_info = update_manager.check_for_updates()

            if update_info:
                if use_spinner:
                    spinner.finish("🎉 UPDATE DETECTED!")
                else:
                    print("\n🎉 UPDATE DETECTED!")

                print(f"📦 Available version: v{update_info.version}")
                print(f"📊 Size: {update_info.file_size // 1024} KB")
                print(f"🔐 Critical: {'Yes' if update_info.is_critical else 'No'}")
                print(f"📁 URL: {update_info.download_url}")

                if update_info.release_notes:
                    notes_preview = update_info.release_notes[:150]
                    print(f"\n📝 Notes (preview): {notes_preview}...")

                print("\n✅ OTA system working!")
                return True
            else:
                if use_spinner:
                    spinner.finish("❌ No update detected")
                else:
                    print("\n❌ No update detected")

                print("🔍 Check:")
                print("   - GitHub release published?")
                print("   - Tag format 'v2.x.x'?")
                print("   - Repository public?")
                return False

        except Exception as e:
            error_msg = f"❌ Error: {e}"
            if use_spinner:
                spinner.finish(error_msg)
            else:
                print(f"\n{error_msg}")
            return False

    def cleanup_temp_files(self):
        """Clean temporary files"""
        print("\n🧹 Cleaning temporary files...")

        patterns = [
            "pladria-v*-update.zip",
            "release_notes_v*.md",
            "*.pyc",
            "__pycache__",
            "*.log"
        ]

        removed_count = 0
        for pattern in patterns:
            matches = list(self.package_dir.glob(pattern))
            for match in matches:
                try:
                    if match.is_file():
                        match.unlink()
                        print(f"   ✅ Removed: {match.name}")
                        removed_count += 1
                    elif match.is_dir():
                        shutil.rmtree(match)
                        print(f"   ✅ Removed dir: {match.name}")
                        removed_count += 1
                except Exception as e:
                    print(f"   ❌ Error removing {match.name}: {e}")

        print(f"✅ Cleanup complete! {removed_count} items removed.")
        return removed_count > 0

    def create_git_tag(self):
        """Create and push git tag"""
        print(f"\n🏷️ Creating git tag v{self.version}...")

        tag_name = f"v{self.version}"

        # Create tag
        success, _ = self.run_cmd(f'git tag -a {tag_name} -m "Version {self.version}"', f"Create tag {tag_name}")
        if not success:
            print("⚠️ Tag may already exist, continuing...")

        # Push tag
        success, _ = self.run_cmd(f"git push origin {tag_name}", f"Push tag {tag_name}")
        if not success:
            print("⚠️ Push tag failed, continuing...")

        return True

    def show_github_instructions(self, package_info):
        """Show GitHub release instructions"""
        print(f"\n🌐 GitHub Release Instructions:")
        print("=" * 50)
        print(f"1. Go to: https://github.com/wissemelj/Pladria_Dev_v2.5/releases")
        print(f"2. Click 'Create a new release'")
        print(f"3. Tag version: v{self.version}")
        print(f"4. Release title: Pladria v{self.version}")
        print(f"5. Copy content from: release_notes_v{self.version}.md")
        print(f"6. Attach file: {package_info['package_name']}")
        print(f"7. ❌ DO NOT check 'pre-release'")
        print(f"8. ✅ Check 'latest release'")
        print(f"9. Click 'Publish release'")

    def full_build_and_package(self):
        """Complete build and package process with progress tracking"""
        print("🚀 Pladria Build & Package System")
        print("=" * 50)
        print(f"📋 Version: {self.version}")

        # Confirm
        confirm = input(f"\n🔄 Build and package version {self.version}? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Operation cancelled")
            return False

        # Initialize global progress bar
        progress = ProgressBar(total_steps=100, width=50)

        try:
            print("\n" + "=" * 60)
            progress.start("Initializing build process...")
            time.sleep(0.5)  # Brief pause to show initialization

            # Step 1: Fix dependencies (20% of total progress)
            progress.update(5, "Step 1/6: Fixing dependencies...")
            if not self.fix_dependencies(progress_bar=progress):
                progress.update(20, "⚠️ Some dependencies failed, but continuing...")
            else:
                progress.update(20, "Dependencies fixed successfully")

            # Step 2: Clean builds (5% of total progress)
            progress.update(25, "Step 2/6: Cleaning previous builds...")
            self.cleanup_build()
            progress.update(30, "Previous builds cleaned")

            # Step 3: Build app (40% of total progress)
            progress.update(35, "Step 3/6: Building application...")
            if not self.build_app(progress_bar=progress):
                progress.finish("❌ Build failed")
                return False
            progress.update(70, "Application built successfully")

            # Step 4: Create package (20% of total progress)
            progress.update(75, "Step 4/6: Creating update package...")
            package_info = self.create_update_package(progress_bar=progress)
            if not package_info:
                progress.finish("❌ Package creation failed")
                return False
            progress.update(90, "Update package created")

            # Step 5: Create git tag (5% of total progress)
            progress.update(92, "Step 5/6: Creating git tag...")
            self.create_git_tag()
            progress.update(95, "Git tag created")

            # Step 6: Finalize (5% of total progress)
            progress.update(98, "Step 6/6: Finalizing...")
            time.sleep(0.5)  # Brief pause for finalization

            progress.finish("🎉 Build and package complete!")

            # Show final results
            print(f"\n📦 Package: {package_info['package_name']}")
            print(f"📊 Size: {package_info['size'] / (1024*1024):.2f} MB")
            print(f"🔐 SHA256: {package_info['checksum'][:16]}...")

            # Show GitHub instructions
            print(f"\n📋 Step 6/6: GitHub release instructions")
            self.show_github_instructions(package_info)

            return True

        except Exception as e:
            progress.finish(f"❌ Error in build process: {e}")
            return False

def main():
    """Main function"""

    # Check we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ Run this script from the Package/ directory")
        return

    builder = PladriaBuilder()

    print("🛠️ Pladria Unified Build System")
    print("=" * 40)
    print("Available commands:")
    print("1. Full building and packaging")
    print("2. Fix Dependencies Only")
    print("3. Build Pladria.exe Only")
    print("4. Create New Release Only")
    print("5. Test OTA detection")
    print("6. Clean temp files")
    print("7. Test OTA detection")
    print("0. Exit")

    while True:
        try:
            choice = input("\nSelect option (0-7): ").strip()

            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                builder.full_build_and_package()
            elif choice == "2":
                print("\n🔧 Fixing dependencies...")
                progress = ProgressBar(total_steps=10, width=40)
                builder.fix_dependencies(progress_bar=progress)
            elif choice == "3":
                print("\n📦 Building application...")
                builder.cleanup_build()
                progress = ProgressBar(total_steps=10, width=40)
                progress.start("Building application...")
                success = builder.build_app(progress_bar=progress)
                if success:
                    progress.finish("✅ Build completed successfully!")
                else:
                    progress.finish("❌ Build failed!")
            elif choice == "4":
                print("\n📦 Creating update package...")
                progress = ProgressBar(total_steps=10, width=40)
                progress.start("Creating package...")
                package_info = builder.create_update_package(progress_bar=progress)
                if package_info:
                    progress.finish("✅ Package created successfully!")
                    print(f"📦 Package: {package_info['package_name']}")
                    print(f"📊 Size: {package_info['size'] / (1024*1024):.2f} MB")
                else:
                    progress.finish("❌ Package creation failed!")
            elif choice == "5":
                builder.test_ota_detection(use_spinner=False)
            elif choice == "6":
                builder.cleanup_temp_files()
            elif choice == "7":
                builder.test_ota_detection(use_spinner=True)
            else:
                print("❌ Invalid option")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

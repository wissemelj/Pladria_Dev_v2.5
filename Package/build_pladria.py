#!/usr/bin/env python3
"""
Streamlined Pladria Build System
Simplified, maintainable build script with minimal redundancy
"""

import os
import sys
import subprocess
import zipfile
import shutil
import hashlib
import time
from pathlib import Path
from datetime import datetime

from build_config import BuildConfig, SimpleProgress, PathConfig

class PladriaBuilder:
    """Simplified Pladria builder with unified configuration"""
    
    def __init__(self):
        self.config = BuildConfig()
        self.paths = PathConfig()
        self.version = self.config.get_version()
        
    def run_command(self, cmd: str, description: str) -> bool:
        """Run command with error handling"""
        print(f"⏳ {description}...")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} - Success")
                return True
            else:
                print(f"❌ {description} - Failed")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                return False
        except Exception as e:
            print(f"❌ {description} - Error: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Install all required dependencies"""
        print("\n🔧 Installing Dependencies")
        print("=" * 40)
        
        # Update pip first
        if not self.run_command("python -m pip install --upgrade pip", "Update pip"):
            return False
        
        # Install core packages
        core_packages = ["setuptools", "wheel", "pyinstaller"]
        for pkg in core_packages:
            if not self.run_command(f"pip install --upgrade {pkg}", f"Install {pkg}"):
                print(f"⚠️ Failed to install {pkg}, continuing...")
        
        # Install from requirements
        if self.paths.package_dir.joinpath("requirements.txt").exists():
            if not self.run_command("pip install -r requirements.txt", "Install requirements"):
                return False
        
        # Test imports
        print("\n🧪 Testing Dependencies")
        all_ok = True
        for name, import_stmt in self.config.get_import_tests():
            try:
                exec(import_stmt)
                print(f"   ✅ {name}")
            except ImportError:
                print(f"   ❌ {name}")
                all_ok = False
        
        return all_ok
    
    def clean_build(self):
        """Clean previous builds"""
        print("\n🧹 Cleaning Previous Builds")
        print("=" * 40)
        
        dirs_to_clean = [self.paths.dist_dir, self.paths.build_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✅ Removed {dir_path.name}/")
        
        # Remove spec files
        for spec_file in self.paths.package_dir.glob("*.spec"):
            spec_file.unlink()
            print(f"   ✅ Removed {spec_file.name}")
    
    def build_executable(self) -> bool:
        """Build the executable using PyInstaller"""
        print(f"\n📦 Building Pladria v{self.version}")
        print("=" * 40)
        
        # Generate PyInstaller command
        cmd_args = self.config.get_pyinstaller_args(self.paths.src_dir, self.paths.icon_path)
        cmd = " ".join(cmd_args)
        
        # Run build
        success = self.run_command(cmd, "PyInstaller build")
        
        if not success:
            print("\n⚠️ Standard build failed, trying minimal build...")
            minimal_cmd = [
                "pyinstaller", "--name=Pladria", "--onedir", "--windowed",
                "--noconfirm", "--clean", f"--icon={self.paths.icon_path}",
                str(self.paths.src_dir / "main.py")
            ]
            success = self.run_command(" ".join(minimal_cmd), "Minimal build")
        
        # Copy assets
        if success:
            self._copy_assets()
        
        return success and (self.paths.dist_dir / "Pladria" / "Pladria.exe").exists()
    
    def _copy_assets(self):
        """Copy additional assets to build directory"""
        print("📄 Copying Assets")
        app_dir = self.paths.dist_dir / "Pladria"
        if app_dir.exists():
            for asset_path in self.paths.get_asset_paths():
                if asset_path.exists():
                    shutil.copy2(asset_path, app_dir)
                    print(f"   ✅ Copied {asset_path.name}")
    
    def create_package(self) -> dict:
        """Create update package ZIP"""
        print(f"\n📦 Creating Update Package v{self.version}")
        print("=" * 40)
        
        build_path = self.paths.dist_dir / "Pladria"
        if not build_path.exists():
            print("❌ Build directory not found")
            return None
        
        package_name = f"pladria-v{self.version}-update.zip"
        package_path = self.paths.package_dir / package_name
        
        try:
            with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
                # Add essential files
                essential_files = ["Pladria.exe"] + self.config.ASSETS
                for file_name in essential_files:
                    file_path = build_path / file_name
                    if file_path.exists():
                        zipf.write(file_path, file_name)
                        print(f"   ✅ Added {file_name}")
                
                # Add _internal directory
                internal_dir = build_path / "_internal"
                if internal_dir.exists():
                    for root, _, files in os.walk(internal_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arc_name = file_path.relative_to(build_path)
                            zipf.write(file_path, str(arc_name))
                    print(f"   ✅ Added _internal/ directory")
                
                # Add metadata
                metadata = f"""# Pladria Update Package
Version: {self.version}
Created: {datetime.now().isoformat()}
Package Type: Full Update
"""
                zipf.writestr("UPDATE_INFO.txt", metadata)
                print(f"   ✅ Added metadata")
            
            # Calculate stats
            package_size = package_path.stat().st_size
            checksum = self._calculate_checksum(package_path)
            
            print(f"\n✅ Package Created Successfully!")
            print(f"📁 File: {package_name}")
            print(f"📊 Size: {package_size / (1024*1024):.2f} MB")
            print(f"🔐 SHA256: {checksum[:16]}...")
            
            return {
                'package_path': package_path,
                'package_name': package_name,
                'version': self.version,
                'size': package_size,
                'checksum': checksum
            }
            
        except Exception as e:
            print(f"❌ Error creating package: {e}")
            return None
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def full_build(self) -> bool:
        """Complete build process"""
        print("🚀 Pladria Build System")
        print("=" * 50)
        print(f"📋 Version: {self.version}")
        
        # Confirm
        confirm = input(f"\n🔄 Build and package version {self.version}? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Operation cancelled")
            return False
        
        progress = SimpleProgress(6)
        
        try:
            # Step 1: Dependencies
            progress.update(1, "Installing dependencies...")
            if not self.install_dependencies():
                print("⚠️ Some dependencies failed, but continuing...")
            
            # Step 2: Clean
            progress.update(2, "Cleaning previous builds...")
            self.clean_build()
            
            # Step 3: Build
            progress.update(3, "Building executable...")
            if not self.build_executable():
                progress.finish("❌ Build failed")
                return False
            
            # Step 4: Package
            progress.update(4, "Creating package...")
            package_info = self.create_package()
            if not package_info:
                progress.finish("❌ Package creation failed")
                return False
            
            # Step 5: Git tag
            progress.update(5, "Creating git tag...")
            self._create_git_tag()
            
            # Step 6: Complete
            progress.update(6, "Build complete!")
            progress.finish("🎉 Build and package complete!")
            
            self._show_github_instructions(package_info)
            return True
            
        except Exception as e:
            progress.finish(f"❌ Error: {e}")
            return False
    
    def _create_git_tag(self):
        """Create git tag for version"""
        tag_name = f"v{self.version}"
        self.run_command(f'git tag -a {tag_name} -m "Version {self.version}"', f"Create tag {tag_name}")
        self.run_command(f"git push origin {tag_name}", f"Push tag {tag_name}")
    
    def _show_github_instructions(self, package_info: dict):
        """Show GitHub release instructions"""
        print(f"\n🌐 GitHub Release Instructions:")
        print("=" * 50)
        print(f"1. Go to: https://github.com/wissemelj/Pladria_Dev_v2.5/releases")
        print(f"2. Click 'Create a new release'")
        print(f"3. Tag version: v{self.version}")
        print(f"4. Release title: Pladria v{self.version}")
        print(f"5. Attach file: {package_info['package_name']}")
        print(f"6. Click 'Publish release'")

def main():
    """Main function with simple menu"""
    if not Path("requirements.txt").exists():
        print("❌ Run this script from the Package/ directory")
        return
    
    builder = PladriaBuilder()
    
    print("🛠️ Pladria Build System")
    print("=" * 30)
    print("1. Full Build & Package")
    print("2. Install Dependencies Only")
    print("3. Build Executable Only")
    print("4. Create Package Only")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (0-4): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                builder.full_build()
            elif choice == "2":
                builder.install_dependencies()
            elif choice == "3":
                builder.clean_build()
                builder.build_executable()
            elif choice == "4":
                builder.create_package()
            else:
                print("❌ Invalid option")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

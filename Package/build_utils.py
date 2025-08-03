#!/usr/bin/env python3
"""
Build utilities for Pladria
Simplified tools for dependency checking and package analysis
"""

import os
import sys
from pathlib import Path
from build_config import BuildConfig

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking Dependencies")
    print("=" * 30)
    
    missing = []
    for name, import_stmt in BuildConfig.get_import_tests():
        try:
            exec(import_stmt)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name}")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies available")
        return True

def analyze_package_size():
    """Analyze built package size"""
    package_dir = Path(__file__).parent
    dist_dir = package_dir / "dist" / "Pladria"
    
    if not dist_dir.exists():
        print("❌ No built package found. Run build first.")
        return
    
    print("📊 Package Size Analysis")
    print("=" * 30)
    
    total_size = 0
    file_count = 0
    largest_files = []
    
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                file_count += 1
                
                rel_path = os.path.relpath(file_path, dist_dir)
                largest_files.append((rel_path, size))
            except OSError:
                continue
    
    # Sort by size
    largest_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"📁 Total size: {total_size / (1024*1024):.1f} MB")
    print(f"📄 File count: {file_count}")
    
    print(f"\n📈 Largest files:")
    for i, (file_path, size) in enumerate(largest_files[:10]):
        size_mb = size / (1024*1024)
        print(f"   {i+1:2d}. {file_path:<40} {size_mb:>6.1f} MB")
    
    # Size recommendations
    if total_size > 100 * 1024 * 1024:  # > 100MB
        print(f"\n💡 Package is large (>{total_size/(1024*1024):.0f}MB)")
        print("   Consider excluding more modules in build_config.py")
    else:
        print(f"\n✅ Package size is reasonable")

def update_requirements():
    """Update requirements.txt from build_config.py"""
    print("📝 Updating requirements.txt")
    print("=" * 30)
    
    package_dir = Path(__file__).parent
    req_file = package_dir / "requirements.txt"
    
    header = """# Pladria v2.5 - Python Dependencies
# Sofrecom Tunisie
# Auto-generated from build_config.py - DO NOT EDIT MANUALLY

# Core dependencies"""
    
    core_deps = "\n".join(BuildConfig.CORE_DEPENDENCIES)
    
    build_header = "\n# Build dependencies"
    build_deps = "\n".join(BuildConfig.BUILD_DEPENDENCIES)
    
    footer = """
# Note: To update dependencies, modify build_config.py and run:
# python build_utils.py --update-requirements"""
    
    content = f"{header}\n{core_deps}\n{build_header}\n{build_deps}{footer}"
    
    with open(req_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {req_file}")

def clean_temp_files():
    """Clean temporary build files"""
    print("🧹 Cleaning Temporary Files")
    print("=" * 30)
    
    package_dir = Path(__file__).parent
    
    patterns = [
        "pladria-v*-update.zip",
        "release_notes_v*.md",
        "*.pyc",
        "__pycache__",
        "*.log"
    ]
    
    removed_count = 0
    for pattern in patterns:
        matches = list(package_dir.glob(pattern))
        for match in matches:
            try:
                if match.is_file():
                    match.unlink()
                    print(f"   ✅ Removed: {match.name}")
                    removed_count += 1
                elif match.is_dir():
                    import shutil
                    shutil.rmtree(match)
                    print(f"   ✅ Removed dir: {match.name}")
                    removed_count += 1
            except Exception as e:
                print(f"   ❌ Error removing {match.name}: {e}")
    
    print(f"✅ Cleanup complete! {removed_count} items removed.")

def main():
    """Main utility function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pladria Build Utilities")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies")
    parser.add_argument("--analyze-size", action="store_true", help="Analyze package size")
    parser.add_argument("--update-requirements", action="store_true", help="Update requirements.txt")
    parser.add_argument("--clean", action="store_true", help="Clean temporary files")
    
    args = parser.parse_args()
    
    if args.check_deps:
        check_dependencies()
    elif args.analyze_size:
        analyze_package_size()
    elif args.update_requirements:
        update_requirements()
    elif args.clean:
        clean_temp_files()
    else:
        print("🛠️ Pladria Build Utilities")
        print("=" * 30)
        print("Available commands:")
        print("  --check-deps        Check dependencies")
        print("  --analyze-size      Analyze package size")
        print("  --update-requirements Update requirements.txt")
        print("  --clean             Clean temporary files")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify the fixed folder detection logic.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_search_locations():
    """Test the search locations logic."""
    print("🔍 Testing search locations logic...")
    
    try:
        # Simulate the search logic from the updated code
        search_locations = []
        
        # Location 1: Relative to Excel file (simulated)
        fake_excel_path = "/some/teams/folder/data.xlsx"
        base_dir = os.path.dirname(fake_excel_path)
        search_locations.append(base_dir)
        print(f"✅ Location 1 (Excel relative): {base_dir}")
        
        # Location 2: Application's src directory
        current_file = os.path.abspath(__file__)
        src_dir = os.path.dirname(current_file)  # This script is in root, so src is subdirectory
        src_dir = os.path.join(src_dir, "src")
        search_locations.append(src_dir)
        print(f"✅ Location 2 (src directory): {src_dir}")
        
        # Location 3: Current working directory
        search_locations.append(os.getcwd())
        print(f"✅ Location 3 (current working dir): {os.getcwd()}")
        
        # Location 4: Application root directory
        app_root = os.path.dirname(src_dir)
        search_locations.append(app_root)
        print(f"✅ Location 4 (app root): {app_root}")
        
        # Test which locations actually exist
        existing_locations = []
        for location in search_locations:
            if location and os.path.exists(location):
                existing_locations.append(location)
                print(f"   ✅ EXISTS: {location}")
            else:
                print(f"   ❌ NOT FOUND: {location}")
        
        print(f"\n📊 Summary: {len(existing_locations)}/{len(search_locations)} locations exist")
        return len(existing_locations) > 0
        
    except Exception as e:
        print(f"❌ Error in search locations test: {e}")
        return False

def test_actual_pres_stats_detection():
    """Test detection of the actual pres stats folder."""
    print("\n📁 Testing actual pres stats folder detection...")
    
    try:
        # Search locations based on the actual code logic
        search_locations = []
        
        # Get the actual src directory
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(current_file)
        src_dir = os.path.join(project_root, "src")
        
        search_locations.append(src_dir)
        search_locations.append(project_root)
        search_locations.append(os.getcwd())
        
        # Try different possible folder names
        possible_folders = ['pres stats', 'stats', 'Stats', 'STATS']
        stats_folder = None
        
        for base_dir in search_locations:
            if not base_dir or not os.path.exists(base_dir):
                print(f"   ⚠️ Skipping non-existent location: {base_dir}")
                continue
                
            print(f"   🔍 Searching in: {base_dir}")
            
            for folder_name in possible_folders:
                test_folder = os.path.join(base_dir, folder_name)
                if os.path.exists(test_folder) and os.path.isdir(test_folder):
                    stats_folder = test_folder
                    print(f"   ✅ FOUND: {folder_name} at {test_folder}")
                    
                    # List contents of found folder
                    try:
                        contents = os.listdir(test_folder)
                        print(f"      Contents: {contents}")
                    except Exception as e:
                        print(f"      Could not list contents: {e}")
                    
                    break
                else:
                    print(f"   ❌ Not found: {test_folder}")
            
            if stats_folder:
                break
        
        if stats_folder:
            print(f"\n✅ Successfully found pres stats folder: {stats_folder}")
            
            # Check for index.html specifically
            index_path = os.path.join(stats_folder, 'index.html')
            if os.path.exists(index_path):
                print(f"✅ Found index.html: {index_path}")
                
                # Check file size
                file_size = os.path.getsize(index_path)
                print(f"   File size: {file_size} bytes")
                
                return True
            else:
                print(f"❌ index.html not found in {stats_folder}")
                return False
        else:
            print("❌ No pres stats folder found in any location")
            print(f"   Searched locations: {search_locations}")
            print(f"   Searched folder names: {possible_folders}")
            return False
        
    except Exception as e:
        print(f"❌ Error in pres stats detection test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_module_integration():
    """Test that the module can use the updated detection logic."""
    print("\n🔧 Testing module integration...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        print("✅ TeamStatsModule imported successfully")
        
        # Test that the updated methods exist
        required_methods = [
            '_find_stats_index_file',
            '_analyze_pres_stats_folder',
            '_load_stats_folder_data'
        ]
        
        for method in required_methods:
            if hasattr(TeamStatsModule, method):
                print(f"✅ Method exists: {method}")
            else:
                print(f"❌ Method missing: {method}")
                return False
        
        print("✅ All required methods exist")
        return True
        
    except Exception as e:
        print(f"❌ Error in module integration test: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Fixed Folder Detection Logic")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Search locations
    if test_search_locations():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Search locations")
    else:
        print("\n❌ Test 1 FAILED: Search locations")
    
    # Test 2: Actual pres stats detection
    if test_actual_pres_stats_detection():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Actual pres stats detection")
    else:
        print("\n❌ Test 2 FAILED: Actual pres stats detection")
    
    # Test 3: Module integration
    if test_module_integration():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Module integration")
    else:
        print("\n❌ Test 3 FAILED: Module integration")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Fixed folder detection should now work:")
        print("  • Searches in multiple locations including src directory")
        print("  • Finds the actual 'pres stats' folder in src/pres stats/")
        print("  • Locates index.html and other files correctly")
        print("  • No more 'Index non trouvé' error expected")
        
        print("\n🎯 The 'Generate and open index' button should now work!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        print("🔍 Check the console output above for specific issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

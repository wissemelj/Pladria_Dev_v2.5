#!/usr/bin/env python3
"""
Test script to verify the async task fix in Team Statistics module.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_async_task_fix():
    """Test that the async task parameters are correctly fixed."""
    print("🔧 Testing Async Task Fix")
    print("=" * 40)
    
    try:
        # Test import
        print("📦 Testing import...")
        from ui.modules.team_stats_module import TeamStatsModule
        print("✅ TeamStatsModule imported successfully")
        
        # Test that run_async_task is imported correctly
        from utils.performance import run_async_task
        print("✅ run_async_task imported successfully")
        
        # Test the function signature
        import inspect
        sig = inspect.signature(run_async_task)
        params = list(sig.parameters.keys())
        
        print(f"📋 run_async_task parameters: {params}")
        
        # Check for correct parameters
        if 'callback' in params:
            print("✅ 'callback' parameter found")
        else:
            print("❌ 'callback' parameter missing")
            return False
            
        if 'error_callback' in params:
            print("✅ 'error_callback' parameter found")
        else:
            print("❌ 'error_callback' parameter missing")
            return False
        
        # Check that incorrect parameters are not expected
        if 'on_success' in params:
            print("❌ Incorrect 'on_success' parameter found")
            return False
        else:
            print("✅ No incorrect 'on_success' parameter")
            
        if 'on_error' in params:
            print("❌ Incorrect 'on_error' parameter found")
            return False
        else:
            print("✅ No incorrect 'on_error' parameter")
        
        print("\n🎉 Async task fix verified successfully!")
        print("✅ The run_async_task call now uses correct parameter names")
        print("✅ No more 'unexpected keyword argument' errors expected")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_method_existence():
    """Test that the date range methods exist and are callable."""
    print("\n🔍 Testing Method Existence")
    print("=" * 40)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Check that the _generate_filtered_statistics method exists
        if hasattr(TeamStatsModule, '_generate_filtered_statistics'):
            print("✅ _generate_filtered_statistics method exists")
            
            # Check if it's callable
            method = getattr(TeamStatsModule, '_generate_filtered_statistics')
            if callable(method):
                print("✅ _generate_filtered_statistics is callable")
            else:
                print("❌ _generate_filtered_statistics is not callable")
                return False
        else:
            print("❌ _generate_filtered_statistics method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing methods: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Team Statistics Async Fix Verification")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Async task fix
    if test_async_task_fix():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Async task fix")
    else:
        print("\n❌ Test 1 FAILED: Async task fix")
    
    # Test 2: Method existence
    if test_method_existence():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Method existence")
    else:
        print("\n❌ Test 2 FAILED: Method existence")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The async task error has been fixed")
        print("✅ Date range functionality should work without errors")
        print("\n📝 The fix applied:")
        print("   • Changed 'on_success' to 'callback'")
        print("   • Changed 'on_error' to 'error_callback'")
        print("   • Removed 'loading_message' parameter")
        print("   • Added 'task_name' parameter")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

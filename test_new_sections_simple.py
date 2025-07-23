#!/usr/bin/env python3
"""
Simple test to verify UPR and 501/511 sections implementation.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_methods_exist():
    """Test that the new methods exist."""
    print("🔍 Testing New Methods Existence")
    print("=" * 50)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Check if new methods exist
        required_methods = [
            '_extract_upr_data_for_dashboard',
            '_extract_501511_data_for_dashboard'
        ]
        
        for method_name in required_methods:
            if hasattr(TeamStatsModule, method_name):
                print(f"   ✅ Method exists: {method_name}")
            else:
                print(f"   ❌ Method missing: {method_name}")
                return False
        
        print(f"   ✅ All new methods found")
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking methods: {e}")
        return False

def test_data_validator():
    """Test that data validator has new methods."""
    print("\n🔍 Testing Data Validator Updates")
    print("=" * 50)
    
    try:
        from core.data_validator import DataValidator
        
        # Check if new validation methods exist
        validator = DataValidator()
        required_methods = [
            '_validate_upr_data',
            '_validate_tickets_501511_data'
        ]
        
        for method_name in required_methods:
            if hasattr(validator, method_name):
                print(f"   ✅ Validation method exists: {method_name}")
            else:
                print(f"   ❌ Validation method missing: {method_name}")
                return False
        
        print(f"   ✅ All validation methods found")
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking validation methods: {e}")
        return False

def test_html_structure():
    """Test that HTML has new sections."""
    print("\n🔍 Testing HTML Structure Updates")
    print("=" * 50)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ HTML file not found")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for new sections
        required_elements = [
            'Tickets UPR',
            'Tickets 501/511',
            'uprChart',
            'tickets501511Chart',
            'upr-cree',
            'upr-non',
            'tickets-501511'
        ]
        
        for element in required_elements:
            if element in html_content:
                print(f"   ✅ HTML element found: {element}")
            else:
                print(f"   ❌ HTML element missing: {element}")
                return False
        
        print(f"   ✅ All HTML elements found")
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking HTML: {e}")
        return False

def test_script_structure():
    """Test that script.js has new charts."""
    print("\n🔍 Testing Script.js Structure Updates")
    print("=" * 50)
    
    try:
        script_file = Path(__file__).parent / "src" / "pres stats" / "script.js"
        
        if not script_file.exists():
            print(f"   ❌ Script file not found")
            return False
        
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Check for new chart elements
        required_elements = [
            'uprCtx',
            'tickets501511Ctx',
            'uprCree',
            'uprNon',
            'tickets501511'
        ]
        
        for element in required_elements:
            if element in script_content:
                print(f"   ✅ Script element found: {element}")
            else:
                print(f"   ❌ Script element missing: {element}")
                return False
        
        print(f"   ✅ All script elements found")
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking script: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Simple Test of UPR and 501/511 Implementation")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Methods exist
    if test_methods_exist():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Methods exist")
    else:
        print("\n❌ Test 1 FAILED: Methods missing")
    
    # Test 2: Data validator updated
    if test_data_validator():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Data validator updated")
    else:
        print("\n❌ Test 2 FAILED: Data validator not updated")
    
    # Test 3: HTML structure
    if test_html_structure():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: HTML structure updated")
    else:
        print("\n❌ Test 3 FAILED: HTML structure not updated")
    
    # Test 4: Script structure
    if test_script_structure():
        tests_passed += 1
        print("\n✅ Test 4 PASSED: Script structure updated")
    else:
        print("\n❌ Test 4 FAILED: Script structure not updated")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL STRUCTURE TESTS PASSED!")
        print("\n✅ UPR and 501/511 sections successfully implemented!")
        print("\n🎯 Implementation includes:")
        print("  • New extraction methods in TeamStatsModule")
        print("  • Data validation methods in DataValidator")
        print("  • HTML sections for both UPR and 501/511 tickets")
        print("  • Chart.js configurations for both sections")
        print("  • Integration with existing dashboard mapping")
        
        print("\n📝 Ready for testing with real data:")
        print("  1. Load Suivi Global data in the application")
        print("  2. Select a date range with data")
        print("  3. Click 'Generate and open index'")
        print("  4. Verify both new sections show real filtered data")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

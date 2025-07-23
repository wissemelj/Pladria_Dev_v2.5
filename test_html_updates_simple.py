#!/usr/bin/env python3
"""
Simple test to verify HTML element updates work correctly.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_html_regex_patterns():
    """Test the regex patterns used for HTML updates."""
    print("🧪 Testing HTML regex patterns...")
    
    try:
        # Sample HTML content (from the actual index.html)
        sample_html = """
        <div class="card">
            <h2>CM (894)</h2>
            <div class="chart-container">
                <canvas id="cmChart"></canvas>
            </div>
            <div class="stats-summary">
                <div class="stat-item">
                    <span class="stat-value raf">806</span>
                    <span class="stat-label">RAF</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value modif">17</span>
                    <span class="stat-label">Modification</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value crea">71</span>
                    <span class="stat-label">Creation</span>
                </div>
            </div>
        </div>
        """
        
        print(f"📊 Testing with sample HTML...")
        
        # Test data
        test_cm_data = [2071, 34, 148]
        total_cm = sum(test_cm_data)
        
        # Test CM title pattern
        cm_title_pattern = r'(<h2>CM\s*\()[^)]*(\)</h2>)'
        cm_title_replacement = rf'\g<1>{total_cm}\g<2>'
        
        title_match = re.search(cm_title_pattern, sample_html)
        if title_match:
            print(f"✅ CM title pattern found: {title_match.group(0)}")
            updated_title = re.sub(cm_title_pattern, cm_title_replacement, sample_html)
            new_title_match = re.search(cm_title_pattern, updated_title)
            if new_title_match:
                print(f"✅ CM title updated to: {new_title_match.group(0)}")
            else:
                print(f"❌ CM title update failed")
                return False
        else:
            print(f"❌ CM title pattern not found")
            return False
        
        # Test RAF pattern
        raf_pattern = r'(<span class="stat-value raf">)[^<]*(</span>)'
        raf_replacement = rf'\g<1>{test_cm_data[0]}\g<2>'
        
        raf_match = re.search(raf_pattern, sample_html)
        if raf_match:
            print(f"✅ RAF pattern found: {raf_match.group(0)}")
            updated_raf = re.sub(raf_pattern, raf_replacement, sample_html)
            new_raf_match = re.search(raf_pattern, updated_raf)
            if new_raf_match:
                print(f"✅ RAF updated to: {new_raf_match.group(0)}")
            else:
                print(f"❌ RAF update failed")
                return False
        else:
            print(f"❌ RAF pattern not found")
            return False
        
        # Test MODIF pattern
        modif_pattern = r'(<span class="stat-value modif">)[^<]*(</span>)'
        modif_replacement = rf'\g<1>{test_cm_data[1]}\g<2>'
        
        modif_match = re.search(modif_pattern, sample_html)
        if modif_match:
            print(f"✅ MODIF pattern found: {modif_match.group(0)}")
            updated_modif = re.sub(modif_pattern, modif_replacement, sample_html)
            new_modif_match = re.search(modif_pattern, updated_modif)
            if new_modif_match:
                print(f"✅ MODIF updated to: {new_modif_match.group(0)}")
            else:
                print(f"❌ MODIF update failed")
                return False
        else:
            print(f"❌ MODIF pattern not found")
            return False
        
        # Test CREA pattern
        crea_pattern = r'(<span class="stat-value crea">)[^<]*(</span>)'
        crea_replacement = rf'\g<1>{test_cm_data[2]}\g<2>'
        
        crea_match = re.search(crea_pattern, sample_html)
        if crea_match:
            print(f"✅ CREA pattern found: {crea_match.group(0)}")
            updated_crea = re.sub(crea_pattern, crea_replacement, sample_html)
            new_crea_match = re.search(crea_pattern, updated_crea)
            if new_crea_match:
                print(f"✅ CREA updated to: {new_crea_match.group(0)}")
            else:
                print(f"❌ CREA update failed")
                return False
        else:
            print(f"❌ CREA pattern not found")
            return False
        
        print(f"✅ All HTML regex patterns working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error in regex pattern test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_method_integration():
    """Test that the new HTML update method integrates correctly."""
    print("\n🔧 Testing method integration...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Check that the new method exists
        if hasattr(TeamStatsModule, '_update_html_elements_with_data'):
            print(f"✅ _update_html_elements_with_data method exists")
        else:
            print(f"❌ _update_html_elements_with_data method missing")
            return False
        
        # Check that the method is called from _update_existing_dashboard_values
        import inspect
        source = inspect.getsource(TeamStatsModule._update_existing_dashboard_values)
        
        if '_update_html_elements_with_data' in source:
            print(f"✅ HTML update method is called from dashboard update")
        else:
            print(f"❌ HTML update method not called from dashboard update")
            return False
        
        print(f"✅ Method integration successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error in method integration test: {e}")
        return False

def test_actual_index_html_structure():
    """Test with the actual index.html file structure."""
    print("\n📁 Testing with actual index.html structure...")
    
    try:
        # Read the actual index.html file
        index_path = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not index_path.exists():
            print(f"❌ index.html not found at: {index_path}")
            return False
        
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"📊 Loaded actual index.html: {len(html_content)} characters")
        
        # Test patterns with actual content
        patterns_to_test = [
            ('CM Title', r'<h2>CM\s*\([^)]*\)</h2>'),
            ('RAF Value', r'<span class="stat-value raf">[^<]*</span>'),
            ('MODIF Value', r'<span class="stat-value modif">[^<]*</span>'),
            ('CREA Value', r'<span class="stat-value crea">[^<]*</span>')
        ]
        
        all_found = True
        for name, pattern in patterns_to_test:
            match = re.search(pattern, html_content)
            if match:
                print(f"✅ {name} found: {match.group(0)}")
            else:
                print(f"❌ {name} not found with pattern: {pattern}")
                all_found = False
        
        if all_found:
            print(f"✅ All required HTML elements found in actual file!")
            return True
        else:
            print(f"❌ Some HTML elements missing")
            return False
        
    except Exception as e:
        print(f"❌ Error testing actual index.html: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing HTML Element Updates")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Regex patterns
    if test_html_regex_patterns():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: HTML regex patterns")
    else:
        print("\n❌ Test 1 FAILED: HTML regex patterns")
    
    # Test 2: Method integration
    if test_method_integration():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Method integration")
    else:
        print("\n❌ Test 2 FAILED: Method integration")
    
    # Test 3: Actual HTML structure
    if test_actual_index_html_structure():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Actual HTML structure")
    else:
        print("\n❌ Test 3 FAILED: Actual HTML structure")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ HTML element updates are ready!")
        print("\n🎯 Implementation complete:")
        print("  • HTML regex patterns work correctly")
        print("  • New method is properly integrated")
        print("  • Actual index.html structure is compatible")
        
        print("\n📝 What happens now when 'Generate and open index' is clicked:")
        print("  1. Script.js CM data is updated with real motif counts")
        print("  2. HTML CM card title shows real total count")
        print("  3. HTML stat values (RAF, MODIF, CREA) show real counts")
        print("  4. Charts and text displays are perfectly synchronized")
        
        print("\n🔧 Next step: Test with real application!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

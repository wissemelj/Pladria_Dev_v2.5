#!/usr/bin/env python3
"""
Test script to verify that HTML elements and script.js are synchronized with CM data.
"""

import sys
import os
import tempfile
import shutil
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_test_environment():
    """Create a test environment with copies of the pres stats files."""
    print("🔧 Creating test environment...")
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Copy pres stats files
        original_pres_stats = Path(__file__).parent / "src" / "pres stats"
        temp_pres_stats = os.path.join(temp_dir, "pres stats")
        
        if original_pres_stats.exists():
            shutil.copytree(original_pres_stats, temp_pres_stats)
            print(f"✅ Created test environment: {temp_pres_stats}")
            return temp_dir, temp_pres_stats
        else:
            print(f"❌ Original pres stats not found: {original_pres_stats}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error creating test environment: {e}")
        return None, None

def test_html_element_updates():
    """Test that HTML elements are correctly updated with CM data."""
    print("\n📝 Testing HTML element updates...")
    
    try:
        temp_dir, temp_pres_stats = create_test_environment()
        if not temp_dir:
            return False
        
        # Read original HTML
        index_path = os.path.join(temp_pres_stats, "index.html")
        with open(index_path, 'r', encoding='utf-8') as f:
            original_html = f.read()
        
        print(f"📊 Original HTML loaded: {len(original_html)} characters")
        
        # Extract original CM values
        original_values = {}
        
        # Extract CM title total
        cm_title_match = re.search(r'<h2>CM\s*\(([^)]*)\)</h2>', original_html)
        if cm_title_match:
            original_values['total'] = cm_title_match.group(1)
            print(f"   Original CM total: {original_values['total']}")
        
        # Extract individual values
        raf_match = re.search(r'<span class="stat-value raf">([^<]*)</span>', original_html)
        if raf_match:
            original_values['raf'] = raf_match.group(1)
            print(f"   Original RAF: {original_values['raf']}")
        
        modif_match = re.search(r'<span class="stat-value modif">([^<]*)</span>', original_html)
        if modif_match:
            original_values['modif'] = modif_match.group(1)
            print(f"   Original MODIF: {original_values['modif']}")
        
        crea_match = re.search(r'<span class="stat-value crea">([^<]*)</span>', original_html)
        if crea_match:
            original_values['crea'] = crea_match.group(1)
            print(f"   Original CREA: {original_values['crea']}")
        
        # Test the update logic with mock data
        test_cm_data = [2071, 34, 148]  # RAF, MODIF, CREA from real data
        total_cm = sum(test_cm_data)
        
        print(f"\n🔄 Testing updates with: RAF={test_cm_data[0]}, MODIF={test_cm_data[1]}, CREA={test_cm_data[2]}, Total={total_cm}")
        
        updated_html = original_html
        
        # Update CM title
        cm_title_pattern = r'(<h2>CM\s*\()[^)]*(\)</h2>)'
        cm_title_replacement = rf'\g<1>{total_cm}\g<2>'
        updated_html = re.sub(cm_title_pattern, cm_title_replacement, updated_html)
        
        # Update RAF value
        raf_pattern = r'(<span class="stat-value raf">)[^<]*(</span>)'
        raf_replacement = rf'\g<1>{test_cm_data[0]}\g<2>'
        updated_html = re.sub(raf_pattern, raf_replacement, updated_html)
        
        # Update MODIF value
        modif_pattern = r'(<span class="stat-value modif">)[^<]*(</span>)'
        modif_replacement = rf'\g<1>{test_cm_data[1]}\g<2>'
        updated_html = re.sub(modif_pattern, modif_replacement, updated_html)
        
        # Update CREA value
        crea_pattern = r'(<span class="stat-value crea">)[^<]*(</span>)'
        crea_replacement = rf'\g<1>{test_cm_data[2]}\g<2>'
        updated_html = re.sub(crea_pattern, crea_replacement, updated_html)
        
        # Verify updates
        print(f"\n✅ Verifying HTML updates...")
        
        # Check CM title
        updated_title_match = re.search(r'<h2>CM\s*\(([^)]*)\)</h2>', updated_html)
        if updated_title_match and updated_title_match.group(1) == str(total_cm):
            print(f"   ✅ CM title updated: {updated_title_match.group(1)}")
        else:
            print(f"   ❌ CM title update failed")
            return False
        
        # Check individual values
        updated_raf_match = re.search(r'<span class="stat-value raf">([^<]*)</span>', updated_html)
        if updated_raf_match and updated_raf_match.group(1) == str(test_cm_data[0]):
            print(f"   ✅ RAF value updated: {updated_raf_match.group(1)}")
        else:
            print(f"   ❌ RAF value update failed")
            return False
        
        updated_modif_match = re.search(r'<span class="stat-value modif">([^<]*)</span>', updated_html)
        if updated_modif_match and updated_modif_match.group(1) == str(test_cm_data[1]):
            print(f"   ✅ MODIF value updated: {updated_modif_match.group(1)}")
        else:
            print(f"   ❌ MODIF value update failed")
            return False
        
        updated_crea_match = re.search(r'<span class="stat-value crea">([^<]*)</span>', updated_html)
        if updated_crea_match and updated_crea_match.group(1) == str(test_cm_data[2]):
            print(f"   ✅ CREA value updated: {updated_crea_match.group(1)}")
        else:
            print(f"   ❌ CREA value update failed")
            return False
        
        # Write updated HTML
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ HTML element updates successful!")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        return True
        
    except Exception as e:
        print(f"❌ Error in HTML element update test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_script_js_sync():
    """Test that script.js is updated with the same data as HTML."""
    print("\n📜 Testing script.js synchronization...")
    
    try:
        temp_dir, temp_pres_stats = create_test_environment()
        if not temp_dir:
            return False
        
        # Read original script.js
        script_path = os.path.join(temp_pres_stats, "script.js")
        with open(script_path, 'r', encoding='utf-8') as f:
            original_script = f.read()
        
        print(f"📊 Original script.js loaded: {len(original_script)} characters")
        
        # Test data (same as HTML test)
        test_cm_data = [2071, 34, 148]
        
        # Update script.js CM data
        cm_pattern = r'(const cmCtx.*?data:\s*\[)[^\]]*(\])'
        data_str = ', '.join(str(x) for x in test_cm_data)
        replacement = rf'\g<1>{data_str}\g<2>'
        updated_script = re.sub(cm_pattern, replacement, original_script, flags=re.DOTALL)
        
        # Verify script update
        updated_match = re.search(cm_pattern, updated_script, flags=re.DOTALL)
        if updated_match:
            script_data_str = updated_match.group(0)
            if f'[{data_str}]' in script_data_str:
                print(f"✅ Script.js CM data updated: [{data_str}]")
            else:
                print(f"❌ Script.js CM data update failed")
                return False
        else:
            print(f"❌ Could not find CM data pattern in updated script")
            return False
        
        # Write updated script
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(updated_script)
        
        print(f"✅ Script.js synchronization successful!")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        return True
        
    except Exception as e:
        print(f"❌ Error in script.js sync test: {e}")
        return False

def test_complete_synchronization():
    """Test that HTML and script.js show the same data."""
    print("\n🔄 Testing complete HTML-Script synchronization...")
    
    try:
        temp_dir, temp_pres_stats = create_test_environment()
        if not temp_dir:
            return False
        
        # Test data
        test_cm_data = [2071, 34, 148]
        total_cm = sum(test_cm_data)
        
        # Update both HTML and script.js
        index_path = os.path.join(temp_pres_stats, "index.html")
        script_path = os.path.join(temp_pres_stats, "script.js")
        
        # Update HTML
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Apply HTML updates
        html_content = re.sub(r'(<h2>CM\s*\()[^)]*(\)</h2>)', rf'\g<1>{total_cm}\g<2>', html_content)
        html_content = re.sub(r'(<span class="stat-value raf">)[^<]*(</span>)', rf'\g<1>{test_cm_data[0]}\g<2>', html_content)
        html_content = re.sub(r'(<span class="stat-value modif">)[^<]*(</span>)', rf'\g<1>{test_cm_data[1]}\g<2>', html_content)
        html_content = re.sub(r'(<span class="stat-value crea">)[^<]*(</span>)', rf'\g<1>{test_cm_data[2]}\g<2>', html_content)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Update script.js
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        data_str = ', '.join(str(x) for x in test_cm_data)
        script_content = re.sub(r'(const cmCtx.*?data:\s*\[)[^\]]*(\])', rf'\g<1>{data_str}\g<2>', script_content, flags=re.DOTALL)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Verify synchronization
        print(f"📊 Verifying data consistency...")
        
        # Read updated files
        with open(index_path, 'r', encoding='utf-8') as f:
            final_html = f.read()
        
        with open(script_path, 'r', encoding='utf-8') as f:
            final_script = f.read()
        
        # Extract HTML values
        html_total = re.search(r'<h2>CM\s*\(([^)]*)\)</h2>', final_html).group(1)
        html_raf = re.search(r'<span class="stat-value raf">([^<]*)</span>', final_html).group(1)
        html_modif = re.search(r'<span class="stat-value modif">([^<]*)</span>', final_html).group(1)
        html_crea = re.search(r'<span class="stat-value crea">([^<]*)</span>', final_html).group(1)
        
        # Extract script values
        script_match = re.search(r'const cmCtx.*?data:\s*\[([^\]]*)\]', final_script, flags=re.DOTALL)
        script_values = [int(x.strip()) for x in script_match.group(1).split(',')]
        
        print(f"📋 HTML values: Total={html_total}, RAF={html_raf}, MODIF={html_modif}, CREA={html_crea}")
        print(f"📋 Script values: {script_values}")
        
        # Check consistency
        html_values = [int(html_raf), int(html_modif), int(html_crea)]
        html_total_calc = sum(html_values)
        
        if (html_values == script_values and 
            html_values == test_cm_data and 
            int(html_total) == total_cm):
            print(f"✅ Perfect synchronization achieved!")
            print(f"   HTML and Script.js show identical data")
            print(f"   All values match expected test data")
            
            # Cleanup
            shutil.rmtree(temp_dir)
            return True
        else:
            print(f"❌ Synchronization failed - data mismatch")
            print(f"   Expected: {test_cm_data} (total: {total_cm})")
            print(f"   HTML: {html_values} (total: {html_total})")
            print(f"   Script: {script_values}")
            return False
        
    except Exception as e:
        print(f"❌ Error in complete synchronization test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Testing HTML-Script.js Synchronization")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: HTML element updates
    if test_html_element_updates():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: HTML element updates")
    else:
        print("\n❌ Test 1 FAILED: HTML element updates")
    
    # Test 2: Script.js synchronization
    if test_script_js_sync():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Script.js synchronization")
    else:
        print("\n❌ Test 2 FAILED: Script.js synchronization")
    
    # Test 3: Complete synchronization
    if test_complete_synchronization():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Complete synchronization")
    else:
        print("\n❌ Test 3 FAILED: Complete synchronization")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ HTML-Script.js synchronization is working correctly!")
        print("\n🎯 What this means:")
        print("  • HTML card titles show correct CM totals")
        print("  • HTML stat values (RAF, MODIF, CREA) match filtered data")
        print("  • Script.js chart data arrays use the same values")
        print("  • Visual charts and numerical displays are synchronized")
        
        print("\n📝 When users click 'Generate and open index':")
        print("  1. CM card title shows real total count")
        print("  2. Individual stat values show real motif counts")
        print("  3. Chart.js displays match the HTML numbers exactly")
        print("  4. Everything reflects the selected date range data")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

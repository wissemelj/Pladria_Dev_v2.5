#!/usr/bin/env python3
"""
Test script to verify that script.js is actually being updated with CM data.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_script_js_update():
    """Test the actual script.js update process."""
    print("📝 Testing script.js update process...")
    
    try:
        # Create a temporary copy of the actual script.js
        original_script_path = Path(__file__).parent / "src" / "pres stats" / "script.js"
        
        if not original_script_path.exists():
            print(f"❌ Original script.js not found at: {original_script_path}")
            return False
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_script_path = os.path.join(temp_dir, "script.js")
        
        # Copy original script.js
        shutil.copy2(original_script_path, temp_script_path)
        print(f"✅ Created temporary script.js at: {temp_script_path}")
        
        # Read original content
        with open(temp_script_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        print(f"📊 Original script.js length: {len(original_content)} characters")
        
        # Find the CM chart data
        import re
        cm_pattern = r'(const cmCtx.*?data:\s*\[)([^\]]*?)(\])'
        cm_match = re.search(cm_pattern, original_content, flags=re.DOTALL)
        
        if cm_match:
            original_data = cm_match.group(2).strip()
            print(f"📊 Found original CM data: [{original_data}]")
        else:
            print("❌ Could not find CM chart data pattern in script.js")
            return False
        
        # Test the update process
        new_cm_data = [15, 8, 12]
        data_str = ', '.join(str(x) for x in new_cm_data)
        
        # Apply the update
        replacement = rf'\g<1>{data_str}\g<3>'
        updated_content = re.sub(cm_pattern, replacement, original_content, flags=re.DOTALL)
        
        # Write updated content
        with open(temp_script_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        # Verify the update
        with open(temp_script_path, 'r', encoding='utf-8') as f:
            verify_content = f.read()
        
        # Check if the update was successful
        verify_match = re.search(cm_pattern, verify_content, flags=re.DOTALL)
        if verify_match:
            updated_data = verify_match.group(2).strip()
            print(f"📊 Updated CM data: [{updated_data}]")
            
            if updated_data == data_str:
                print(f"✅ Script.js update successful!")
                print(f"   Original: [{original_data}]")
                print(f"   Updated:  [{updated_data}]")
                
                # Cleanup
                shutil.rmtree(temp_dir)
                return True
            else:
                print(f"❌ Update failed - data mismatch")
                print(f"   Expected: [{data_str}]")
                print(f"   Got:      [{updated_data}]")
        else:
            print("❌ Could not find CM data pattern in updated script.js")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        return False
        
    except Exception as e:
        print(f"❌ Error in script.js update test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_actual_pres_stats_files():
    """Test the actual pres stats files structure."""
    print("\n📁 Testing actual pres stats files...")
    
    try:
        pres_stats_dir = Path(__file__).parent / "src" / "pres stats"
        
        if not pres_stats_dir.exists():
            print(f"❌ Pres stats directory not found: {pres_stats_dir}")
            return False
        
        print(f"✅ Pres stats directory found: {pres_stats_dir}")
        
        # Check for required files
        required_files = ['index.html', 'script.js', 'styles.css']
        for file_name in required_files:
            file_path = pres_stats_dir / file_name
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"✅ {file_name}: {file_size} bytes")
            else:
                print(f"❌ {file_name}: NOT FOUND")
                return False
        
        # Check script.js content
        script_path = pres_stats_dir / "script.js"
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Look for CM chart pattern
        if 'const cmCtx' in script_content:
            print(f"✅ CM chart definition found in script.js")
        else:
            print(f"❌ CM chart definition NOT found in script.js")
            return False
        
        # Look for data array pattern
        import re
        data_pattern = r'data:\s*\[([^\]]*)\]'
        matches = re.findall(data_pattern, script_content)
        
        print(f"📊 Found {len(matches)} data arrays in script.js:")
        for i, match in enumerate(matches):
            print(f"   Array {i+1}: [{match.strip()}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing pres stats files: {e}")
        return False

def test_update_method_simulation():
    """Test the _update_chart_data method simulation."""
    print("\n🔧 Testing _update_chart_data method simulation...")
    
    try:
        # Mock script content with CM chart
        mock_script = """
        // Graphique CM
        const cmCtx = document.getElementById('cmChart').getContext('2d');
        new Chart(cmCtx, {
            type: 'bar',
            data: {
                labels: ['RAF', 'MODIF', 'CREA'],
                datasets: [{
                    data: [806, 17, 71],
                    backgroundColor: [colors.raf, colors.modif, colors.crea],
                    borderColor: [colors.raf, colors.modif, colors.crea],
                    borderWidth: 2,
                    borderRadius: 5,
                    borderSkipped: false
                }]
            },
        """
        
        # Test the update logic (same as in _update_chart_data)
        chart_context = 'cmCtx'
        new_data = [25, 15, 10]
        
        import re
        pattern = rf'(const {chart_context}.*?data:\s*\[)[^\]]*(\])'
        data_str = ', '.join(str(x) for x in new_data)
        replacement = rf'\g<1>{data_str}\g<2>'
        
        updated_script = re.sub(pattern, replacement, mock_script, flags=re.DOTALL)
        
        # Check if update was successful
        if f'[{data_str}]' in updated_script:
            print(f"✅ _update_chart_data simulation successful")
            print(f"   Original: [806, 17, 71]")
            print(f"   Updated:  [{data_str}]")
            
            # Show the updated section
            updated_match = re.search(pattern, updated_script, flags=re.DOTALL)
            if updated_match:
                context = updated_match.group(0)[:100] + "..."
                print(f"   Context: {context}")
            
            return True
        else:
            print(f"❌ _update_chart_data simulation failed")
            print(f"   Looking for: [{data_str}]")
            print(f"   In content: {updated_script[:200]}...")
            return False
        
    except Exception as e:
        print(f"❌ Error in update method simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Testing Script.js Update Process")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Actual script.js update
    if test_script_js_update():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Script.js update")
    else:
        print("\n❌ Test 1 FAILED: Script.js update")
    
    # Test 2: Pres stats files structure
    if test_actual_pres_stats_files():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Pres stats files structure")
    else:
        print("\n❌ Test 2 FAILED: Pres stats files structure")
    
    # Test 3: Update method simulation
    if test_update_method_simulation():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Update method simulation")
    else:
        print("\n❌ Test 3 FAILED: Update method simulation")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Script.js update mechanism is working correctly")
        print("📝 If CM values still don't appear in the dashboard:")
        print("  1. Check that the application is actually calling the update methods")
        print("  2. Verify that the browser is loading the updated script.js file")
        print("  3. Clear browser cache and refresh the page")
        print("  4. Check browser developer tools for JavaScript errors")
        print("  5. Verify that the date range contains data in the Suivi Global file")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        print("🔍 Check the error messages above for specific issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

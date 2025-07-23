#!/usr/bin/env python3
"""
Diagnostic script to identify why CM values are not appearing in the dashboard.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_current_script_js_state():
    """Check the current state of script.js."""
    print("📝 Checking current script.js state...")
    
    try:
        script_path = Path(__file__).parent / "src" / "pres stats" / "script.js"
        
        if not script_path.exists():
            print(f"❌ Script.js not found at: {script_path}")
            return False
        
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for CM chart data
        import re
        cm_pattern = r'const cmCtx.*?data:\s*\[([^\]]*)\]'
        cm_match = re.search(cm_pattern, content, flags=re.DOTALL)
        
        if cm_match:
            cm_data = cm_match.group(1).strip()
            print(f"📊 Current CM data in script.js: [{cm_data}]")
            
            # Check if it's all zeros
            if cm_data == "0, 0, 0":
                print("⚠️ CM data is all zeros - this suggests the update ran but found no data")
                return "zeros"
            elif cm_data in ["806, 17, 71", "56, 4"]:
                print("📊 CM data shows original hardcoded values - update hasn't run yet")
                return "original"
            else:
                print("✅ CM data shows custom values - update has run with real data")
                return "updated"
        else:
            print("❌ Could not find CM chart data pattern")
            return False
        
    except Exception as e:
        print(f"❌ Error checking script.js: {e}")
        return False

def check_for_update_comments():
    """Check for update comments in the files."""
    print("\n💬 Checking for update comments...")
    
    try:
        # Check index.html for update comments
        index_path = Path(__file__).parent / "src" / "pres stats" / "index.html"
        script_path = Path(__file__).parent / "src" / "pres stats" / "script.js"
        
        files_to_check = [
            ("index.html", index_path),
            ("script.js", script_path)
        ]
        
        for file_name, file_path in files_to_check:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for Pladria update comments
                if "Pladria Statistics Updated:" in content:
                    print(f"✅ {file_name}: Found update comment")
                    
                    # Extract timestamp
                    import re
                    timestamp_pattern = r'Pladria Statistics Updated: ([^|]*)'
                    timestamp_match = re.search(timestamp_pattern, content)
                    if timestamp_match:
                        timestamp = timestamp_match.group(1).strip()
                        print(f"   Last updated: {timestamp}")
                else:
                    print(f"⚠️ {file_name}: No update comment found")
            else:
                print(f"❌ {file_name}: File not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking update comments: {e}")
        return False

def simulate_real_data_extraction():
    """Simulate what happens with real data extraction."""
    print("\n🔍 Simulating real data extraction scenario...")
    
    try:
        # Simulate common issues
        scenarios = [
            {
                'name': 'No global_suivi_data loaded',
                'global_suivi_data': None,
                'expected_result': 'No CM data extracted'
            },
            {
                'name': 'Missing Traitement CMS Adr sheet',
                'global_suivi_data': {'Suivi Tickets': 'dummy'},
                'expected_result': 'No CM data extracted'
            },
            {
                'name': 'Empty Traitement CMS Adr sheet',
                'global_suivi_data': {'Traitement CMS Adr': []},
                'expected_result': 'No CM data extracted'
            },
            {
                'name': 'No date range set',
                'global_suivi_data': {'Traitement CMS Adr': 'dummy'},
                'date_from_selected': None,
                'date_to_selected': None,
                'expected_result': 'No CM data extracted'
            },
            {
                'name': 'Date range with no matching data',
                'global_suivi_data': {'Traitement CMS Adr': 'dummy'},
                'date_from_selected': '2020-01-01',
                'date_to_selected': '2020-01-02',
                'expected_result': 'CM data with zeros'
            }
        ]
        
        for scenario in scenarios:
            print(f"\n🧪 Scenario: {scenario['name']}")
            print(f"   Expected: {scenario['expected_result']}")
            
            # This would be the actual logic check
            if scenario['global_suivi_data'] is None:
                print("   ❌ Would fail: No global_suivi_data")
            elif 'Traitement CMS Adr' not in scenario['global_suivi_data']:
                print("   ❌ Would fail: Missing sheet")
            elif not scenario['global_suivi_data']['Traitement CMS Adr']:
                print("   ❌ Would fail: Empty sheet")
            elif scenario.get('date_from_selected') is None:
                print("   ❌ Would fail: No date range")
            else:
                print("   ✅ Would proceed to data extraction")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in simulation: {e}")
        return False

def provide_troubleshooting_steps():
    """Provide specific troubleshooting steps based on findings."""
    print("\n🔧 Troubleshooting Steps:")
    
    # Check script.js state
    script_state = check_current_script_js_state()
    
    if script_state == "zeros":
        print("\n📋 Issue: CM data is all zeros")
        print("   Possible causes:")
        print("   1. Date range selected contains no data")
        print("   2. Column names don't match (Motif Voie, Date livraison)")
        print("   3. Date format issues in the Excel file")
        print("   4. Sheet 2 is empty or has wrong structure")
        print("\n   Solutions:")
        print("   ✅ Try selecting a different date range")
        print("   ✅ Check that Sheet 2 has data in columns D and H")
        print("   ✅ Verify date formats are YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY")
        
    elif script_state == "original":
        print("\n📋 Issue: Update hasn't run yet")
        print("   Possible causes:")
        print("   1. 'Generate and open index' button not clicked")
        print("   2. Error occurred during update process")
        print("   3. No data loaded in the application")
        print("\n   Solutions:")
        print("   ✅ Load Suivi Global data first")
        print("   ✅ Select a date range")
        print("   ✅ Click 'Generate and open index' button")
        print("   ✅ Check console logs for errors")
        
    elif script_state == "updated":
        print("\n📋 Issue: Update ran but values not visible")
        print("   Possible causes:")
        print("   1. Browser cache showing old version")
        print("   2. JavaScript errors preventing chart update")
        print("   3. Chart.js not loading properly")
        print("\n   Solutions:")
        print("   ✅ Clear browser cache and refresh")
        print("   ✅ Check browser developer tools for errors")
        print("   ✅ Try opening in incognito/private mode")
        
    else:
        print("\n📋 Issue: Cannot determine script.js state")
        print("   Solutions:")
        print("   ✅ Check that pres stats folder exists")
        print("   ✅ Verify script.js file is not corrupted")
        print("   ✅ Restore original script.js if needed")

def main():
    """Main diagnostic function."""
    print("🔍 Diagnostic: Why CM Values Don't Appear")
    print("=" * 60)
    
    # Check current state
    script_state = check_current_script_js_state()
    
    # Check for update comments
    check_for_update_comments()
    
    # Simulate scenarios
    simulate_real_data_extraction()
    
    # Provide troubleshooting
    provide_troubleshooting_steps()
    
    print("\n" + "=" * 60)
    print("📊 Diagnostic Complete")
    
    print("\n🎯 Next Steps:")
    print("1. Follow the troubleshooting steps above")
    print("2. If issue persists, check application logs")
    print("3. Verify Suivi Global file structure matches expectations")
    print("4. Test with a known date range that contains data")
    
    return True

if __name__ == "__main__":
    main()

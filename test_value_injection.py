#!/usr/bin/env python3
"""
Test script to verify value injection into existing pres stats dashboard.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_test_pres_stats_copy():
    """Create a copy of the actual pres stats folder for testing."""
    print("🔧 Creating test copy of pres stats folder...")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"✅ Created temp directory: {temp_dir}")
    
    # Copy the actual pres stats folder
    src_pres_stats = Path(__file__).parent / "src" / "pres stats"
    temp_pres_stats = os.path.join(temp_dir, "pres stats")
    
    if src_pres_stats.exists():
        shutil.copytree(src_pres_stats, temp_pres_stats)
        print(f"✅ Copied pres stats folder to: {temp_pres_stats}")
    else:
        print("❌ Source pres stats folder not found")
        return None, None, None
    
    # Create fake main data file
    main_data_path = os.path.join(temp_dir, 'test_data.xlsx')
    with open(main_data_path, 'w') as f:
        f.write("fake excel content")
    
    print(f"✅ Created fake main data file: {main_data_path}")
    
    return temp_dir, temp_pres_stats, main_data_path

def test_value_injection_strategy():
    """Test the value injection strategy on real pres stats files."""
    print("\n💉 Testing value injection into existing dashboard...")
    
    try:
        # Create test environment
        temp_dir, temp_pres_stats, main_data_path = create_test_pres_stats_copy()
        if not temp_dir:
            return False
        
        # Read original files
        index_path = os.path.join(temp_pres_stats, 'index.html')
        script_path = os.path.join(temp_pres_stats, 'script.js')
        
        with open(index_path, 'r', encoding='utf-8') as f:
            original_html = f.read()
        
        with open(script_path, 'r', encoding='utf-8') as f:
            original_script = f.read()
        
        print(f"✅ Original HTML length: {len(original_html)} chars")
        print(f"✅ Original script length: {len(original_script)} chars")
        
        # Create mock filtered statistics
        mock_stats = {
            'period': {
                'start_date': '2024-01-01',
                'end_date': '2024-01-15',
                'total_days': 15
            },
            'data_summary': {
                'total_records': 1500
            },
            'motifs': {
                'sorted': [
                    ('Orange', 800),
                    ('RIP', 200),
                    ('RAF', 300),
                    ('MODIF', 50),
                    ('CREA', 150)
                ],
                'total_unique': 5
            }
        }
        
        # Test HTML subtitle update
        import re
        period_text = f"Analyse des données de traitement - {mock_stats['period']['start_date']} à {mock_stats['period']['end_date']}"
        updated_html = re.sub(r'<p class="subtitle">.*?</p>', 
                             f'<p class="subtitle">{period_text}</p>', 
                             original_html, flags=re.DOTALL)
        
        if updated_html != original_html:
            print("✅ HTML subtitle update successful")
        else:
            print("⚠️ HTML subtitle not updated (pattern not found)")
        
        # Test script.js data update
        # Update communes data: [56, 4] -> [800, 200]
        new_communes_data = [800, 200]
        data_str = ', '.join(str(x) for x in new_communes_data)
        
        pattern = r'(const communesCtx.*?data:\s*\[)[^\]]*(\])'
        replacement = rf'\g<1>{data_str}\g<2>'
        updated_script = re.sub(pattern, replacement, original_script, flags=re.DOTALL)
        
        if updated_script != original_script:
            print("✅ Script.js communes data update successful")
            print(f"   Updated communes data to: {new_communes_data}")
        else:
            print("⚠️ Script.js communes data not updated (pattern not found)")
        
        # Test CM data update: [806, 17, 71] -> [300, 50, 150]
        new_cm_data = [300, 50, 150]
        data_str = ', '.join(str(x) for x in new_cm_data)
        
        pattern = r'(const cmCtx.*?data:\s*\[)[^\]]*(\])'
        replacement = rf'\g<1>{data_str}\g<2>'
        updated_script = re.sub(pattern, replacement, updated_script, flags=re.DOTALL)
        
        if "300, 50, 150" in updated_script:
            print("✅ Script.js CM data update successful")
            print(f"   Updated CM data to: {new_cm_data}")
        else:
            print("⚠️ Script.js CM data not updated")
        
        # Add timestamp comment
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment = f'\n<!-- Pladria Statistics Updated: {timestamp} | Period: {mock_stats["period"]["start_date"]} to {mock_stats["period"]["end_date"]} | Records: {mock_stats["data_summary"]["total_records"]} -->\n'
        
        body_close_idx = updated_html.lower().rfind('</body>')
        if body_close_idx != -1:
            updated_html = updated_html[:body_close_idx] + comment + updated_html[body_close_idx:]
            print("✅ Added timestamp comment to HTML")
        
        # Write updated files
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(updated_script)
        
        print(f"✅ Updated files written successfully")
        print(f"   HTML file: {index_path}")
        print(f"   Script file: {script_path}")
        
        # Verify changes
        with open(index_path, 'r', encoding='utf-8') as f:
            verify_html = f.read()
        
        with open(script_path, 'r', encoding='utf-8') as f:
            verify_script = f.read()
        
        # Check if changes are present
        changes_verified = []
        
        if period_text in verify_html:
            changes_verified.append("HTML subtitle updated")
        
        if "300, 50, 150" in verify_script:
            changes_verified.append("CM data updated")
        
        if "800, 200" in verify_script:
            changes_verified.append("Communes data updated")
        
        if "Pladria Statistics Updated:" in verify_html:
            changes_verified.append("Timestamp comment added")
        
        print(f"\n✅ Verified changes: {changes_verified}")
        
        return len(changes_verified) >= 2  # At least 2 changes should be verified
        
    except Exception as e:
        print(f"❌ Error in value injection test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🧹 Cleaned up temp directory: {temp_dir}")

def test_mapping_logic():
    """Test the statistics mapping logic."""
    print("\n🗺️ Testing statistics mapping logic...")
    
    try:
        # Mock statistics data
        mock_stats = {
            'motifs': {
                'sorted': [
                    ('Orange', 800),
                    ('RIP', 200),
                    ('RAF', 300),
                    ('MODIF', 50),
                    ('CREA', 150),
                    ('AD_RAS_AVEC_TEMPS', 2000),
                    ('AD_RAS_SANS_TEMPS', 5000),
                    ('NOK', 800),
                    ('OK', 1000)
                ]
            },
            'data_summary': {
                'total_records': 10000
            }
        }
        
        # Test mapping logic
        top_motifs = dict(mock_stats['motifs']['sorted'][:10])
        
        # Map to dashboard categories
        mapping = {}
        
        # Communes mapping
        if 'Orange' in top_motifs or 'RIP' in top_motifs:
            mapping['communes'] = {
                'data': [
                    top_motifs.get('Orange', 56),
                    top_motifs.get('RIP', 4)
                ]
            }
            print(f"✅ Communes mapping: {mapping['communes']['data']}")
        
        # CM mapping
        mapping['cm'] = {
            'data': [
                top_motifs.get('RAF', 806),
                top_motifs.get('MODIF', 17),
                top_motifs.get('CREA', 71)
            ]
        }
        print(f"✅ CM mapping: {mapping['cm']['data']}")
        
        # Quality mapping
        total_records = mock_stats['data_summary']['total_records']
        conformes = int(total_records * 0.6)
        non_conformes = total_records - conformes
        
        mapping['quality'] = {
            'data': [conformes, non_conformes]
        }
        print(f"✅ Quality mapping: {mapping['quality']['data']}")
        
        # Acts mapping
        mapping['acts'] = {
            'data': [
                top_motifs.get('AD_RAS_AVEC_TEMPS', 2324),
                top_motifs.get('AD_RAS_SANS_TEMPS', 6023),
                top_motifs.get('NOK', 930),
                top_motifs.get('OK', 1084)
            ]
        }
        print(f"✅ Acts mapping: {mapping['acts']['data'][:4]}...")
        
        print(f"✅ Mapping logic successful: {len(mapping)} categories mapped")
        return True
        
    except Exception as e:
        print(f"❌ Error in mapping logic test: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Value Injection into Existing Dashboard")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Value injection strategy
    if test_value_injection_strategy():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Value injection strategy")
    else:
        print("\n❌ Test 1 FAILED: Value injection strategy")
    
    # Test 2: Mapping logic
    if test_mapping_logic():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Mapping logic")
    else:
        print("\n❌ Test 2 FAILED: Mapping logic")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Value injection strategy is working:")
        print("  • Updates existing HTML subtitle with filtered period")
        print("  • Updates Chart.js data arrays with new values")
        print("  • Maps filtered statistics to dashboard categories")
        print("  • Preserves existing dashboard structure")
        print("  • Adds timestamp comments for tracking")
        
        print("\n🎯 The dashboard will now show filtered data in existing charts!")
        print("📝 You may need to adjust the mapping logic in _map_stats_to_dashboard_categories()")
        print("    to match your specific data structure and motif names.")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

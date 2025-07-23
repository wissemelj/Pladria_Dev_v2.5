#!/usr/bin/env python3
"""
Test script to debug CM data injection into the pres stats dashboard.
"""

import sys
import os
import pandas as pd
import tempfile
import shutil
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_mock_team_stats_module():
    """Create a mock TeamStatsModule with the necessary data."""
    print("🔧 Creating mock TeamStatsModule...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create a mock instance (we won't actually initialize the UI)
        class MockTeamStatsModule:
            def __init__(self):
                # Copy the methods we need from the real class
                for method_name in ['_extract_cm_data_for_dashboard', '_map_motifs_to_cm_categories', '_map_stats_to_dashboard_categories']:
                    if hasattr(TeamStatsModule, method_name):
                        setattr(self, method_name, getattr(TeamStatsModule, method_name).__get__(self, MockTeamStatsModule))
                
                # Set up mock data
                self.global_suivi_data = {
                    'Suivi Tickets': pd.DataFrame({'test': [1, 2, 3]}),
                    'Traitement CMS Adr': pd.DataFrame({
                        'Commune': ['Commune1', 'Commune2', 'Commune3', 'Commune4', 'Commune5'],
                        'Collaborateur': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
                        'Status': ['Completed', 'In Progress', 'Completed', 'Completed', 'In Progress'],
                        'Motif Voie': ['RAF', 'MODIF', 'CREA', 'RAF', 'MODIF'],  # Column D
                        'Processing_Info': ['Info1', 'Info2', 'Info3', 'Info4', 'Info5'],
                        'Additional_Data': ['Data1', 'Data2', 'Data3', 'Data4', 'Data5'],
                        'Date traitement': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],  # Column G
                        'Date livraison': ['2024-01-20', '2024-01-21', '2024-01-22', '2024-01-23', '2024-01-24']   # Column H
                    }),
                    'Traitement PA': pd.DataFrame({'test': [4, 5, 6]})
                }
                
                # Set up date range
                self.date_from_selected = date(2024, 1, 15)
                self.date_to_selected = date(2024, 1, 25)
                
                # Set up filtered statistics
                self.filtered_statistics = {
                    'period': {
                        'start_date': '2024-01-15',
                        'end_date': '2024-01-25',
                        'total_days': 10
                    },
                    'data_summary': {
                        'total_records': 100
                    },
                    'motifs': {
                        'sorted': [('RAF', 30), ('MODIF', 25), ('CREA', 20)],
                        'total_unique': 3
                    }
                }
                
                # Set up logger
                import logging
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
        
        mock_module = MockTeamStatsModule()
        print("✅ Mock TeamStatsModule created successfully")
        return mock_module
        
    except Exception as e:
        print(f"❌ Error creating mock module: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_cm_data_extraction():
    """Test the CM data extraction process."""
    print("\n💉 Testing CM data extraction...")
    
    try:
        mock_module = create_mock_team_stats_module()
        if not mock_module:
            return False
        
        # Test the CM data extraction
        print("📊 Calling _extract_cm_data_for_dashboard()...")
        cm_data = mock_module._extract_cm_data_for_dashboard()
        
        if cm_data:
            print(f"✅ CM data extracted successfully:")
            print(f"   Data: {cm_data['data']}")
            print(f"   Total records: {cm_data['total_records']}")
            print(f"   Motif breakdown: {cm_data['motif_breakdown']}")
            return True
        else:
            print("❌ No CM data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error in CM data extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_mapping():
    """Test the dashboard mapping process."""
    print("\n🗺️ Testing dashboard mapping...")
    
    try:
        mock_module = create_mock_team_stats_module()
        if not mock_module:
            return False
        
        # Test the dashboard mapping
        print("📊 Calling _map_stats_to_dashboard_categories()...")
        stats = mock_module.filtered_statistics
        mapping = mock_module._map_stats_to_dashboard_categories(stats)
        
        if mapping:
            print(f"✅ Dashboard mapping successful:")
            for category, data in mapping.items():
                print(f"   {category}: {data}")
            
            # Check if CM data is present
            if 'cm' in mapping:
                cm_data = mapping['cm']['data']
                print(f"   ✅ CM chart data: {cm_data}")
                if sum(cm_data) > 0:
                    print(f"   ✅ CM data has non-zero values")
                    return True
                else:
                    print(f"   ⚠️ CM data is all zeros")
                    return False
            else:
                print(f"   ❌ No CM data in mapping")
                return False
        else:
            print("❌ No dashboard mapping generated")
            return False
            
    except Exception as e:
        print(f"❌ Error in dashboard mapping test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_script_js_update_simulation():
    """Test the script.js update simulation."""
    print("\n📝 Testing script.js update simulation...")
    
    try:
        # Create mock script.js content
        mock_script_content = """
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
        """
        
        # Test the update logic
        new_cm_data = [15, 8, 12]
        data_str = ', '.join(str(x) for x in new_cm_data)
        
        # Simulate the regex replacement
        import re
        pattern = r'(const cmCtx.*?data:\s*\[)[^\]]*(\])'
        replacement = rf'\g<1>{data_str}\g<2>'
        updated_script = re.sub(pattern, replacement, mock_script_content, flags=re.DOTALL)
        
        print(f"📊 Original data pattern found: {bool(re.search(pattern, mock_script_content, flags=re.DOTALL))}")
        print(f"📊 Original data: [806, 17, 71]")
        print(f"📊 New data: [{data_str}]")
        
        if f'[{data_str}]' in updated_script:
            print(f"✅ Script.js update simulation successful")
            print(f"   Data successfully replaced with: [{data_str}]")
            return True
        else:
            print(f"❌ Script.js update simulation failed")
            print(f"   Updated content: {updated_script[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error in script.js update simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_integration():
    """Test the full integration process."""
    print("\n🔄 Testing full integration...")
    
    try:
        mock_module = create_mock_team_stats_module()
        if not mock_module:
            return False
        
        # Step 1: Extract CM data
        print("Step 1: Extracting CM data...")
        cm_data = mock_module._extract_cm_data_for_dashboard()
        if not cm_data:
            print("❌ Step 1 failed: No CM data extracted")
            return False
        print(f"✅ Step 1 passed: CM data = {cm_data['data']}")
        
        # Step 2: Map to dashboard categories
        print("Step 2: Mapping to dashboard categories...")
        stats = mock_module.filtered_statistics
        mapping = mock_module._map_stats_to_dashboard_categories(stats)
        if not mapping or 'cm' not in mapping:
            print("❌ Step 2 failed: No CM mapping generated")
            return False
        print(f"✅ Step 2 passed: CM mapping = {mapping['cm']['data']}")
        
        # Step 3: Verify data consistency
        print("Step 3: Verifying data consistency...")
        extracted_data = cm_data['data']
        mapped_data = mapping['cm']['data']
        if extracted_data == mapped_data:
            print(f"✅ Step 3 passed: Data consistent = {extracted_data}")
        else:
            print(f"⚠️ Step 3 warning: Data mismatch - extracted: {extracted_data}, mapped: {mapped_data}")
        
        # Step 4: Check if data is non-zero
        print("Step 4: Checking data values...")
        if sum(mapped_data) > 0:
            print(f"✅ Step 4 passed: Non-zero data = {mapped_data}")
            return True
        else:
            print(f"❌ Step 4 failed: All zero data = {mapped_data}")
            return False
            
    except Exception as e:
        print(f"❌ Error in full integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🚀 Debugging CM Data Injection")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: CM data extraction
    if test_cm_data_extraction():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: CM data extraction")
    else:
        print("\n❌ Test 1 FAILED: CM data extraction")
    
    # Test 2: Dashboard mapping
    if test_dashboard_mapping():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Dashboard mapping")
    else:
        print("\n❌ Test 2 FAILED: Dashboard mapping")
    
    # Test 3: Script.js update simulation
    if test_script_js_update_simulation():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Script.js update simulation")
    else:
        print("\n❌ Test 3 FAILED: Script.js update simulation")
    
    # Test 4: Full integration
    if test_full_integration():
        tests_passed += 1
        print("\n✅ Test 4 PASSED: Full integration")
    else:
        print("\n❌ Test 4 FAILED: Full integration")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ CM data injection should be working correctly")
        print("📝 If values still don't appear in the dashboard:")
        print("  1. Check that the Suivi Global file is loaded")
        print("  2. Verify that Sheet 2 contains 'Traitement CMS Adr' data")
        print("  3. Ensure date range is set correctly")
        print("  4. Check browser console for JavaScript errors")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        print("🔍 Check the error messages above for specific issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

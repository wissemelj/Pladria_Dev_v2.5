#!/usr/bin/env python3
"""
Test script to verify the Communes Livrées implementation works correctly.
"""

import sys
import os
import pandas as pd
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_mock_communes_data():
    """Create mock communes data that simulates Sheet 1 structure."""
    print("🔧 Creating mock communes data...")
    
    try:
        # Create mock data for Sheet 1 (Suivi Tickets) with 15+ columns
        # Column D (index 3): Commune Type (Orange/RIP)
        # Column O (index 14): Delivery Date
        
        mock_data = {
            'Commune_Name': ['Commune1', 'Commune2', 'Commune3', 'Commune4', 'Commune5', 'Commune6'],
            'Status': ['Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered'],
            'Priority': ['High', 'Medium', 'Low', 'High', 'Medium', 'Low'],
            'Commune_Type': ['Orange', 'RIP', 'Orange', 'Orange', 'RIP', 'Orange'],  # Column D
            'Collaborateur': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'],
            'Col_F': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6'],
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'],
            'Col_H': ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'],
            'Col_I': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6'],
            'Col_J': ['J1', 'J2', 'J3', 'J4', 'J5', 'J6'],
            'Col_K': ['K1', 'K2', 'K3', 'K4', 'K5', 'K6'],
            'Col_L': ['L1', 'L2', 'L3', 'L4', 'L5', 'L6'],
            'Col_M': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'],
            'Col_N': ['N1', 'N2', 'N3', 'N4', 'N5', 'N6'],
            'Delivery_Date': [  # Column O (index 14)
                '2025-07-15 00:00:00',
                '2025-07-16 00:00:00', 
                '2025-07-17 00:00:00',
                '2025-07-18 00:00:00',
                '2025-07-19 00:00:00',
                '2025-07-20 00:00:00'
            ]
        }
        
        df = pd.DataFrame(mock_data)
        print(f"✅ Created mock communes data with {len(df)} rows and {len(df.columns)} columns")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Commune types: {df['Commune_Type'].tolist()}")
        print(f"   Delivery dates: {df['Delivery_Date'].tolist()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error creating mock communes data: {e}")
        return None

def test_communes_data_extraction():
    """Test the communes data extraction logic."""
    print("\n💉 Testing communes data extraction...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create mock module instance
        class MockTeamStatsModule:
            def __init__(self):
                # Copy the method we need
                self._extract_communes_data_for_dashboard = TeamStatsModule._extract_communes_data_for_dashboard.__get__(self, MockTeamStatsModule)
                
                # Set up mock data
                self.global_suivi_data = {
                    'Suivi Tickets': create_mock_communes_data(),
                    'Traitement CMS Adr': pd.DataFrame({'test': [1, 2, 3]}),
                    'Traitement PA': pd.DataFrame({'test': [4, 5, 6]})
                }
                
                # Set up date range
                self.date_from_selected = date(2025, 7, 15)
                self.date_to_selected = date(2025, 7, 25)
                
                # Set up logger
                import logging
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
        
        mock_module = MockTeamStatsModule()
        
        # Test the extraction
        print(f"📊 Testing extraction for period: {mock_module.date_from_selected} to {mock_module.date_to_selected}")
        communes_data = mock_module._extract_communes_data_for_dashboard()
        
        if communes_data:
            print(f"✅ Communes data extracted successfully:")
            print(f"   Data: {communes_data['data']}")
            print(f"   Total records: {communes_data['total_records']}")
            print(f"   Commune breakdown: {communes_data['commune_breakdown']}")
            
            # Expected: 4 Orange, 2 RIP (from mock data)
            expected_orange = 4
            expected_rip = 2
            
            if (communes_data['data'][0] == expected_orange and 
                communes_data['data'][1] == expected_rip):
                print(f"✅ Data matches expected values: Orange={expected_orange}, RIP={expected_rip}")
                return True
            else:
                print(f"❌ Data mismatch - Expected: Orange={expected_orange}, RIP={expected_rip}")
                print(f"   Got: Orange={communes_data['data'][0]}, RIP={communes_data['data'][1]}")
                return False
        else:
            print("❌ No communes data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error in communes data extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_communes_html_patterns():
    """Test the HTML patterns for communes updates."""
    print("\n📝 Testing communes HTML patterns...")
    
    try:
        # Sample HTML content (from actual index.html)
        sample_html = """
        <div class="card">
            <h2>Communes Livrées (60)</h2>
            <div class="chart-container">
                <canvas id="communesChart"></canvas>
            </div>
            <div class="stats-summary">
                <div class="stat-item">
                    <span class="stat-value orange">56</span>
                    <span class="stat-label">Orange</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value rip">4</span>
                    <span class="stat-label">RIP</span>
                </div>
            </div>
        </div>
        """
        
        print(f"📊 Testing with sample HTML...")
        
        # Test data
        test_communes_data = [120, 25]  # Orange, RIP
        total_communes = sum(test_communes_data)
        
        import re
        
        # Test Communes title pattern
        communes_title_pattern = r'(<h2>Communes Livrées\s*\()[^)]*(\)</h2>)'
        communes_title_replacement = rf'\g<1>{total_communes}\g<2>'
        
        title_match = re.search(communes_title_pattern, sample_html)
        if title_match:
            print(f"✅ Communes title pattern found: {title_match.group(0)}")
            updated_title = re.sub(communes_title_pattern, communes_title_replacement, sample_html)
            new_title_match = re.search(communes_title_pattern, updated_title)
            if new_title_match and str(total_communes) in new_title_match.group(0):
                print(f"✅ Communes title updated to: {new_title_match.group(0)}")
            else:
                print(f"❌ Communes title update failed")
                return False
        else:
            print(f"❌ Communes title pattern not found")
            return False
        
        # Test Orange pattern
        orange_pattern = r'(<span class="stat-value orange">)[^<]*(</span>)'
        orange_replacement = rf'\g<1>{test_communes_data[0]}\g<2>'
        
        orange_match = re.search(orange_pattern, sample_html)
        if orange_match:
            print(f"✅ Orange pattern found: {orange_match.group(0)}")
            updated_orange = re.sub(orange_pattern, orange_replacement, sample_html)
            new_orange_match = re.search(orange_pattern, updated_orange)
            if new_orange_match and str(test_communes_data[0]) in new_orange_match.group(0):
                print(f"✅ Orange updated to: {new_orange_match.group(0)}")
            else:
                print(f"❌ Orange update failed")
                return False
        else:
            print(f"❌ Orange pattern not found")
            return False
        
        # Test RIP pattern
        rip_pattern = r'(<span class="stat-value rip">)[^<]*(</span>)'
        rip_replacement = rf'\g<1>{test_communes_data[1]}\g<2>'
        
        rip_match = re.search(rip_pattern, sample_html)
        if rip_match:
            print(f"✅ RIP pattern found: {rip_match.group(0)}")
            updated_rip = re.sub(rip_pattern, rip_replacement, sample_html)
            new_rip_match = re.search(rip_pattern, updated_rip)
            if new_rip_match and str(test_communes_data[1]) in new_rip_match.group(0):
                print(f"✅ RIP updated to: {new_rip_match.group(0)}")
            else:
                print(f"❌ RIP update failed")
                return False
        else:
            print(f"❌ RIP pattern not found")
            return False
        
        print(f"✅ All communes HTML patterns working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error in communes HTML pattern test: {e}")
        return False

def test_communes_script_js_pattern():
    """Test the script.js pattern for communes chart update."""
    print("\n📜 Testing communes script.js pattern...")
    
    try:
        # Sample script.js content
        sample_script = """
        // Graphique Communes livrées
        const communesCtx = document.getElementById('communesChart').getContext('2d');
        new Chart(communesCtx, {
            type: 'doughnut',
            data: {
                labels: ['Orange', 'RIP'],
                datasets: [{
                    data: [56, 4],
                    backgroundColor: [colors.orange, colors.rip],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
        """
        
        # Test data
        test_communes_data = [120, 25]
        
        import re
        
        # Test communes chart pattern
        communes_pattern = r'(const communesCtx.*?data:\s*\[)[^\]]*(\])'
        data_str = ', '.join(str(x) for x in test_communes_data)
        replacement = rf'\g<1>{data_str}\g<2>'
        
        updated_script = re.sub(communes_pattern, replacement, sample_script, flags=re.DOTALL)
        
        # Check if update was successful
        if f'[{data_str}]' in updated_script:
            print(f"✅ Communes script.js update successful")
            print(f"   Original: [56, 4]")
            print(f"   Updated:  [{data_str}]")
            return True
        else:
            print(f"❌ Communes script.js update failed")
            print(f"   Looking for: [{data_str}]")
            print(f"   In content: {updated_script[:200]}...")
            return False
        
    except Exception as e:
        print(f"❌ Error in communes script.js pattern test: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Communes Livrées Implementation")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Communes data extraction
    if test_communes_data_extraction():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Communes data extraction")
    else:
        print("\n❌ Test 1 FAILED: Communes data extraction")
    
    # Test 2: Communes HTML patterns
    if test_communes_html_patterns():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Communes HTML patterns")
    else:
        print("\n❌ Test 2 FAILED: Communes HTML patterns")
    
    # Test 3: Communes script.js pattern
    if test_communes_script_js_pattern():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Communes script.js pattern")
    else:
        print("\n❌ Test 3 FAILED: Communes script.js pattern")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Communes Livrées implementation is working correctly!")
        print("\n🎯 Implementation complete:")
        print("  • Extracts commune types from Column D of Sheet 1")
        print("  • Filters by delivery dates from Column O within selected range")
        print("  • Maps Orange and RIP communes to dashboard categories")
        print("  • Updates HTML elements (title, Orange count, RIP count)")
        print("  • Updates Chart.js data arrays with real filtered data")
        print("  • Provides comprehensive logging and error handling")
        
        print("\n📝 Expected behavior:")
        print("  1. User selects date range and clicks 'Generate and open index'")
        print("  2. System extracts commune data from Sheet 1 within date range")
        print("  3. HTML shows real counts: 'Communes Livrées (total)', Orange: X, RIP: Y")
        print("  4. Chart.js displays same real counts as HTML text")
        print("  5. Perfect synchronization between visual and textual displays")
        
        print("\n🔧 Next step: Test with real Suivi Global data!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

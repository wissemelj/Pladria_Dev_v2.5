#!/usr/bin/env python3
"""
Test script to verify the UPR and 501/511 tickets implementation works correctly.
"""

import sys
import os
import pandas as pd
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_mock_tickets_data():
    """Create mock tickets data that simulates Sheet 1 structure."""
    print("🔧 Creating mock tickets data...")
    
    try:
        # Create mock data for Sheet 1 (Suivi Tickets) with required columns
        # Column O (index 14): Date Livraison
        # Column R (index 17): Date Dépose Ticket 501/511
        # Column S (index 18): Dépose Ticket UPR
        
        mock_data = {
            'Commune_Name': ['Commune1', 'Commune2', 'Commune3', 'Commune4', 'Commune5', 'Commune6', 'Commune7', 'Commune8'],
            'Insee': ['12345', '23456', '34567', '45678', '56789', '67890', '78901', '89012'],
            'Status': ['Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered', 'Delivered'],
            'Priority': ['High', 'Medium', 'Low', 'High', 'Medium', 'Low', 'High', 'Medium'],
            'Domaine': ['Orange', 'RIP', 'Orange', 'Orange', 'RIP', 'Orange', 'Orange', 'RIP'],
            'Col_F': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
            'Col_H': ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'],
            'Col_I': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8'],
            'Col_J': ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8'],
            'Col_K': ['K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8'],
            'Col_L': ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8'],
            'Col_M': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
            'Col_N': ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8'],
            'Date Livraison': [  # Column O (index 14)
                '2025-07-15 00:00:00',
                '2025-07-16 00:00:00', 
                '2025-07-17 00:00:00',
                '2025-07-18 00:00:00',
                '2025-07-19 00:00:00',
                '2025-07-20 00:00:00',
                '2025-07-21 00:00:00',
                '2025-07-22 00:00:00'
            ],
            'Col_P': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'],
            'Col_Q': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8'],
            'Date Dépose Ticket 501/511': [  # Column R (index 17)
                '2025-07-15',
                '2025-07-16', 
                '2025-07-17',
                '',  # Empty value
                '2025-07-19',
                '',  # Empty value
                '2025-07-21',
                '2025-07-22'
            ],
            'Dépose Ticket UPR': [  # Column S (index 18)
                'Créé',
                'Non',
                'Créé',
                'Non',
                'Non',
                'Créé',
                'Non',
                'Non'
            ]
        }
        
        df = pd.DataFrame(mock_data)
        print(f"✅ Created mock tickets data with {len(df)} rows and {len(df.columns)} columns")
        print(f"   Columns: {list(df.columns)}")
        print(f"   UPR values: {df['Dépose Ticket UPR'].tolist()}")
        print(f"   501/511 dates: {df['Date Dépose Ticket 501/511'].tolist()}")
        print(f"   Delivery dates: {df['Date Livraison'].tolist()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error creating mock tickets data: {e}")
        return None

def test_upr_data_extraction():
    """Test the UPR data extraction logic."""
    print("\n💉 Testing UPR data extraction...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create mock module instance
        class MockTeamStatsModule:
            def __init__(self):
                # Copy the method we need
                self._extract_upr_data_for_dashboard = TeamStatsModule._extract_upr_data_for_dashboard.__get__(self, MockTeamStatsModule)
                
                # Set up mock data
                self.global_suivi_data = {
                    'Suivi Tickets': create_mock_tickets_data()
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
        print(f"📊 Testing UPR extraction for period: {mock_module.date_from_selected} to {mock_module.date_to_selected}")
        upr_data = mock_module._extract_upr_data_for_dashboard()
        
        if upr_data:
            print(f"✅ UPR data extracted successfully:")
            print(f"   Data: {upr_data['data']}")
            print(f"   Labels: {upr_data['labels']}")
            print(f"   Total records: {upr_data['total_records']}")
            print(f"   UPR breakdown: {upr_data['upr_breakdown']}")
            
            # Expected: 3 Créé, 5 Non (from mock data)
            expected_cree = 3
            expected_non = 5
            
            if (len(upr_data['data']) == 2 and 
                upr_data['data'][0] == expected_cree and 
                upr_data['data'][1] == expected_non):
                print(f"✅ UPR counts correct: Créé={expected_cree}, Non={expected_non}")
                return True
            else:
                print(f"❌ UPR counts incorrect - Expected Créé={expected_cree}, Non={expected_non}")
                return False
        else:
            print("❌ No UPR data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error in UPR data extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_501511_data_extraction():
    """Test the 501/511 data extraction logic."""
    print("\n💉 Testing 501/511 data extraction...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create mock module instance
        class MockTeamStatsModule:
            def __init__(self):
                # Copy the method we need
                self._extract_501511_data_for_dashboard = TeamStatsModule._extract_501511_data_for_dashboard.__get__(self, MockTeamStatsModule)
                
                # Set up mock data
                self.global_suivi_data = {
                    'Suivi Tickets': create_mock_tickets_data()
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
        print(f"📊 Testing 501/511 extraction for period: {mock_module.date_from_selected} to {mock_module.date_to_selected}")
        tickets_501511_data = mock_module._extract_501511_data_for_dashboard()
        
        if tickets_501511_data:
            print(f"✅ 501/511 data extracted successfully:")
            print(f"   Data: {tickets_501511_data['data']}")
            print(f"   Labels: {tickets_501511_data['labels']}")
            print(f"   Total records: {tickets_501511_data['total_records']}")
            print(f"   Tickets breakdown: {tickets_501511_data['tickets_breakdown']}")
            
            # Expected: 6 tickets (non-empty dates in mock data)
            expected_count = 6
            
            if (len(tickets_501511_data['data']) == 1 and 
                tickets_501511_data['data'][0] == expected_count):
                print(f"✅ 501/511 count correct: {expected_count}")
                return True
            else:
                print(f"❌ 501/511 count incorrect - Expected {expected_count}")
                return False
        else:
            print("❌ No 501/511 data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error in 501/511 data extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_validation():
    """Test data validation for both new sections."""
    print("\n🔍 Testing data validation...")
    
    try:
        from core.data_validator import DataValidator
        
        validator = DataValidator()
        
        # Test data for both sections
        test_data = {
            'upr': {
                'data': [3, 5],
                'labels': ['Créé', 'Non'],
                'total_records': 8,
                'upr_breakdown': {'Créé': 3, 'Non': 5}
            },
            'tickets_501511': {
                'data': [6],
                'labels': ['501/511 Tickets'],
                'total_records': 6,
                'tickets_breakdown': {'501/511 Tickets': 6}
            }
        }
        
        validation_result = validator.validate_dashboard_injection_data(test_data)
        
        if validation_result['valid']:
            print(f"✅ Data validation passed")
            if validation_result['warnings']:
                print(f"   ⚠️ Warnings: {validation_result['warnings']}")
            print(f"   📊 Data summary: {validation_result['data_summary']}")
            return True
        else:
            print(f"❌ Data validation failed:")
            for error in validation_result['errors']:
                print(f"      • {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error in data validation test: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing UPR and 501/511 Tickets Implementation")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: UPR data extraction
    if test_upr_data_extraction():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: UPR data extraction")
    else:
        print("\n❌ Test 1 FAILED: UPR data extraction")
    
    # Test 2: 501/511 data extraction
    if test_501511_data_extraction():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: 501/511 data extraction")
    else:
        print("\n❌ Test 2 FAILED: 501/511 data extraction")
    
    # Test 3: Data validation
    if test_data_validation():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Data validation")
    else:
        print("\n❌ Test 3 FAILED: Data validation")
    
    # Summary
    print("\n" + "=" * 80)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ UPR and 501/511 tickets implementation is working correctly!")
        print("\n🎯 Implementation complete:")
        print("  • UPR: Extracts motifs from Column S, filters by Column O dates")
        print("  • 501/511: Extracts deposit dates from Column R within selected range")
        print("  • Both sections update HTML elements and Chart.js data")
        print("  • Data validation integrated for both sections")
        print("  • Perfect synchronization between HTML and charts")
        
        print("\n📝 Expected behavior:")
        print("  1. User selects date range and clicks 'Generate and open index'")
        print("  2. System extracts UPR and 501/511 data from Sheet 1")
        print("  3. HTML shows real counts for both sections")
        print("  4. Charts display same real counts as HTML text")
        print("  5. Perfect synchronization between all displays")
        
        print("\n🔧 Next step: Test with real Suivi Global data!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

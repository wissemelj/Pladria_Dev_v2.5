#!/usr/bin/env python3
"""
Test de l'implémentation complète de la section RIP (P0 P1).
"""

import sys
import os
import pandas as pd
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_mock_rip_data():
    """Create mock RIP data that simulates Sheet 4 structure."""
    print("🔧 Creating mock RIP data...")
    
    try:
        # Create mock data for Sheet 4 (Traitement RIP) with required columns
        # Column D (index 3): Type (P0/P1)
        # Column E (index 4): Acte de traitement (motifs)
        # Column I (index 8): Date de livraison
        
        mock_data = {
            'Nom commune': ['Commune1', 'Commune2', 'Commune3', 'Commune4', 'Commune5', 'Commune6', 'Commune7', 'Commune8'],
            'Code INSEE': ['12345', '23456', '34567', '45678', '56789', '67890', '78901', '89012'],
            'ID tâche': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8'],
            'Type': ['P0', 'P1', 'P0', 'P2', 'P1', 'P0', 'P1', 'P3'],  # Column D - Mix of P0/P1 and others
            'Acte de traitement': [  # Column E - Motifs
                'rien a faire',
                'modification',
                'creation',
                'rien a faire',
                'modification',
                'creation',
                'rien a faire',
                'modification'
            ],
            'Commentaire': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
            'Date d\'affectation': ['2025-07-10', '2025-07-11', '2025-07-12', '2025-07-13', '2025-07-14', '2025-07-15', '2025-07-16', '2025-07-17'],
            'Date de traitement': ['2025-07-11', '2025-07-12', '2025-07-13', '2025-07-14', '2025-07-15', '2025-07-16', '2025-07-17', '2025-07-18'],
            'Date de livraison': [  # Column I - Delivery dates
                '2025-07-15 00:00:00',
                '2025-07-16 00:00:00', 
                '2025-07-17 00:00:00',
                '2025-07-18 00:00:00',
                '2025-07-19 00:00:00',
                '2025-07-20 00:00:00',
                '2025-07-21 00:00:00',
                '2025-07-22 00:00:00'
            ],
            'Collaborateur': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
            'Durée': [1.0, 2.0, 1.5, 2.5, 1.0, 3.0, 1.5, 2.0]
        }
        
        df = pd.DataFrame(mock_data)
        print(f"✅ Created mock RIP data with {len(df)} rows and {len(df.columns)} columns")
        print(f"   Types: {df['Type'].tolist()}")
        print(f"   Motifs: {df['Acte de traitement'].tolist()}")
        print(f"   Delivery dates: {df['Date de livraison'].tolist()}")
        
        # Expected P0/P1 filtering: indices 0,1,2,4,5,6 (6 records)
        # Expected motifs for P0/P1: rien a faire (3), modification (2), creation (1)
        
        return df
        
    except Exception as e:
        print(f"❌ Error creating mock RIP data: {e}")
        return None

def test_rip_data_extraction():
    """Test the RIP data extraction logic."""
    print("\n💉 Testing RIP data extraction...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create mock module instance
        class MockTeamStatsModule:
            def __init__(self):
                # Copy the methods we need
                self._extract_rip_data_for_dashboard = TeamStatsModule._extract_rip_data_for_dashboard.__get__(self, MockTeamStatsModule)
                self._normalize_rip_motif = TeamStatsModule._normalize_rip_motif.__get__(self, MockTeamStatsModule)
                
                # Set up mock data
                self.global_suivi_data = {
                    'Traitement RIP': create_mock_rip_data()
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
        print(f"📊 Testing RIP extraction for period: {mock_module.date_from_selected} to {mock_module.date_to_selected}")
        rip_data = mock_module._extract_rip_data_for_dashboard()
        
        if rip_data:
            print(f"✅ RIP data extracted successfully:")
            print(f"   Data: {rip_data['data']}")
            print(f"   Labels: {rip_data['labels']}")
            print(f"   Total records: {rip_data['total_records']}")
            print(f"   RIP breakdown: {rip_data['rip_breakdown']}")
            
            # Expected: P0/P1 records only (6 total)
            # Expected motifs: rien a faire (3), modification (2), creation (1)
            expected_rien = 3
            expected_modification = 2
            expected_creation = 1
            
            if (len(rip_data['data']) == 3 and 
                rip_data['data'][0] == expected_rien and 
                rip_data['data'][1] == expected_modification and
                rip_data['data'][2] == expected_creation):
                print(f"✅ RIP counts correct: Rien={expected_rien}, Modification={expected_modification}, Création={expected_creation}")
                return True
            else:
                print(f"❌ RIP counts incorrect - Expected Rien={expected_rien}, Modification={expected_modification}, Création={expected_creation}")
                print(f"   Got: {rip_data['data']}")
                return False
        else:
            print("❌ No RIP data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error in RIP data extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rip_motif_normalization():
    """Test RIP motif normalization logic."""
    print("\n🔧 Testing RIP motif normalization...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create mock module for normalization testing
        class MockNormalizationModule:
            def __init__(self):
                self._normalize_rip_motif = TeamStatsModule._normalize_rip_motif.__get__(self, MockNormalizationModule)
                
                import logging
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
        
        mock_module = MockNormalizationModule()
        
        # Test cases for normalization
        test_cases = [
            # Rien à faire variations
            ('RIEN A FAIRE', 'Rien à faire'),
            ('rien a faire', 'Rien à faire'),
            ('RIEN À FAIRE', 'Rien à faire'),
            ('RIEN_A_FAIRE', 'Rien à faire'),
            
            # Modification variations
            ('MODIFICATION', 'Modification'),
            ('modification', 'Modification'),
            ('MODIF', 'Modification'),
            ('MODIFY', 'Modification'),
            
            # Création variations
            ('CREATION', 'Création'),
            ('creation', 'Création'),
            ('CRÉATION', 'Création'),
            ('CREATE', 'Création'),
            
            # Unknown motif
            ('UNKNOWN_MOTIF', 'UNKNOWN_MOTIF')
        ]
        
        print(f"🧪 Testing normalization cases:")
        all_passed = True
        
        for input_motif, expected_output in test_cases:
            actual_output = mock_module._normalize_rip_motif(input_motif.upper())
            
            if actual_output == expected_output:
                status = "✅"
            else:
                status = "❌"
                all_passed = False
            
            print(f"   {status} '{input_motif}' → '{actual_output}' (attendu: '{expected_output}')")
        
        if all_passed:
            print(f"✅ Tous les tests de normalisation RIP réussis!")
            return True
        else:
            print(f"❌ Certains tests de normalisation RIP ont échoué")
            return False
            
    except Exception as e:
        print(f"❌ Error in RIP normalization test: {e}")
        return False

def test_rip_html_structure():
    """Test que le HTML contient la section RIP."""
    print("\n🔍 Testing RIP HTML structure...")
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ HTML file not found")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for RIP section elements
        rip_elements = [
            'RIP (P0 P1)',
            'rip-rien',
            'rip-modification',
            'rip-creation',
            'rip-total',
            'Rien à faire',
            'Modification',
            'Création',
            'Total RIP',
            'third-width'
        ]
        
        for element in rip_elements:
            if element in html_content:
                print(f"   ✅ RIP HTML element found: {element}")
            else:
                print(f"   ❌ RIP HTML element missing: {element}")
                return False
        
        # Check that we have 3 third-width sections now
        third_width_count = html_content.count('third-width')
        if third_width_count == 3:
            print(f"   ✅ Three third-width sections found (UPR, 501/511, RIP)")
        else:
            print(f"   ❌ Expected 3 third-width sections, found {third_width_count}")
            return False
        
        print(f"   ✅ RIP HTML structure correct")
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking RIP HTML: {e}")
        return False

def test_rip_data_validation():
    """Test RIP data validation."""
    print("\n🔍 Testing RIP data validation...")
    
    try:
        from core.data_validator import DataValidator
        
        validator = DataValidator()
        
        # Test data for RIP section
        test_data = {
            'rip': {
                'data': [3, 2, 1],
                'labels': ['Rien à faire', 'Modification', 'Création'],
                'total_records': 6,
                'rip_breakdown': {'Rien à faire': 3, 'Modification': 2, 'Création': 1}
            }
        }
        
        validation_result = validator.validate_dashboard_injection_data(test_data)
        
        if validation_result['valid']:
            print(f"✅ RIP data validation passed")
            if validation_result['warnings']:
                print(f"   ⚠️ Warnings: {validation_result['warnings']}")
            print(f"   📊 Data summary: {validation_result['data_summary']}")
            return True
        else:
            print(f"❌ RIP data validation failed:")
            for error in validation_result['errors']:
                print(f"      • {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error in RIP data validation test: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing RIP (P0 P1) Section Implementation")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: RIP data extraction
    if test_rip_data_extraction():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: RIP data extraction")
    else:
        print("\n❌ Test 1 FAILED: RIP data extraction")
    
    # Test 2: RIP motif normalization
    if test_rip_motif_normalization():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: RIP motif normalization")
    else:
        print("\n❌ Test 2 FAILED: RIP motif normalization")
    
    # Test 3: RIP HTML structure
    if test_rip_html_structure():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: RIP HTML structure")
    else:
        print("\n❌ Test 3 FAILED: RIP HTML structure")
    
    # Test 4: RIP data validation
    if test_rip_data_validation():
        tests_passed += 1
        print("\n✅ Test 4 PASSED: RIP data validation")
    else:
        print("\n❌ Test 4 FAILED: RIP data validation")
    
    # Summary
    print("\n" + "=" * 80)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ RIP (P0 P1) section implementation complete!")
        print("\n🎯 Implementation includes:")
        print("  • RIP data extraction from Sheet 4 (Traitement RIP)")
        print("  • P0/P1 type filtering from Column D")
        print("  • Motif extraction and normalization from Column E")
        print("  • Date filtering from Column I (Date de livraison)")
        print("  • HTML section with 4 bannettes (3 motifs + total)")
        print("  • Horizontal layout with UPR and 501/511 (3 sections)")
        print("  • Data validation for RIP section")
        print("  • Perfect integration with existing dashboard")
        
        print("\n📐 Layout:")
        print("  ┌─────────────┬─────────────┬─────────────┐")
        print("  │ Tickets UPR │ Tickets     │ RIP (P0 P1) │")
        print("  │             │ 501/511     │             │")
        print("  └─────────────┴─────────────┴─────────────┘")
        
        print("\n🔧 Ready for testing with real Sheet 4 data!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

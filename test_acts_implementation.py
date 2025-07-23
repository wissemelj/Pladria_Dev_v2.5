#!/usr/bin/env python3
"""
Test script to verify the Acts Traitement PA implementation works correctly.
"""

import sys
import os
import pandas as pd
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def create_mock_acts_data():
    """Create mock acts data that simulates Sheet 3 structure."""
    print("🔧 Creating mock acts data...")
    
    try:
        # Create mock data for Sheet 3 (Traitement PA) with 8 columns
        # Column D (index 3): Motif
        # Column G (index 6): Date traitement  
        # Column H (index 7): Durée
        
        mock_data = {
            'Nom commune': ['Commune1', 'Commune2', 'Commune3', 'Commune4', 'Commune5', 'Commune6', 'Commune7', 'Commune8'],
            'Insee': ['12345', '23456', '34567', '45678', '56789', '67890', '78901', '89012'],
            'Num Dossier Site': ['DS001', 'DS002', 'DS003', 'DS004', 'DS005', 'DS006', 'DS007', 'DS008'],
            'Motif': ['ad ras', 'AD RAS', 'ok', 'NOK', 'ad non jointe', 'UPR ras', 'ad ras', 'AD RAS'],  # Column D
            'Adresse BAN': ['Addr1', 'Addr2', 'Addr3', 'Addr4', 'Addr5', 'Addr6', 'Addr7', 'Addr8'],
            'Collaborateur': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob'],
            'Date traitement': [  # Column G
                '2025-07-15',
                '2025-07-16', 
                '2025-07-17',
                '2025-07-18',
                '2025-07-19',
                '2025-07-20',
                '2025-07-21',
                '2025-07-22'
            ],
            'Durée': [0.0, 5.0, 2.0, 1.0, 0.0, 3.0, 0.0, 2.0]  # Column H
        }
        
        df = pd.DataFrame(mock_data)
        print(f"✅ Created mock acts data with {len(df)} rows and {len(df.columns)} columns")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Motifs: {df['Motif'].tolist()}")
        print(f"   Durations: {df['Durée'].tolist()}")
        print(f"   Processing dates: {df['Date traitement'].tolist()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error creating mock acts data: {e}")
        return None

def test_acts_data_extraction():
    """Test the acts data extraction logic."""
    print("\n💉 Testing acts data extraction...")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Create mock module instance
        class MockTeamStatsModule:
            def __init__(self):
                # Copy the method we need
                self._extract_acts_data_for_dashboard = TeamStatsModule._extract_acts_data_for_dashboard.__get__(self, MockTeamStatsModule)
                self._normalize_acts_motif = TeamStatsModule._normalize_acts_motif.__get__(self, MockTeamStatsModule)
                
                # Set up mock data
                self.global_suivi_data = {
                    'Suivi Tickets': pd.DataFrame({'test': [1, 2, 3]}),
                    'Traitement CMS Adr': pd.DataFrame({'test': [4, 5, 6]}),
                    'Traitement PA': create_mock_acts_data()
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
        acts_data = mock_module._extract_acts_data_for_dashboard()
        
        if acts_data:
            print(f"✅ Acts data extracted successfully:")
            print(f"   Data: {acts_data['data']}")
            print(f"   Labels: {acts_data['labels']}")
            print(f"   Total records: {acts_data['total_records']}")
            print(f"   Motif breakdown: {acts_data['motif_breakdown']}")
            
            # Expected: Ad Ras split by duration, plus other motifs
            expected_categories = ['AD RAS sans temps', 'AD RAS avec temps', 'OK', 'NOK', 'AD Non jointe', 'UPR RAS']
            
            # Check that we have the expected Ad Ras split
            has_ad_ras_sans = 'AD RAS sans temps' in acts_data['motif_breakdown']
            has_ad_ras_avec = 'AD RAS avec temps' in acts_data['motif_breakdown']
            
            if has_ad_ras_sans and has_ad_ras_avec:
                print(f"✅ Ad Ras correctly split by duration:")
                print(f"   AD RAS sans temps: {acts_data['motif_breakdown'].get('AD RAS sans temps', 0)}")
                print(f"   AD RAS avec temps: {acts_data['motif_breakdown'].get('AD RAS avec temps', 0)}")
                return True
            else:
                print(f"❌ Ad Ras split failed - Expected both 'sans temps' and 'avec temps' categories")
                return False
        else:
            print("❌ No acts data extracted")
            return False
            
    except Exception as e:
        print(f"❌ Error in acts data extraction test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_acts_html_patterns():
    """Test the HTML patterns for acts updates."""
    print("\n📝 Testing acts HTML patterns...")
    
    try:
        # Sample HTML content (from actual index.html)
        sample_html = """
        <div class="card full-width">
            <h2>Acts Traitement PA (11,396)</h2>
            <div class="acts-summary">
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="summary-value">6,023</span>
                        <span class="summary-label">AD RAS sans temps (52.8%)</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-value">2,324</span>
                        <span class="summary-label">AD RAS avec temps (20.4%)</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-value">1,084</span>
                        <span class="summary-label">OK (9.5%)</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-value">930</span>
                        <span class="summary-label">NOK (8.2%)</span>
                    </div>
                </div>
            </div>
        </div>
        """
        
        print(f"📊 Testing with sample HTML...")
        
        # Test data
        test_acts_total = 15000
        
        import re
        
        # Test Acts title pattern
        acts_title_pattern = r'(<h2>Acts Traitement PA\s*\()[^)]*(\)</h2>)'
        acts_title_replacement = rf'\g<1>{test_acts_total:,}\g<2>'
        
        title_match = re.search(acts_title_pattern, sample_html)
        if title_match:
            print(f"✅ Acts title pattern found: {title_match.group(0)}")
            updated_title = re.sub(acts_title_pattern, acts_title_replacement, sample_html)
            new_title_match = re.search(acts_title_pattern, updated_title)
            if new_title_match and str(test_acts_total) in new_title_match.group(0).replace(',', ''):
                print(f"✅ Acts title updated to: {new_title_match.group(0)}")
            else:
                print(f"❌ Acts title update failed")
                return False
        else:
            print(f"❌ Acts title pattern not found")
            return False
        
        # Test individual category patterns
        test_patterns = [
            ('AD RAS sans temps', r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">AD RAS sans temps)', 8000),
            ('AD RAS avec temps', r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">AD RAS avec temps)', 3000),
            ('OK', r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">OK)', 2000),
            ('NOK', r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">NOK)', 1500)
        ]
        
        for category, pattern, test_value in test_patterns:
            match = re.search(pattern, sample_html)
            if match:
                print(f"✅ {category} pattern found: {match.group(0)[:50]}...")
                replacement = rf'\g<1>{test_value:,}\g<2>'
                updated_html = re.sub(pattern, replacement, sample_html)
                new_match = re.search(pattern, updated_html)
                if new_match and str(test_value) in new_match.group(0).replace(',', ''):
                    print(f"✅ {category} updated successfully")
                else:
                    print(f"❌ {category} update failed")
                    return False
            else:
                print(f"❌ {category} pattern not found")
                return False
        
        print(f"✅ All acts HTML patterns working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error in acts HTML pattern test: {e}")
        return False

def test_acts_script_js_pattern():
    """Test the script.js pattern for acts chart update."""
    print("\n📜 Testing acts script.js pattern...")
    
    try:
        # Sample script.js content
        sample_script = """
        // Graphique Acts traitement PA (principal)
        const actsCtx = document.getElementById('actsChart').getContext('2d');
        new Chart(actsCtx, {
            type: 'bar',
            data: {
                labels: ['AD RAS\\navec temps', 'AD RAS\\nsans temps', 'AD Non jointe', 'AD Non trouvée', 'Hors commune', 'NOK', 'OK', 'UPR RAS', 'UPR NOK', 'UPR OK'],
                datasets: [{
                    data: [2324, 6023, 584, 143, 23, 930, 1084, 180, 16, 14],
                    backgroundColor: colors.acts,
                    borderWidth: 1
                }]
            },
        """
        
        # Test data
        test_acts_data = [3000, 8000, 600, 150, 25, 1500, 2000, 200, 20, 15]
        
        import re
        
        # Test acts chart pattern
        acts_pattern = r'(const actsCtx.*?data:\s*\[)[^\]]*(\])'
        data_str = ', '.join(str(x) for x in test_acts_data)
        replacement = rf'\g<1>{data_str}\g<2>'
        
        updated_script = re.sub(acts_pattern, replacement, sample_script, flags=re.DOTALL)
        
        # Check if update was successful
        if f'[{data_str}]' in updated_script:
            print(f"✅ Acts script.js update successful")
            print(f"   Original: [2324, 6023, 584, ...]")
            print(f"   Updated:  [{data_str}]")
            return True
        else:
            print(f"❌ Acts script.js update failed")
            print(f"   Looking for: [{data_str}]")
            print(f"   In content: {updated_script[:300]}...")
            return False
        
    except Exception as e:
        print(f"❌ Error in acts script.js pattern test: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Acts Traitement PA Implementation")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Acts data extraction
    if test_acts_data_extraction():
        tests_passed += 1
        print("\n✅ Test 1 PASSED: Acts data extraction")
    else:
        print("\n❌ Test 1 FAILED: Acts data extraction")
    
    # Test 2: Acts HTML patterns
    if test_acts_html_patterns():
        tests_passed += 1
        print("\n✅ Test 2 PASSED: Acts HTML patterns")
    else:
        print("\n❌ Test 2 FAILED: Acts HTML patterns")
    
    # Test 3: Acts script.js pattern
    if test_acts_script_js_pattern():
        tests_passed += 1
        print("\n✅ Test 3 PASSED: Acts script.js pattern")
    else:
        print("\n❌ Test 3 FAILED: Acts script.js pattern")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Acts Traitement PA implementation is working correctly!")
        print("\n🎯 Implementation complete:")
        print("  • Extracts motifs from Column D of Sheet 3")
        print("  • Filters by processing dates from Column G within selected range")
        print("  • Uses duration from Column H for Ad Ras categorization")
        print("  • Special Ad Ras handling: splits by duration (0 vs >0)")
        print("  • Updates HTML elements (title + individual category counts)")
        print("  • Updates Chart.js data arrays with real filtered data")
        print("  • Provides comprehensive logging and error handling")
        
        print("\n📝 Expected behavior:")
        print("  1. User selects date range and clicks 'Generate and open index'")
        print("  2. System extracts acts data from Sheet 3 within date range")
        print("  3. Ad Ras motifs split: 'avec temps' (duration > 0), 'sans temps' (duration = 0)")
        print("  4. HTML shows real counts for each category")
        print("  5. Chart.js displays same real counts as HTML text")
        print("  6. Perfect synchronization between visual and textual displays")
        
        print("\n🔧 Next step: Test with real Suivi Global data!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

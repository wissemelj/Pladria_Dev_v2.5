#!/usr/bin/env python3
"""
Debug script pour analyser les motifs réels dans les données Acts.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def analyze_real_motifs():
    """Analyser les motifs réels dans Sheet 3."""
    print("🔍 Analyse des Motifs Réels dans les Données Acts")
    print("=" * 70)
    
    try:
        from config.constants import TeamsConfig
        
        # Get the Teams folder path
        teams_folder_path = TeamsConfig.get_global_teams_path()
        global_excel_filename = "Suivis Global Tickets CMS Adr_PA.xlsx"
        global_file_path = os.path.join(teams_folder_path, global_excel_filename)
        
        if not os.path.exists(global_file_path):
            print(f"❌ Suivi Global file not found")
            return False
        
        print(f"✅ Found Suivi Global file")
        
        # Load Sheet 3
        import pandas as pd
        excel_file = pd.ExcelFile(global_file_path)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) >= 3:
            sheet3_name = sheet_names[2]  # Third sheet
            print(f"📊 Loading Sheet 3: '{sheet3_name}'")
            
            df_acts = pd.read_excel(global_file_path, sheet_name=sheet3_name, date_format=None)
            print(f"   Loaded: {len(df_acts)} rows, {len(df_acts.columns)} columns")
            
            # Analyze Column D (motifs)
            motif_column = df_acts.columns[3]  # Column D
            print(f"\n🎯 Analyzing motifs in Column D: '{motif_column}'")
            
            # Get all unique motifs
            all_motifs = df_acts.iloc[:, 3].dropna().value_counts()
            print(f"   Total unique motifs: {len(all_motifs)}")
            print(f"   Total records with motifs: {all_motifs.sum()}")
            
            print(f"\n📋 All motifs found (with counts):")
            for i, (motif, count) in enumerate(all_motifs.items()):
                print(f"   {i+1:2d}. '{motif}': {count:,}")
            
            # Look for specific patterns
            print(f"\n🔍 Analysis of specific patterns:")
            
            # NOK patterns
            nok_patterns = []
            upr_nok_patterns = []
            upr_ok_patterns = []
            ok_patterns = []
            
            for motif in all_motifs.index:
                motif_upper = str(motif).upper().strip()
                
                if 'UPR' in motif_upper and 'NOK' in motif_upper:
                    upr_nok_patterns.append((motif, all_motifs[motif]))
                elif 'UPR' in motif_upper and 'OK' in motif_upper:
                    upr_ok_patterns.append((motif, all_motifs[motif]))
                elif 'NOK' in motif_upper or 'KO' in motif_upper:
                    if 'UPR' not in motif_upper:
                        nok_patterns.append((motif, all_motifs[motif]))
                elif motif_upper == 'OK':
                    ok_patterns.append((motif, all_motifs[motif]))
            
            print(f"\n   NOK patterns found: {len(nok_patterns)}")
            for motif, count in nok_patterns:
                print(f"     '{motif}': {count:,}")
            
            print(f"\n   UPR NOK patterns found: {len(upr_nok_patterns)}")
            for motif, count in upr_nok_patterns:
                print(f"     '{motif}': {count:,}")
            
            print(f"\n   UPR OK patterns found: {len(upr_ok_patterns)}")
            for motif, count in upr_ok_patterns:
                print(f"     '{motif}': {count:,}")
            
            print(f"\n   OK patterns found: {len(ok_patterns)}")
            for motif, count in ok_patterns:
                print(f"     '{motif}': {count:,}")
            
            # Test current normalization logic
            print(f"\n🔧 Testing current normalization logic:")
            
            from ui.modules.team_stats_module import TeamStatsModule
            
            class MockModule:
                def _normalize_acts_motif(self, motif_upper):
                    return TeamStatsModule._normalize_acts_motif(None, motif_upper)
            
            mock = MockModule()
            
            print(f"   Testing normalization for found motifs:")
            for motif in all_motifs.index[:20]:  # Test first 20 motifs
                motif_upper = str(motif).upper().strip()
                normalized = mock._normalize_acts_motif(motif_upper)
                print(f"     '{motif}' → '{normalized}'")
            
            # Calculate expected totals
            print(f"\n📊 Expected totals based on patterns:")
            
            total_nok = sum(count for _, count in nok_patterns)
            total_upr_nok = sum(count for _, count in upr_nok_patterns)
            total_upr_ok = sum(count for _, count in upr_ok_patterns)
            total_ok = sum(count for _, count in ok_patterns)
            
            print(f"   NOK total: {total_nok:,}")
            print(f"   UPR NOK total: {total_upr_nok:,}")
            print(f"   UPR OK total: {total_upr_ok:,}")
            print(f"   OK total: {total_ok:,}")
            
            if total_nok == 0 and total_upr_nok == 0 and total_upr_ok == 0:
                print(f"\n⚠️ WARNING: No NOK/UPR patterns found!")
                print(f"   This explains why these categories show 0 in the dashboard")
                print(f"   The motifs in the data may use different naming conventions")
            else:
                print(f"\n✅ Patterns found - should appear in dashboard")
            
            return True
            
        else:
            print(f"❌ Not enough sheets found")
            return False
        
    except Exception as e:
        print(f"❌ Error analyzing motifs: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_date_filter():
    """Test avec filtre de date pour voir les motifs dans la période sélectionnée."""
    print(f"\n📅 Test avec filtre de date (Juillet 2025):")
    
    try:
        from config.constants import TeamsConfig
        from datetime import datetime, date
        
        teams_folder_path = TeamsConfig.get_global_teams_path()
        global_excel_filename = "Suivis Global Tickets CMS Adr_PA.xlsx"
        global_file_path = os.path.join(teams_folder_path, global_excel_filename)
        
        import pandas as pd
        excel_file = pd.ExcelFile(global_file_path)
        sheet3_name = excel_file.sheet_names[2]
        df_acts = pd.read_excel(global_file_path, sheet_name=sheet3_name, date_format=None)
        
        # Filter by July 2025
        date_from = date(2025, 7, 1)
        date_to = date(2025, 7, 31)
        
        motif_column = df_acts.columns[3]  # Column D
        date_column = df_acts.columns[6]   # Column G
        
        print(f"   Filtering by date range: {date_from} to {date_to}")
        
        filtered_motifs = {}
        total_filtered = 0
        
        for index, row in df_acts.iterrows():
            try:
                # Get processing date
                processing_date = row.get(date_column, '')
                if not processing_date or str(processing_date).strip() == '':
                    continue
                
                # Parse date
                date_obj = None
                processing_date_str = str(processing_date).strip()
                
                try:
                    date_obj = datetime.strptime(processing_date_str, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        date_obj = datetime.strptime(processing_date_str, '%Y-%m-%d %H:%M:%S').date()
                    except ValueError:
                        continue
                
                if not date_obj or not (date_from <= date_obj <= date_to):
                    continue
                
                # Get motif
                motif = row.get(motif_column, '')
                if not motif or str(motif).strip() == '':
                    continue
                
                motif = str(motif).strip()
                if motif in filtered_motifs:
                    filtered_motifs[motif] += 1
                else:
                    filtered_motifs[motif] = 1
                
                total_filtered += 1
                
            except Exception as e:
                continue
        
        print(f"   Total records in July 2025: {total_filtered:,}")
        print(f"   Unique motifs in July 2025: {len(filtered_motifs)}")
        
        if filtered_motifs:
            print(f"\n   Motifs found in July 2025:")
            sorted_motifs = sorted(filtered_motifs.items(), key=lambda x: x[1], reverse=True)
            for motif, count in sorted_motifs:
                print(f"     '{motif}': {count:,}")
            
            # Check for NOK patterns in filtered data
            nok_in_july = 0
            upr_nok_in_july = 0
            upr_ok_in_july = 0
            
            for motif, count in filtered_motifs.items():
                motif_upper = str(motif).upper().strip()
                if 'UPR' in motif_upper and 'NOK' in motif_upper:
                    upr_nok_in_july += count
                elif 'UPR' in motif_upper and 'OK' in motif_upper:
                    upr_ok_in_july += count
                elif ('NOK' in motif_upper or 'KO' in motif_upper) and 'UPR' not in motif_upper:
                    nok_in_july += count
            
            print(f"\n   July 2025 totals:")
            print(f"     NOK: {nok_in_july:,}")
            print(f"     UPR NOK: {upr_nok_in_july:,}")
            print(f"     UPR OK: {upr_ok_in_july:,}")
            
            if nok_in_july == 0 and upr_nok_in_july == 0 and upr_ok_in_july == 0:
                print(f"\n⚠️ No NOK/UPR patterns in July 2025 data!")
                print(f"   This explains the 0 values in the dashboard")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error in date filter test: {e}")
        return False

def main():
    """Main analysis function."""
    print("🚀 Debug des Motifs Acts - Analyse NOK/UPR")
    print("=" * 70)
    
    if analyze_real_motifs():
        test_with_date_filter()
        
        print(f"\n📝 Conclusions:")
        print(f"  • Vérifiez si les motifs NOK/UPR existent dans les données")
        print(f"  • Vérifiez si ces motifs sont présents dans la période sélectionnée")
        print(f"  • La normalisation des motifs peut nécessiter des ajustements")
        print(f"  • Les valeurs 0 peuvent être correctes si ces motifs n'existent pas")
        
        return True
    else:
        print(f"\n❌ Analyse échouée")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

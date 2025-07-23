#!/usr/bin/env python3
"""
Script to analyze Sheet 4 data structure for RIP (P0 P1) section.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def analyze_sheet4_for_rip_section():
    """Analyze Sheet 4 for RIP (P0 P1) data."""
    print("📊 Analyzing Sheet 4 for RIP (P0 P1) Data")
    print("=" * 80)
    
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
        
        # Load Sheet 4
        import pandas as pd
        excel_file = pd.ExcelFile(global_file_path)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) >= 4:
            sheet4_name = sheet_names[3]  # Fourth sheet (index 3)
            print(f"📊 Loading Sheet 4: '{sheet4_name}'")
            
            df_rip = pd.read_excel(global_file_path, sheet_name=sheet4_name, date_format=None)
            print(f"   Loaded: {len(df_rip)} rows, {len(df_rip.columns)} columns")
            
            # Display all columns for reference
            print(f"\n📋 All columns in Sheet 4:")
            for i, col in enumerate(df_rip.columns):
                print(f"   {chr(65+i) if i < 26 else f'A{chr(65+i-26)}'} (index {i}): '{col}'")
            
            # Analyze Column D (index 3) - Type filter (P0/P1)
            print(f"\n🎯 Analyzing Column D (index 3) for Type data:")
            if len(df_rip.columns) > 3:
                col_d_name = df_rip.columns[3]
                print(f"   Column name: '{col_d_name}'")
                
                col_d_values = df_rip.iloc[:, 3].dropna().value_counts()
                print(f"   Total non-null values: {col_d_values.sum()}")
                print(f"   Unique values: {len(col_d_values)}")
                
                if len(col_d_values) > 0:
                    print("   All type values:")
                    for value, count in col_d_values.items():
                        print(f"     '{value}': {count}")
                    
                    # Look for P0/P1 patterns
                    p0_count = 0
                    p1_count = 0
                    p0_p1_variations = []
                    
                    for value in col_d_values.index:
                        value_str = str(value).upper().strip()
                        if 'P0' in value_str:
                            p0_count += col_d_values[value]
                            p0_p1_variations.append((value, col_d_values[value], 'P0'))
                        elif 'P1' in value_str:
                            p1_count += col_d_values[value]
                            p0_p1_variations.append((value, col_d_values[value], 'P1'))
                    
                    print(f"\n   🔍 P0/P1 related values:")
                    print(f"     P0 total: {p0_count}")
                    print(f"     P1 total: {p1_count}")
                    print(f"     P0+P1 total: {p0_count + p1_count}")
                    
                    if p0_p1_variations:
                        print(f"   P0/P1 variations found:")
                        for value, count, type_detected in p0_p1_variations:
                            print(f"     '{value}': {count} ({type_detected})")
                else:
                    print("   ❌ No values found in Column D!")
            else:
                print("   ❌ Column D (index 3) not available")
            
            # Analyze Column E (index 4) - Motif data
            print(f"\n🎯 Analyzing Column E (index 4) for Motif data:")
            if len(df_rip.columns) > 4:
                col_e_name = df_rip.columns[4]
                print(f"   Column name: '{col_e_name}'")
                
                col_e_values = df_rip.iloc[:, 4].dropna().value_counts()
                print(f"   Total non-null values: {col_e_values.sum()}")
                print(f"   Unique values: {len(col_e_values)}")
                
                if len(col_e_values) > 0:
                    print("   All motif values:")
                    for value, count in col_e_values.items():
                        print(f"     '{value}': {count}")
                    
                    # Look for expected motifs
                    expected_motifs = ['rien a faire', 'modification', 'creation']
                    found_motifs = {}
                    
                    for expected in expected_motifs:
                        found_motifs[expected] = 0
                        for value in col_e_values.index:
                            value_lower = str(value).lower().strip()
                            if expected in value_lower:
                                found_motifs[expected] += col_e_values[value]
                    
                    print(f"\n   🔍 Expected motifs analysis:")
                    for motif, count in found_motifs.items():
                        print(f"     '{motif}': {count}")
                else:
                    print("   ❌ No values found in Column E!")
            else:
                print("   ❌ Column E (index 4) not available")
            
            # Analyze Column I (index 8) - Date de livraison
            print(f"\n📅 Analyzing Column I (index 8) for Date data:")
            if len(df_rip.columns) > 8:
                col_i_name = df_rip.columns[8]
                print(f"   Column name: '{col_i_name}'")
                
                col_i_values = df_rip.iloc[:, 8].dropna()
                print(f"   Total non-null values: {len(col_i_values)}")
                
                if len(col_i_values) > 0:
                    print("   Sample date values:")
                    for i, value in enumerate(col_i_values.head(10)):
                        print(f"     {i+1}. '{value}' (type: {type(value)})")
                    
                    # Try to parse dates
                    valid_dates = []
                    date_formats = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%d',
                        '%d/%m/%Y %H:%M:%S',
                        '%d/%m/%Y',
                        '%d-%m-%Y %H:%M:%S',
                        '%d-%m-%Y'
                    ]
                    
                    for value in col_i_values.head(20):  # Test first 20 values
                        if pd.isna(value):
                            continue
                            
                        parsed_date = None
                        for date_format in date_formats:
                            try:
                                from datetime import datetime
                                parsed_date = datetime.strptime(str(value), date_format).date()
                                break
                            except ValueError:
                                continue
                        
                        if parsed_date:
                            valid_dates.append(parsed_date)
                    
                    print(f"   Valid parsed dates: {len(valid_dates)}")
                    if len(valid_dates) > 0:
                        min_date = min(valid_dates)
                        max_date = max(valid_dates)
                        print(f"   📅 Date range: {min_date} to {max_date}")
                    else:
                        print("   ❌ No valid dates could be parsed!")
                else:
                    print("   ❌ No values found in Column I!")
            else:
                print("   ❌ Column I (index 8) not available")
            
            # Cross-analysis: P0/P1 records with motifs and dates
            print(f"\n🔄 Cross-analysis: P0/P1 records with motifs and dates")
            
            if len(df_rip.columns) > 8:
                p0_p1_with_data = 0
                motif_breakdown = {}
                
                for index, row in df_rip.iterrows():
                    type_value = row.iloc[3] if len(df_rip.columns) > 3 else None  # Column D
                    motif_value = row.iloc[4] if len(df_rip.columns) > 4 else None  # Column E
                    date_value = row.iloc[8] if len(df_rip.columns) > 8 else None  # Column I
                    
                    if (pd.notna(type_value) and pd.notna(motif_value) and pd.notna(date_value)):
                        type_str = str(type_value).upper().strip()
                        if 'P0' in type_str or 'P1' in type_str:
                            p0_p1_with_data += 1
                            
                            motif_str = str(motif_value).lower().strip()
                            if motif_str in motif_breakdown:
                                motif_breakdown[motif_str] += 1
                            else:
                                motif_breakdown[motif_str] = 1
                
                print(f"   P0/P1 records with complete data: {p0_p1_with_data}")
                
                if motif_breakdown:
                    print(f"   Motif breakdown for P0/P1 records:")
                    sorted_motifs = sorted(motif_breakdown.items(), key=lambda x: x[1], reverse=True)
                    for motif, count in sorted_motifs[:10]:  # Top 10
                        print(f"     '{motif}': {count}")
            
            print(f"\n✅ Sheet 4 analysis complete!")
            print(f"💡 Implementation suggestions:")
            print(f"   • RIP data: Extract from Column D (type P0/P1), Column E (motifs), Column I (dates)")
            print(f"   • Filter by type: P0 or P1 in Column D")
            print(f"   • Extract motifs: Column E with categories 'rien a faire', 'modification', 'creation'")
            print(f"   • Date filtering: Column I for delivery dates")
            
            return True
            
        else:
            print(f"❌ Sheet 4 not found (only {len(sheet_names)} sheets available)")
            return False
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main analysis function."""
    print("🚀 Analysis of RIP (P0 P1) Data Structure in Sheet 4")
    print("=" * 80)
    
    if analyze_sheet4_for_rip_section():
        print(f"\n📝 Next steps:")
        print(f"  1. Implement _extract_rip_data_for_dashboard() method")
        print(f"  2. Add RIP section to horizontal tickets-row")
        print(f"  3. Update dashboard mapping and HTML updates")
        print(f"  4. Add data validation for RIP section")
        print(f"  5. Test with real data to verify implementation")
        
        return True
    else:
        print(f"\n❌ Analysis failed - check the file structure")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

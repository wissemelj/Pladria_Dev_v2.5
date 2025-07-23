#!/usr/bin/env python3
"""
Script to analyze Sheet 3 (Traitement PA) for Acts data structure.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def find_and_analyze_sheet3():
    """Find and analyze Sheet 3 of the Suivi Global file."""
    print("📊 Analyzing Sheet 3 (Traitement PA) for Acts Data")
    print("=" * 70)
    
    try:
        from config.constants import TeamsConfig
        
        # Get the Teams folder path
        teams_folder_path = TeamsConfig.get_global_teams_path()
        global_excel_filename = "Suivis Global Tickets CMS Adr_PA.xlsx"
        
        global_file_path = os.path.join(teams_folder_path, global_excel_filename)
        
        print(f"📁 Teams folder: {teams_folder_path}")
        print(f"📄 Looking for: {global_excel_filename}")
        
        if not os.path.exists(global_file_path):
            print(f"❌ Suivi Global file not found at: {global_file_path}")
            return False
        
        print(f"✅ Found Suivi Global file: {global_file_path}")
        
        # Read all sheets to find Sheet 3
        import pandas as pd
        print("\n📖 Reading Excel file to identify sheets...")
        
        # Get sheet names
        excel_file = pd.ExcelFile(global_file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"📋 Available sheets ({len(sheet_names)} total):")
        for i, sheet_name in enumerate(sheet_names):
            print(f"   {i+1}. '{sheet_name}'")
        
        # Try to find Sheet 3 (third sheet)
        if len(sheet_names) < 3:
            print(f"\n⚠️ Warning: Expected at least 3 sheets, found {len(sheet_names)}")
            return False
        
        sheet3_name = sheet_names[2]  # Third sheet (index 2)
        print(f"\n🎯 Analyzing Sheet 3: '{sheet3_name}'")
        
        # Read Sheet 3
        df_acts = pd.read_excel(global_file_path, sheet_name=sheet3_name, date_format=None)
        
        print(f"✅ Sheet 3 loaded: {len(df_acts)} rows, {len(df_acts.columns)} columns")
        print(f"📋 Columns ({len(df_acts.columns)} total):")
        for i, col in enumerate(df_acts.columns):
            print(f"   {chr(65+i)} (index {i}): '{col}'")
        
        # Check if we have enough columns
        if len(df_acts.columns) < 8:
            print(f"\n⚠️ Warning: Expected at least 8 columns for Column H, found {len(df_acts.columns)}")
            return False
        
        # Analyze Column D (index 3) - Expected motif
        print(f"\n🎯 Analyzing Column D (index 3): '{df_acts.columns[3]}'")
        col_d_values = df_acts.iloc[:, 3].dropna().value_counts()
        print(f"   Total non-null values: {col_d_values.sum()}")
        print(f"   Unique values: {len(col_d_values)}")
        
        if len(col_d_values) > 0:
            print("   Top motif values:")
            for value, count in col_d_values.head(15).items():
                print(f"     '{value}': {count}")
            
            # Check for Ad Ras patterns
            ad_ras_count = 0
            ad_ras_variations = []
            for value in col_d_values.index:
                value_upper = str(value).upper()
                if 'AD' in value_upper and 'RAS' in value_upper:
                    ad_ras_count += col_d_values[value]
                    ad_ras_variations.append((value, col_d_values[value]))
            
            print(f"\n   🔍 Ad Ras related values: {ad_ras_count}")
            if ad_ras_variations:
                print(f"   Ad Ras variations found:")
                for value, count in ad_ras_variations:
                    print(f"     '{value}': {count}")
        else:
            print("   ❌ No values found in Column D!")
        
        # Analyze Column G (index 6) - Expected processing date
        print(f"\n📅 Analyzing Column G (index 6): '{df_acts.columns[6]}'")
        col_g_values = df_acts.iloc[:, 6].dropna()
        print(f"   Total non-null values: {len(col_g_values)}")
        
        if len(col_g_values) > 0:
            print("   Sample values:")
            for i, value in enumerate(col_g_values.head(5)):
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
            
            for value in col_g_values.head(20):  # Test first 20 values
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
            print("   ❌ No values found in Column G!")
        
        # Analyze Column H (index 7) - Expected duration
        print(f"\n⏱️ Analyzing Column H (index 7): '{df_acts.columns[7]}'")
        col_h_values = df_acts.iloc[:, 7].dropna()
        print(f"   Total non-null values: {len(col_h_values)}")
        
        if len(col_h_values) > 0:
            print("   Sample values:")
            for i, value in enumerate(col_h_values.head(10)):
                print(f"     {i+1}. '{value}' (type: {type(value)})")
            
            # Analyze numeric values
            numeric_values = []
            zero_count = 0
            positive_count = 0
            
            for value in col_h_values:
                try:
                    num_val = float(value)
                    numeric_values.append(num_val)
                    if num_val == 0:
                        zero_count += 1
                    elif num_val > 0:
                        positive_count += 1
                except (ValueError, TypeError):
                    continue
            
            print(f"   Numeric values: {len(numeric_values)}")
            print(f"   Zero values (duration = 0): {zero_count}")
            print(f"   Positive values (duration > 0): {positive_count}")
            
            if len(numeric_values) > 0:
                import statistics
                print(f"   📊 Duration statistics:")
                print(f"      Min: {min(numeric_values)}")
                print(f"      Max: {max(numeric_values)}")
                print(f"      Mean: {statistics.mean(numeric_values):.2f}")
        else:
            print("   ❌ No values found in Column H!")
        
        # Cross-analysis: Ad Ras with duration
        print(f"\n🔄 Cross-analysis: Ad Ras motifs with duration")
        
        if len(col_d_values) > 0 and len(col_h_values) > 0:
            ad_ras_with_time = 0
            ad_ras_without_time = 0
            
            for index, row in df_acts.iterrows():
                motif = row.iloc[3]  # Column D
                duration = row.iloc[7]  # Column H
                
                if (pd.notna(motif) and pd.notna(duration) and 
                    str(motif).strip() != '' and str(duration).strip() != ''):
                    
                    motif_upper = str(motif).upper()
                    if 'AD' in motif_upper and 'RAS' in motif_upper:
                        try:
                            duration_val = float(duration)
                            if duration_val == 0:
                                ad_ras_without_time += 1
                            elif duration_val > 0:
                                ad_ras_with_time += 1
                        except (ValueError, TypeError):
                            continue
            
            print(f"   Ad Ras avec temps (duration > 0): {ad_ras_with_time}")
            print(f"   Ad Ras sans temps (duration = 0): {ad_ras_without_time}")
            print(f"   Total Ad Ras with duration data: {ad_ras_with_time + ad_ras_without_time}")
            
            if ad_ras_with_time + ad_ras_without_time > 0:
                print(f"\n✅ Sheet 3 contains usable Acts data!")
                print(f"💡 Suggested implementation:")
                print(f"   • Extract motifs from Column D")
                print(f"   • Extract processing dates from Column G")
                print(f"   • Extract durations from Column H")
                print(f"   • Special handling for Ad Ras: split by duration (0 vs >0)")
            else:
                print(f"❌ No Ad Ras records with duration data found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing Sheet 3: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main analysis function."""
    success = find_and_analyze_sheet3()
    
    if success:
        print(f"\n✅ Analysis complete!")
        print(f"📝 Use the information above to:")
        print(f"  1. Verify that Column D contains motifs (including Ad Ras variations)")
        print(f"  2. Verify that Column G contains processing dates")
        print(f"  3. Verify that Column H contains duration values")
        print(f"  4. Implement special Ad Ras handling based on duration")
        print(f"  5. Test the acts implementation with real data")
    else:
        print(f"\n❌ Analysis failed - check the file structure")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

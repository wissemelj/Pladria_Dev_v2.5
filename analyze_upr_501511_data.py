#!/usr/bin/env python3
"""
Script to analyze Sheet 1 data structure for UPR and 501/511 tickets sections.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def analyze_sheet1_for_new_sections():
    """Analyze Sheet 1 for UPR and 501/511 tickets data."""
    print("📊 Analyzing Sheet 1 for UPR and 501/511 Tickets Data")
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
        
        # Load Sheet 1
        import pandas as pd
        excel_file = pd.ExcelFile(global_file_path)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) >= 1:
            sheet1_name = sheet_names[0]  # First sheet
            print(f"📊 Loading Sheet 1: '{sheet1_name}'")
            
            df_tickets = pd.read_excel(global_file_path, sheet_name=sheet1_name, date_format=None)
            print(f"   Loaded: {len(df_tickets)} rows, {len(df_tickets.columns)} columns")
            
            # Display all columns for reference
            print(f"\n📋 All columns in Sheet 1:")
            for i, col in enumerate(df_tickets.columns):
                print(f"   {chr(65+i) if i < 26 else f'A{chr(65+i-26)}'} (index {i}): '{col}'")
            
            # Check if we have enough columns
            if len(df_tickets.columns) < 19:
                print(f"\n⚠️ Warning: Expected at least 19 columns for Column S, found {len(df_tickets.columns)}")
                return False
            
            # Analyze Column S (index 18) - UPR motif data
            print(f"\n🎯 Analyzing Column S (index 18) for UPR data:")
            if len(df_tickets.columns) > 18:
                col_s_name = df_tickets.columns[18]
                print(f"   Column name: '{col_s_name}'")
                
                col_s_values = df_tickets.iloc[:, 18].dropna().value_counts()
                print(f"   Total non-null values: {col_s_values.sum()}")
                print(f"   Unique values: {len(col_s_values)}")
                
                if len(col_s_values) > 0:
                    print("   Top values:")
                    for value, count in col_s_values.head(15).items():
                        print(f"     '{value}': {count}")
                    
                    # Look for UPR patterns
                    upr_count = 0
                    upr_variations = []
                    for value in col_s_values.index:
                        value_upper = str(value).upper()
                        if 'UPR' in value_upper:
                            upr_count += col_s_values[value]
                            upr_variations.append((value, col_s_values[value]))
                    
                    print(f"\n   🔍 UPR related values: {upr_count}")
                    if upr_variations:
                        print(f"   UPR variations found:")
                        for value, count in upr_variations:
                            print(f"     '{value}': {count}")
                else:
                    print("   ❌ No values found in Column S!")
            else:
                print("   ❌ Column S (index 18) not available")
            
            # Analyze Column R (index 17) - 501/511 deposit dates
            print(f"\n📅 Analyzing Column R (index 17) for 501/511 data:")
            if len(df_tickets.columns) > 17:
                col_r_name = df_tickets.columns[17]
                print(f"   Column name: '{col_r_name}'")
                
                col_r_values = df_tickets.iloc[:, 17].dropna()
                print(f"   Total non-null values: {len(col_r_values)}")
                
                if len(col_r_values) > 0:
                    print("   Sample values:")
                    for i, value in enumerate(col_r_values.head(10)):
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
                    
                    for value in col_r_values.head(20):  # Test first 20 values
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
                    print("   ❌ No values found in Column R!")
            else:
                print("   ❌ Column R (index 17) not available")
            
            # Verify Column O (index 14) - Delivery dates (already used for Communes)
            print(f"\n📅 Verifying Column O (index 14) for delivery dates:")
            col_o_name = df_tickets.columns[14]
            print(f"   Column name: '{col_o_name}'")
            
            col_o_values = df_tickets.iloc[:, 14].dropna()
            print(f"   Total non-null values: {len(col_o_values)}")
            
            if len(col_o_values) > 0:
                print("   Sample delivery dates:")
                for i, value in enumerate(col_o_values.head(5)):
                    print(f"     {i+1}. '{value}' (type: {type(value)})")
            
            # Cross-analysis for UPR tickets with delivery dates
            print(f"\n🔄 Cross-analysis: UPR tickets with delivery dates")
            
            if len(df_tickets.columns) > 18:
                upr_with_delivery = 0
                total_with_both = 0
                
                for index, row in df_tickets.iterrows():
                    upr_motif = row.iloc[18] if len(df_tickets.columns) > 18 else None  # Column S
                    delivery_date = row.iloc[14]  # Column O
                    
                    if (pd.notna(upr_motif) and pd.notna(delivery_date) and 
                        str(upr_motif).strip() != '' and str(delivery_date).strip() != ''):
                        
                        total_with_both += 1
                        upr_motif_upper = str(upr_motif).upper()
                        if 'UPR' in upr_motif_upper:
                            upr_with_delivery += 1
                
                print(f"   Records with both UPR motif and delivery date: {total_with_both}")
                print(f"   UPR tickets with delivery dates: {upr_with_delivery}")
            
            # Cross-analysis for 501/511 tickets
            print(f"\n🔄 Cross-analysis: 501/511 tickets")
            
            if len(df_tickets.columns) > 17:
                tickets_501511_count = 0
                
                for index, row in df_tickets.iterrows():
                    deposit_date = row.iloc[17] if len(df_tickets.columns) > 17 else None  # Column R
                    
                    if (pd.notna(deposit_date) and str(deposit_date).strip() != ''):
                        tickets_501511_count += 1
                
                print(f"   Total 501/511 tickets with deposit dates: {tickets_501511_count}")
            
            print(f"\n✅ Sheet 1 analysis complete!")
            print(f"💡 Implementation suggestions:")
            print(f"   • UPR tickets: Extract from Column S, filter by Column O dates")
            print(f"   • 501/511 tickets: Extract from Column R dates")
            print(f"   • Both sections can use the same date filtering logic")
            print(f"   • UPR section may need motif categorization like Acts section")
            
            return True
            
        else:
            print(f"❌ Sheet 1 not found")
            return False
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main analysis function."""
    print("🚀 Analysis of UPR and 501/511 Tickets Data Structure")
    print("=" * 80)
    
    if analyze_sheet1_for_new_sections():
        print(f"\n📝 Next steps:")
        print(f"  1. Implement _extract_upr_data_for_dashboard() method")
        print(f"  2. Implement _extract_501511_data_for_dashboard() method")
        print(f"  3. Update dashboard mapping and HTML/script.js updates")
        print(f"  4. Add data validation for both new sections")
        print(f"  5. Test with real data to verify implementation")
        
        return True
    else:
        print(f"\n❌ Analysis failed - check the file structure")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

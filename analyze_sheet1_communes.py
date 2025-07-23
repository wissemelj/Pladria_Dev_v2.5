#!/usr/bin/env python3
"""
Script to analyze Sheet 1 (Suivi Tickets) for communes data structure.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def find_and_analyze_sheet1():
    """Find and analyze Sheet 1 of the Suivi Global file."""
    print("📊 Analyzing Sheet 1 (Suivi Tickets) for Communes Data")
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
        
        # Read Sheet 1
        import pandas as pd
        print("\n📖 Reading Sheet 1 (Suivi Tickets)...")
        df_tickets = pd.read_excel(global_file_path, sheet_name='Suivi Tickets', date_format=None)
        
        print(f"✅ Sheet 1 loaded: {len(df_tickets)} rows, {len(df_tickets.columns)} columns")
        print(f"📋 Columns ({len(df_tickets.columns)} total):")
        for i, col in enumerate(df_tickets.columns):
            print(f"   {chr(65+i)} (index {i}): '{col}'")
        
        # Check if we have enough columns
        if len(df_tickets.columns) < 15:
            print(f"\n⚠️ Warning: Expected at least 15 columns for Column O, found {len(df_tickets.columns)}")
            return False
        
        # Analyze Column D (index 3) - Expected commune type
        print(f"\n🎯 Analyzing Column D (index 3): '{df_tickets.columns[3]}'")
        col_d_values = df_tickets.iloc[:, 3].dropna().value_counts()
        print(f"   Total non-null values: {col_d_values.sum()}")
        print(f"   Unique values: {len(col_d_values)}")
        
        if len(col_d_values) > 0:
            print("   Top values:")
            for value, count in col_d_values.head(10).items():
                print(f"     '{value}': {count}")
            
            # Check for Orange/RIP
            orange_count = 0
            rip_count = 0
            for value in col_d_values.index:
                value_upper = str(value).upper()
                if 'ORANGE' in value_upper:
                    orange_count += col_d_values[value]
                elif 'RIP' in value_upper:
                    rip_count += col_d_values[value]
            
            print(f"\n   🔍 Orange-related values: {orange_count}")
            print(f"   🔍 RIP-related values: {rip_count}")
        else:
            print("   ❌ No values found in Column D!")
        
        # Analyze Column O (index 14) - Expected delivery date
        print(f"\n📅 Analyzing Column O (index 14): '{df_tickets.columns[14]}'")
        col_o_values = df_tickets.iloc[:, 14].dropna()
        print(f"   Total non-null values: {len(col_o_values)}")
        
        if len(col_o_values) > 0:
            print("   Sample values:")
            for i, value in enumerate(col_o_values.head(5)):
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
            
            for value in col_o_values.head(20):  # Test first 20 values
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
                
                # Show date distribution
                from collections import defaultdict
                date_counts = defaultdict(int)
                
                for date_obj in valid_dates:
                    year_month = f"{date_obj.year}-{date_obj.month:02d}"
                    date_counts[year_month] += 1
                
                print(f"   📊 Date distribution by month:")
                for year_month in sorted(date_counts.keys()):
                    count = date_counts[year_month]
                    print(f"     {year_month}: {count} records")
            else:
                print("   ❌ No valid dates could be parsed!")
        else:
            print("   ❌ No values found in Column O!")
        
        # Cross-analysis: Communes with dates
        print(f"\n🔄 Cross-analysis: Communes with valid delivery dates")
        
        if len(col_d_values) > 0 and len(col_o_values) > 0:
            # Count records that have both commune type and delivery date
            both_valid = 0
            orange_with_date = 0
            rip_with_date = 0
            
            for index, row in df_tickets.iterrows():
                commune_type = row.iloc[3]  # Column D
                delivery_date = row.iloc[14]  # Column O
                
                if (pd.notna(commune_type) and pd.notna(delivery_date) and 
                    str(commune_type).strip() != '' and str(delivery_date).strip() != ''):
                    
                    both_valid += 1
                    commune_type_upper = str(commune_type).upper()
                    
                    if 'ORANGE' in commune_type_upper:
                        orange_with_date += 1
                    elif 'RIP' in commune_type_upper:
                        rip_with_date += 1
            
            print(f"   Records with both commune type and delivery date: {both_valid}")
            print(f"   Orange communes with dates: {orange_with_date}")
            print(f"   RIP communes with dates: {rip_with_date}")
            
            if both_valid > 0:
                print(f"\n✅ Sheet 1 contains usable communes data!")
                print(f"💡 Suggested date range for testing:")
                if len(valid_dates) > 0:
                    print(f"   From: {min_date}")
                    print(f"   To:   {max_date}")
                    print(f"   Expected Orange communes: ~{orange_with_date}")
                    print(f"   Expected RIP communes: ~{rip_with_date}")
            else:
                print(f"❌ No records with both commune type and delivery date found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing Sheet 1: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main analysis function."""
    success = find_and_analyze_sheet1()
    
    if success:
        print(f"\n✅ Analysis complete!")
        print(f"📝 Use the information above to:")
        print(f"  1. Verify that Column D contains commune types (Orange/RIP)")
        print(f"  2. Verify that Column O contains delivery dates")
        print(f"  3. Use the suggested date range for testing")
        print(f"  4. Test the communes implementation with real data")
    else:
        print(f"\n❌ Analysis failed - check the file structure")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

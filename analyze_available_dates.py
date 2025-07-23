#!/usr/bin/env python3
"""
Script to analyze available dates in the Suivi Global file to help select a valid date range.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def find_suivi_global_file():
    """Find the Suivi Global Excel file."""
    print("🔍 Looking for Suivi Global Excel file...")
    
    try:
        from config.constants import TeamsConfig
        
        # Get the Teams folder path
        teams_folder_path = TeamsConfig.get_global_teams_path()
        global_excel_filename = "Suivis Global Tickets CMS Adr_PA.xlsx"
        
        global_file_path = os.path.join(teams_folder_path, global_excel_filename)
        
        print(f"📁 Teams folder: {teams_folder_path}")
        print(f"📄 Looking for: {global_excel_filename}")
        
        if os.path.exists(global_file_path):
            print(f"✅ Found Suivi Global file: {global_file_path}")
            return global_file_path
        else:
            print(f"❌ Suivi Global file not found at: {global_file_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error finding Suivi Global file: {e}")
        return None

def analyze_sheet2_dates(file_path):
    """Analyze dates in Sheet 2 (Traitement CMS Adr)."""
    print(f"\n📊 Analyzing Sheet 2 dates in: {file_path}")
    
    try:
        # Import pandas directly
        import pandas as pd
        
        # Read Sheet 2
        print("📖 Reading Sheet 2 (Traitement CMS Adr)...")
        df_cms = pd.read_excel(file_path, sheet_name='Traitement CMS Adr', date_format=None)
        
        print(f"✅ Sheet 2 loaded: {len(df_cms)} rows, {len(df_cms.columns)} columns")
        print(f"📋 Columns: {list(df_cms.columns)}")
        
        # Check if we have the expected columns
        if len(df_cms.columns) < 8:
            print(f"⚠️ Warning: Expected at least 8 columns, found {len(df_cms.columns)}")
            return False
        
        # Column D (index 3) - Motif Voie
        motif_column = df_cms.columns[3]
        print(f"📍 Column D (Motif): '{motif_column}'")
        
        # Column H (index 7) - Date livraison
        if len(df_cms.columns) > 7:
            date_column = df_cms.columns[7]
            print(f"📍 Column H (Date): '{date_column}'")
        else:
            # Fallback to Column G
            date_column = df_cms.columns[6]
            print(f"📍 Column G (Date fallback): '{date_column}'")
        
        # Analyze motifs
        print(f"\n🎯 Analyzing motifs in column '{motif_column}':")
        motif_counts = df_cms[motif_column].value_counts()
        print(f"   Total non-null motifs: {motif_counts.sum()}")
        print(f"   Unique motifs: {len(motif_counts)}")
        
        if len(motif_counts) > 0:
            print("   Top motifs:")
            for motif, count in motif_counts.head(10).items():
                print(f"     {motif}: {count}")
        else:
            print("   ❌ No motifs found!")
        
        # Analyze dates
        print(f"\n📅 Analyzing dates in column '{date_column}':")
        
        # Get non-null dates
        dates_series = df_cms[date_column].dropna()
        print(f"   Total non-null dates: {len(dates_series)}")
        
        if len(dates_series) == 0:
            print("   ❌ No dates found!")
            return False
        
        # Try to parse dates
        valid_dates = []
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
        
        for idx, date_value in dates_series.items():
            if pd.isna(date_value) or str(date_value).strip() == '':
                continue
                
            # Try parsing with different formats
            parsed_date = None
            for date_format in date_formats:
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(str(date_value), date_format).date()
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
            
            # Show date distribution by year/month
            from collections import defaultdict
            date_counts = defaultdict(int)
            
            for date_obj in valid_dates:
                year_month = f"{date_obj.year}-{date_obj.month:02d}"
                date_counts[year_month] += 1
            
            print(f"   📊 Date distribution by month:")
            for year_month in sorted(date_counts.keys()):
                count = date_counts[year_month]
                print(f"     {year_month}: {count} records")
            
            # Suggest good date ranges
            print(f"\n💡 Suggested date ranges for testing:")
            
            # Get months with most data
            sorted_months = sorted(date_counts.items(), key=lambda x: x[1], reverse=True)
            
            for i, (year_month, count) in enumerate(sorted_months[:3]):
                year, month = year_month.split('-')
                print(f"   {i+1}. {year}-{month}-01 to {year}-{month}-31 ({count} records)")
            
            return True
        else:
            print("   ❌ No valid dates could be parsed!")
            return False
        
    except Exception as e:
        print(f"❌ Error analyzing Sheet 2: {e}")
        import traceback
        traceback.print_exc()
        return False

def provide_recommendations():
    """Provide recommendations based on analysis."""
    print(f"\n🎯 Recommendations:")
    print(f"1. ✅ Use one of the suggested date ranges above")
    print(f"2. ✅ Make sure the date range contains actual data")
    print(f"3. ✅ Check that Column D has motif values (RAF, MODIF, CREA, etc.)")
    print(f"4. ✅ Verify that Column H has delivery dates")
    print(f"5. ✅ Try a broader date range if specific dates don't work")
    
    print(f"\n📝 Steps to fix the CM display issue:")
    print(f"1. Load the Suivi Global data in the application")
    print(f"2. Select a date range from the suggestions above")
    print(f"3. Click 'Generate and open index'")
    print(f"4. The CM chart should now show real data instead of [0, 0, 0]")

def main():
    """Main analysis function."""
    print("📊 Analyzing Available Dates in Suivi Global File")
    print("=" * 70)
    
    # Find the file
    file_path = find_suivi_global_file()
    if not file_path:
        print("\n❌ Cannot proceed without Suivi Global file")
        print("💡 Make sure the 'Suivi Global Tickets' module has been run at least once")
        return False
    
    # Analyze Sheet 2
    success = analyze_sheet2_dates(file_path)
    
    if success:
        provide_recommendations()
        print("\n✅ Analysis complete - use the suggested date ranges!")
    else:
        print("\n❌ Analysis failed - check the file structure")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

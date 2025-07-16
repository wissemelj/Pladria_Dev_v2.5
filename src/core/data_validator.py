"""
Data validation and cleaning module.
Handles data validation, filtering, and cleaning operations.
"""

import logging
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.lazy_imports import get_pandas
from config.constants import VALIDATION_LISTS, FileConfig


class DataValidator:
    """Handles data validation and cleaning operations."""
    
    def __init__(self):
        """Initialize the data validator."""
        self.logger = logging.getLogger(__name__)
    
    def validate_required_fields(self, data: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Validate required fields are not empty.
        
        Args:
            data: Dictionary of field names and values
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        required_fields = ['domaine', 'nom_commune', 'id_tache', 'insee']
        
        for field in required_fields:
            value = data.get(field, '').strip()
            if not value:
                errors.append(f"Field '{field}' is required")
        
        # Validate INSEE format
        insee = data.get('insee', '').strip()
        if insee and not self._is_valid_insee(insee):
            errors.append("INSEE code must be 5 digits")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def clean_qgis_data(self, df: 'pd.DataFrame', has_column_u: bool = False) -> 'pd.DataFrame':
        """
        Clean and process QGis data.
        
        Args:
            df: Raw QGis DataFrame
            has_column_u: Whether the DataFrame has column U
            
        Returns:
            Cleaned DataFrame
        """
        pd = get_pandas()
        
        try:
            # Rename columns according to specification
            if has_column_u:
                df.columns = FileConfig.PLAN_ADRESSAGE_COLUMNS_WITH_U
            else:
                df.columns = FileConfig.PLAN_ADRESSAGE_COLUMNS
            
            # Reorganize columns
            df = self._reorganize_plan_adressage_columns(df, has_column_u)
            
            # Add new fields
            num_rows = len(df)
            if has_column_u:
                df['Collaborateur'] = [''] * num_rows
                df['Date traitement'] = [''] * num_rows
                df['Durée'] = [''] * num_rows
            else:
                df['Collaborateur'] = [''] * num_rows
                df['Date traitement'] = [''] * num_rows
                df['Durée'] = [''] * num_rows
            
            # Filter data according to business rules
            df = self._filter_plan_adressage_data(df)
            
            self.logger.info(f"QGis data cleaned: {len(df)} rows remaining")
            return df
            
        except Exception as e:
            self.logger.error(f"Error cleaning QGis data: {e}")
            raise
    
    def prepare_moai_data(self, df: 'pd.DataFrame') -> Dict[str, Any]:
        """
        Extract and prepare data from MOAI DataFrame.
        
        Args:
            df: MOAI DataFrame
            
        Returns:
            Dictionary with extracted data
        """
        try:
            # Extract ID tasks (column A)
            id_taches = df.iloc[:, 0] if len(df.columns) > 0 else []
            
            # Extract requested roads (column G)
            voies_demandees = df.iloc[:, 6] if len(df.columns) > 6 else []
            
            # Find locality column
            localite_col = self._find_locality_column(df)
            communes_moai = df[localite_col] if localite_col else []
            
            return {
                'id_taches': id_taches,
                'voies_demandees': voies_demandees,
                'communes_moai': communes_moai,
                'num_rows': len(df)
            }
            
        except Exception as e:
            self.logger.error(f"Error preparing MOAI data: {e}")
            raise
    
    def _reorganize_plan_adressage_columns(self, df: 'pd.DataFrame', has_column_u: bool) -> 'pd.DataFrame':
        """
        Reorganize Plan Adressage columns according to specification.
        
        Args:
            df: DataFrame to reorganize
            has_column_u: Whether DataFrame has column U
            
        Returns:
            Reorganized DataFrame
        """
        if has_column_u:
            column_order = [
                'Num Dossier Site',      # A
                'Num Voie Site',         # B
                'Comp Voie Site',        # C
                'Batiment IMB',          # D (moved from G)
                'Libelle Voie Site',     # E (was D)
                'Même Adresse',          # F (moved from O)
                'Motif',                 # G (was J)
                'Numero Voie BAN',       # H (was P)
                'Repondant Voie BAN',    # I (was Q)
                'Libelle Voie BAN',      # J (was R)
                'Adresse BAN'            # K (was U)
            ]
        else:
            column_order = [
                'Num Dossier Site',      # A
                'Num Voie Site',         # B
                'Comp Voie Site',        # C
                'Batiment IMB',          # D (moved from G)
                'Libelle Voie Site',     # E (was D)
                'Même Adresse',          # F (moved from O)
                'Motif',                 # G (was J)
                'Numero Voie BAN',       # H (was P)
                'Repondant Voie BAN',    # I (was Q)
                'Libelle Voie BAN'       # J (was R)
            ]
        
        return df[column_order]
    
    def _filter_plan_adressage_data(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """
        Filter Plan Adressage data according to business rules.
        
        Excludes rows that have "à analyser" in Motif AND have columns A, P, Q, R all empty.
        
        Args:
            df: DataFrame to filter
            
        Returns:
            Filtered DataFrame
        """
        try:
            # Condition for exclusion
            condition_exclusion = (
                # Check if Motif contains "à analyser" (case insensitive)
                (df['Motif'].astype(str).str.lower().str.contains('à analyser', na=False)) &
                # AND check that columns A, P, Q, R are all empty
                (
                    (df['Num Dossier Site'].isna() | (df['Num Dossier Site'].astype(str).str.strip() == '')) &
                    (df['Numero Voie BAN'].isna() | (df['Numero Voie BAN'].astype(str).str.strip() == '')) &
                    (df['Repondant Voie BAN'].isna() | (df['Repondant Voie BAN'].astype(str).str.strip() == '')) &
                    (df['Libelle Voie BAN'].isna() | (df['Libelle Voie BAN'].astype(str).str.strip() == ''))
                )
            )
            
            # Keep all rows EXCEPT those that match the exclusion condition
            filtered_df = df[~condition_exclusion]
            
            excluded_count = len(df) - len(filtered_df)
            if excluded_count > 0:
                self.logger.info(f"Filtered out {excluded_count} rows with 'à analyser' and empty key columns")
            
            return filtered_df
            
        except Exception as e:
            self.logger.error(f"Error filtering Plan Adressage data: {e}")
            return df  # Return original data if filtering fails
    
    def _find_locality_column(self, df: 'pd.DataFrame') -> Optional[str]:
        """
        Find the locality column in MOAI data.
        
        Args:
            df: MOAI DataFrame
            
        Returns:
            Column name if found, None otherwise
        """
        for col in df.columns:
            col_str = str(col).lower()
            if 'localité' in col_str and 'demande' in col_str:
                return col
        return None
    
    def _is_valid_insee(self, insee_code: str) -> bool:
        """
        Validate INSEE code format.
        
        Args:
            insee_code: INSEE code to validate
            
        Returns:
            True if valid, False otherwise
        """
        return insee_code.isdigit() and len(insee_code) == 5
    
    def get_validation_list(self, list_name: str) -> List[str]:
        """
        Get validation list by name.
        
        Args:
            list_name: Name of the validation list
            
        Returns:
            List of valid values
        """
        return VALIDATION_LISTS.get(list_name, [])

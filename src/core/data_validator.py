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
    
    def validate_dashboard_injection_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data before injecting into dashboard HTML.

        Args:
            data: Dictionary containing dashboard data to validate
                  Expected format: {
                      'cm': {'data': [raf, modif, crea], 'total_records': int, 'motif_breakdown': dict},
                      'communes': {'data': [orange, rip], 'total_records': int, 'commune_breakdown': dict}
                  }

        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []

        try:
            # Validate CM data
            if 'cm' in data:
                cm_validation = self._validate_cm_data(data['cm'])
                errors.extend(cm_validation['errors'])
                warnings.extend(cm_validation['warnings'])

            # Validate Communes data
            if 'communes' in data:
                communes_validation = self._validate_communes_data(data['communes'])
                errors.extend(communes_validation['errors'])
                warnings.extend(communes_validation['warnings'])

            # Validate Acts data
            if 'acts' in data:
                acts_validation = self._validate_acts_data(data['acts'])
                errors.extend(acts_validation['errors'])
                warnings.extend(acts_validation['warnings'])

            # Validate UPR data
            if 'upr' in data:
                upr_validation = self._validate_upr_data(data['upr'])
                errors.extend(upr_validation['errors'])
                warnings.extend(upr_validation['warnings'])

            # Validate 501/511 tickets data
            if 'tickets_501511' in data:
                tickets_501511_validation = self._validate_tickets_501511_data(data['tickets_501511'])
                errors.extend(tickets_501511_validation['errors'])
                warnings.extend(tickets_501511_validation['warnings'])

            # Validate RIP data
            if 'rip' in data:
                rip_validation = self._validate_rip_data(data['rip'])
                errors.extend(rip_validation['errors'])
                warnings.extend(rip_validation['warnings'])

            # Cross-validation checks
            cross_validation = self._validate_cross_section_data(data)
            errors.extend(cross_validation['errors'])
            warnings.extend(cross_validation['warnings'])

            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'data_summary': self._generate_data_summary(data)
            }

        except Exception as e:
            self.logger.error(f"Error validating dashboard injection data: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'data_summary': {}
            }

    def _validate_cm_data(self, cm_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate CM section data."""
        errors = []
        warnings = []

        # Check data array structure
        if 'data' not in cm_data:
            errors.append("CM data missing 'data' array")
        else:
            data_array = cm_data['data']

            # Must have exactly 3 values (RAF, MODIF, CREA)
            if not isinstance(data_array, list) or len(data_array) != 3:
                errors.append("CM data array must contain exactly 3 values [RAF, MODIF, CREA]")
            else:
                # Validate each value
                for i, value in enumerate(data_array):
                    category_names = ['RAF', 'MODIF', 'CREA']
                    if not isinstance(value, (int, float)):
                        errors.append(f"CM {category_names[i]} value must be a number")
                    elif value < 0:
                        errors.append(f"CM {category_names[i]} value cannot be negative")
                    elif value == 0:
                        warnings.append(f"CM {category_names[i]} value is zero - check if this is expected")

        # Check total records
        if 'total_records' in cm_data:
            total_records = cm_data['total_records']
            if not isinstance(total_records, int) or total_records < 0:
                errors.append("CM total_records must be a non-negative integer")
            elif total_records == 0:
                warnings.append("CM total_records is zero - no data was processed")

        # Check motif breakdown
        if 'motif_breakdown' in cm_data:
            motif_breakdown = cm_data['motif_breakdown']
            if not isinstance(motif_breakdown, dict):
                errors.append("CM motif_breakdown must be a dictionary")
            elif len(motif_breakdown) == 0:
                warnings.append("CM motif_breakdown is empty")

        return {'errors': errors, 'warnings': warnings}

    def _validate_communes_data(self, communes_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate Communes section data."""
        errors = []
        warnings = []

        # Check data array structure
        if 'data' not in communes_data:
            errors.append("Communes data missing 'data' array")
        else:
            data_array = communes_data['data']

            # Must have exactly 2 values (Orange, RIP)
            if not isinstance(data_array, list) or len(data_array) != 2:
                errors.append("Communes data array must contain exactly 2 values [Orange, RIP]")
            else:
                # Validate each value
                for i, value in enumerate(data_array):
                    category_names = ['Orange', 'RIP']
                    if not isinstance(value, (int, float)):
                        errors.append(f"Communes {category_names[i]} value must be a number")
                    elif value < 0:
                        errors.append(f"Communes {category_names[i]} value cannot be negative")
                    elif value == 0:
                        warnings.append(f"Communes {category_names[i]} value is zero - check if this is expected")

        # Check total records
        if 'total_records' in communes_data:
            total_records = communes_data['total_records']
            if not isinstance(total_records, int) or total_records < 0:
                errors.append("Communes total_records must be a non-negative integer")
            elif total_records == 0:
                warnings.append("Communes total_records is zero - no data was processed")

        # Check commune breakdown
        if 'commune_breakdown' in communes_data:
            commune_breakdown = communes_data['commune_breakdown']
            if not isinstance(commune_breakdown, dict):
                errors.append("Communes commune_breakdown must be a dictionary")
            elif len(commune_breakdown) == 0:
                warnings.append("Communes commune_breakdown is empty")

        return {'errors': errors, 'warnings': warnings}

    def _validate_acts_data(self, acts_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate Acts section data."""
        errors = []
        warnings = []

        # Check data array structure
        if 'data' not in acts_data:
            errors.append("Acts data missing 'data' array")
        else:
            data_array = acts_data['data']

            # Must have at least 1 value (flexible number of categories)
            if not isinstance(data_array, list) or len(data_array) < 1:
                errors.append("Acts data array must contain at least 1 value")
            else:
                # Validate each value
                for i, value in enumerate(data_array):
                    if not isinstance(value, (int, float)):
                        errors.append(f"Acts data value {i+1} must be a number")
                    elif value < 0:
                        errors.append(f"Acts data value {i+1} cannot be negative")
                    elif value == 0:
                        warnings.append(f"Acts data value {i+1} is zero - check if this is expected")

        # Check labels array structure
        if 'labels' not in acts_data:
            errors.append("Acts data missing 'labels' array")
        else:
            labels_array = acts_data['labels']

            if not isinstance(labels_array, list):
                errors.append("Acts labels must be a list")
            elif len(labels_array) == 0:
                errors.append("Acts labels array cannot be empty")
            else:
                # Check that data and labels arrays have same length
                if 'data' in acts_data and isinstance(acts_data['data'], list):
                    if len(labels_array) != len(acts_data['data']):
                        errors.append(f"Acts labels ({len(labels_array)}) and data ({len(acts_data['data'])}) arrays must have same length")

        # Check total records
        if 'total_records' in acts_data:
            total_records = acts_data['total_records']
            if not isinstance(total_records, int) or total_records < 0:
                errors.append("Acts total_records must be a non-negative integer")
            elif total_records == 0:
                warnings.append("Acts total_records is zero - no data was processed")

        # Check motif breakdown
        if 'motif_breakdown' in acts_data:
            motif_breakdown = acts_data['motif_breakdown']
            if not isinstance(motif_breakdown, dict):
                errors.append("Acts motif_breakdown must be a dictionary")
            elif len(motif_breakdown) == 0:
                warnings.append("Acts motif_breakdown is empty")

        return {'errors': errors, 'warnings': warnings}

    def _validate_upr_data(self, upr_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate UPR tickets section data."""
        errors = []
        warnings = []

        # Check data array structure
        if 'data' not in upr_data:
            errors.append("UPR data missing 'data' array")
        else:
            data_array = upr_data['data']

            # Must have exactly 2 values (Créé, Non)
            if not isinstance(data_array, list) or len(data_array) != 2:
                errors.append("UPR data array must contain exactly 2 values [Créé, Non]")
            else:
                # Validate each value
                for i, value in enumerate(data_array):
                    category_names = ['Créé', 'Non']
                    if not isinstance(value, (int, float)):
                        errors.append(f"UPR {category_names[i]} value must be a number")
                    elif value < 0:
                        errors.append(f"UPR {category_names[i]} value cannot be negative")
                    elif value == 0:
                        warnings.append(f"UPR {category_names[i]} value is zero - check if this is expected")

        # Check labels array structure
        if 'labels' not in upr_data:
            errors.append("UPR data missing 'labels' array")
        else:
            labels_array = upr_data['labels']

            if not isinstance(labels_array, list):
                errors.append("UPR labels must be a list")
            elif len(labels_array) != 2:
                errors.append("UPR labels array must contain exactly 2 values")
            else:
                # Check that data and labels arrays have same length
                if 'data' in upr_data and isinstance(upr_data['data'], list):
                    if len(labels_array) != len(upr_data['data']):
                        errors.append(f"UPR labels ({len(labels_array)}) and data ({len(upr_data['data'])}) arrays must have same length")

        # Check total records
        if 'total_records' in upr_data:
            total_records = upr_data['total_records']
            if not isinstance(total_records, int) or total_records < 0:
                errors.append("UPR total_records must be a non-negative integer")
            elif total_records == 0:
                warnings.append("UPR total_records is zero - no data was processed")

        # Check UPR breakdown
        if 'upr_breakdown' in upr_data:
            upr_breakdown = upr_data['upr_breakdown']
            if not isinstance(upr_breakdown, dict):
                errors.append("UPR upr_breakdown must be a dictionary")
            elif len(upr_breakdown) == 0:
                warnings.append("UPR upr_breakdown is empty")

        return {'errors': errors, 'warnings': warnings}

    def _validate_tickets_501511_data(self, tickets_501511_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate 501/511 tickets section data."""
        errors = []
        warnings = []

        # Check data array structure
        if 'data' not in tickets_501511_data:
            errors.append("501/511 tickets data missing 'data' array")
        else:
            data_array = tickets_501511_data['data']

            # Must have at least 1 value
            if not isinstance(data_array, list) or len(data_array) < 1:
                errors.append("501/511 tickets data array must contain at least 1 value")
            else:
                # Validate each value
                for i, value in enumerate(data_array):
                    if not isinstance(value, (int, float)):
                        errors.append(f"501/511 tickets data value {i+1} must be a number")
                    elif value < 0:
                        errors.append(f"501/511 tickets data value {i+1} cannot be negative")
                    elif value == 0:
                        warnings.append(f"501/511 tickets data value {i+1} is zero - check if this is expected")

        # Check labels array structure
        if 'labels' not in tickets_501511_data:
            errors.append("501/511 tickets data missing 'labels' array")
        else:
            labels_array = tickets_501511_data['labels']

            if not isinstance(labels_array, list):
                errors.append("501/511 tickets labels must be a list")
            elif len(labels_array) == 0:
                errors.append("501/511 tickets labels array cannot be empty")
            else:
                # Check that data and labels arrays have same length
                if 'data' in tickets_501511_data and isinstance(tickets_501511_data['data'], list):
                    if len(labels_array) != len(tickets_501511_data['data']):
                        errors.append(f"501/511 tickets labels ({len(labels_array)}) and data ({len(tickets_501511_data['data'])}) arrays must have same length")

        # Check total records
        if 'total_records' in tickets_501511_data:
            total_records = tickets_501511_data['total_records']
            if not isinstance(total_records, int) or total_records < 0:
                errors.append("501/511 tickets total_records must be a non-negative integer")
            elif total_records == 0:
                warnings.append("501/511 tickets total_records is zero - no data was processed")

        # Check tickets breakdown
        if 'tickets_breakdown' in tickets_501511_data:
            tickets_breakdown = tickets_501511_data['tickets_breakdown']
            if not isinstance(tickets_breakdown, dict):
                errors.append("501/511 tickets tickets_breakdown must be a dictionary")
            elif len(tickets_breakdown) == 0:
                warnings.append("501/511 tickets tickets_breakdown is empty")

        return {'errors': errors, 'warnings': warnings}

    def _validate_rip_data(self, rip_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate RIP (P0 P1) section data."""
        errors = []
        warnings = []

        # Check data array structure
        if 'data' not in rip_data:
            errors.append("RIP data missing 'data' array")
        else:
            data_array = rip_data['data']

            # Must have exactly 3 values (Rien à faire, Modification, Création)
            if not isinstance(data_array, list) or len(data_array) != 3:
                errors.append("RIP data array must contain exactly 3 values [Rien à faire, Modification, Création]")
            else:
                # Validate each value
                for i, value in enumerate(data_array):
                    category_names = ['Rien à faire', 'Modification', 'Création']
                    if not isinstance(value, (int, float)):
                        errors.append(f"RIP {category_names[i]} value must be a number")
                    elif value < 0:
                        errors.append(f"RIP {category_names[i]} value cannot be negative")
                    elif value == 0:
                        warnings.append(f"RIP {category_names[i]} value is zero - check if this is expected")

        # Check labels array structure
        if 'labels' not in rip_data:
            errors.append("RIP data missing 'labels' array")
        else:
            labels_array = rip_data['labels']

            if not isinstance(labels_array, list):
                errors.append("RIP labels must be a list")
            elif len(labels_array) != 3:
                errors.append("RIP labels array must contain exactly 3 values")
            else:
                # Check that data and labels arrays have same length
                if 'data' in rip_data and isinstance(rip_data['data'], list):
                    if len(labels_array) != len(rip_data['data']):
                        errors.append(f"RIP labels ({len(labels_array)}) and data ({len(rip_data['data'])}) arrays must have same length")

                # Check expected labels
                expected_labels = ['Rien à faire', 'Modification', 'Création']
                for i, expected_label in enumerate(expected_labels):
                    if i < len(labels_array) and labels_array[i] != expected_label:
                        warnings.append(f"RIP label {i+1} is '{labels_array[i]}', expected '{expected_label}'")

        # Check total records
        if 'total_records' in rip_data:
            total_records = rip_data['total_records']
            if not isinstance(total_records, int) or total_records < 0:
                errors.append("RIP total_records must be a non-negative integer")
            elif total_records == 0:
                warnings.append("RIP total_records is zero - no P0/P1 data was processed")

        # Check RIP breakdown
        if 'rip_breakdown' in rip_data:
            rip_breakdown = rip_data['rip_breakdown']
            if not isinstance(rip_breakdown, dict):
                errors.append("RIP rip_breakdown must be a dictionary")
            elif len(rip_breakdown) == 0:
                warnings.append("RIP rip_breakdown is empty")

        return {'errors': errors, 'warnings': warnings}

    def _validate_cross_section_data(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate cross-section consistency."""
        errors = []
        warnings = []

        # Check if sections have data
        has_cm = 'cm' in data and 'data' in data['cm']
        has_communes = 'communes' in data and 'data' in data['communes']
        has_acts = 'acts' in data and 'data' in data['acts']
        has_upr = 'upr' in data and 'data' in data['upr']
        has_tickets_501511 = 'tickets_501511' in data and 'data' in data['tickets_501511']
        has_rip = 'rip' in data and 'data' in data['rip']

        sections_with_data = sum([has_cm, has_communes, has_acts, has_upr, has_tickets_501511, has_rip])
        total_sections = 6

        if sections_with_data == 0:
            errors.append("No valid data found for any dashboard section")
        elif sections_with_data < total_sections:
            missing_sections = []
            if not has_cm:
                missing_sections.append("CM")
            if not has_communes:
                missing_sections.append("Communes")
            if not has_acts:
                missing_sections.append("Acts")
            if not has_upr:
                missing_sections.append("UPR")
            if not has_tickets_501511:
                missing_sections.append("501/511 Tickets")
            if not has_rip:
                missing_sections.append("RIP (P0 P1)")

            if len(missing_sections) > 0:
                warnings.append(f"Missing data for sections: {', '.join(missing_sections)} - these will use fallback values")

        # Check data consistency
        if has_cm and has_communes:
            cm_total = sum(data['cm']['data']) if isinstance(data['cm']['data'], list) else 0
            communes_total = sum(data['communes']['data']) if isinstance(data['communes']['data'], list) else 0

            if cm_total == 0 and communes_total == 0:
                warnings.append("Both CM and Communes totals are zero - dashboard will show no activity")
            elif cm_total == 0:
                warnings.append("CM total is zero while Communes has data - check date range or data source")
            elif communes_total == 0:
                warnings.append("Communes total is zero while CM has data - check date range or data source")

        return {'errors': errors, 'warnings': warnings}

    def _generate_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the data for logging."""
        summary = {}

        if 'cm' in data and 'data' in data['cm']:
            cm_data = data['cm']['data']
            summary['cm'] = {
                'values': cm_data,
                'total': sum(cm_data) if isinstance(cm_data, list) else 0,
                'categories': ['RAF', 'MODIF', 'CREA']
            }

        if 'communes' in data and 'data' in data['communes']:
            communes_data = data['communes']['data']
            summary['communes'] = {
                'values': communes_data,
                'total': sum(communes_data) if isinstance(communes_data, list) else 0,
                'categories': ['Orange', 'RIP']
            }

        if 'acts' in data and 'data' in data['acts']:
            acts_data = data['acts']['data']
            acts_labels = data['acts'].get('labels', [])
            summary['acts'] = {
                'values': acts_data,
                'total': sum(acts_data) if isinstance(acts_data, list) else 0,
                'categories': acts_labels,
                'num_categories': len(acts_labels)
            }

        if 'upr' in data and 'data' in data['upr']:
            upr_data = data['upr']['data']
            upr_labels = data['upr'].get('labels', [])
            summary['upr'] = {
                'values': upr_data,
                'total': sum(upr_data) if isinstance(upr_data, list) else 0,
                'categories': upr_labels,
                'num_categories': len(upr_labels)
            }

        if 'tickets_501511' in data and 'data' in data['tickets_501511']:
            tickets_501511_data = data['tickets_501511']['data']
            tickets_501511_labels = data['tickets_501511'].get('labels', [])
            summary['tickets_501511'] = {
                'values': tickets_501511_data,
                'total': sum(tickets_501511_data) if isinstance(tickets_501511_data, list) else 0,
                'categories': tickets_501511_labels,
                'num_categories': len(tickets_501511_labels)
            }

        if 'rip' in data and 'data' in data['rip']:
            rip_data = data['rip']['data']
            rip_labels = data['rip'].get('labels', [])
            summary['rip'] = {
                'values': rip_data,
                'total': sum(rip_data) if isinstance(rip_data, list) else 0,
                'categories': rip_labels,
                'num_categories': len(rip_labels)
            }

        return summary

    def get_validation_list(self, list_name: str) -> List[str]:
        """
        Get validation list by name.

        Args:
            list_name: Name of the validation list

        Returns:
            List of valid values
        """
        return VALIDATION_LISTS.get(list_name, [])

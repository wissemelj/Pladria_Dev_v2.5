"""
File processing module for handling Excel file operations.
Handles reading, parsing, and extracting data from MOAI and QGis files.
"""

import os
import re
import logging
from typing import Optional, Tuple, List, Dict, Any
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.lazy_imports import get_pandas
from config.constants import FileConfig
from utils.performance import timed_operation, optimize_dataframe_memory


class FileProcessor:
    """Handles Excel file processing operations."""

    def __init__(self):
        """Initialize the file processor."""
        self.logger = logging.getLogger(__name__)
        self._file_cache = {}  # Cache for file metadata
        self._data_cache = {}  # Cache for processed data
    
    @timed_operation('file_read')
    def read_moai_file(self, file_path: str) -> 'pd.DataFrame':
        """
        Read and process MOAI Excel file with caching.

        Args:
            file_path: Path to the MOAI Excel file

        Returns:
            DataFrame containing MOAI data

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
            Exception: For other file reading errors
        """
        # Check cache first
        cache_key = f"moai_{file_path}_{os.path.getmtime(file_path)}"
        if cache_key in self._data_cache:
            self.logger.debug(f"Using cached MOAI data for: {os.path.basename(file_path)}")
            return self._data_cache[cache_key]

        self._validate_file_access(file_path)

        try:
            pd = get_pandas()
            # Optimize reading - only read necessary columns if file is large
            df = pd.read_excel(file_path, engine='openpyxl', date_format=None)

            # Optimize memory usage
            df = optimize_dataframe_memory(df)

            # Cache the result
            self._data_cache[cache_key] = df

            self.logger.info(f"MOAI file loaded successfully: {os.path.basename(file_path)} ({len(df)} rows)")
            return df
        except Exception as e:
            self.logger.error(f"Error reading MOAI file: {e}")
            raise
    
    def read_qgis_file(self, file_path: str) -> Tuple['pd.DataFrame', bool]:
        """
        Read and process QGis Excel file with column U detection.
        
        Args:
            file_path: Path to the QGis Excel file
            
        Returns:
            Tuple of (DataFrame, has_column_u)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
            Exception: For other file reading errors
        """
        self._validate_file_access(file_path)
        
        try:
            pd = get_pandas()
            
            # Try to read with column U first
            try:
                df = pd.read_excel(file_path, usecols=FileConfig.QGIS_COLUMNS_WITH_U, date_format=None)
                has_column_u = True
                self.logger.info("QGis file loaded with column U")
            except Exception:
                # Fallback to reading without column U
                df = pd.read_excel(file_path, usecols=FileConfig.QGIS_COLUMNS, date_format=None)
                has_column_u = False
                self.logger.info("QGis file loaded without column U")
            
            self.logger.info(f"QGis file loaded successfully: {os.path.basename(file_path)}")
            return df, has_column_u
            
        except Exception as e:
            self.logger.error(f"Error reading QGis file: {e}")
            raise
    
    def extract_insee_from_filename(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract INSEE code and commune name from MOAI filename.
        
        Expected format: insee_Fiabilisation_voies_nomcommune_date_time_matrice_globale.xlsx
        Example: 09117_Fiabilisation_voies_ESPLAS_20250526_1412_matrice_globale.xlsx
        
        Args:
            file_path: Path to the MOAI file
            
        Returns:
            Tuple of (insee_code, commune_name) or (None, None) if extraction fails
        """
        try:
            filename = os.path.basename(file_path)
            
            if '_' not in filename:
                self.logger.warning("Filename format not recognized for automatic extraction")
                return None, None
            
            parts = filename.split('_')
            
            # Extract INSEE code (first part)
            insee_part = parts[0]
            if not self._is_valid_insee(insee_part):
                self.logger.warning(f"Invalid INSEE code format: {insee_part}")
                return None, None
            
            # Extract commune name (4th part if available)
            commune_name = None
            if len(parts) >= 4:
                commune_name = self._extract_commune_name(parts[3])
            
            self.logger.info(f"Extracted INSEE: {insee_part}, Commune: {commune_name}")
            return insee_part, commune_name
            
        except Exception as e:
            self.logger.error(f"Error extracting INSEE from filename: {e}")
            return None, None
    
    def _validate_file_access(self, file_path: str) -> None:
        """
        Validate file exists and is readable.
        
        Args:
            file_path: Path to validate
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Permission denied: {file_path}")
    
    def _is_valid_insee(self, insee_code: str) -> bool:
        """
        Validate INSEE code format (5 digits).
        
        Args:
            insee_code: INSEE code to validate
            
        Returns:
            True if valid, False otherwise
        """
        return insee_code.isdigit() and len(insee_code) == 5
    
    def _extract_commune_name(self, commune_part: str) -> str:
        """
        Extract and clean commune name from filename part.
        
        Args:
            commune_part: Raw commune part from filename
            
        Returns:
            Cleaned commune name
        """
        # Remove date numbers if they're attached
        commune_clean = re.sub(r'\d{8}.*', '', commune_part)
        return commune_clean.upper() if commune_clean and len(commune_clean) > 1 else ""
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get basic information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            stat = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'exists': True,
                'readable': os.access(file_path, os.R_OK)
            }
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return {
                'name': os.path.basename(file_path) if file_path else '',
                'exists': False,
                'readable': False,
                'error': str(e)
            }

"""
File import section component for the Suivi Generator application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import os
from typing import Callable, Optional, List
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig, FileConfig
from utils.file_utils import validate_file_path, truncate_filename
from ui.styles import create_card_frame, create_section_header

logger = logging.getLogger(__name__)


class FileImportSection:
    """File import section component."""
    
    def __init__(self, parent: tk.Widget, on_file_loaded: Optional[Callable] = None):
        """
        Initialize the file import section.
        
        Args:
            parent: Parent widget
            on_file_loaded: Callback function when a file is loaded
        """
        self.parent = parent
        self.on_file_loaded = on_file_loaded
        self.files = [None, None]  # [MOAI_file, QGis_file]
        self.logger = logging.getLogger(__name__)
        
        # UI elements
        self.moai_button = None
        self.qgis_button = None
        self.moai_label = None
        self.qgis_label = None
        
        self._create_section()
    
    def _create_section(self):
        """Create the file import section UI."""
        # Main card for file import
        files_card = create_card_frame(self.parent)
        files_card.pack(fill=tk.X, pady=(0, 8), padx=3)
        
        # Section header
        header_frame = create_section_header(files_card, "📁", "Import des fichiers")
        header_frame.pack(fill=tk.X, padx=12, pady=(8, 5))
        
        # Content frame
        content_frame = tk.Frame(files_card, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.X, padx=12, pady=(0, 8))
        
        # MOAI section
        self._create_moai_section(content_frame)
        
        # QGis section
        self._create_qgis_section(content_frame)
    
    def _create_moai_section(self, parent: tk.Widget):
        """Create the MOAI file import section."""
        # MOAI section container - Ultra compact
        moai_section = tk.Frame(parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        moai_section.pack(fill=tk.X, pady=(0, 2))  # Ultra minimal spacing

        moai_content = tk.Frame(moai_section, bg=COLORS['LIGHT'])
        moai_content.pack(fill=tk.X, padx=4, pady=3)  # Ultra minimal padding

        # MOAI header - Ultra compact
        moai_header = tk.Frame(moai_content, bg=COLORS['LIGHT'])
        moai_header.pack(fill=tk.X, pady=(0, 1))  # Ultra minimal spacing
        
        tk.Label(
            moai_header,
            text="📊 Export MOAI",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['SECONDARY'],
            bg=COLORS['LIGHT']
        ).pack(side=tk.LEFT)
        
        # MOAI action frame
        moai_action = tk.Frame(moai_content, bg=COLORS['LIGHT'])
        moai_action.pack(fill=tk.X)
        
        # MOAI button
        self.moai_button = ttk.Button(
            moai_action,
            text="Sélectionner",
            command=lambda: self._load_file(0),
            style='Primary.TButton'
        )
        self.moai_button.pack(side=tk.LEFT, padx=(0, 8))
        
        # MOAI status label
        self.moai_label = tk.Label(
            moai_action,
            text="Aucun fichier sélectionné",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['LIGHT']
        )
        self.moai_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _create_qgis_section(self, parent: tk.Widget):
        """Create the QGis file import section."""
        # QGis section container
        qgis_section = tk.Frame(parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        qgis_section.pack(fill=tk.X)
        
        qgis_content = tk.Frame(qgis_section, bg=COLORS['LIGHT'])
        qgis_content.pack(fill=tk.X, padx=8, pady=6)
        
        # QGis header
        qgis_header = tk.Frame(qgis_content, bg=COLORS['LIGHT'])
        qgis_header.pack(fill=tk.X, pady=(0, 3))
        
        tk.Label(
            qgis_header,
            text="🗺️ Résultats QGis",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['SECONDARY'],
            bg=COLORS['LIGHT']
        ).pack(side=tk.LEFT)
        
        # QGis action frame
        qgis_action = tk.Frame(qgis_content, bg=COLORS['LIGHT'])
        qgis_action.pack(fill=tk.X)
        
        # QGis button
        self.qgis_button = ttk.Button(
            qgis_action,
            text="Sélectionner",
            command=lambda: self._load_file(1),
            style='Primary.TButton'
        )
        self.qgis_button.pack(side=tk.LEFT, padx=(0, 8))
        
        # QGis status label
        self.qgis_label = tk.Label(
            qgis_action,
            text="Aucun fichier sélectionné",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['LIGHT']
        )
        self.qgis_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _load_file(self, index: int):
        """
        Load a file and update the UI.
        
        Args:
            index: 0 for MOAI, 1 for QGis
        """
        try:
            # Open file dialog
            file_path = filedialog.askopenfilename(
                title=f"Sélectionner le fichier {'MOAI' if index == 0 else 'QGis'}",
                filetypes=FileConfig.EXCEL_FILETYPES
            )
            
            if not file_path:
                self.logger.info("No file selected")
                return
            
            # Validate file
            validation = validate_file_path(file_path)
            if not validation['valid']:
                error_msg = validation.get('error', 'Unknown error')
                self.logger.error(f"File validation failed: {error_msg}")
                messagebox.showerror("Erreur", f"Erreur avec le fichier:\n{error_msg}")
                return
            
            # Store file path
            self.files[index] = file_path
            filename = os.path.basename(file_path)
            
            # Update UI
            if index == 0:  # MOAI file
                self._update_moai_ui(filename)
            else:  # QGis file
                self._update_qgis_ui(filename)
            
            # Notify parent component
            if self.on_file_loaded:
                self.on_file_loaded(index, file_path)
            
            self.logger.info(f"File loaded successfully: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error loading file: {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue lors du chargement du fichier:\n{e}")
    
    def _update_moai_ui(self, filename: str):
        """Update MOAI UI after file selection."""
        truncated_name = truncate_filename(filename, 50)
        self.moai_label.config(
            text=f"✅ {truncated_name}",
            fg=COLORS['SUCCESS']
        )
        self.moai_button.config(text="✅ MOAI OK")
    
    def _update_qgis_ui(self, filename: str):
        """Update QGis UI after file selection."""
        truncated_name = truncate_filename(filename, 40)
        self.qgis_label.config(
            text=f"✅ {truncated_name}",
            fg=COLORS['SUCCESS']
        )
        self.qgis_button.config(text="✅ QGis OK")
    
    def get_files(self) -> List[Optional[str]]:
        """
        Get the list of loaded files.
        
        Returns:
            List of file paths [MOAI_file, QGis_file]
        """
        return self.files.copy()
    
    def are_all_files_loaded(self) -> bool:
        """
        Check if all required files are loaded.
        
        Returns:
            True if all files are loaded
        """
        return all(self.files)
    
    def reset(self):
        """Reset the file import section to initial state."""
        self.files = [None, None]
        
        # Reset MOAI UI
        self.moai_label.config(
            text="Aucun fichier sélectionné",
            fg=COLORS['INFO']
        )
        self.moai_button.config(text="Sélectionner")
        
        # Reset QGis UI
        self.qgis_label.config(
            text="Aucun fichier sélectionné",
            fg=COLORS['INFO']
        )
        self.qgis_button.config(text="Sélectionner")
        
        self.logger.info("File import section reset")
    
    def get_file_info(self, index: int) -> Optional[dict]:
        """
        Get information about a loaded file.
        
        Args:
            index: File index (0 for MOAI, 1 for QGis)
            
        Returns:
            File information dictionary or None
        """
        if index < 0 or index >= len(self.files) or not self.files[index]:
            return None
        
        file_path = self.files[index]
        validation = validate_file_path(file_path)
        
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'type': 'MOAI' if index == 0 else 'QGis',
            'valid': validation['valid'],
            'size': validation.get('size', 0),
            'exists': validation.get('exists', False),
            'readable': validation.get('readable', False)
        }

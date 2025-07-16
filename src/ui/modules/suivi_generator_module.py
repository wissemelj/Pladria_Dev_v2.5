"""
Suivi Generator module - the original functionality converted to a module.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import logging
import os
from typing import Optional

import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig
from core import FileProcessor, DataValidator, ExcelGenerator
from utils.file_utils import get_icon_path
from utils.lazy_imports import get_PIL
from utils.performance import run_async_task

from ui.styles import StyleManager
from ui.components import (
    FileImportSection, ProjectInfoSection, GenerationSection
)
from ui.keyboard_shortcuts import KeyboardShortcutManager

logger = logging.getLogger(__name__)


class SuiviGeneratorModule:
    """Suivi Generator module containing the original functionality."""
    
    def __init__(self, parent: tk.Widget, navigation_manager=None):
        """
        Initialize the Suivi Generator module.

        Args:
            parent: Parent widget
            navigation_manager: Navigation manager instance
        """
        self.parent = parent
        self.navigation_manager = navigation_manager
        self.logger = logging.getLogger(__name__)

        # Initialize core components
        try:
            self.file_processor = FileProcessor()
            self.data_validator = DataValidator()
            self.excel_generator = ExcelGenerator()
            self.logger.info("Core components initialized")
        except Exception as e:
            self.logger.error(f"Error initializing core components: {e}")
            # Create minimal fallback
            self.file_processor = None
            self.data_validator = None
            self.excel_generator = None

        # UI components
        self.file_import_section = None
        self.project_info_section = None
        self.generation_section = None

        # Data storage
        self.moai_data = None
        self.plan_data = None
        self.has_column_u = False

        # Keyboard shortcuts (optional)
        self.keyboard_manager = None

        # Create UI first
        self._create_module_ui()

        # Initialize optional features after UI is created
        self.parent.after(100, self._initialize_optional_features)

    def _initialize_optional_features(self):
        """Initialize optional features after UI is ready."""
        try:
            # Setup keyboard shortcuts
            if self.navigation_manager and hasattr(self.navigation_manager, 'root'):
                self.keyboard_manager = KeyboardShortcutManager(self.navigation_manager.root)
                self._setup_module_shortcuts()

            self.logger.info("Optional features initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing optional features: {e}")
            # Continue without optional features

    def _create_module_ui(self):
        """Create the module user interface."""
        try:
            # Module title bar
            self._create_title_bar()

            # Main content area
            self._create_content_area()

            self.logger.info("Module UI created successfully")

        except Exception as e:
            self.logger.error(f"Error creating module UI: {e}")
            # Create a simple error display
            self._create_error_ui(str(e))

    def _create_error_ui(self, error_message: str):
        """Create a simple error display when module fails to load."""
        error_frame = tk.Frame(self.parent, bg=COLORS['BG'])
        error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Error icon and message
        error_label = tk.Label(
            error_frame,
            text=f"❌ Erreur lors du chargement du module:\n\n{error_message}",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['DANGER'],
            bg=COLORS['BG'],
            justify=tk.CENTER
        )
        error_label.pack(expand=True)

        # Retry button
        retry_btn = tk.Button(
            error_frame,
            text="🔄 Réessayer",
            command=self._retry_initialization,
            bg=COLORS['PRIMARY'],
            fg='white',
            font=UIConfig.FONT_BUTTON,
            relief='flat',
            padx=20,
            pady=10
        )
        retry_btn.pack(pady=10)

    def _retry_initialization(self):
        """Retry module initialization."""
        try:
            # Clear the parent
            for widget in self.parent.winfo_children():
                widget.destroy()

            # Reinitialize
            self.__init__(self.parent, self.navigation_manager)

        except Exception as e:
            self.logger.error(f"Retry failed: {e}")
            messagebox.showerror("Erreur", f"Impossible de réinitialiser le module:\n{e}")
    
    def _create_title_bar(self):
        """Create the module title bar."""
        title_frame = tk.Frame(self.parent, bg=COLORS['CARD'], height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        # Title content
        title_content = tk.Frame(title_frame, bg=COLORS['CARD'])
        title_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Module icon and title
        title_left = tk.Frame(title_content, bg=COLORS['CARD'])
        title_left.pack(side=tk.LEFT, fill=tk.Y)
        
        # Icon
        icon_label = tk.Label(
            title_left,
            text="📊",
            font=("Segoe UI", 20),
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Title and description
        title_text_frame = tk.Frame(title_left, bg=COLORS['CARD'])
        title_text_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(
            title_text_frame,
            text="Générateur Suivi",
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            title_text_frame,
            text="Traitement MOAI et QGis pour génération Excel",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['CARD']
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Action buttons on the right (help button removed)
        title_right = tk.Frame(title_content, bg=COLORS['CARD'])
        title_right.pack(side=tk.RIGHT, fill=tk.Y)


    
    def _create_content_area(self):
        """Create the main content area with two columns."""
        # Content container - Maximum compact
        content_container = tk.Frame(self.parent, bg=COLORS['BG'])
        content_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Reduced from 10 for compactness
        
        # Configure columns
        content_container.grid_columnconfigure(0, weight=1, minsize=280)  # Left column
        content_container.grid_columnconfigure(1, weight=1, minsize=280)  # Right column
        
        # Left column - File import - Maximum compact
        left_column = tk.Frame(content_container, bg=COLORS['BG'])
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 2))  # Reduced from 5 for compactness

        # Right column - Project info and generation - Maximum compact
        right_column = tk.Frame(content_container, bg=COLORS['BG'])
        right_column.grid(row=0, column=1, sticky="nsew", padx=(2, 0))  # Reduced from 5 for compactness
        
        # Create sections
        self.file_import_section = FileImportSection(
            left_column, 
            on_file_loaded=self._on_file_loaded
        )
        
        self.project_info_section = ProjectInfoSection(
            right_column,
            on_data_changed=self._on_project_data_changed
        )
        
        self.generation_section = GenerationSection(
            right_column,
            on_generate=self._on_generate_excel
        )
    
    def _setup_module_shortcuts(self):
        """Set up keyboard shortcuts specific to this module."""
        # Override some shortcuts for this module
        self.keyboard_manager.set_callback("Control-o", self._open_file_shortcut)
        self.keyboard_manager.set_callback("Control-g", self._generate_shortcut)
        self.keyboard_manager.set_callback("F5", self._refresh_shortcut)
        self.keyboard_manager.set_callback("Control-1", self._focus_moai_shortcut)
        self.keyboard_manager.set_callback("Control-2", self._focus_qgis_shortcut)
        self.keyboard_manager.set_callback("Control-3", self._focus_project_shortcut)
    
    def _on_file_loaded(self, index: int, file_path: str):
        """Handle file loading events."""
        try:
            if not self.file_processor:
                messagebox.showerror("Erreur", "Les composants de traitement ne sont pas initialisés.")
                return

            if index == 0:  # MOAI file
                self._process_moai_file(file_path)
            elif index == 1:  # QGis file
                self._process_qgis_file(file_path)

            self._update_generation_status()

        except Exception as e:
            self.logger.error(f"Error processing file: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du traitement du fichier:\n{e}")
    
    def _process_moai_file(self, file_path: str):
        """Process MOAI file and extract information."""
        def process():
            # Read MOAI file
            self.moai_data = self.file_processor.read_moai_file(file_path)
            
            # Extract INSEE and commune from filename
            insee, commune = self.file_processor.extract_insee_from_filename(file_path)
            
            return insee, commune
        
        def on_success(result):
            insee, commune = result
            # Update project info fields
            if self.project_info_section:
                if insee:
                    self.project_info_section.update_insee_field(insee)
                if commune:
                    self.project_info_section.update_commune_field(commune)

            self.logger.info("MOAI file processed successfully")
        
        def on_error(error):
            self.logger.error(f"Error processing MOAI file: {error}")
            messagebox.showerror("Erreur", f"Erreur lors du traitement du fichier MOAI:\n{error}")
        
        # Process asynchronously
        run_async_task(process, on_success, on_error, "MOAI file processing")
    
    def _process_qgis_file(self, file_path: str):
        """Process QGis file."""
        def process():
            # Read QGis file
            raw_data, has_column_u = self.file_processor.read_qgis_file(file_path)
            
            # Clean and validate data
            plan_data = self.data_validator.clean_qgis_data(raw_data, has_column_u)
            
            return plan_data, has_column_u
        
        def on_success(result):
            self.plan_data, self.has_column_u = result
            self.logger.info("QGis file processed successfully")
        
        def on_error(error):
            self.logger.error(f"Error processing QGis file: {error}")
            messagebox.showerror("Erreur", f"Erreur lors du traitement du fichier QGis:\n{error}")
        
        # Process asynchronously
        run_async_task(process, on_success, on_error, "QGis file processing")
    
    def _on_project_data_changed(self):
        """Handle project data changes."""
        self._update_generation_status()
    
    def _update_generation_status(self):
        """Update the generation section status based on current state."""
        # Check if UI components are initialized
        if not self.file_import_section or not self.project_info_section or not self.generation_section:
            self.logger.debug("UI components not yet initialized, skipping status update")
            return

        try:
            files_loaded = self.file_import_section.are_all_files_loaded()
            project_complete = self.project_info_section.is_complete()

            if files_loaded and project_complete:
                self.generation_section.enable_generation(True)
            elif files_loaded:
                missing_fields = self.project_info_section.get_missing_fields()
                message = f"Veuillez remplir: {', '.join(missing_fields)}"
                self.generation_section.show_warning(message)
                self.generation_section.enable_generation(False)
            else:
                self.generation_section.enable_generation(False)
        except Exception as e:
            self.logger.error(f"Error updating generation status: {e}")
            # Don't propagate the error to avoid breaking the UI

    def _on_generate_excel(self):
        """Handle Excel generation."""
        try:
            # Check if components are initialized
            if not self.project_info_section or not self.generation_section or not self.excel_generator:
                messagebox.showerror("Erreur", "Les composants ne sont pas initialisés.")
                return

            # Validate project data
            validation = self.project_info_section.validate_data()
            if not validation['valid']:
                error_msg = '\n'.join(validation['errors'])
                messagebox.showerror("Erreurs de validation", error_msg)
                return

            project_data = validation['data']

            # Generate filename
            filename = self.excel_generator.generate_filename(
                project_data['nom_commune'],
                project_data['id_tache'],
                project_data['insee']
            )

            # Get save path (pass project_data for Teams integration)
            save_path = self.generation_section.get_save_path(filename, project_data)
            if not save_path:
                return

            # Show progress
            self.generation_section.show_progress(True)

            def generate():
                # Process MOAI data
                moai_processed = self.data_validator.prepare_moai_data(self.moai_data)

                # Generate Excel file
                success = self.excel_generator.generate_excel_file(
                    moai_processed,
                    self.plan_data,
                    project_data,
                    save_path
                )
                return success, save_path

            def on_success(result):
                success, save_path = result
                if self.generation_section:
                    if success:
                        self.generation_section.show_success("Fichier généré avec succès")
                        self.generation_section.show_generation_complete(save_path)
                    else:
                        self.generation_section.show_error("Erreur lors de la génération")

            def on_error(error):
                self.logger.error(f"Error generating Excel file: {error}")
                if self.generation_section:
                    self.generation_section.show_error(f"Erreur: {str(error)}")
                messagebox.showerror("Erreur", f"Erreur lors de la génération:\n{error}")

            # Generate asynchronously
            run_async_task(generate, on_success, on_error, "Excel generation")

        except Exception as e:
            self.logger.error(f"Error in generate Excel: {e}")
            if self.generation_section:
                self.generation_section.show_error(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Erreur lors de la génération:\n{e}")





    # Keyboard shortcut handlers
    def _open_file_shortcut(self):
        """Handle open file shortcut."""
        # Focus on the first file import button
        if hasattr(self.file_import_section, 'moai_button'):
            self.file_import_section.moai_button.focus_set()

    def _generate_shortcut(self):
        """Handle generate shortcut."""
        if self.generation_section and hasattr(self.generation_section, 'generate_button'):
            if self.generation_section.generate_button['state'] == 'normal':
                self._on_generate_excel()

    def _refresh_shortcut(self):
        """Handle refresh shortcut."""
        self._update_generation_status()

    def _focus_moai_shortcut(self):
        """Focus MOAI section."""
        if hasattr(self.file_import_section, 'moai_button'):
            self.file_import_section.moai_button.focus_set()

    def _focus_qgis_shortcut(self):
        """Focus QGis section."""
        if hasattr(self.file_import_section, 'qgis_button'):
            self.file_import_section.qgis_button.focus_set()

    def _focus_project_shortcut(self):
        """Focus project info section."""
        if hasattr(self.project_info_section, 'entry_id_tache'):
            self.project_info_section.entry_id_tache.focus_set()

    def refresh(self, **kwargs):
        """Refresh the module."""
        self._update_generation_status()

    def cleanup(self):
        """Clean up resources when module is closed."""
        try:
            self.logger.info("Module cleanup completed")

        except Exception as e:
            self.logger.error(f"Error during module cleanup: {e}")

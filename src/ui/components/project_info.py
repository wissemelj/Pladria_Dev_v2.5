"""
Project information section component for the Suivi Generator application.
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, Optional, Callable
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig, VALIDATION_LISTS
from ui.styles import create_card_frame, create_section_header, create_form_field

logger = logging.getLogger(__name__)


class ProjectInfoSection:
    """Project information section component."""
    
    def __init__(self, parent: tk.Widget, on_data_changed: Optional[Callable] = None):
        """
        Initialize the project information section.
        
        Args:
            parent: Parent widget
            on_data_changed: Callback function when data changes
        """
        self.parent = parent
        self.on_data_changed = on_data_changed
        self.logger = logging.getLogger(__name__)
        
        # Entry widgets
        self.entry_commune = None
        self.entry_insee = None
        self.entry_id_tache = None
        self.domaine_var = None
        self.domaine_combo = None
        
        self._create_section()
    
    def _create_section(self):
        """Create the project information section UI."""
        # Main card for project information - Ultra compact
        input_card = create_card_frame(self.parent)
        input_card.pack(fill=tk.X, pady=(0, 3), padx=1)  # Ultra minimal spacing

        # Section header - Ultra compact
        header_frame = create_section_header(input_card, "✏️", "Informations du projet")
        header_frame.pack(fill=tk.X, padx=6, pady=(3, 2))  # Ultra minimal padding

        # Form content frame - Ultra compact
        form_frame = tk.Frame(input_card, bg=COLORS['CARD'])
        form_frame.pack(fill=tk.X, padx=6, pady=(0, 3))  # Ultra minimal padding
        
        # Configure grid
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Create form fields
        self._create_form_fields(form_frame)
        
        # Create info note
        self._create_info_note(form_frame)
    
    def _create_form_fields(self, parent: tk.Widget):
        """Create the form fields."""
        # Domaine field (required dropdown)
        self._create_domaine_field(parent, 0)

        # Commune field (auto-filled)
        self.entry_commune = create_form_field(
            parent,
            "Nom de la commune",
            1,
            icon="🏘️",
            placeholder="Récupéré automatiquement du fichier MOAI",
            readonly=True
        )

        # INSEE field (auto-filled)
        self.entry_insee = create_form_field(
            parent,
            "Code INSEE",
            2,
            icon="🏛️",
            placeholder="Récupéré automatiquement du fichier MOAI",
            readonly=True
        )

        # Task ID field (required)
        self.entry_id_tache = create_form_field(
            parent,
            "ID tâche Plan Adressage",
            3,
            icon="📋",
            placeholder="Saisir l'ID de la tâche Plan Adressage",
            required=True
        )

        # Bind change event to task ID field
        self.entry_id_tache.bind('<KeyRelease>', self._on_data_change)
        self.entry_id_tache.bind('<FocusOut>', self._on_data_change)

    def _create_domaine_field(self, parent: tk.Widget, row: int):
        """Create the domaine dropdown field."""
        # Field container - Ultra compact
        field_frame = tk.Frame(parent, bg=COLORS['CARD'])
        field_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(0, 2))  # Ultra minimal spacing
        field_frame.grid_columnconfigure(1, weight=1)

        # Label frame - Ultra compact
        label_frame = tk.Frame(field_frame, bg=COLORS['CARD'])
        label_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 1))  # Ultra minimal spacing

        # Icon
        tk.Label(
            label_frame,
            text="🌐",
            font=("Segoe UI", 9),
            fg=COLORS['SECONDARY'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT, padx=(0, 1))  # Ultra minimal spacing

        # Label text
        label_text = tk.Label(
            label_frame,
            text="Domaine de la commune",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        label_text.pack(side=tk.LEFT)

        # Required indicator
        tk.Label(
            label_frame,
            text=" *",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['DANGER'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT)

        # Dropdown field
        self.domaine_var = tk.StringVar()
        self.domaine_combo = ttk.Combobox(
            field_frame,
            textvariable=self.domaine_var,
            font=UIConfig.FONT_SMALL,
            state="readonly",
            values=VALIDATION_LISTS["Domaine"]
        )
        self.domaine_combo.grid(row=1, column=0, columnspan=2, sticky=tk.EW, ipady=4)

        # Set default value to first option
        if VALIDATION_LISTS["Domaine"]:
            self.domaine_var.set(VALIDATION_LISTS["Domaine"][0])

        # Bind change event
        self.domaine_combo.bind('<<ComboboxSelected>>', self._on_data_change)

    def _create_info_note(self, parent: tk.Widget):
        """Create the informational note - Ultra compact."""
        note_frame = tk.Frame(parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        note_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=(3, 0))  # Ultra minimal spacing

        note_content = tk.Frame(note_frame, bg=COLORS['LIGHT'])
        note_content.pack(fill=tk.X, padx=4, pady=2)  # Ultra minimal padding
        
        # Info icon
        tk.Label(
            note_content,
            text="ℹ️",
            font=("Segoe UI", 10),
            fg=COLORS['SECONDARY'],
            bg=COLORS['LIGHT']
        ).pack(side=tk.LEFT, padx=(0, 2))  # Ultra minimal spacing
        
        # Info text
        tk.Label(
            note_content,
            text="Champs 🔒 = auto-remplis",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['LIGHT']
        ).pack(side=tk.LEFT)
    
    def _on_data_change(self, event=None):
        """Handle data change events."""
        if self.on_data_changed:
            self.on_data_changed()
    
    def update_commune_field(self, commune_name: str):
        """
        Update the commune field with extracted data.
        
        Args:
            commune_name: Name of the commune
        """
        if self.entry_commune:
            self.entry_commune.config(state='normal')
            self.entry_commune.delete(0, tk.END)
            self.entry_commune.insert(0, commune_name)
            self.entry_commune.config(state='readonly')
            self.logger.info(f"Commune field updated: {commune_name}")
    
    def update_insee_field(self, insee_code: str):
        """
        Update the INSEE field with extracted data.
        
        Args:
            insee_code: INSEE code
        """
        if self.entry_insee:
            self.entry_insee.config(state='normal')
            self.entry_insee.delete(0, tk.END)
            self.entry_insee.insert(0, insee_code)
            self.entry_insee.config(state='readonly')
            self.logger.info(f"INSEE field updated: {insee_code}")
    
    def get_project_data(self) -> Dict[str, str]:
        """
        Get the current project data.

        Returns:
            Dictionary with project information
        """
        return {
            'domaine': self.domaine_var.get().strip() if self.domaine_var else '',
            'nom_commune': self.entry_commune.get().strip() if self.entry_commune else '',
            'insee': self.entry_insee.get().strip() if self.entry_insee else '',
            'id_tache': self.entry_id_tache.get().strip() if self.entry_id_tache else ''
        }
    
    def validate_data(self) -> Dict[str, any]:
        """
        Validate the project data.
        
        Returns:
            Validation result dictionary
        """
        data = self.get_project_data()
        errors = []
        warnings = []
        
        # Check required fields
        if not data['domaine']:
            errors.append("Le domaine de la commune est requis")
        elif data['domaine'] not in VALIDATION_LISTS["Domaine"]:
            errors.append("Le domaine doit être Orange ou RIP")

        if not data['nom_commune']:
            errors.append("Le nom de la commune est requis")

        if not data['insee']:
            errors.append("Le code INSEE est requis")
        elif not (data['insee'].isdigit() and len(data['insee']) == 5):
            errors.append("Le code INSEE doit contenir 5 chiffres")

        if not data['id_tache']:
            errors.append("L'ID de la tâche Plan Adressage est requis")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'data': data
        }
    
    def clear_fields(self):
        """Clear all form fields."""
        if self.domaine_var and VALIDATION_LISTS["Domaine"]:
            self.domaine_var.set(VALIDATION_LISTS["Domaine"][0])

        if self.entry_commune:
            self.entry_commune.config(state='normal')
            self.entry_commune.delete(0, tk.END)
            self.entry_commune.config(state='readonly')

        if self.entry_insee:
            self.entry_insee.config(state='normal')
            self.entry_insee.delete(0, tk.END)
            self.entry_insee.config(state='readonly')

        if self.entry_id_tache:
            self.entry_id_tache.delete(0, tk.END)

        self.logger.info("Project info fields cleared")
    
    def set_field_values(self, data: Dict[str, str]):
        """
        Set field values from a data dictionary.

        Args:
            data: Dictionary with field values
        """
        if 'domaine' in data and data['domaine'] and self.domaine_var:
            if data['domaine'] in VALIDATION_LISTS["Domaine"]:
                self.domaine_var.set(data['domaine'])

        if 'nom_commune' in data and data['nom_commune']:
            self.update_commune_field(data['nom_commune'])

        if 'insee' in data and data['insee']:
            self.update_insee_field(data['insee'])

        if 'id_tache' in data and data['id_tache'] and self.entry_id_tache:
            self.entry_id_tache.delete(0, tk.END)
            self.entry_id_tache.insert(0, data['id_tache'])
    
    def is_complete(self) -> bool:
        """
        Check if all required fields are completed.
        
        Returns:
            True if all required fields have values
        """
        validation = self.validate_data()
        return validation['valid']
    
    def get_missing_fields(self) -> list:
        """
        Get list of missing required fields.

        Returns:
            List of missing field names
        """
        data = self.get_project_data()
        missing = []

        if not data['domaine']:
            missing.append('Domaine de la commune')
        if not data['nom_commune']:
            missing.append('Nom de la commune')
        if not data['insee']:
            missing.append('Code INSEE')
        if not data['id_tache']:
            missing.append('ID tâche Plan Adressage')

        return missing
    
    def focus_first_empty_field(self):
        """Focus on the first empty required field."""
        data = self.get_project_data()

        if not data['domaine'] and self.domaine_combo:
            self.domaine_combo.focus_set()
            return

        if not data['id_tache'] and self.entry_id_tache:
            self.entry_id_tache.focus_set()
            return

        # If auto-filled fields are empty, there might be an issue with file loading
        if not data['nom_commune'] or not data['insee']:
            self.logger.warning("Auto-filled fields are empty - check file loading")
    
    def enable_editing(self, enable: bool = True):
        """
        Enable or disable editing of the task ID field.
        
        Args:
            enable: Whether to enable editing
        """
        if self.entry_id_tache:
            state = 'normal' if enable else 'disabled'
            self.entry_id_tache.config(state=state)

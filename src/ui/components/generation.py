"""
Generation section component for the Suivi Generator application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
from typing import Callable, Optional, Dict
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig
from ui.styles import create_card_frame, create_section_header, create_status_indicator, update_status_indicator

logger = logging.getLogger(__name__)


class GenerationSection:
    """Generation section component."""
    
    def __init__(self, parent: tk.Widget, on_generate: Optional[Callable] = None):
        """
        Initialize the generation section.
        
        Args:
            parent: Parent widget
            on_generate: Callback function when generate button is clicked
        """
        self.parent = parent
        self.on_generate = on_generate
        self.logger = logging.getLogger(__name__)
        
        # UI elements
        self.status_icon = None
        self.status_label = None
        self.generate_button = None
        self.progress_bar = None
        self.teams_status_label = None

        self._create_section()
        self._check_teams_status()
    
    def _create_section(self):
        """Create the generation section UI."""
        # Main card for generation - Ultra compact
        gen_card = create_card_frame(self.parent)
        gen_card.pack(fill=tk.X, pady=(0, 3), padx=1)  # Ultra minimal spacing

        # Section header - Ultra compact
        header_frame = create_section_header(gen_card, "🚀", "Génération du fichier")
        header_frame.pack(fill=tk.X, padx=6, pady=(3, 2))  # Ultra minimal padding

        # Content frame - Ultra compact
        content_frame = tk.Frame(gen_card, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.X, padx=6, pady=(0, 3))  # Ultra minimal padding
        
        # Status section
        self._create_status_section(content_frame)
        
        # Progress section
        self._create_progress_section(content_frame)
        
        # Button section
        self._create_button_section(content_frame)
    
    def _create_status_section(self, parent: tk.Widget):
        """Create the status display section."""
        status_section = tk.Frame(parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        status_section.pack(fill=tk.X, pady=(0, 5))
        
        status_content = tk.Frame(status_section, bg=COLORS['LIGHT'])
        status_content.pack(fill=tk.X, padx=8, pady=6)
        
        # Create status indicator
        self.status_icon, self.status_label = create_status_indicator(status_content, COLORS['LIGHT'])
        
        # Set initial status
        self.update_status('waiting', 'En attente des fichiers...')
    
    def _create_progress_section(self, parent: tk.Widget):
        """Create the progress bar section."""
        progress_section = tk.Frame(parent, bg=COLORS['CARD'])
        progress_section.pack(fill=tk.X, pady=(0, 5))
        
        # Progress bar (initially hidden)
        self.progress_bar = ttk.Progressbar(
            progress_section,
            mode='indeterminate',
            style='TProgressbar'
        )
        # Don't pack initially - will be shown during generation
    
    def _create_button_section(self, parent: tk.Widget):
        """Create the generation button section."""
        button_section = tk.Frame(parent, bg=COLORS['CARD'])
        button_section.pack(fill=tk.X)

        # Teams status label
        self.teams_status_label = tk.Label(
            button_section,
            text="",
            font=('Segoe UI', 8),
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        self.teams_status_label.pack(pady=(0, 3))

        # Generate button
        self.generate_button = ttk.Button(
            button_section,
            text="📄 Générer Excel",
            command=self._on_generate_clicked,
            style='Success.TButton',
            state=tk.DISABLED
        )
        self.generate_button.pack(pady=3)
    
    def _on_generate_clicked(self):
        """Handle generate button click."""
        if self.on_generate:
            self.on_generate()
    
    def update_status(self, status: str, message: str):
        """
        Update the status indicator.
        
        Args:
            status: Status type ('waiting', 'warning', 'success', 'error')
            message: Status message
        """
        if self.status_icon and self.status_label:
            update_status_indicator(self.status_icon, self.status_label, status, message)
    
    def enable_generation(self, enable: bool = True):
        """
        Enable or disable the generation button.
        
        Args:
            enable: Whether to enable the button
        """
        if self.generate_button:
            state = tk.NORMAL if enable else tk.DISABLED
            self.generate_button.config(state=state)
            
            if enable:
                self.update_status('success', 'Prêt à générer le fichier Excel')
            else:
                self.update_status('waiting', 'En attente des fichiers...')
    
    def show_progress(self, show: bool = True):
        """
        Show or hide the progress bar.
        
        Args:
            show: Whether to show the progress bar
        """
        if self.progress_bar:
            if show:
                self.progress_bar.pack(fill=tk.X, pady=(0, 5))
                self.progress_bar.start(10)  # Start animation
                self.update_status('waiting', 'Génération en cours...')
                self.enable_generation(False)
            else:
                self.progress_bar.stop()  # Stop animation
                self.progress_bar.pack_forget()
    
    def show_success(self, message: str = "Fichier généré avec succès"):
        """
        Show success state.
        
        Args:
            message: Success message
        """
        self.show_progress(False)
        self.update_status('success', message)
        self.enable_generation(True)
    
    def show_error(self, message: str = "Erreur lors de la génération"):
        """
        Show error state.
        
        Args:
            message: Error message
        """
        self.show_progress(False)
        self.update_status('error', message)
        self.enable_generation(True)
    
    def show_warning(self, message: str):
        """
        Show warning state.
        
        Args:
            message: Warning message
        """
        self.update_status('warning', message)
    
    def reset(self):
        """Reset the generation section to initial state."""
        self.show_progress(False)
        self.update_status('waiting', 'En attente des fichiers...')
        self.enable_generation(False)
        self.logger.info("Generation section reset")
    
    def get_save_path(self, default_filename: str, project_data: Optional[Dict] = None) -> Optional[str]:
        """
        Get the save path for Teams channel or fallback to dialog.

        Args:
            default_filename: Default filename to suggest
            project_data: Project data containing commune and task info

        Returns:
            Selected file path or None if cancelled/failed
        """
        try:
            from config.constants import TeamsConfig
            from utils.file_utils import (
                validate_teams_path, create_teams_folder,
                get_teams_file_path
            )

            # Check if Teams saving is enabled and project data is available
            if (TeamsConfig.ENABLE_TEAMS_SAVING and project_data and
                'nom_commune' in project_data and 'id_tache' in project_data):

                # Validate Teams base path
                teams_validation = validate_teams_path()
                if teams_validation['valid']:
                    # Create Teams folder
                    folder_result = create_teams_folder(
                        project_data['nom_commune'],
                        project_data['id_tache']
                    )

                    if folder_result['success']:
                        # Generate Teams file path
                        teams_path = get_teams_file_path(
                            project_data['nom_commune'],
                            project_data['id_tache'],
                            default_filename
                        )

                        # Show confirmation with Teams path
                        folder_name = f"{project_data['nom_commune']}_{project_data['id_tache']}"
                        message = (f"Le fichier sera sauvegardé dans le canal Teams :\n\n"
                                 f"Dossier: {folder_name}\n"
                                 f"Fichier: {default_filename}\n\n"
                                 f"Continuer ?")

                        if messagebox.askyesno("Sauvegarde Teams", message, icon='question'):
                            self.logger.info(f"Teams save path confirmed: {teams_path}")
                            return teams_path
                        else:
                            self.logger.info("Teams save cancelled by user")
                            return None
                    else:
                        # Show error and fallback
                        error_msg = f"Impossible de créer le dossier Teams:\n{folder_result['error']}"
                        if TeamsConfig.FALLBACK_TO_DIALOG:
                            error_msg += "\n\nUtilisation du dialogue de sauvegarde standard."
                            messagebox.showwarning("Avertissement Teams", error_msg)
                        else:
                            messagebox.showerror("Erreur Teams", error_msg)
                            return None
                else:
                    # Show error and fallback
                    error_msg = f"Canal Teams non accessible:\n{teams_validation['error']}"
                    if TeamsConfig.FALLBACK_TO_DIALOG:
                        error_msg += "\n\nUtilisation du dialogue de sauvegarde standard."
                        messagebox.showwarning("Avertissement Teams", error_msg)
                    else:
                        messagebox.showerror("Erreur Teams", error_msg)
                        return None

            # Fallback to standard file dialog
            if TeamsConfig.FALLBACK_TO_DIALOG or not TeamsConfig.ENABLE_TEAMS_SAVING:
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    title="Enregistrer le fichier Excel généré",
                    initialfile=default_filename
                )

                if save_path:
                    self.logger.info(f"Standard save path selected: {save_path}")
                else:
                    self.logger.info("Save dialog cancelled")

                return save_path

            return None

        except Exception as e:
            self.logger.error(f"Error in get_save_path: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la sélection du fichier:\n{e}")
            return None
    
    def confirm_generation(self, filename: str) -> bool:
        """
        Show confirmation dialog before generation.
        
        Args:
            filename: Filename that will be generated
            
        Returns:
            True if user confirms, False otherwise
        """
        message = f"Générer le fichier Excel ?\n\nFichier: {filename}"
        result = messagebox.askyesno(
            "Confirmation",
            message,
            icon='question'
        )
        
        self.logger.info(f"Generation confirmation: {result}")
        return result
    
    def show_generation_complete(self, filepath: str):
        """
        Show generation complete dialog.

        Args:
            filepath: Path to the generated file
        """
        import os
        filename = os.path.basename(filepath)

        message = f"Fichier généré avec succès !\n\nFichier: {filename}\n\nVoulez-vous ouvrir le dossier ?"

        result = messagebox.askyesno(
            "Génération terminée",
            message,
            icon='info'
        )
        
        if result:  # Yes - open folder
            try:
                import subprocess
                import platform
                
                folder_path = os.path.dirname(filepath)
                
                if platform.system() == "Windows":
                    subprocess.run(["explorer", folder_path])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", folder_path])
                else:  # Linux
                    subprocess.run(["xdg-open", folder_path])
                    
                self.logger.info(f"Opened folder: {folder_path}")
                
            except Exception as e:
                self.logger.error(f"Failed to open folder: {e}")
                messagebox.showwarning("Avertissement", f"Impossible d'ouvrir le dossier:\n{e}")
    
    def update_button_text(self, text: str):
        """
        Update the generate button text.

        Args:
            text: New button text
        """
        if self.generate_button:
            self.generate_button.config(text=text)

    def _check_teams_status(self):
        """Check and display Teams channel status."""
        try:
            from config.constants import TeamsConfig
            from utils.file_utils import validate_teams_path

            if not TeamsConfig.ENABLE_TEAMS_SAVING:
                self._update_teams_status("💾 Sauvegarde: Dialogue standard", COLORS['TEXT_SECONDARY'])
                return

            # Validate Teams path
            teams_validation = validate_teams_path()
            if teams_validation['valid']:
                self._update_teams_status("☁️ Sauvegarde: Canal Teams", COLORS['SUCCESS'])
            else:
                if TeamsConfig.FALLBACK_TO_DIALOG:
                    self._update_teams_status("⚠️ Teams indisponible - Dialogue standard", COLORS['WARNING'])
                else:
                    self._update_teams_status("❌ Canal Teams inaccessible", COLORS['ERROR'])

        except Exception as e:
            self.logger.error(f"Error checking Teams status: {e}")
            self._update_teams_status("❓ Statut Teams inconnu", COLORS['TEXT_SECONDARY'])

    def _update_teams_status(self, text: str, color: str):
        """Update the Teams status label."""
        if self.teams_status_label:
            self.teams_status_label.config(text=text, fg=color)

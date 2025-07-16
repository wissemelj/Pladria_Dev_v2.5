"""
Keyboard shortcuts and hotkeys for the Suivi Generator application.
"""

import tkinter as tk
import logging
from typing import Dict, Callable, Optional

logger = logging.getLogger(__name__)


class KeyboardShortcutManager:
    """Manages keyboard shortcuts for the application."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the keyboard shortcut manager.
        
        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.shortcuts: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)
        
        # Setup default shortcuts
        self._setup_default_shortcuts()
    
    def _setup_default_shortcuts(self):
        """Set up default keyboard shortcuts."""
        # File operations
        self.register_shortcut("Control-o", self._open_file_dialog, "Ouvrir fichier")
        self.register_shortcut("Control-s", self._save_file, "Sauvegarder")
        self.register_shortcut("Control-q", self._quit_application, "Quitter")
        
        # Generation
        self.register_shortcut("Control-g", self._generate_excel, "Générer Excel")
        self.register_shortcut("F5", self._refresh_data, "Actualiser")
        
        # Navigation
        self.register_shortcut("Control-1", self._focus_moai_section, "Focus section MOAI")
        self.register_shortcut("Control-2", self._focus_qgis_section, "Focus section QGis")
        self.register_shortcut("Control-3", self._focus_project_info, "Focus informations projet")
        

        
        self.logger.info("Default keyboard shortcuts registered")
    
    def register_shortcut(self, key_sequence: str, callback: Callable, description: str = ""):
        """
        Register a keyboard shortcut.
        
        Args:
            key_sequence: Key sequence (e.g., "Control-o")
            callback: Function to call when shortcut is pressed
            description: Description of the shortcut
        """
        try:
            self.root.bind_all(f"<{key_sequence}>", lambda event: self._handle_shortcut(callback, event))
            self.shortcuts[key_sequence] = {
                'callback': callback,
                'description': description
            }
            self.logger.debug(f"Registered shortcut: {key_sequence} - {description}")
        except Exception as e:
            self.logger.error(f"Failed to register shortcut {key_sequence}: {e}")
    
    def _handle_shortcut(self, callback: Callable, event):
        """Handle shortcut execution with error handling."""
        try:
            callback()
        except Exception as e:
            self.logger.error(f"Error executing shortcut: {e}")
    
    def get_shortcuts_info(self) -> str:
        """Get formatted info text for all shortcuts."""
        info_text = "Raccourcis clavier disponibles:\n\n"

        categories = {
            "Fichiers": ["Control-o", "Control-s", "Control-q"],
            "Génération": ["Control-g", "F5"],
            "Navigation": ["Control-1", "Control-2", "Control-3"]
        }

        for category, keys in categories.items():
            info_text += f"{category}:\n"
            for key in keys:
                if key in self.shortcuts:
                    desc = self.shortcuts[key]['description']
                    info_text += f"  {key.replace('Control-', 'Ctrl+')} - {desc}\n"
            info_text += "\n"

        return info_text
    
    # Default shortcut handlers (to be overridden by main window)
    def _open_file_dialog(self):
        """Default open file handler."""
        self.logger.info("Open file shortcut pressed")
    
    def _save_file(self):
        """Default save file handler."""
        self.logger.info("Save file shortcut pressed")
    
    def _quit_application(self):
        """Default quit handler."""
        self.logger.info("Quit shortcut pressed")
        self.root.quit()
    
    def _generate_excel(self):
        """Default generate Excel handler."""
        self.logger.info("Generate Excel shortcut pressed")
    
    def _refresh_data(self):
        """Default refresh handler."""
        self.logger.info("Refresh shortcut pressed")
    
    def _focus_moai_section(self):
        """Default focus MOAI section handler."""
        self.logger.info("Focus MOAI section shortcut pressed")
    
    def _focus_qgis_section(self):
        """Default focus QGis section handler."""
        self.logger.info("Focus QGis section shortcut pressed")
    
    def _focus_project_info(self):
        """Default focus project info handler."""
        self.logger.info("Focus project info shortcut pressed")
    

    
    def set_callback(self, shortcut_name: str, callback: Callable):
        """
        Set a custom callback for a shortcut.
        
        Args:
            shortcut_name: Name of the shortcut (e.g., "Control-o")
            callback: New callback function
        """
        if shortcut_name in self.shortcuts:
            self.shortcuts[shortcut_name]['callback'] = callback
            # Re-bind the shortcut
            self.root.bind_all(f"<{shortcut_name}>", lambda event: self._handle_shortcut(callback, event))
            self.logger.debug(f"Updated callback for shortcut: {shortcut_name}")


class ContextMenu:
    """Context menu for right-click operations."""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the context menu.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.menu = tk.Menu(parent, tearoff=0)
        self.logger = logging.getLogger(__name__)
        
        # Setup default menu items
        self._setup_default_menu()
    
    def _setup_default_menu(self):
        """Set up default context menu items."""
        self.menu.add_command(label="Copier", command=self._copy, accelerator="Ctrl+C")
        self.menu.add_command(label="Coller", command=self._paste, accelerator="Ctrl+V")
        self.menu.add_separator()
        self.menu.add_command(label="Sélectionner tout", command=self._select_all, accelerator="Ctrl+A")
        self.menu.add_separator()
        self.menu.add_command(label="Actualiser", command=self._refresh, accelerator="F5")
    
    def show(self, event):
        """Show the context menu."""
        try:
            self.menu.post(event.x_root, event.y_root)
        except Exception as e:
            self.logger.error(f"Error showing context menu: {e}")
    
    def _copy(self):
        """Copy operation."""
        try:
            self.parent.event_generate("<<Copy>>")
        except Exception as e:
            self.logger.error(f"Copy operation failed: {e}")
    
    def _paste(self):
        """Paste operation."""
        try:
            self.parent.event_generate("<<Paste>>")
        except Exception as e:
            self.logger.error(f"Paste operation failed: {e}")
    
    def _select_all(self):
        """Select all operation."""
        try:
            self.parent.event_generate("<<SelectAll>>")
        except Exception as e:
            self.logger.error(f"Select all operation failed: {e}")
    
    def _refresh(self):
        """Refresh operation."""
        self.logger.info("Refresh requested from context menu")

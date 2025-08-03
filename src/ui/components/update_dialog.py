"""
Update Dialog UI Component for Pladria v2.5
Provides user interface for OTA updates
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from typing import Optional, Callable

from config.constants import COLORS, AppInfo
from core.update_manager import UpdateManager, UpdateInfo
from ui.styles import create_card_frame

logger = logging.getLogger(__name__)


class UpdateDialog:
    """Dialog for handling application updates"""
    
    def __init__(self, parent: tk.Widget, update_manager: UpdateManager):
        self.parent = parent
        self.update_manager = update_manager
        self.dialog = None
        self.update_info: Optional[UpdateInfo] = None
        self.logger = logging.getLogger(__name__)
        
        # UI components
        self.progress_var = tk.IntVar()
        self.status_var = tk.StringVar()
        self.progress_bar = None
        self.status_label = None
        self.update_button = None
        self.cancel_button = None
        
        # Set up callbacks
        self.update_manager.set_progress_callback(self._on_progress_update)
        self.update_manager.set_status_callback(self._on_status_update)
    
    def check_for_updates(self, show_no_updates: bool = True) -> bool:
        """
        Check for updates and show dialog if available
        
        Args:
            show_no_updates: Whether to show message when no updates available
            
        Returns:
            True if updates are available, False otherwise
        """
        def check_updates_thread():
            try:
                self.update_info = self.update_manager.check_for_updates()
                
                if self.update_info:
                    # Schedule UI update on main thread
                    self.parent.after(0, lambda: self._show_update_available_dialog())
                    return True
                else:
                    if show_no_updates:
                        self.parent.after(0, lambda: self._show_no_updates_message())
                    return False
                    
            except Exception as e:
                self.logger.error(f"Error checking for updates: {e}")
                self.parent.after(0, lambda: self._show_error_message(str(e)))
                return False
        
        # Run check in background thread
        thread = threading.Thread(target=check_updates_thread, daemon=True)
        thread.start()
        return False  # Will be updated asynchronously
    
    def _show_update_available_dialog(self):
        """Show dialog when update is available"""
        if not self.update_info:
            return
        
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Mise à jour disponible - Pladria")
        self.dialog.geometry("600x500")  # Augmenté la taille
        self.dialog.resizable(True, True)  # Permettre le redimensionnement
        self.dialog.configure(bg=COLORS['BG'])
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Main container
        main_frame = tk.Frame(self.dialog, bg=COLORS['BG'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self._create_header(main_frame)
        
        # Update info
        self._create_update_info(main_frame)
        
        # Progress section
        self._create_progress_section(main_frame)
        
        # Buttons
        self._create_buttons(main_frame)
        
        # Set initial status
        self.status_var.set("Prêt à installer la mise à jour")
    
    def _create_header(self, parent: tk.Widget):
        """Create dialog header"""
        header_frame = tk.Frame(parent, bg=COLORS['BG'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Icon and title
        title_label = tk.Label(
            header_frame,
            text="🔄 Mise à jour disponible",
            font=("Segoe UI", 16, "bold"),
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        title_label.pack(side=tk.LEFT)
        
        # Version info
        version_label = tk.Label(
            header_frame,
            text=f"v{self.update_info.version}",
            font=("Segoe UI", 12),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['BG']
        )
        version_label.pack(side=tk.RIGHT)
    
    def _create_update_info(self, parent: tk.Widget):
        """Create update information section"""
        info_card = create_card_frame(parent)
        info_card.pack(fill=tk.X, pady=(0, 15))
        
        # Current version
        current_frame = tk.Frame(info_card, bg=COLORS['CARD'])
        current_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(
            current_frame,
            text=f"Version actuelle: v{AppInfo.VERSION}",
            font=("Segoe UI", 10),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT)
        
        # New version
        new_frame = tk.Frame(info_card, bg=COLORS['CARD'])
        new_frame.pack(fill=tk.X, padx=15, pady=(0, 5))
        
        tk.Label(
            new_frame,
            text=f"Nouvelle version: v{self.update_info.version}",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS['SUCCESS'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT)
        
        # Critical update indicator
        if self.update_info.is_critical:
            critical_frame = tk.Frame(info_card, bg=COLORS['CARD'])
            critical_frame.pack(fill=tk.X, padx=15, pady=(0, 5))
            
            tk.Label(
                critical_frame,
                text="⚠️ Mise à jour critique",
                font=("Segoe UI", 10, "bold"),
                fg=COLORS['DANGER'],
                bg=COLORS['CARD']
            ).pack(side=tk.LEFT)
        
        # File size
        if self.update_info.file_size > 0:
            size_mb = self.update_info.file_size / (1024 * 1024)
            size_frame = tk.Frame(info_card, bg=COLORS['CARD'])
            size_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
            
            tk.Label(
                size_frame,
                text=f"Taille: {size_mb:.1f} MB",
                font=("Segoe UI", 9),
                fg=COLORS['TEXT_MUTED'],
                bg=COLORS['CARD']
            ).pack(side=tk.LEFT)
        
        # Release notes
        if self.update_info.release_notes:
            notes_label = tk.Label(
                info_card,
                text="Notes de version:",
                font=("Segoe UI", 10, "bold"),
                fg=COLORS['TEXT_PRIMARY'],
                bg=COLORS['CARD']
            )
            notes_label.pack(anchor=tk.W, padx=15, pady=(5, 5))
            
            # Scrollable text for release notes
            notes_frame = tk.Frame(info_card, bg=COLORS['CARD'])
            notes_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

            notes_text = tk.Text(
                notes_frame,
                height=10,  # Augmenté de 6 à 10 lignes
                wrap=tk.WORD,
                font=("Segoe UI", 9),
                fg=COLORS['TEXT_PRIMARY'],
                bg=COLORS['LIGHT'],
                relief=tk.SOLID,
                borderwidth=1,
                padx=10,
                pady=8
            )
            notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=notes_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            notes_text.config(yscrollcommand=scrollbar.set)
            
            # Insert release notes
            notes_text.insert(tk.END, self.update_info.release_notes)
            notes_text.config(state=tk.DISABLED)
    
    def _create_progress_section(self, parent: tk.Widget):
        """Create progress section"""
        progress_frame = tk.Frame(parent, bg=COLORS['BG'])
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['BG']
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style='TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X)
    
    def _create_buttons(self, parent: tk.Widget):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg=COLORS['BG'])
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Cancel button
        self.cancel_button = ttk.Button(
            button_frame,
            text="Annuler",
            command=self._on_cancel,
            style='Secondary.TButton'
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Update button
        self.update_button = ttk.Button(
            button_frame,
            text="Installer maintenant",
            command=self._on_install_update,
            style='Primary.TButton'
        )
        self.update_button.pack(side=tk.RIGHT)
    
    def _on_progress_update(self, progress: int, message: str = ""):
        """Handle progress updates"""
        if self.dialog and self.dialog.winfo_exists():
            self.progress_var.set(progress)
            if message:
                self.status_var.set(message)
    
    def _on_status_update(self, message: str):
        """Handle status updates"""
        if self.dialog and self.dialog.winfo_exists():
            self.status_var.set(message)

    def _on_install_update(self):
        """Handle install update button click"""
        if not self.update_info:
            return

        # Disable buttons during update
        self.update_button.config(state=tk.DISABLED)
        self.cancel_button.config(text="Fermer", state=tk.DISABLED)

        def install_update_thread():
            try:
                # Use quick update method for faster installation
                if self.update_manager.perform_quick_update(self.update_info):
                    # Success - offer to restart
                    self.parent.after(0, lambda: self._show_restart_dialog())
                else:
                    self.parent.after(0, lambda: self._show_error_message("Échec de l'installation"))

            except Exception as e:
                self.logger.error(f"Error during update installation: {e}")
                error_msg = f"Erreur lors de la mise à jour: {str(e)}"
                self.parent.after(0, lambda: self._show_error_message(error_msg))
            finally:
                # Re-enable cancel button
                self.parent.after(0, lambda: self.cancel_button.config(state=tk.NORMAL))

        # Run installation in background thread
        thread = threading.Thread(target=install_update_thread, daemon=True)
        thread.start()

    def _on_cancel(self):
        """Handle cancel button click"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

    def _show_restart_dialog(self):
        """Show restart confirmation dialog"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

        result = messagebox.askyesno(
            "Mise à jour terminée",
            "La mise à jour a été installée avec succès!\n\n"
            "L'application doit redémarrer pour appliquer les changements.\n\n"
            "Redémarrer maintenant?",
            icon='question'
        )

        if result:
            self.update_manager.restart_application()

    def _show_no_updates_message(self):
        """Show message when no updates are available"""
        messagebox.showinfo(
            "Aucune mise à jour",
            f"Vous utilisez déjà la dernière version de Pladria (v{AppInfo.VERSION}).",
            icon='info'
        )

    def _show_error_message(self, error_message: str):
        """Show error message"""
        messagebox.showerror(
            "Erreur de mise à jour",
            f"Une erreur s'est produite lors de la mise à jour:\n\n{error_message}",
            icon='error'
        )

        # Re-enable buttons
        if self.update_button:
            self.update_button.config(state=tk.NORMAL)
        if self.cancel_button:
            self.cancel_button.config(text="Annuler", state=tk.NORMAL)


class UpdateNotification:
    """Simple notification for available updates"""

    def __init__(self, parent: tk.Widget, update_info: UpdateInfo, on_update_click: Callable):
        self.parent = parent
        self.update_info = update_info
        self.on_update_click = on_update_click
        self.notification = None

    def show(self):
        """Show update notification"""
        self.notification = tk.Toplevel(self.parent)
        self.notification.title("Mise à jour disponible")
        self.notification.geometry("350x150")
        self.notification.resizable(False, False)
        self.notification.configure(bg=COLORS['BG'])

        # Position in bottom right
        self.notification.withdraw()
        self.notification.update_idletasks()
        x = self.notification.winfo_screenwidth() - self.notification.winfo_width() - 20
        y = self.notification.winfo_screenheight() - self.notification.winfo_height() - 60
        self.notification.geometry(f"+{x}+{y}")
        self.notification.deiconify()

        # Make it stay on top but not modal
        self.notification.attributes('-topmost', True)

        # Content
        main_frame = tk.Frame(self.notification, bg=COLORS['BG'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header
        header_label = tk.Label(
            main_frame,
            text="🔄 Mise à jour disponible",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        header_label.pack(anchor=tk.W)

        # Version info
        version_label = tk.Label(
            main_frame,
            text=f"Nouvelle version: v{self.update_info.version}",
            font=("Segoe UI", 10),
            fg=COLORS['TEXT_PRIMARY'],
            bg=COLORS['BG']
        )
        version_label.pack(anchor=tk.W, pady=(5, 0))

        # Critical indicator
        if self.update_info.is_critical:
            critical_label = tk.Label(
                main_frame,
                text="⚠️ Mise à jour critique",
                font=("Segoe UI", 9, "bold"),
                fg=COLORS['DANGER'],
                bg=COLORS['BG']
            )
            critical_label.pack(anchor=tk.W, pady=(2, 0))

        # Buttons
        button_frame = tk.Frame(main_frame, bg=COLORS['BG'])
        button_frame.pack(fill=tk.X, pady=(15, 0))

        # Later button
        later_btn = ttk.Button(
            button_frame,
            text="Plus tard",
            command=self._on_later,
            style='Secondary.TButton'
        )
        later_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Update button
        update_btn = ttk.Button(
            button_frame,
            text="Mettre à jour",
            command=self._on_update,
            style='Primary.TButton'
        )
        update_btn.pack(side=tk.RIGHT)

        # Auto-close after 30 seconds
        self.notification.after(30000, self._on_later)

    def _on_update(self):
        """Handle update button click"""
        if self.notification:
            self.notification.destroy()
            self.notification = None
        self.on_update_click()

    def _on_later(self):
        """Handle later button click"""
        if self.notification:
            self.notification.destroy()
            self.notification = None

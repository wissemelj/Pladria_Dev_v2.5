"""
Password dialog component for secure module access.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from config.constants import COLORS, UIConfig

logger = logging.getLogger(__name__)


class PasswordDialog:
    """Password dialog for secure access to protected modules."""
    
    def __init__(self, parent, title="Accès Sécurisé", message="Veuillez saisir le mot de passe :"):
        """
        Initialize the password dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
        """
        self.parent = parent
        self.title = title
        self.message = message
        self.password = None
        self.result = False
        self.dialog = None
        
        self.logger = logging.getLogger(__name__)
    
    def show(self):
        """
        Show the password dialog and return the result.

        Returns:
            tuple: (success: bool, password: str)
        """
        try:
            self.logger.info("Creating password dialog")
            self._create_dialog()

            self.logger.info("Centering password dialog")
            self._center_dialog()

            # Make dialog modal
            self.logger.info("Making dialog modal")
            self.dialog.transient(self.parent)
            self.dialog.grab_set()

            # Wait for dialog to close
            self.logger.info("Waiting for dialog to close")
            self.dialog.wait_window()

            self.logger.info(f"Dialog closed with result: {self.result}, password length: {len(self.password) if self.password else 0}")
            return self.result, self.password

        except Exception as e:
            self.logger.error(f"Error showing password dialog: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return False, None
    
    def _create_dialog(self):
        """Create the password dialog UI with modern Sofrecom design."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("")  # Remove title bar text
        self.dialog.geometry("450x320")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLORS['BG'])

        # Make dialog modal and centered
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Main container with modern card design
        main_frame = tk.Frame(self.dialog, bg=COLORS['BG'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Card container with subtle shadow effect
        card_frame = tk.Frame(main_frame, bg=COLORS['CARD'], relief=tk.FLAT, bd=0)
        card_frame.pack(fill=tk.BOTH, expand=True)

        # Add subtle border
        border_frame = tk.Frame(card_frame, bg=COLORS['BORDER'], height=1)
        border_frame.pack(fill=tk.X, side=tk.TOP)

        # Content container
        content_frame = tk.Frame(card_frame, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # Header section with Sofrecom branding
        header_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X, pady=(0, 25))

        # Sofrecom-style security icon with gradient effect
        icon_frame = tk.Frame(header_frame, bg=COLORS['ACCENT'], width=60, height=60)
        icon_frame.pack(pady=(0, 15))
        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text="🔐",
            font=("Segoe UI", 24),
            bg=COLORS['ACCENT'],
            fg=COLORS['PRIMARY']
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Modern title with Sofrecom typography
        title_label = tk.Label(
            header_frame,
            text="Accès Sécurisé",
            font=UIConfig.FONT_HEADER,
            bg=COLORS['CARD'],
            fg=COLORS['PRIMARY']
        )
        title_label.pack()

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Module Statistiques Équipe",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        subtitle_label.pack(pady=(5, 0))

        # Message section with better spacing
        message_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        message_frame.pack(fill=tk.X, pady=(0, 20))

        message_label = tk.Label(
            message_frame,
            text="Ce module contient des données sensibles.\nVeuillez vous authentifier pour continuer.",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['INFO'],
            justify=tk.CENTER,
            wraplength=380
        )
        message_label.pack()

        # Password input section with modern styling
        input_section = tk.Frame(content_frame, bg=COLORS['CARD'])
        input_section.pack(fill=tk.X, pady=(0, 25))

        # Password label with icon
        label_frame = tk.Frame(input_section, bg=COLORS['CARD'])
        label_frame.pack(fill=tk.X, pady=(0, 8))

        password_label = tk.Label(
            label_frame,
            text="🔑 Mot de passe",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['INFO']
        )
        password_label.pack(anchor=tk.W)

        # Modern password entry with border
        entry_container = tk.Frame(input_section, bg=COLORS['BORDER'], relief=tk.FLAT, bd=1)
        entry_container.pack(fill=tk.X, pady=(0, 5))

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            entry_container,
            textvariable=self.password_var,
            font=UIConfig.FONT_SUBTITLE,
            show="●",  # Modern bullet character
            relief=tk.FLAT,
            bd=0,
            bg=COLORS['WHITE'],
            fg=COLORS['INFO']
        )
        self.password_entry.pack(fill=tk.X, padx=12, pady=8)
        self.password_entry.focus_set()

        # Bind events
        self.password_entry.bind('<Return>', lambda e: self._on_ok())
        self.password_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.password_entry.bind('<FocusOut>', self._on_entry_focus_out)
        self.dialog.bind('<Escape>', lambda e: self._on_cancel())

        # Status label for feedback
        self.status_label = tk.Label(
            input_section,
            text="",
            font=UIConfig.FONT_SMALL,
            bg=COLORS['CARD'],
            fg=COLORS['DANGER']
        )
        self.status_label.pack(anchor=tk.W)

        # Action buttons with modern Sofrecom styling
        buttons_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        buttons_frame.pack(fill=tk.X)

        # Cancel button - secondary style
        cancel_button = tk.Button(
            buttons_frame,
            text="Annuler",
            font=UIConfig.FONT_BUTTON,
            bg=COLORS['LIGHT'],
            fg=COLORS['TEXT_SECONDARY'],
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=10,
            command=self._on_cancel,
            cursor='hand2'
        )
        cancel_button.pack(side=tk.RIGHT, padx=(10, 0))

        # OK button - primary Sofrecom style
        ok_button = tk.Button(
            buttons_frame,
            text="🔓 Accéder",
            font=UIConfig.FONT_BUTTON,
            bg=COLORS['PRIMARY'],
            fg=COLORS['WHITE'],
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=10,
            command=self._on_ok,
            cursor='hand2'
        )
        ok_button.pack(side=tk.RIGHT)

        # Add hover effects
        self._add_button_hover_effects(ok_button, cancel_button)

    def _add_button_hover_effects(self, ok_button, cancel_button):
        """Add modern hover effects to buttons."""
        # OK button hover effects
        def on_ok_enter(e):
            ok_button.config(bg=COLORS['PRIMARY_DARK'])

        def on_ok_leave(e):
            ok_button.config(bg=COLORS['PRIMARY'])

        ok_button.bind('<Enter>', on_ok_enter)
        ok_button.bind('<Leave>', on_ok_leave)

        # Cancel button hover effects
        def on_cancel_enter(e):
            cancel_button.config(bg=COLORS['BORDER'])

        def on_cancel_leave(e):
            cancel_button.config(bg=COLORS['LIGHT'])

        cancel_button.bind('<Enter>', on_cancel_enter)
        cancel_button.bind('<Leave>', on_cancel_leave)

    def _on_entry_focus_in(self, event):
        """Handle entry focus in event."""
        try:
            event.widget.master.config(bg=COLORS['PRIMARY'], relief=tk.FLAT, bd=2)
        except Exception as e:
            self.logger.error(f"Error in focus in handler: {e}")

    def _on_entry_focus_out(self, event):
        """Handle entry focus out event."""
        try:
            event.widget.master.config(bg=COLORS['BORDER'], relief=tk.FLAT, bd=1)
        except Exception as e:
            self.logger.error(f"Error in focus out handler: {e}")

    def _center_dialog(self):
        """Center the dialog on the parent window."""
        try:
            # Update dialog to get actual size
            self.dialog.update_idletasks()
            
            # Get parent window position and size
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            # Get dialog size
            dialog_width = self.dialog.winfo_reqwidth()
            dialog_height = self.dialog.winfo_reqheight()
            
            # Calculate center position
            x = parent_x + (parent_width - dialog_width) // 2
            y = parent_y + (parent_height - dialog_height) // 2
            
            # Set position
            self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
            
        except Exception as e:
            self.logger.error(f"Error centering dialog: {e}")
    
    def _on_ok(self):
        """Handle OK button click."""
        self.password = self.password_var.get().strip()
        
        if not self.password:
            self.status_label.config(text="⚠️ Veuillez saisir un mot de passe")
            self.password_entry.focus_set()
            return
        
        self.result = True
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button click."""
        self.result = False
        self.password = None
        self.dialog.destroy()


def show_password_dialog(parent, title="Accès Sécurisé", message="Veuillez saisir le mot de passe :"):
    """
    Convenience function to show a password dialog.
    
    Args:
        parent: Parent window
        title: Dialog title
        message: Message to display
        
    Returns:
        tuple: (success: bool, password: str)
    """
    dialog = PasswordDialog(parent, title, message)
    return dialog.show()

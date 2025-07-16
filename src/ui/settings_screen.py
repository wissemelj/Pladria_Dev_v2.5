"""
About screen for the Suivi Generator platform.
Application information and details.
"""

import tkinter as tk
from tkinter import ttk
import logging

from config.constants import COLORS, UIConfig, AppInfo
from ui.styles import create_card_frame, create_section_header

logger = logging.getLogger(__name__)


class SettingsScreen:
    """About screen with application information."""

    def __init__(self, parent: tk.Widget, navigation_manager=None):
        """
        Initialize the about screen.

        Args:
            parent: Parent widget
            navigation_manager: Navigation manager instance
        """
        self.parent = parent
        self.navigation_manager = navigation_manager
        self.logger = logging.getLogger(__name__)

        self._create_about_screen()
    
    def _create_about_screen(self):
        """Create the about screen interface."""
        # Main container
        main_container = tk.Frame(self.parent, bg=COLORS['BG'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title section
        self._create_title_section(main_container)

        # Info section
        self._create_info_section(main_container)

        # Action buttons
        self._create_action_buttons(main_container)
    
    def _create_title_section(self, parent: tk.Widget):
        """Create the title section."""
        title_card = create_card_frame(parent)
        title_card.pack(fill=tk.X, pady=(0, 20))

        title_content = tk.Frame(title_card, bg=COLORS['CARD'])
        title_content.pack(fill=tk.X, padx=20, pady=15)

        # Title
        title_label = tk.Label(
            title_content,
            text="ℹ️ À propos",
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        title_label.pack(anchor=tk.W)

        # Subtitle
        subtitle_label = tk.Label(
            title_content,
            text="Informations sur l'application",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['INFO'],
            bg=COLORS['CARD']
        )
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_info_section(self, parent: tk.Widget):
        """Create application information section."""
        info_card = create_card_frame(parent)
        info_card.pack(fill=tk.X, pady=(0, 15))

        # Section header
        header_frame = create_section_header(info_card, "ℹ️", "Informations sur l'application")
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))

        # Info content
        content_frame = tk.Frame(info_card, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Application info
        info_items = [
            ("Nom:", "Pladria"),
            ("Version:", AppInfo.VERSION),
            ("Auteur:", AppInfo.AUTHOR),
            ("Description:", AppInfo.FULL_DESCRIPTION),
            ("Copyright:", AppInfo.COPYRIGHT)
        ]

        for label_text, value_text in info_items:
            item_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
            item_frame.pack(fill=tk.X, pady=(0, 8))

            # Label
            label = tk.Label(
                item_frame,
                text=label_text,
                font=UIConfig.FONT_SMALL,
                fg=COLORS['SECONDARY'],
                bg=COLORS['CARD'],
                width=12,
                anchor=tk.W
            )
            label.pack(side=tk.LEFT)

            # Value
            value = tk.Label(
                item_frame,
                text=value_text,
                font=UIConfig.FONT_SMALL,
                fg=COLORS['INFO'],
                bg=COLORS['CARD'],
                anchor=tk.W,
                wraplength=400,
                justify=tk.LEFT
            )
            value.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _create_action_buttons(self, parent: tk.Widget):
        """Create action buttons."""
        action_frame = tk.Frame(parent, bg=COLORS['BG'])
        action_frame.pack(fill=tk.X, pady=(10, 0))

        # Back button
        back_btn = ttk.Button(
            action_frame,
            text="🏠 Retour à l'accueil",
            command=self._go_back,
            style='Primary.TButton'
        )
        back_btn.pack(side=tk.RIGHT)
    
    def _go_back(self):
        """Go back to home screen."""
        if self.navigation_manager:
            from ui.navigation import NavigationState
            self.navigation_manager.navigate_to(NavigationState.HOME)

    def refresh(self, **kwargs):
        """Refresh the about screen."""
        # About screen doesn't need refreshing
        pass

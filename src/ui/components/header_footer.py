"""
Header and footer components for the Suivi Generator application.
"""

import tkinter as tk
from tkinter import ttk
import logging
import os
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig, AppInfo
from utils.file_utils import get_logo_path
from utils.lazy_imports import get_PIL

logger = logging.getLogger(__name__)


class HeaderSection:
    """Header section component with logo and title."""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the header section.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.logo_image = None
        self.logo_placeholder = None
        self.logger = logging.getLogger(__name__)
        
        self._create_header()
        
        # Load logo asynchronously
        parent.after(10, self._load_logo_async)
    
    def _create_header(self):
        """Create the header UI elements."""
        # Main header card - Ultra compact
        header_card = tk.Frame(self.parent, bg=COLORS['CARD'], relief='flat', bd=0)
        header_card.pack(fill=tk.X, pady=(0, 3), padx=1)  # Ultra minimal spacing

        # Subtle border
        border_frame = tk.Frame(header_card, bg=COLORS['BORDER'], height=1)
        border_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Content frame - Ultra compact
        content_frame = tk.Frame(header_card, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.X, padx=6, pady=3)  # Ultra minimal padding
        
        # Logo and title section
        logo_title_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        logo_title_frame.pack(fill=tk.X)
        
        # Logo placeholder (will be replaced with actual logo) - Ultra compact
        self.logo_placeholder = tk.Label(
            logo_title_frame,
            text="🏢",
            font=("Segoe UI", 16),  # Reduced from 24 for compactness
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        self.logo_placeholder.pack(side=tk.LEFT, padx=(0, 4))  # Ultra minimal spacing
        
        # Title section
        title_section = tk.Frame(logo_title_frame, bg=COLORS['CARD'])
        title_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Main title
        main_title = tk.Label(
            title_section,
            text=UIConfig.WINDOW_TITLE,
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        main_title.pack(anchor=tk.W)
        
        # Subtitle
        subtitle = tk.Label(
            title_section,
            text=AppInfo.DESCRIPTION,
            font=UIConfig.FONT_SUBHEADER,
            fg=COLORS['INFO'],
            bg=COLORS['CARD']
        )
        subtitle.pack(anchor=tk.W, pady=(0, 0))  # Ultra minimal spacing

        # Separator - Ultra compact
        ttk.Separator(self.parent, orient='horizontal', style='Modern.TSeparator').pack(fill=tk.X, pady=(0, 3))
    
    def _load_logo_async(self):
        """Load the logo asynchronously."""
        try:
            logo_path = get_logo_path()
            
            if not os.path.exists(logo_path):
                self.logger.warning(f"Logo file not found: {logo_path}")
                return
            
            Image, ImageTk = get_PIL()
            
            # Load and resize logo
            image = Image.open(logo_path)
            image = image.resize((120, 50), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(image)
            
            # Replace placeholder with actual logo
            if self.logo_placeholder:
                self.logo_placeholder.configure(image=self.logo_image)
                self.logger.info("Logo loaded successfully")
                
        except Exception as e:
            self.logger.warning(f"Failed to load logo: {e}")


class FooterSection:
    """Footer section component with copyright information."""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the footer section.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self._create_footer()
    
    def _create_footer(self):
        """Create the footer UI elements."""
        # Separator before footer - Ultra compact
        ttk.Separator(self.parent, orient='horizontal', style='Modern.TSeparator').pack(fill=tk.X, pady=(3, 0))

        # Footer frame - Ultra compact
        footer_frame = tk.Frame(self.parent, bg=COLORS['BG'])
        footer_frame.pack(fill=tk.X, pady=(3, 2))  # Ultra minimal spacing
        
        # Footer content
        footer_content = tk.Frame(footer_frame, bg=COLORS['BG'])
        footer_content.pack()
        
        # Copyright text
        tk.Label(
            footer_content,
            text=AppInfo.COPYRIGHT,
            font=("Segoe UI", 7),
            fg=COLORS['INFO'],
            bg=COLORS['BG']
        ).pack()


class StatusBar:
    """Status bar component for displaying application status."""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the status bar.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.status_label = None
        self._create_status_bar()
    
    def _create_status_bar(self):
        """Create the status bar UI elements."""
        # Status bar frame
        status_frame = tk.Frame(self.parent, bg=COLORS['LIGHT'], relief='sunken', bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="Prêt",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['LIGHT'],
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=2, pady=1)  # Ultra minimal padding
    
    def update_status(self, message: str):
        """
        Update the status bar message.
        
        Args:
            message: Status message to display
        """
        if self.status_label:
            self.status_label.config(text=message)
    
    def show_progress(self, message: str):
        """
        Show a progress message.
        
        Args:
            message: Progress message
        """
        self.update_status(f"⏳ {message}")
    
    def show_success(self, message: str):
        """
        Show a success message.
        
        Args:
            message: Success message
        """
        self.update_status(f"✅ {message}")
    
    def show_error(self, message: str):
        """
        Show an error message.
        
        Args:
            message: Error message
        """
        self.update_status(f"❌ {message}")
    
    def show_warning(self, message: str):
        """
        Show a warning message.
        
        Args:
            message: Warning message
        """
        self.update_status(f"⚠️ {message}")


class InfoPanel:
    """Information panel for displaying help or status information."""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the info panel.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.panel_frame = None
        self.info_label = None
        self._create_panel()
    
    def _create_panel(self):
        """Create the info panel UI elements."""
        self.panel_frame = tk.Frame(self.parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        
        # Info content
        info_content = tk.Frame(self.panel_frame, bg=COLORS['LIGHT'])
        info_content.pack(fill=tk.X, padx=8, pady=4)
        
        # Info icon
        tk.Label(
            info_content,
            text="ℹ️",
            font=("Segoe UI", 10),
            fg=COLORS['SECONDARY'],
            bg=COLORS['LIGHT']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Info text
        self.info_label = tk.Label(
            info_content,
            text="",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['LIGHT'],
            wraplength=400,
            justify=tk.LEFT
        )
        self.info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def show(self, message: str):
        """
        Show the info panel with a message.
        
        Args:
            message: Message to display
        """
        self.info_label.config(text=message)
        self.panel_frame.pack(fill=tk.X, pady=(0, 5))
    
    def hide(self):
        """Hide the info panel."""
        self.panel_frame.pack_forget()
    
    def update_message(self, message: str):
        """
        Update the info panel message.
        
        Args:
            message: New message to display
        """
        if self.info_label:
            self.info_label.config(text=message)

"""
UI styling and theme management for the Suivi Generator application.
"""

import tkinter as tk
from tkinter import ttk
import logging
import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig

logger = logging.getLogger(__name__)


class StyleManager:
    """Manages UI styles and themes for the application."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the style manager.
        
        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.style = ttk.Style()
        self.logger = logging.getLogger(__name__)
    
    def setup_styles(self):
        """Set up all application styles."""
        try:
            self._setup_base_theme()
            self._setup_button_styles()
            self._setup_frame_styles()
            self._setup_separator_styles()
            self.logger.info("UI styles configured successfully")
        except Exception as e:
            self.logger.error(f"Error setting up styles: {e}")
    
    def _setup_base_theme(self):
        """Set up the base theme."""
        try:
            self.style.theme_use('clam')
            self.logger.debug("Base theme 'clam' applied")
        except Exception as e:
            self.logger.warning(f"Failed to set base theme: {e}")
    
    def _setup_button_styles(self):
        """Set up button styles - Sofrecom inspired."""
        # Primary button style (Bleu Sofrecom) - Maximum compact
        self.style.configure('Primary.TButton',
                           background=COLORS['PRIMARY'],
                           foreground='white',
                           font=UIConfig.FONT_BUTTON,
                           padding=(4, 2),  # Ultra minimal padding
                           relief='flat',
                           borderwidth=0,
                           focuscolor='none')

        self.style.map('Primary.TButton',
                      background=[('active', COLORS['PRIMARY_LIGHT']),
                                ('pressed', COLORS['PRIMARY_DARK'])],
                      relief=[('pressed', 'flat')])

        # Secondary button style (Orange Sofrecom) - Maximum compact
        self.style.configure('Secondary.TButton',
                           background=COLORS['SECONDARY'],
                           foreground='white',
                           font=UIConfig.FONT_BUTTON,
                           padding=(4, 2),  # Ultra minimal padding
                           relief='flat',
                           borderwidth=0,
                           focuscolor='none')

        self.style.map('Secondary.TButton',
                      background=[('active', COLORS['SECONDARY_LIGHT']),
                                ('pressed', '#E55A00')])

        # Success button style - Maximum compact
        self.style.configure('Success.TButton',
                           background=COLORS['SUCCESS'],
                           foreground='white',
                           font=UIConfig.FONT_BUTTON,
                           padding=(4, 2),  # Ultra minimal padding
                           relief='flat',
                           borderwidth=0,
                           focuscolor='none')

        self.style.map('Success.TButton',
                      background=[('active', '#34CE57'),
                                ('pressed', '#1E7E34')])

        # Outline button style (moderne) - Maximum compact
        self.style.configure('Outline.TButton',
                           background=COLORS['WHITE'],
                           foreground=COLORS['PRIMARY'],
                           font=UIConfig.FONT_BUTTON,
                           padding=(4, 2),  # Ultra minimal padding
                           relief='solid',
                           borderwidth=1,
                           focuscolor='none')

        self.style.map('Outline.TButton',
                      background=[('active', COLORS['ACCENT']),
                                ('pressed', COLORS['PRIMARY_LIGHT'])],
                      foreground=[('active', COLORS['PRIMARY_DARK'])])

        # Compact button style for module headers - Maximum compact
        self.style.configure('Compact.TButton',
                           background=COLORS['SECONDARY'],
                           foreground='white',
                           font=UIConfig.FONT_SMALL,
                           padding=(3, 1),  # Ultra minimal padding
                           relief='flat',
                           borderwidth=0,
                           focuscolor='none')

        self.style.map('Compact.TButton',
                      background=[('active', COLORS['SECONDARY_LIGHT']),
                                ('pressed', '#E55A00')])

        # Compact warning button style - Maximum compact
        self.style.configure('CompactWarning.TButton',
                           background=COLORS['WARNING'],
                           foreground='white',
                           font=UIConfig.FONT_SMALL,
                           padding=(3, 1),  # Ultra minimal padding
                           relief='flat',
                           borderwidth=0,
                           focuscolor='none')

        self.style.map('CompactWarning.TButton',
                      background=[('active', '#FFD54F'),
                                ('pressed', '#FFA000')])
    
    def _setup_frame_styles(self):
        """Set up frame styles - Sofrecom inspired."""
        # Card style for modern frames
        self.style.configure('Card.TLabelframe',
                           background=COLORS['CARD'],
                           borderwidth=1,
                           relief='solid',
                           bordercolor=COLORS['BORDER'])

        self.style.configure('Card.TLabelframe.Label',
                           background=COLORS['CARD'],
                           foreground=COLORS['PRIMARY'],
                           font=UIConfig.FONT_CARD_TITLE)

        # Modern card style without label
        self.style.configure('ModernCard.TFrame',
                           background=COLORS['CARD'],
                           borderwidth=1,
                           relief='solid',
                           bordercolor=COLORS['BORDER'])
    
    def _setup_separator_styles(self):
        """Set up separator styles."""
        self.style.configure('Modern.TSeparator',
                           background=COLORS['BORDER'])


def create_card_frame(parent: tk.Widget, bg_color: str = None, shadow: bool = True) -> tk.Frame:
    """
    Create a modern card-style frame - Sofrecom inspired.

    Args:
        parent: Parent widget
        bg_color: Background color (defaults to COLORS['CARD'])
        shadow: Whether to add shadow effect

    Returns:
        Configured frame widget
    """
    if bg_color is None:
        bg_color = COLORS['CARD']

    # Container for shadow effect
    if shadow:
        container = tk.Frame(parent, bg=parent.cget('bg'))

        # Shadow frame
        shadow_frame = tk.Frame(container, bg=COLORS['BORDER'], height=2)
        shadow_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=2, pady=2)

        # Main card frame
        frame = tk.Frame(container, bg=bg_color, relief='flat', bd=1,
                        highlightbackground=COLORS['BORDER'], highlightthickness=1)
        frame.pack(fill=tk.BOTH, expand=True)

        return container
    else:
        frame = tk.Frame(parent, bg=bg_color, relief='flat', bd=1,
                        highlightbackground=COLORS['BORDER'], highlightthickness=1)
        return frame


def create_sofrecom_card(parent: tk.Widget, title: str = "", subtitle: str = "",
                        description: str = "", icon: str = "", clickable: bool = False,
                        command: callable = None) -> tk.Frame:
    """
    Create a Sofrecom-style feature card - COMPACT VERSION.

    Args:
        parent: Parent widget
        title: Card title
        subtitle: Card subtitle
        description: Card description
        icon: Icon emoji or text
        clickable: Whether the card is clickable
        command: Command to execute on click

    Returns:
        Card frame widget
    """
    # Main card container
    card_container = tk.Frame(parent, bg=parent.cget('bg'))

    # Card frame with hover effects - MAXIMUM COMPACT
    card_frame = tk.Frame(card_container, bg=COLORS['CARD'], relief='flat', bd=0,
                         cursor='hand2' if clickable else 'arrow')
    card_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)  # Maximum compact spacing

    # Add border
    card_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

    # Card content - ULTRA MINIMAL PADDING
    content_frame = tk.Frame(card_frame, bg=COLORS['CARD'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)  # Ultra minimal padding

    # Header with icon and title - ULTRA COMPACT
    if icon or title:
        header_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X, pady=(0, 3))  # Ultra minimal padding

        if icon:
            icon_label = tk.Label(header_frame, text=icon, font=("Segoe UI", 10),  # Ultra compact icon size
                                fg=COLORS['PRIMARY'], bg=COLORS['CARD'])
            icon_label.pack(side=tk.LEFT, padx=(0, 3))  # Ultra minimal padding

        if title:
            title_label = tk.Label(header_frame, text=title, font=UIConfig.FONT_TITLE,  # Reduced font
                                 fg=COLORS['INFO'], bg=COLORS['CARD'])
            title_label.pack(side=tk.LEFT, anchor=tk.W)

    # Subtitle - COMPACT
    if subtitle:
        subtitle_label = tk.Label(content_frame, text=subtitle, font=UIConfig.FONT_SUBTITLE,  # Reduced font
                                fg=COLORS['PRIMARY'], bg=COLORS['CARD'])
        subtitle_label.pack(anchor=tk.W, pady=(0, 6))  # Reduced padding

    # Description - COMPACT
    if description:
        desc_label = tk.Label(content_frame, text=description, font=UIConfig.FONT_SMALL,  # Reduced font
                            fg=COLORS['TEXT_SECONDARY'], bg=COLORS['CARD'],
                            wraplength=280, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W, fill=tk.X)

    # Make clickable if specified
    if clickable and command:
        def on_click(event=None):
            command()

        # Bind click events to all elements
        elements = [card_frame, content_frame]
        if icon: elements.append(icon_label)
        if title: elements.append(title_label)
        if subtitle: elements.append(subtitle_label)
        if description: elements.append(desc_label)

        for element in elements:
            element.bind("<Button-1>", on_click)
            element.config(cursor='hand2')

        # Add hover effects
        _add_sofrecom_hover_effects(card_frame, content_frame, elements)

    return card_container


def _add_sofrecom_hover_effects(card_frame: tk.Widget, content_frame: tk.Widget, elements: list):
    """Add Sofrecom-style hover effects to a card."""
    def on_enter(event):
        card_frame.config(bg=COLORS['CARD_HOVER'], highlightbackground=COLORS['PRIMARY'], highlightthickness=2)
        content_frame.config(bg=COLORS['CARD_HOVER'])
        for element in elements:
            if hasattr(element, 'config'):
                element.config(bg=COLORS['CARD_HOVER'])

    def on_leave(event):
        card_frame.config(bg=COLORS['CARD'], highlightbackground=COLORS['BORDER'], highlightthickness=1)
        content_frame.config(bg=COLORS['CARD'])
        for element in elements:
            if hasattr(element, 'config'):
                element.config(bg=COLORS['CARD'])

    # Bind hover events
    for element in [card_frame, content_frame] + elements:
        element.bind("<Enter>", on_enter)
        element.bind("<Leave>", on_leave)


def create_section_header(parent: tk.Widget, icon: str, title: str, bg_color: str = None) -> tk.Frame:
    """
    Create a standardized section header - Ultra compact.

    Args:
        parent: Parent widget
        icon: Icon emoji or text
        title: Section title
        bg_color: Background color (defaults to COLORS['CARD'])

    Returns:
        Header frame widget
    """
    if bg_color is None:
        bg_color = COLORS['CARD']

    header_frame = tk.Frame(parent, bg=bg_color)

    # Icon - Ultra compact
    tk.Label(
        header_frame,
        text=icon,
        font=("Segoe UI", 8),  # Reduced from 12 for ultra compactness
        fg=COLORS['SECONDARY'],
        bg=bg_color
    ).pack(side=tk.LEFT, padx=(0, 2))  # Reduced from 5 to 2

    # Title - Ultra compact
    tk.Label(
        header_frame,
        text=title,
        font=UIConfig.FONT_TITLE,
        fg=COLORS['SECONDARY'],
        bg=bg_color
    ).pack(side=tk.LEFT)

    return header_frame


def create_form_field(parent: tk.Widget, 
                     label_text: str,
                     row: int,
                     icon: str = "",
                     placeholder: str = "",
                     readonly: bool = False,
                     required: bool = False) -> tk.Entry:
    """
    Create a standardized form field.
    
    Args:
        parent: Parent widget
        label_text: Label text
        row: Grid row position
        icon: Icon emoji or text
        placeholder: Placeholder text
        readonly: Whether field is readonly
        required: Whether field is required
        
    Returns:
        Entry widget
    """
    # Field container
    field_frame = tk.Frame(parent, bg=COLORS['CARD'])
    field_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(0, 6))
    field_frame.grid_columnconfigure(1, weight=1)
    
    # Label frame
    label_frame = tk.Frame(field_frame, bg=COLORS['CARD'])
    label_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 2))
    
    # Icon
    if icon:
        tk.Label(
            label_frame,
            text=icon,
            font=("Segoe UI", 9),
            fg=COLORS['SECONDARY'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT, padx=(0, 3))
    
    # Label
    label_color = COLORS['PRIMARY'] if required else COLORS['SECONDARY']
    label_font = UIConfig.FONT_SUBTITLE if required else UIConfig.FONT_SMALL
    
    tk.Label(
        label_frame,
        text=label_text + (" *" if required else ""),
        font=label_font,
        fg=label_color,
        bg=COLORS['CARD']
    ).pack(side=tk.LEFT)
    
    # Readonly indicator
    if readonly:
        tk.Label(
            label_frame,
            text="🔒",
            font=("Segoe UI", 7),
            fg=COLORS['INFO'],
            bg=COLORS['CARD']
        ).pack(side=tk.RIGHT)
    
    # Entry field
    entry_bg = COLORS['LIGHT'] if readonly else COLORS['WHITE']
    entry_state = 'readonly' if readonly else 'normal'
    
    entry = tk.Entry(
        field_frame,
        font=UIConfig.FONT_SMALL,
        bg=entry_bg,
        fg=COLORS['INFO'] if readonly else 'black',
        relief='flat',
        bd=1,
        state=entry_state,
        highlightthickness=1,
        highlightcolor=COLORS['PRIMARY'],
        highlightbackground=COLORS['BORDER']
    )
    entry.grid(row=1, column=0, columnspan=2, sticky=tk.EW, ipady=4)
    
    # Set placeholder if provided and readonly
    if placeholder and readonly:
        entry.config(state='normal')
        entry.insert(0, placeholder)
        entry.config(state='readonly')
    
    return entry


def create_status_indicator(parent: tk.Widget, bg_color: str = None) -> tuple:
    """
    Create a status indicator with icon and label.
    
    Args:
        parent: Parent widget
        bg_color: Background color (defaults to COLORS['LIGHT'])
        
    Returns:
        Tuple of (icon_label, text_label)
    """
    if bg_color is None:
        bg_color = COLORS['LIGHT']
    
    status_frame = tk.Frame(parent, bg=bg_color)
    status_frame.pack(fill=tk.X)
    
    icon_label = tk.Label(
        status_frame,
        text="⏳",
        font=("Segoe UI", 12),
        fg=COLORS['INFO'],
        bg=bg_color
    )
    icon_label.pack(side=tk.LEFT, padx=(0, 5))
    
    text_label = tk.Label(
        status_frame,
        text="En attente...",
        font=UIConfig.FONT_SMALL,
        fg=COLORS['INFO'],
        bg=bg_color
    )
    text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    return icon_label, text_label


def update_status_indicator(icon_label: tk.Label, 
                          text_label: tk.Label,
                          status: str,
                          message: str):
    """
    Update a status indicator.
    
    Args:
        icon_label: Icon label widget
        text_label: Text label widget
        status: Status type ('waiting', 'warning', 'success', 'error')
        message: Status message
    """
    status_config = {
        'waiting': {'icon': '⏳', 'color': COLORS['INFO']},
        'warning': {'icon': '⚠️', 'color': COLORS['WARNING']},
        'success': {'icon': '✅', 'color': COLORS['SUCCESS']},
        'error': {'icon': '❌', 'color': COLORS['DANGER']}
    }
    
    config = status_config.get(status, status_config['waiting'])
    
    icon_label.config(text=config['icon'], fg=config['color'])
    text_label.config(text=message, fg=config['color'])

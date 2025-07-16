"""
Splash screen for Pladria application.

This module provides a professional splash screen that loads dependencies
while displaying progress to the user, using the same design language as the main application.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import logging
from pathlib import Path
import os

# Defer heavy imports to avoid splash screen delay
logger = logging.getLogger(__name__)


class SplashScreen:
    """Professional splash screen with dependency loading and progress tracking."""
    
    def __init__(self, on_complete_callback=None):
        """
        Initialize the splash screen.
        
        Args:
            on_complete_callback: Function to call when loading is complete
        """
        self.on_complete_callback = on_complete_callback
        self.root = None
        self.progress_var = None
        self.status_var = None
        self.loading_complete = False
        self.error_occurred = False
        self.error_message = ""
        
        # Simplified loading steps for faster startup
        self.loading_steps = [
            ("Initialisation...", self._init_environment),
            ("Chargement Des Bibliothèques...", self._load_dependencies_fast),
            ("Finalisation...", self._finalize_loading)
        ]
        
        self.current_step = 0
        self.total_steps = len(self.loading_steps)
        
        self.logger = logging.getLogger(__name__)
    
    def show(self):
        """Display the splash screen and start loading."""
        self._create_splash_window()

        # Show the splash screen immediately
        self.root.update()
        self.root.update_idletasks()

        # Small delay to ensure splash is visible before starting loading
        self.root.after(100, self._start_loading)
        self.root.mainloop()
    
    def _create_splash_window(self):
        """Create and configure the splash screen window."""
        # Import colors here to avoid delay at module load
        from config.constants import COLORS

        self.root = tk.Tk()
        self.root.title("Pladria")

        # Window configuration - smaller for faster display
        window_width = 400
        window_height = 250

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.configure(bg=COLORS['WHITE'])

        # Set icon for splash screen
        self._set_splash_icon()

        self._create_splash_content()

        # Add subtle shadow effect
        self.root.wm_attributes("-topmost", True)
    
    def _create_splash_content(self):
        """Create the splash screen content with Sofrecom design language."""
        # Import constants here to avoid delay at module load
        from config.constants import COLORS, UIConfig, AppInfo

        # Main container with border
        main_frame = tk.Frame(
            self.root,
            bg=COLORS['WHITE'],
            relief='solid',
            bd=1,
            highlightbackground=COLORS['BORDER'],
            highlightthickness=1
        )
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Header section - smaller for faster display
        header_frame = tk.Frame(main_frame, bg=COLORS['PRIMARY'], height=60)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)

        # App title only (no icon for faster loading)
        title_label = tk.Label(
            header_frame,
            text="Pladria",
            font=("Segoe UI", 18, "bold"),
            fg=COLORS['WHITE'],
            bg=COLORS['PRIMARY']
        )
        title_label.pack(pady=15)

        # Content area - reduced padding for smaller size
        content_frame = tk.Frame(main_frame, bg=COLORS['WHITE'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Loading status
        self.status_var = tk.StringVar(value="Initialisation...")
        status_label = tk.Label(
            content_frame,
            textvariable=self.status_var,
            font=UIConfig.FONT_SUBHEADER,
            fg=COLORS['INFO'],
            bg=COLORS['WHITE']
        )
        status_label.pack(pady=(20, 10))

        # Progress bar with Sofrecom styling
        progress_frame = tk.Frame(content_frame, bg=COLORS['WHITE'])
        progress_frame.pack(fill='x', pady=(0, 20))

        # Custom progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Sofrecom.Horizontal.TProgressbar",
            background=COLORS['PRIMARY'],
            troughcolor=COLORS['LIGHT'],
            borderwidth=0,
            lightcolor=COLORS['PRIMARY'],
            darkcolor=COLORS['PRIMARY']
        )

        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="Sofrecom.Horizontal.TProgressbar",
            length=300
        )
        progress_bar.pack()

        # Progress percentage
        self.progress_text_var = tk.StringVar(value="0%")
        progress_text = tk.Label(
            content_frame,
            textvariable=self.progress_text_var,
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['WHITE']
        )
        progress_text.pack(pady=(5, 0))

        # Footer with version and copyright
        footer_frame = tk.Frame(main_frame, bg=COLORS['LIGHT'], height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        footer_content = tk.Frame(footer_frame, bg=COLORS['LIGHT'])
        footer_content.pack(expand=True, fill='both')

        version_label = tk.Label(
            footer_content,
            text=f"Version {AppInfo.VERSION} - {AppInfo.COPYRIGHT}",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_MUTED'],
            bg=COLORS['LIGHT']
        )
        version_label.pack(pady=10)
    
    # Icon loading removed for faster startup
    
    def _start_loading(self):
        """Start the dependency loading process in a separate thread."""
        loading_thread = threading.Thread(target=self._load_dependencies, daemon=True)
        loading_thread.start()
    
    def _load_dependencies(self):
        """Load all dependencies with progress updates."""
        try:
            for i, (status_text, load_function) in enumerate(self.loading_steps):
                self.current_step = i
                
                # Update status
                self.root.after(0, lambda text=status_text: self.status_var.set(text))
                
                # Update progress
                progress = (i / self.total_steps) * 100
                self.root.after(0, lambda p=progress: self._update_progress(p))
                
                # Execute loading step
                try:
                    load_function()
                    # No artificial delay for faster startup
                except Exception as e:
                    self.logger.error(f"Error in loading step '{status_text}': {e}")
                    self.error_occurred = True
                    self.error_message = f"Erreur lors du chargement: {str(e)}"
                    break

            # Final progress update
            if not self.error_occurred:
                self.root.after(0, lambda: self._update_progress(100))
                self.root.after(0, lambda: self.status_var.set("Chargement terminé!"))
                # No delay for faster startup
                self.loading_complete = True
            
            # Close splash screen and start main app
            self.root.after(100, self._finish_loading)
            
        except Exception as e:
            self.logger.error(f"Critical error during loading: {e}")
            self.error_occurred = True
            self.error_message = f"Erreur critique: {str(e)}"
            self.root.after(0, self._show_error)
    
    def _update_progress(self, value):
        """Update the progress bar and percentage text."""
        self.progress_var.set(value)
        self.progress_text_var.set(f"{int(value)}%")
        self.root.update_idletasks()
    
    def _finish_loading(self):
        """Finish loading and close splash screen."""
        if self.error_occurred:
            self._show_error()
        else:
            self.root.destroy()
            if self.on_complete_callback:
                self.on_complete_callback()
    
    def _show_error(self):
        """Show error message and close application."""
        import tkinter.messagebox as messagebox
        messagebox.showerror(
            "Erreur de chargement",
            f"Impossible de charger l'application:\n\n{self.error_message}\n\nVeuillez vérifier que toutes les dépendances sont installées."
        )
        self.root.destroy()

    # Loading step implementations

    def _init_environment(self):
        """Initialize the application environment."""
        from utils.logging_config import setup_logging, configure_third_party_loggers
        from config.constants import AppInfo

        setup_logging(log_level="INFO", log_to_file=True)
        configure_third_party_loggers()

        # Log application startup information
        logger = logging.getLogger(__name__)
        logger.info("=" * 60)
        logger.info(f"Starting {AppInfo.DESCRIPTION}")
        logger.info(f"Version: {AppInfo.VERSION}")
        logger.info(f"Author: {AppInfo.AUTHOR}")
        logger.info("=" * 60)

    def _load_dependencies_fast(self):
        """Load all dependencies quickly in one step."""
        from utils.lazy_imports import _import_cache

        # Load all dependencies at once for faster startup
        import pandas as pd
        from PIL import Image, ImageTk
        import openpyxl

        # Store in global cache for lazy imports
        _import_cache['pandas'] = pd
        _import_cache['PIL_Image'] = Image
        _import_cache['PIL_ImageTk'] = ImageTk
        _import_cache['openpyxl'] = openpyxl

    def _setup_modules(self):
        """Set up application modules."""
        # Pre-load any other necessary modules
        pass

    def _finalize_loading(self):
        """Finalize the loading process."""
        # Any final setup steps
        pass

    def _set_splash_icon(self):
        """Set the splash screen icon."""
        try:
            from utils.file_utils import ensure_valid_icon
            import os

            # Get a valid icon path
            icon_path = ensure_valid_icon()

            if os.path.exists(icon_path) and icon_path.lower().endswith('.ico'):
                self.root.iconbitmap(icon_path)
                self.logger.debug(f"Splash icon set: {os.path.basename(icon_path)}")
            else:
                # For PNG files or if ICO fails, use PIL
                try:
                    from utils.lazy_imports import get_PIL
                    Image, ImageTk = get_PIL()

                    with Image.open(icon_path) as img:
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')

                        # Create a small icon for splash
                        resized = img.resize((32, 32), Image.Resampling.LANCZOS)
                        icon_image = ImageTk.PhotoImage(resized)
                        self.root.iconphoto(True, icon_image)

                        # Keep reference
                        self.root._splash_icon = icon_image

                        self.logger.debug(f"Splash icon set (PNG): {os.path.basename(icon_path)}")

                except Exception as e:
                    self.logger.debug(f"Could not set splash icon: {e}")

        except Exception as e:
            self.logger.debug(f"Failed to set splash icon: {e}")
            # Don't fail splash screen for icon issues



"""
Main window class for the Suivi Generator platform.
Now serves as the application shell with navigation system.
"""

import tkinter as tk
from tkinter import messagebox
import logging
import os
from typing import Optional

import sys
from pathlib import Path

# Ensure src directory is in path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.constants import COLORS, UIConfig
from utils.file_utils import get_icon_path
from utils.lazy_imports import get_PIL
from .styles import StyleManager
from .responsive_utils import get_responsive_manager
from .navigation import NavigationManager, NavigationState
from .home_screen import HomeScreen
from .settings_screen import SettingsScreen
from .modules import SuiviGeneratorModule, SuiviGlobalModule, TeamStatsModule, DataViewerModule, QualityControlModule

logger = logging.getLogger(__name__)


class MainWindow:
    """Main application window with navigation system."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the main window.

        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.logger = logging.getLogger(__name__)

        # Responsive management
        self.responsive_manager = get_responsive_manager(root)

        # Navigation system
        self.navigation_manager = None

        # UI components
        self.style_manager = None

        self._setup_window()
        self._setup_responsive_fonts()
        self._setup_navigation()

        # Post-initialization
        self.root.after(10, self._post_init)
    
    def _setup_window(self):
        """Set up the main window properties with responsive sizing."""
        self.root.title("Pladria - Sofrecom")

        # Get responsive minimum size
        min_width, min_height = self.responsive_manager.get_minimum_window_size()

        # Configure basic window properties with responsive sizing
        self.root.minsize(min_width, min_height)
        self.root.configure(bg=COLORS['BG'])
        self.root.resizable(True, True)

        # Bind window resize events for responsive updates
        self.root.bind('<Configure>', self._on_window_configure)

        # Lancer en plein écran (maximisé) - improved state management
        try:
            # For Windows
            self.root.state('zoomed')
            self.logger.info("Window maximized using 'zoomed' state")
        except:
            try:
                # For Linux
                self.root.attributes('-zoomed', True)
                self.logger.info("Window maximized using '-zoomed' attribute")
            except:
                try:
                    # For macOS - use normal maximized geometry
                    self.root.geometry("1200x800")
                    # Try to maximize after geometry is set
                    self.root.after(50, lambda: self.root.state('zoomed'))
                    self.logger.info("Window set to large size with delayed maximization")
                except:
                    # Final fallback
                    self.root.geometry("1200x800")
                    self.logger.warning("Using fallback window size")

        # Set window icon with delay to ensure window is ready
        self.root.after(100, self._set_window_icon)

        # Initialize style manager
        self.style_manager = StyleManager(self.root)
        self.style_manager.setup_styles()

        self.logger.info("Main window configured")

    def _setup_navigation(self):
        """Set up the navigation system."""
        # Create navigation manager
        self.navigation_manager = NavigationManager(self.root)

        # Register modules
        self.navigation_manager.register_module(
            NavigationState.SUIVI_GENERATOR,
            SuiviGeneratorModule,
            "Générateur Suivi",
            "Traitement MOAI et QGis"
        )

        self.navigation_manager.register_module(
            NavigationState.SUIVI_GLOBAL,
            SuiviGlobalModule,
            "Suivi Global Tickets",
            "Agrégation des suivis de communes"
        )

        self.navigation_manager.register_module(
            NavigationState.TEAM_STATS,
            TeamStatsModule,
            "Statistiques Équipe",
            "Tableau de bord des performances de l'équipe"
        )

        self.navigation_manager.register_module(
            NavigationState.DATA_VIEWER,
            DataViewerModule,
            "Visualiseur de Données",
            "Visualisation des données global tickets"
        )

        self.navigation_manager.register_module(
            NavigationState.QUALITY_CONTROL,
            QualityControlModule,
            "Contrôle Qualité",
            "Système d'analyse et de validation de la qualité des données"
        )

        # Register callbacks for simple screens
        self.navigation_manager.register_callback(
            NavigationState.HOME,
            self._show_home_screen
        )

        self.navigation_manager.register_callback(
            NavigationState.ABOUT,
            self._show_about_screen
        )

        # Start with home screen
        self.navigation_manager.navigate_to(NavigationState.HOME)

        self.logger.info("Navigation system initialized")
    
    def _show_home_screen(self):
        """Show the home screen."""
        content_frame = self.navigation_manager.get_content_frame()
        HomeScreen(content_frame, self.navigation_manager)
        self.navigation_manager.set_window_title("Accueil")

    def _show_about_screen(self):
        """Show the about screen."""
        content_frame = self.navigation_manager.get_content_frame()
        SettingsScreen(content_frame, self.navigation_manager)
        self.navigation_manager.set_window_title("À propos")
    
    def _post_init(self):
        """Post-initialization tasks."""
        # Only center window if not maximized
        current_state = self.root.state()
        self.logger.info(f"Window state after initialization: {current_state}")

        if current_state != 'zoomed':
            self._center_window()
        else:
            # Ensure the window layout is properly updated for maximized state
            self.root.update_idletasks()

        self.logger.info("Main window initialization complete")

    def _setup_responsive_fonts(self):
        """Set up responsive font scaling."""
        try:
            UIConfig.update_responsive_fonts(self.responsive_manager)
            self.logger.info("Responsive fonts configured")
        except Exception as e:
            self.logger.warning(f"Failed to setup responsive fonts: {e}")

    def _on_window_configure(self, event):
        """Handle window resize events for responsive updates."""
        try:
            # Only handle root window events
            if event.widget != self.root:
                return

            # Update screen dimensions
            self.responsive_manager._update_screen_dimensions()

            # Check if we need to update layout based on new size
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()

            # Log significant size changes
            if hasattr(self, '_last_width') and hasattr(self, '_last_height'):
                width_change = abs(current_width - self._last_width)
                height_change = abs(current_height - self._last_height)

                # Only update if significant change (avoid excessive updates)
                if width_change > 50 or height_change > 50:
                    self._update_responsive_layout()

            self._last_width = current_width
            self._last_height = current_height

        except Exception as e:
            self.logger.debug(f"Error in window configure handler: {e}")

    def _update_responsive_layout(self):
        """Update layout based on current window size."""
        try:
            # Update font scaling if DPI changed
            self.responsive_manager._detect_dpi_scaling()
            UIConfig.update_responsive_fonts(self.responsive_manager)

            # Notify navigation manager of layout change if it exists
            if hasattr(self, 'navigation_manager') and self.navigation_manager:
                # The navigation manager can handle responsive updates for current module
                pass

            self.logger.debug("Responsive layout updated")

        except Exception as e:
            self.logger.warning(f"Error updating responsive layout: {e}")

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _set_window_icon(self):
        """Set the window icon with Windows-specific optimizations for crisp display."""
        try:
            from utils.file_utils import get_resource_path
            import os

            # Try multiple approaches for Windows taskbar icon quality

            # Method 1: Try the PNG with iconphoto first (often works better for high DPI)
            png_path = get_resource_path("Icone_App.png")
            if os.path.exists(png_path):
                try:
                    Image, ImageTk = get_PIL()
                    with Image.open(png_path) as img:
                        # Convert to RGBA for better quality
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')

                        # Create specific sizes that Windows expects for taskbar
                        # Windows taskbar typically uses 16x16, 24x24, 32x32, 48x48
                        taskbar_sizes = [16, 24, 32, 48, 64, 128, 256]
                        icon_images = []

                        for size in taskbar_sizes:
                            # Use high-quality resampling
                            resized = img.resize((size, size), Image.Resampling.LANCZOS)
                            icon_images.append(ImageTk.PhotoImage(resized))

                        # Set the icon with all sizes
                        self.root.iconphoto(True, *icon_images)

                        # Keep references to prevent garbage collection
                        self.root._icon_images = icon_images

                        self.logger.info(f"Window icon set with PNG multi-size: {len(icon_images)} sizes")

                        # Also try setting iconbitmap if ICO exists for Windows compatibility
                        ico_path = get_resource_path("Icone_App_Sharp.ico")
                        if os.path.exists(ico_path):
                            try:
                                self.root.iconbitmap(ico_path)
                                self.logger.info("Additional ICO icon set for Windows compatibility")

                                # Try Windows-specific icon setting for taskbar
                                self._set_windows_taskbar_icon(ico_path)

                            except Exception as e:
                                self.logger.debug(f"ICO fallback failed: {e}")

                        return

                except Exception as e:
                    self.logger.warning(f"PNG icon method failed: {e}")

            # Method 2: Fallback to ICO only
            ico_path = get_resource_path("Icone_App_Sharp.ico")
            if os.path.exists(ico_path):
                try:
                    self.root.iconbitmap(ico_path)
                    self.logger.info(f"Window icon set with ICO fallback: {os.path.basename(ico_path)}")
                    return
                except Exception as e:
                    self.logger.warning(f"ICO icon method failed: {e}")

            # Method 3: Last resort - try to create a simple icon
            self.logger.warning("All icon methods failed, using text fallback")
            self.root.iconname("Pladria")

        except Exception as e:
            self.logger.error(f"Critical failure setting window icon: {e}")
            try:
                self.root.iconname("Pladria")
            except:
                pass

    def _set_windows_taskbar_icon(self, ico_path: str):
        """Set Windows taskbar icon using Windows API for maximum quality."""
        try:
            import platform
            if platform.system() != 'Windows':
                return

            import ctypes
            from ctypes import wintypes

            # Get window handle
            hwnd = self.root.winfo_id()

            # Load icon from file
            hicon = ctypes.windll.user32.LoadImageW(
                None,                    # hInst
                ico_path,               # name
                1,                      # IMAGE_ICON
                0,                      # cx (0 = default size)
                0,                      # cy (0 = default size)
                0x00000010 | 0x00000040 # LR_LOADFROMFILE | LR_DEFAULTSIZE
            )

            if hicon:
                # Set both small and large icons for taskbar
                ctypes.windll.user32.SendMessageW(
                    hwnd, 0x0080, 0, hicon  # WM_SETICON, ICON_SMALL
                )
                ctypes.windll.user32.SendMessageW(
                    hwnd, 0x0080, 1, hicon  # WM_SETICON, ICON_BIG
                )

                self.logger.info("Windows taskbar icon set via API")
            else:
                self.logger.debug("Failed to load icon via Windows API")

        except Exception as e:
            self.logger.debug(f"Windows API icon setting failed: {e}")
            # This is optional, so don't fail the application

    def run(self):
        """Start the application main loop."""
        self.logger.info("Starting application main loop")
        self.root.mainloop()

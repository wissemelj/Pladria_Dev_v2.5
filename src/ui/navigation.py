"""
Navigation system for the multi-feature Suivi Generator platform.
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, Callable, Optional, Any
from enum import Enum

from config.constants import COLORS, UIConfig, AppInfo
from ui.styles import create_card_frame

logger = logging.getLogger(__name__)


class NavigationState(Enum):
    """Navigation states for the application."""
    HOME = "home"
    SUIVI_GENERATOR = "suivi_generator"
    SUIVI_GLOBAL = "suivi_global"
    TEAM_STATS = "team_stats"
    DATA_VIEWER = "data_viewer"
    QUALITY_CONTROL = "quality_control"
    ABOUT = "about"


class NavigationManager:
    """Manages navigation between different application modules."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the navigation manager.
        
        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.current_state = NavigationState.HOME
        self.previous_state = None
        self.navigation_history = []
        self.modules = {}
        self.callbacks = {}
        self.logger = logging.getLogger(__name__)
        
        # Navigation frame (always visible)
        self.nav_frame = None
        self.content_frame = None
        self.breadcrumb_frame = None
        
        self._setup_navigation_ui()
    
    def _setup_navigation_ui(self):
        """Set up the navigation UI structure."""
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['BG'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Navigation bar (top) - INCREASED HEIGHT
        self.nav_frame = tk.Frame(main_container, bg=COLORS['CARD'], height=60)  # Increased from 50
        self.nav_frame.pack(fill=tk.X, side=tk.TOP)
        self.nav_frame.pack_propagate(False)
        
        # Breadcrumb frame - INCREASED HEIGHT for better visibility
        self.breadcrumb_frame = tk.Frame(main_container, bg=COLORS['LIGHT'], height=35)  # Increased to 35
        self.breadcrumb_frame.pack(fill=tk.X, side=tk.TOP)
        self.breadcrumb_frame.pack_propagate(False)
        
        # Content frame (main area)
        self.content_frame = tk.Frame(main_container, bg=COLORS['BG'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self._setup_navigation_bar()
        self._setup_breadcrumbs()
    
    def _setup_navigation_bar(self):
        """Set up the navigation bar with menu items - Sofrecom style."""
        # Add subtle border to navigation
        self.nav_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Left side - Logo and title
        left_frame = tk.Frame(self.nav_frame, bg=COLORS['CARD'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15)

        # Try to load Sofrecom logo for navigation
        try:
            from utils.file_utils import get_resource_path
            from PIL import Image, ImageTk
            import os

            logo_path = get_resource_path("logo_Sofrecom.png")
            if os.path.exists(logo_path):
                # Load and resize logo for navigation
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((60, 20), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)

                logo_label = tk.Label(
                    left_frame,
                    image=logo_photo,
                    bg=COLORS['CARD']
                )
                logo_label.image = logo_photo  # Keep a reference
                logo_label.pack(side=tk.LEFT, pady=15, padx=(0, 15))

                self.logger.info(f"Sofrecom logo loaded successfully from: {logo_path}")
            else:
                self.logger.warning(f"Sofrecom logo not found at: {logo_path}")
                # Fallback logo
                logo_label = tk.Label(
                    left_frame,
                    text="🔷",
                    font=("Segoe UI", 14),
                    fg=COLORS['PRIMARY'],
                    bg=COLORS['CARD']
                )
                logo_label.pack(side=tk.LEFT, pady=15, padx=(0, 10))
        except Exception as e:
            self.logger.error(f"Error loading Sofrecom logo: {e}")
            # Fallback logo
            logo_label = tk.Label(
                left_frame,
                text="🔷",
                font=("Segoe UI", 14),
                fg=COLORS['PRIMARY'],
                bg=COLORS['CARD']
            )
            logo_label.pack(side=tk.LEFT, pady=15, padx=(0, 10))

        # Title with Sofrecom styling
        title_label = tk.Label(
            left_frame,
            text="Pladria",
            font=UIConfig.FONT_CARD_TITLE,
            fg=COLORS['INFO'],
            bg=COLORS['CARD']
        )
        title_label.pack(side=tk.LEFT, pady=15)
        
        # Right side - Navigation buttons with Sofrecom styling - BETTER VISIBILITY
        right_frame = tk.Frame(self.nav_frame, bg=COLORS['CARD'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)  # Increased padding

        # About button (Sofrecom style) - BETTER VISIBILITY
        about_btn = ttk.Button(
            right_frame,
            text="À propos",
            command=lambda: self.navigate_to(NavigationState.ABOUT),
            style='Outline.TButton'
        )
        about_btn.pack(side=tk.RIGHT, padx=(8, 0), pady=12)  # Better vertical centering

        # Home button (Sofrecom style) - BETTER VISIBILITY
        home_btn = ttk.Button(
            right_frame,
            text="Accueil",
            command=lambda: self.navigate_to(NavigationState.HOME),
            style='Primary.TButton'
        )
        home_btn.pack(side=tk.RIGHT, padx=(0, 8), pady=12)  # Better vertical centering
    
    def _setup_breadcrumbs(self):
        """Set up the breadcrumb navigation - Sofrecom style."""
        # Add subtle border to breadcrumb
        self.breadcrumb_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        self.breadcrumb_label = tk.Label(
            self.breadcrumb_frame,
            text="Accueil",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['LIGHT'],
            anchor=tk.W
        )
        self.breadcrumb_label.pack(side=tk.LEFT, padx=15, pady=10, fill=tk.X, expand=True)  # Increased pady to 10

        # Back button removed - redundant with Home button
    
    def register_module(self, state: NavigationState, module_class, title: str, description: str = ""):
        """
        Register a module for navigation.
        
        Args:
            state: Navigation state for this module
            module_class: Class to instantiate for this module
            title: Display title for the module
            description: Description of the module
        """
        self.modules[state] = {
            'class': module_class,
            'title': title,
            'description': description,
            'instance': None
        }
        self.logger.info(f"Registered module: {title} ({state.value})")
    
    def register_callback(self, state: NavigationState, callback: Callable):
        """
        Register a callback for a navigation state.
        
        Args:
            state: Navigation state
            callback: Function to call when navigating to this state
        """
        self.callbacks[state] = callback
    
    def navigate_to(self, state: NavigationState, **kwargs):
        """
        Navigate to a specific state.

        Args:
            state: Target navigation state
            **kwargs: Additional arguments to pass to the module
        """
        try:
            self.logger.info(f"Attempting to navigate to: {state.value}")

            # Store previous state for back navigation
            if self.current_state != state:
                self.previous_state = self.current_state
                self.navigation_history.append(self.current_state)

            self.current_state = state

            # Clear content frame completely
            self.logger.debug("Clearing content frame...")
            try:
                if hasattr(self, 'content_frame') and self.content_frame and self.content_frame.winfo_exists():
                    for widget in self.content_frame.winfo_children():
                        if widget.winfo_exists():
                            widget.destroy()
                    # Force update to ensure clearing is complete
                    self.content_frame.update()
            except tk.TclError as e:
                self.logger.warning(f"Erreur lors du nettoyage (widgets détruits): {e}")
            except Exception as e:
                self.logger.error(f"Erreur inattendue lors du nettoyage: {e}")

            # Update breadcrumbs
            self._update_breadcrumbs()

            # Load the appropriate content
            if state in self.modules:
                self.logger.debug(f"Loading module for state: {state.value}")
                self._load_module(state, **kwargs)
            elif state in self.callbacks:
                self.logger.debug(f"Calling callback for state: {state.value}")
                self.callbacks[state](**kwargs)
            else:
                self.logger.warning(f"No handler for navigation state: {state}")
                self._show_error_message(f"Aucun gestionnaire trouvé pour: {state.value}")

            # Force update to ensure content is displayed
            self.content_frame.update()
            self.root.update()

            self.logger.info(f"Successfully navigated to: {state.value}")

        except Exception as e:
            self.logger.error(f"Navigation error: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")

            # Clear any partial content
            try:
                if hasattr(self, 'content_frame') and self.content_frame and self.content_frame.winfo_exists():
                    for widget in self.content_frame.winfo_children():
                        if widget.winfo_exists():
                            widget.destroy()
            except tk.TclError as e:
                self.logger.warning(f"Erreur lors du nettoyage d'erreur (widgets détruits): {e}")
            except Exception as e:
                self.logger.error(f"Erreur inattendue lors du nettoyage d'erreur: {e}")

            # Show error and fallback to home
            self._show_detailed_error_message("Erreur de navigation", str(e))

            # Don't recursively call navigate_to to avoid infinite loops
            if state != NavigationState.HOME:
                self.root.after(1000, lambda: self.navigate_to(NavigationState.HOME))
    
    def _load_module(self, state: NavigationState, **kwargs):
        """Load a registered module."""
        module_info = self.modules[state]

        try:
            self.logger.info(f"Loading module: {state.value} ({module_info['title']})")

            # Always create a new instance for simplicity and reliability
            # This ensures we don't have stale state issues
            self.logger.debug(f"Creating new instance of {module_info['class'].__name__}")

            # Clean up old instance if it exists
            if module_info['instance'] is not None:
                try:
                    if hasattr(module_info['instance'], 'cleanup'):
                        module_info['instance'].cleanup()
                except Exception as cleanup_error:
                    self.logger.warning(f"Error during module cleanup: {cleanup_error}")
                module_info['instance'] = None

            # Create new instance
            module_info['instance'] = module_info['class'](
                self.content_frame,
                navigation_manager=self,
                **kwargs
            )

            # Update window title
            self.set_window_title(module_info['title'])

            self.logger.info(f"Module {state.value} created and loaded successfully")

        except Exception as e:
            self.logger.error(f"Error loading module {state.value}: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")

            # Clear any partial content
            try:
                if hasattr(self, 'content_frame') and self.content_frame and self.content_frame.winfo_exists():
                    for widget in self.content_frame.winfo_children():
                        if widget.winfo_exists():
                            widget.destroy()
            except tk.TclError as e:
                self.logger.warning(f"Erreur lors du nettoyage de module (widgets détruits): {e}")
            except Exception as e:
                self.logger.error(f"Erreur inattendue lors du nettoyage de module: {e}")

            # Show detailed error message
            self._show_detailed_error_message(f"Erreur lors du chargement du module {module_info['title']}", str(e))
    
    def _update_breadcrumbs(self):
        """Update the breadcrumb display."""
        try:
            # Vérifier que le widget existe encore
            if hasattr(self, 'breadcrumb_label') and self.breadcrumb_label and self.breadcrumb_label.winfo_exists():
                breadcrumb_text = self._get_breadcrumb_text()
                self.breadcrumb_label.config(text=breadcrumb_text)
            else:
                self.logger.warning("Breadcrumb label n'existe plus, ignoré")
        except tk.TclError as e:
            self.logger.warning(f"Erreur mise à jour breadcrumbs (widget détruit): {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue mise à jour breadcrumbs: {e}")

        # Back button removed - no longer needed
    
    def _get_breadcrumb_text(self) -> str:
        """Get the breadcrumb text for current state."""
        breadcrumbs = ["Accueil"]
        
        if self.current_state == NavigationState.SUIVI_GENERATOR:
            breadcrumbs.append("Générateur Suivi")
        elif self.current_state == NavigationState.SUIVI_GLOBAL:
            breadcrumbs.append("Suivi Global Tickets")
        elif self.current_state == NavigationState.TEAM_STATS:
            breadcrumbs.append("Statistiques Équipe")
        elif self.current_state == NavigationState.DATA_VIEWER:
            breadcrumbs.append("Visualiseur de Données")
        elif self.current_state == NavigationState.QUALITY_CONTROL:
            breadcrumbs.append("Contrôle Qualité")
        elif self.current_state == NavigationState.ABOUT:
            breadcrumbs.append("À propos")
        
        return " > ".join(breadcrumbs)
    
    def go_back(self):
        """Navigate back to the previous state."""
        if self.previous_state:
            target_state = self.previous_state
            self.previous_state = None
            
            # Remove from history
            if self.navigation_history:
                self.navigation_history.pop()
            
            self.navigate_to(target_state)
    
    def get_current_state(self) -> NavigationState:
        """Get the current navigation state."""
        return self.current_state
    
    def _show_error_message(self, message: str):
        """Show an error message in the content area."""
        error_frame = tk.Frame(self.content_frame, bg=COLORS['BG'])
        error_frame.pack(fill=tk.BOTH, expand=True)

        error_label = tk.Label(
            error_frame,
            text=f"❌ {message}",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['DANGER'],
            bg=COLORS['BG']
        )
        error_label.pack(expand=True)

    def _show_detailed_error_message(self, title: str, error: str):
        """Show a detailed error message with retry option."""
        error_frame = tk.Frame(self.content_frame, bg=COLORS['BG'])
        error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Error title
        title_label = tk.Label(
            error_frame,
            text=f"❌ {title}",
            font=UIConfig.FONT_TITLE,
            fg=COLORS['DANGER'],
            bg=COLORS['BG']
        )
        title_label.pack(pady=(0, 10))

        # Error details
        details_label = tk.Label(
            error_frame,
            text=f"Détails: {error}",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['BG'],
            wraplength=400,
            justify=tk.LEFT
        )
        details_label.pack(pady=(0, 20))

        # Action buttons
        button_frame = tk.Frame(error_frame, bg=COLORS['BG'])
        button_frame.pack()

        # Retry button
        retry_btn = tk.Button(
            button_frame,
            text="🔄 Réessayer",
            command=lambda: self.navigate_to(self.current_state),
            bg=COLORS['PRIMARY'],
            fg='white',
            font=UIConfig.FONT_BUTTON,
            relief='flat',
            padx=15,
            pady=5
        )
        retry_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Home button
        home_btn = tk.Button(
            button_frame,
            text="🏠 Retour à l'accueil",
            command=lambda: self.navigate_to(NavigationState.HOME),
            bg=COLORS['SECONDARY'],
            fg='white',
            font=UIConfig.FONT_BUTTON,
            relief='flat',
            padx=15,
            pady=5
        )
        home_btn.pack(side=tk.LEFT)
    
    def get_content_frame(self) -> tk.Frame:
        """Get the content frame for modules to use."""
        return self.content_frame
    
    def set_window_title(self, title: str):
        """Set the window title with Sofrecom branding."""
        full_title = f"{title} - Pladria - Sofrecom"
        self.root.title(full_title)

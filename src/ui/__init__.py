"""
User interface modules for the Suivi Generator platform.

This package contains the GUI components:
- main_window: Main application window with navigation
- navigation: Navigation system for multi-feature platform
- home_screen: Home/menu screen
- settings_screen: Settings configuration screen
- modules: Feature modules (suivi_generator, etc.)
- components: Individual UI components
- styles: UI styling and themes
- keyboard_shortcuts: Keyboard shortcut management
"""

from .main_window import MainWindow
from .navigation import NavigationManager, NavigationState
from .home_screen import HomeScreen
from .settings_screen import SettingsScreen

__all__ = ['MainWindow', 'NavigationManager', 'NavigationState', 'HomeScreen', 'SettingsScreen']

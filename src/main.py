"""
Main entry point for the Suivi Generator application.
"""

import tkinter as tk
import sys
import os
import logging
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from utils.logging_config import setup_logging, configure_third_party_loggers
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen
from config.constants import AppInfo


def setup_application():
    """Set up the application environment."""
    # Set up logging
    setup_logging(log_level="INFO", log_to_file=True)
    configure_third_party_loggers()
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info(f"Starting {AppInfo.DESCRIPTION}")
    logger.info(f"Version: {AppInfo.VERSION}")
    logger.info(f"Author: {AppInfo.AUTHOR}")
    logger.info("=" * 60)
    
    return logger


def create_application():
    """Create and configure the main application."""
    # Create root window
    root = tk.Tk()
    
    # Create main window
    app = MainWindow(root)
    
    return app


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow Ctrl+C to work normally
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger = logging.getLogger(__name__)
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Show error dialog if tkinter is available
    try:
        import tkinter.messagebox as messagebox
        error_msg = f"Une erreur critique s'est produite:\n\n{exc_type.__name__}: {exc_value}"
        messagebox.showerror("Erreur critique", error_msg)
    except:
        pass


def main():
    """Main application entry point with splash screen."""
    try:
        # Set global exception handler early
        sys.excepthook = handle_exception

        # Show splash screen immediately for fastest startup
        def start_main_application():
            """Callback to start main application after splash screen."""
            try:
                # Create and run main application
                logger = logging.getLogger(__name__)
                logger.info("Creating main application...")
                app = create_application()

                logger.info("Application created successfully")
                logger.info("Starting main loop...")

                app.run()

                logger.info("Application closed normally")

            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to start main application: {e}", exc_info=True)
                import tkinter.messagebox as messagebox
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de démarrer l'application:\n\n{str(e)}"
                )

        # Show splash screen immediately with loading
        splash = SplashScreen(on_complete_callback=start_main_application)
        splash.show()

    except KeyboardInterrupt:
        print("\n❌ Application interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        # Try to log if possible
        try:
            logging.error(f"Failed to start application: {e}", exc_info=True)
        except:
            pass
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)


if __name__ == "__main__":
    main()

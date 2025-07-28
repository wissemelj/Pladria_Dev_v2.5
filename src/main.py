#!/usr/bin/env python3
"""
Point d'entrée principal pour l'application Pladria v2.5
Système de contrôle qualité développé par Sofrecom
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Ajouter le répertoire src au path Python
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def setup_logging():
    """Configure le système de logging."""
    try:
        from utils.logging_config import setup_logging as setup_log
        setup_log()
    except ImportError:
        # Configuration basique si le module n'est pas disponible
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

def launch_main_application():
    """Lance l'application principale après le splash screen."""
    try:
        print("🖥️ Création de la fenêtre principale...")
        root = tk.Tk()

        # Importer et créer l'application principale
        print("📦 Importation des modules UI...")
        from ui.main_window import MainWindow

        print("🏗️ Initialisation de l'application...")
        app = MainWindow(root)

        # Lancer l'application
        print("✅ Lancement de l'interface...")
        app.run()

    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("Vérifiez que tous les modules sont présents dans le répertoire src/")
        import traceback
        traceback.print_exc()
        import tkinter.messagebox as messagebox
        messagebox.showerror(
            "Erreur d'importation",
            f"Erreur d'importation: {e}\n\nVérifiez que tous les modules sont présents dans le répertoire src/"
        )
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        import tkinter.messagebox as messagebox
        messagebox.showerror(
            "Erreur de lancement",
            f"Erreur lors du lancement: {e}"
        )
        sys.exit(1)

def main():
    """Point d'entrée principal de l'application avec splash screen."""
    try:
        print("🚀 Démarrage de Pladria v2.5...")

        # Importer le splash screen
        from ui.splash_screen import SplashScreen

        # Créer et afficher le splash screen
        print("🎨 Affichage du splash screen...")
        splash = SplashScreen(on_complete_callback=launch_main_application)
        splash.show()

    except ImportError as e:
        print(f"❌ Erreur d'importation du splash screen: {e}")
        print("Lancement direct de l'application...")
        # Fallback: lancer directement l'application sans splash screen
        setup_logging()
        launch_main_application()
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    main()

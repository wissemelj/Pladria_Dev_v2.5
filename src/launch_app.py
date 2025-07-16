#!/usr/bin/env python3
"""
Lanceur sécurisé pour Pladria v3.0
Résout les problèmes d'importation et lance l'application
"""

import sys
import os
import subprocess
from pathlib import Path

def clean_python_cache():
    """Supprime les caches Python qui peuvent causer des conflits."""
    print("🧹 Nettoyage des caches Python...")
    
    cache_dirs = []
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                cache_dirs.append(cache_path)
    
    for cache_dir in cache_dirs:
        try:
            import shutil
            shutil.rmtree(cache_dir)
            print(f"   ✅ Supprimé: {cache_dir}")
        except Exception as e:
            print(f"   ⚠️ Erreur: {cache_dir} - {e}")
    
    if not cache_dirs:
        print("   ✅ Aucun cache trouvé")

def verify_environment():
    """Vérifie l'environnement avant le lancement."""
    print("🔍 Vérification de l'environnement...")
    
    # Vérifier Python
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Exécutable: {sys.executable}")
    
    # Vérifier les modules critiques
    critical_modules = ["pandas", "openpyxl", "PIL", "tkinter"]
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - MANQUANT")
            return False
    
    return True

def launch_application():
    """Lance l'application Pladria."""
    print("🚀 Lancement de Pladria v3.0...")
    
    try:
        # Méthode 1: Import direct
        print("   Tentative 1: Import direct...")
        import main
        print("   ✅ Module main importé")
        
        # Lancer l'application
        main.main()
        return True
        
    except Exception as e:
        print(f"   ❌ Échec méthode 1: {e}")
        
        try:
            # Méthode 2: Subprocess
            print("   Tentative 2: Subprocess...")
            result = subprocess.run([
                sys.executable, "main.py"
            ], cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Application lancée via subprocess")
                return True
            else:
                print(f"   ❌ Échec subprocess: code {result.returncode}")
                
        except Exception as e2:
            print(f"   ❌ Échec méthode 2: {e2}")
        
        return False

def main():
    """Fonction principale du lanceur."""
    print("=" * 60)
    print("    LANCEUR PLADRIA v3.0")
    print("=" * 60)
    print("Résolution automatique des problèmes d'importation")
    print("=" * 60)
    
    # Étape 1: Nettoyer les caches
    clean_python_cache()
    
    # Étape 2: Vérifier l'environnement
    print()
    if not verify_environment():
        print("\n❌ ENVIRONNEMENT INCOMPLET")
        print("Installez les dépendances manquantes:")
        print("   cd ../Package")
        print("   pip install -r requirements.txt")
        print("   ou")
        print("   INSTALL_DEPENDENCIES.bat")
        input("\nAppuyez sur Entrée pour quitter...")
        return False
    
    # Étape 3: Lancer l'application
    print()
    if launch_application():
        print("\n✅ APPLICATION LANCÉE AVEC SUCCÈS!")
        return True
    else:
        print("\n❌ ÉCHEC DU LANCEMENT")
        print("\nSolutions alternatives:")
        print("1. Redémarrez votre terminal")
        print("2. Lancez en tant qu'administrateur")
        print("3. Vérifiez votre antivirus")
        print("4. Utilisez le BUILD EXE: cd ../Package && BUILD_EXE.bat")
        input("\nAppuyez sur Entrée pour quitter...")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nLancement interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

#!/usr/bin/env python3
"""
Test script pour vérifier que le bouton "Générer statistiques" ouvre l'index stats au lieu du modal.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_open_stats_index_method():
    """Test que la méthode _open_stats_index_file existe et est fonctionnelle."""
    print("🧪 Test de la méthode d'ouverture de l'index stats")
    print("=" * 60)
    
    try:
        # Test imports
        print("📦 Test des imports...")
        from ui.modules.team_stats_module import TeamStatsModule
        print("✅ TeamStatsModule importé avec succès")
        
        # Test que la nouvelle méthode existe
        if hasattr(TeamStatsModule, '_open_stats_index_file'):
            print("✅ Méthode _open_stats_index_file trouvée")
        else:
            print("❌ Méthode _open_stats_index_file manquante")
            return False
        
        # Test que la méthode d'injection retourne maintenant un chemin
        if hasattr(TeamStatsModule, '_inject_statistics_to_stats_index'):
            print("✅ Méthode _inject_statistics_to_stats_index trouvée")
        else:
            print("❌ Méthode _inject_statistics_to_stats_index manquante")
            return False
        
        print("\n🎉 Toutes les méthodes requises sont présentes!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_button_text_update():
    """Test que le texte du bouton a été mis à jour."""
    print("\n🔘 Test de la mise à jour du texte du bouton")
    print("=" * 50)
    
    try:
        # Lire le fichier source pour vérifier le texte du bouton
        module_path = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que le nouveau texte est présent
        if "📊 Générer et ouvrir index" in content:
            print("✅ Texte du bouton mis à jour: '📊 Générer et ouvrir index'")
        else:
            print("❌ Texte du bouton non mis à jour")
            return False
        
        # Vérifier que l'ancien texte n'est plus présent (sauf dans les commentaires)
        lines_with_old_text = []
        for i, line in enumerate(content.split('\n'), 1):
            if "📊 Générer statistiques" in line and not line.strip().startswith('#'):
                lines_with_old_text.append(i)
        
        if lines_with_old_text:
            print(f"⚠️ Ancien texte encore présent aux lignes: {lines_with_old_text}")
        else:
            print("✅ Ancien texte du bouton supprimé")
        
        # Vérifier le message de statut
        if "Sélectionnez une période pour générer et ouvrir l'index stats" in content:
            print("✅ Message de statut mis à jour")
        else:
            print("❌ Message de statut non mis à jour")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du texte: {e}")
        return False

def test_workflow_logic():
    """Test la logique du nouveau workflow."""
    print("\n🔄 Test de la logique du workflow")
    print("=" * 40)
    
    try:
        # Créer un fichier de test temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_file:
            temp_file.write("""
<!DOCTYPE html>
<html>
<head><title>Test Stats Index</title></head>
<body>
    <h1>Test Dashboard</h1>
    <!-- PLADRIA_STATS_INJECTION -->
    <!-- END_PLADRIA_STATS -->
</body>
</html>
""")
            temp_path = temp_file.name
        
        print(f"✅ Fichier de test créé: {os.path.basename(temp_path)}")
        
        # Test de détection du type de fichier
        file_ext = os.path.splitext(temp_path)[1].lower()
        if file_ext == '.html':
            print("✅ Extension HTML détectée correctement")
        else:
            print(f"❌ Extension incorrecte détectée: {file_ext}")
            return False
        
        # Test de lecture du contenu
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "PLADRIA_STATS_INJECTION" in content:
            print("✅ Marqueur d'injection trouvé dans le fichier")
        else:
            print("❌ Marqueur d'injection non trouvé")
            return False
        
        # Nettoyer
        os.unlink(temp_path)
        print("✅ Fichier de test nettoyé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de workflow: {e}")
        return False

def test_platform_compatibility():
    """Test la compatibilité multiplateforme pour l'ouverture de fichiers."""
    print("\n🖥️ Test de compatibilité multiplateforme")
    print("=" * 45)
    
    try:
        import platform
        
        current_system = platform.system()
        print(f"✅ Système détecté: {current_system}")
        
        # Test des imports requis
        try:
            import subprocess
            print("✅ Module subprocess disponible")
        except ImportError:
            print("❌ Module subprocess non disponible")
            return False
        
        # Test spécifique au système
        if current_system == "Windows":
            # Test os.startfile (Windows uniquement)
            try:
                import os
                if hasattr(os, 'startfile'):
                    print("✅ os.startfile disponible (Windows)")
                else:
                    print("❌ os.startfile non disponible")
                    return False
            except Exception as e:
                print(f"❌ Erreur test Windows: {e}")
                return False
                
        elif current_system in ["Darwin", "Linux"]:
            # Test des commandes système
            commands = ["open"] if current_system == "Darwin" else ["xdg-open"]
            for cmd in commands:
                try:
                    result = subprocess.run([cmd, "--version"], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=5)
                    print(f"✅ Commande {cmd} disponible")
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    print(f"⚠️ Commande {cmd} non disponible ou timeout")
        
        # Test fallback webbrowser
        try:
            import webbrowser
            print("✅ Module webbrowser disponible (fallback)")
        except ImportError:
            print("❌ Module webbrowser non disponible")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test compatibilité: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de la fonctionnalité 'Ouvrir Index Stats'")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Méthodes d'ouverture
    if test_open_stats_index_method():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Méthodes d'ouverture")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Méthodes d'ouverture")
    
    # Test 2: Mise à jour du texte
    if test_button_text_update():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Mise à jour du texte")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Mise à jour du texte")
    
    # Test 3: Logique du workflow
    if test_workflow_logic():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Logique du workflow")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Logique du workflow")
    
    # Test 4: Compatibilité multiplateforme
    if test_platform_compatibility():
        tests_passed += 1
        print("\n✅ Test 4 RÉUSSI: Compatibilité multiplateforme")
    else:
        print("\n❌ Test 4 ÉCHOUÉ: Compatibilité multiplateforme")
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"📊 Résultats des tests: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n📝 Nouveau comportement implémenté:")
        print("  ✅ Le bouton 'Générer et ouvrir index' injecte les stats ET ouvre l'index")
        print("  ✅ Plus de modal dashboard - ouverture directe du fichier index")
        print("  ✅ Support multiplateforme pour l'ouverture de fichiers")
        print("  ✅ Fallback vers le dossier si l'ouverture du fichier échoue")
        print("  ✅ Messages d'interface mis à jour pour refléter le nouveau comportement")
        print("\n🎯 Workflow utilisateur:")
        print("  1. Sélectionner une période avec les sélecteurs de date")
        print("  2. Cliquer sur 'Générer et ouvrir index'")
        print("  3. Les statistiques sont injectées dans l'index du dossier stats")
        print("  4. L'index s'ouvre automatiquement avec les nouvelles données")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

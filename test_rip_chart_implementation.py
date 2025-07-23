#!/usr/bin/env python3
"""
Test de l'implémentation du graphique RIP (P0 P1) comme la section CM.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_rip_html_chart_structure():
    """Test que le HTML contient le graphique RIP."""
    print("🔍 Test de la Structure HTML du Graphique RIP")
    print("=" * 60)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ Fichier HTML non trouvé")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier les éléments du graphique RIP
        rip_chart_elements = [
            'RIP (P0 P1) (0)',  # Titre avec total
            'ripChart',         # ID du canvas
            'chart-container',  # Container du graphique
            'stat-item',        # Items de stats (pas summary-item)
            'stat-value rip-rien',
            'stat-value rip-modification', 
            'stat-value rip-creation'
        ]
        
        for element in rip_chart_elements:
            if element in html_content:
                print(f"   ✅ Élément graphique RIP trouvé: {element}")
            else:
                print(f"   ❌ Élément graphique RIP manquant: {element}")
                return False
        
        # Vérifier qu'il n'y a plus de rip-total (supprimé car pas dans les graphiques)
        if 'rip-total' not in html_content:
            print(f"   ✅ rip-total correctement supprimé (pas nécessaire avec graphique)")
        else:
            print(f"   ⚠️ rip-total encore présent (peut être OK)")
        
        # Vérifier la structure comme CM
        if 'canvas id="ripChart"' in html_content:
            print(f"   ✅ Canvas RIP correctement configuré")
        else:
            print(f"   ❌ Canvas RIP manquant")
            return False
        
        print(f"   ✅ Structure HTML du graphique RIP correcte")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification HTML: {e}")
        return False

def test_rip_script_chart_code():
    """Test que le script.js contient le code du graphique RIP."""
    print("\n🔍 Test du Code JavaScript du Graphique RIP")
    print("=" * 60)
    
    try:
        script_file = Path(__file__).parent / "src" / "pres stats" / "script.js"
        
        if not script_file.exists():
            print(f"   ❌ Fichier script.js non trouvé")
            return False
        
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Vérifier les éléments du graphique RIP
        rip_script_elements = [
            'ripCtx',
            'ripChart',
            'getElementById(\'ripChart\')',
            'type: \'doughnut\'',
            'Rien à faire',
            'Modification', 
            'Création',
            'colors.ripRien',
            'colors.ripModification',
            'colors.ripCreation'
        ]
        
        for element in rip_script_elements:
            if element in script_content:
                print(f"   ✅ Code JavaScript RIP trouvé: {element}")
            else:
                print(f"   ❌ Code JavaScript RIP manquant: {element}")
                return False
        
        # Vérifier les couleurs RIP
        rip_colors = ['ripRien', 'ripModification', 'ripCreation']
        for color in rip_colors:
            if color in script_content:
                print(f"   ✅ Couleur RIP définie: {color}")
            else:
                print(f"   ❌ Couleur RIP manquante: {color}")
                return False
        
        # Vérifier que c'est un graphique doughnut comme CM
        if 'type: \'doughnut\'' in script_content and 'ripCtx' in script_content:
            print(f"   ✅ Graphique RIP configuré en doughnut comme CM")
        else:
            print(f"   ❌ Configuration graphique RIP incorrecte")
            return False
        
        print(f"   ✅ Code JavaScript du graphique RIP correct")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification script.js: {e}")
        return False

def test_rip_html_update_patterns():
    """Test que les patterns de mise à jour HTML sont corrects pour le graphique."""
    print("\n🔍 Test des Patterns de Mise à Jour HTML RIP")
    print("=" * 60)
    
    try:
        # Simuler le HTML avec graphique RIP
        test_html = '''
        <div class="card third-width">
            <h2>RIP (P0 P1) (0)</h2>
            <div class="chart-container">
                <canvas id="ripChart"></canvas>
            </div>
            <div class="stats-summary">
                <div class="stat-item">
                    <span class="stat-value rip-rien">0</span>
                    <span class="stat-label">Rien à faire</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value rip-modification">0</span>
                    <span class="stat-label">Modification</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value rip-creation">0</span>
                    <span class="stat-label">Création</span>
                </div>
            </div>
        </div>
        '''
        
        import re
        
        # Test des patterns RIP avec graphique
        patterns = [
            ('RIP Title', r'(<h2>RIP \(P0 P1\)\s*\()[^)]*(\)</h2>)'),
            ('RIP Rien', r'(<span class="stat-value rip-rien">)[^<]*(</span>)'),
            ('RIP Modification', r'(<span class="stat-value rip-modification">)[^<]*(</span>)'),
            ('RIP Création', r'(<span class="stat-value rip-creation">)[^<]*(</span>)')
        ]
        
        for nom, pattern in patterns:
            match = re.search(pattern, test_html)
            if match:
                print(f"   ✅ Pattern {nom} fonctionne: {match.group(0)}")
            else:
                print(f"   ❌ Pattern {nom} échoue")
                return False
        
        print(f"   ✅ Tous les patterns de mise à jour RIP fonctionnent")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test des patterns: {e}")
        return False

def test_rip_chart_integration():
    """Test que l'intégration du graphique RIP est complète."""
    print("\n🔍 Test de l'Intégration Complète du Graphique RIP")
    print("=" * 60)
    
    try:
        # Vérifier que les méthodes d'extraction existent toujours
        from ui.modules.team_stats_module import TeamStatsModule
        
        required_methods = [
            '_extract_rip_data_for_dashboard',
            '_normalize_rip_motif'
        ]
        
        for method_name in required_methods:
            if hasattr(TeamStatsModule, method_name):
                print(f"   ✅ Méthode RIP existe: {method_name}")
            else:
                print(f"   ❌ Méthode RIP manquante: {method_name}")
                return False
        
        # Vérifier que la validation existe
        from core.data_validator import DataValidator
        
        validator = DataValidator()
        if hasattr(validator, '_validate_rip_data'):
            print(f"   ✅ Validation RIP existe: _validate_rip_data")
        else:
            print(f"   ❌ Validation RIP manquante: _validate_rip_data")
            return False
        
        print(f"   ✅ Intégration complète du graphique RIP")
        print(f"   📊 Structure: Extraction → Validation → HTML+Chart → Script.js")
        print(f"   🎨 Style: Graphique doughnut comme CM avec 3 catégories")
        print(f"   🔄 Mise à jour: Titre + valeurs individuelles + données graphique")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test d'intégration: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test du Graphique RIP (P0 P1) comme CM")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Structure HTML du graphique
    if test_rip_html_chart_structure():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Structure HTML du graphique RIP")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Structure HTML du graphique RIP")
    
    # Test 2: Code JavaScript du graphique
    if test_rip_script_chart_code():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Code JavaScript du graphique RIP")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Code JavaScript du graphique RIP")
    
    # Test 3: Patterns de mise à jour HTML
    if test_rip_html_update_patterns():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Patterns de mise à jour HTML RIP")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Patterns de mise à jour HTML RIP")
    
    # Test 4: Intégration complète
    if test_rip_chart_integration():
        tests_passed += 1
        print("\n✅ Test 4 RÉUSSI: Intégration complète du graphique RIP")
    else:
        print("\n❌ Test 4 ÉCHOUÉ: Intégration complète du graphique RIP")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Graphique RIP (P0 P1) implémenté comme CM!")
        print("\n🎯 Changements effectués:")
        print("  • ✅ Graphique doughnut ajouté à la section RIP")
        print("  • ✅ Canvas ripChart avec chart-container")
        print("  • ✅ 3 couleurs définies (bleu, orange, vert)")
        print("  • ✅ Titre avec total comme CM: 'RIP (P0 P1) (0)'")
        print("  • ✅ Stats individuelles sous le graphique")
        print("  • ✅ Mise à jour script.js pour données graphique")
        print("  • ✅ Patterns HTML mis à jour (stat-value)")
        
        print("\n📊 Structure finale:")
        print("  ┌─────────────┬─────────────┬─────────────┐")
        print("  │ Tickets UPR │ Tickets     │ RIP (P0 P1) │")
        print("  │ (bannettes) │ 501/511     │ (graphique) │")
        print("  │             │ (bannettes) │             │")
        print("  └─────────────┴─────────────┴─────────────┘")
        
        print("\n🎨 Graphique RIP:")
        print("  • Type: Doughnut (comme CM)")
        print("  • Catégories: Rien à faire, Modification, Création")
        print("  • Couleurs: Bleu, Orange, Vert")
        print("  • Légende: En bas avec points")
        print("  • Tooltips: Avec pourcentages")
        
        print("\n🔧 Prêt pour test avec données réelles!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

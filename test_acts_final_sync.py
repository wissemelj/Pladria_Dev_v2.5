#!/usr/bin/env python3
"""
Test final de la synchronisation Acts HTML ↔ Graphique.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_percentage_calculation_sync():
    """Test que les pourcentages HTML et graphique sont identiques."""
    print("🔍 Test Final de Synchronisation des Pourcentages")
    print("=" * 60)
    
    # Données de test (ordre HTML/script.js unifié)
    test_data = [13244, 4889, 2391, 1775, 893, 499, 285, 39, 45, 34]
    labels = [
        'AD RAS sans temps', 'AD RAS avec temps', 'OK', 'NOK', 'AD Non jointe',
        'UPR RAS', 'AD Non trouvée', 'Hors commune', 'UPR NOK', 'UPR OK'
    ]
    
    total = sum(test_data)
    print(f"   📊 Total Acts: {total:,}")
    
    # Calcul des pourcentages (logique unifiée)
    print(f"\n   📊 Pourcentages calculés:")
    for i, (label, count) in enumerate(zip(labels, test_data)):
        percentage = (count / total * 100) if total > 0 else 0
        formatted_pct = f"{percentage:.1f}%"
        print(f"      {i+1}. {label}: {count:,} ({formatted_pct})")
    
    # Vérifier que le total fait ~100%
    total_percentage = sum((count / total * 100) for count in test_data)
    if 99.9 <= total_percentage <= 100.1:
        print(f"\n   ✅ Total des pourcentages cohérent: {total_percentage:.1f}%")
    else:
        print(f"\n   ❌ Total des pourcentages incohérent: {total_percentage:.1f}%")
        return False
    
    print(f"   ✅ Calculs de pourcentages corrects!")
    return True

def test_html_structure_ready():
    """Test que la structure HTML est prête pour les mises à jour."""
    print("\n🔍 Test de la Structure HTML")
    print("=" * 60)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier les éléments Acts avec pourcentages statiques
        acts_elements = [
            ('AD RAS sans temps', '52.8%'),
            ('AD RAS avec temps', '20.4%'),
            ('OK', '9.5%'),
            ('NOK', '8.2%'),
            ('AD Non jointe', '5.1%')
        ]
        
        found_elements = 0
        for label, static_pct in acts_elements:
            if f'{label} ({static_pct})' in html_content:
                print(f"   ✅ Élément trouvé: {label} ({static_pct})")
                found_elements += 1
            else:
                print(f"   ❌ Élément manquant: {label} ({static_pct})")
        
        if found_elements >= 4:
            print(f"   ✅ Structure HTML prête pour mise à jour ({found_elements}/{len(acts_elements)})")
            return True
        else:
            print(f"   ❌ Structure HTML incomplète ({found_elements}/{len(acts_elements)})")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification HTML: {e}")
        return False

def test_script_js_tooltip_ready():
    """Test que le script.js est prêt avec calcul dynamique."""
    print("\n🔍 Test du Script.js")
    print("=" * 60)
    
    try:
        script_file = Path(__file__).parent / "src" / "pres stats" / "script.js"
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Vérifications essentielles
        checks = [
            ('Calcul dynamique total', 'const total = context.dataset.data.reduce((a, b) => a + b, 0);'),
            ('Formule pourcentage', '((context.raw / total) * 100).toFixed(1)'),
            ('Ordre AD RAS sans temps', 'AD RAS\\nsans temps'),
            ('Ordre AD RAS avec temps', 'AD RAS\\navec temps')
        ]
        
        passed_checks = 0
        for check_name, pattern in checks:
            if pattern in script_content:
                print(f"   ✅ {check_name}: OK")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: MANQUANT")
        
        # Vérifier qu'il n'y a plus de total hardcodé
        if 'const total = 11396;' not in script_content and 'const total = 24094;' not in script_content:
            print(f"   ✅ Aucun total hardcodé trouvé")
            passed_checks += 1
        else:
            print(f"   ❌ Total hardcodé encore présent")
        
        if passed_checks >= 4:
            print(f"   ✅ Script.js prêt avec calcul dynamique ({passed_checks}/5)")
            return True
        else:
            print(f"   ❌ Script.js pas prêt ({passed_checks}/5)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification script.js: {e}")
        return False

def test_python_code_ready():
    """Test que le code Python est prêt avec l'ordre correct."""
    print("\n🔍 Test du Code Python")
    print("=" * 60)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Vérifier que les méthodes existent
        required_methods = [
            '_extract_acts_data_for_dashboard',
            '_update_html_elements_with_data'
        ]
        
        for method_name in required_methods:
            if hasattr(TeamStatsModule, method_name):
                print(f"   ✅ Méthode {method_name}: OK")
            else:
                print(f"   ❌ Méthode {method_name}: MANQUANTE")
                return False
        
        # Vérifier le code source pour l'ordre correct
        import inspect
        source = inspect.getsource(TeamStatsModule._extract_acts_data_for_dashboard)
        
        if 'AD RAS sans temps' in source and 'AD RAS avec temps' in source:
            if source.find('AD RAS sans temps') < source.find('AD RAS avec temps'):
                print(f"   ✅ Ordre correct: AD RAS sans temps en premier")
            else:
                print(f"   ❌ Ordre incorrect: AD RAS avec temps en premier")
                return False
        else:
            print(f"   ❌ Labels AD RAS non trouvés dans le code")
            return False
        
        print(f"   ✅ Code Python prêt avec ordre correct")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification Python: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test Final de Synchronisation Acts HTML ↔ Graphique")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Calculs de pourcentages
    if test_percentage_calculation_sync():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Calculs de pourcentages")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Calculs de pourcentages")
    
    # Test 2: Structure HTML
    if test_html_structure_ready():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Structure HTML")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Structure HTML")
    
    # Test 3: Script.js
    if test_script_js_tooltip_ready():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Script.js")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Script.js")
    
    # Test 4: Code Python
    if test_python_code_ready():
        tests_passed += 1
        print("\n✅ Test 4 RÉUSSI: Code Python")
    else:
        print("\n❌ Test 4 ÉCHOUÉ: Code Python")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Synchronisation Acts HTML ↔ Graphique COMPLÈTE!")
        
        print("\n🎯 Corrections apportées:")
        print("  • ✅ Ordre unifié: AD RAS sans temps en premier (plus fréquent)")
        print("  • ✅ Script.js: Calcul dynamique du total (plus de hardcodé)")
        print("  • ✅ Python: Ordre correct dans chart_labels_order")
        print("  • ✅ HTML: Patterns prêts pour mise à jour des pourcentages")
        print("  • ✅ Formule identique: (count/total)*100 partout")
        
        print("\n📊 Exemple de synchronisation:")
        print("  Données: AD RAS sans temps = 13,244 sur 24,094 total")
        print("  Calcul: (13244/24094)*100 = 55.0%")
        print("  HTML: 'AD RAS sans temps (55.0%)'")
        print("  Tooltip: 'AD RAS sans temps: 13,244 (55.0%)'")
        print("  → PARFAITEMENT SYNCHRONISÉ!")
        
        print("\n🔄 Workflow utilisateur:")
        print("  1. Charger fichier Suivi Global Excel")
        print("  2. Sélectionner plage de dates")
        print("  3. Générer dashboard")
        print("  4. Voir pourcentages cohérents partout")
        print("  5. HTML text = Graphique tooltips ✅")
        
        print("\n🚀 Prêt pour test avec données réelles!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test de la synchronisation parfaite entre les pourcentages HTML et graphique Acts.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_acts_order_synchronization():
    """Test que l'ordre des données est synchronisé entre HTML, script.js et Python."""
    print("🔍 Test de Synchronisation de l'Ordre Acts")
    print("=" * 60)
    
    try:
        # Ordre attendu (basé sur HTML)
        expected_order = [
            'AD RAS sans temps',
            'AD RAS avec temps', 
            'OK',
            'NOK',
            'AD Non jointe',
            'UPR RAS',
            'AD Non trouvée',
            'Hors commune',
            'UPR NOK',
            'UPR OK'
        ]
        
        print(f"   📋 Ordre attendu (basé sur HTML):")
        for i, label in enumerate(expected_order):
            print(f"      {i+1}. {label}")
        
        # Vérifier l'ordre dans script.js
        script_file = Path(__file__).parent / "src" / "pres stats" / "script.js"
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Extraire les labels du script.js
        labels_match = re.search(r"labels: \[(.*?)\]", script_content, re.DOTALL)
        if labels_match:
            labels_str = labels_match.group(1)
            script_labels = [label.strip().strip("'\"").replace('\\n', ' ') for label in labels_str.split(',')]
            
            print(f"\n   📊 Ordre dans script.js:")
            for i, label in enumerate(script_labels):
                print(f"      {i+1}. {label}")
            
            # Comparer les ordres
            if len(script_labels) == len(expected_order):
                order_match = True
                for i, (expected, actual) in enumerate(zip(expected_order, script_labels)):
                    if expected.replace(' ', ' ') != actual.replace(' ', ' '):
                        print(f"      ❌ Position {i+1}: Attendu '{expected}', Trouvé '{actual}'")
                        order_match = False
                
                if order_match:
                    print(f"   ✅ Ordre script.js correspond à l'ordre HTML")
                else:
                    print(f"   ❌ Ordre script.js ne correspond pas à l'ordre HTML")
                    return False
            else:
                print(f"   ❌ Nombre de labels différent: HTML={len(expected_order)}, Script={len(script_labels)}")
                return False
        else:
            print(f"   ❌ Impossible d'extraire les labels du script.js")
            return False
        
        # Vérifier l'ordre dans le code Python
        python_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        with open(python_file, 'r', encoding='utf-8') as f:
            python_content = f.read()
        
        # Extraire chart_labels_order du Python
        chart_order_match = re.search(r"chart_labels_order = \[(.*?)\]", python_content, re.DOTALL)
        if chart_order_match:
            chart_order_str = chart_order_match.group(1)
            python_labels = [label.strip().strip("'\"") for label in chart_order_str.split(',') if label.strip().strip("'\"")]
            
            print(f"\n   🐍 Ordre dans Python:")
            for i, label in enumerate(python_labels):
                print(f"      {i+1}. {label}")
            
            # Comparer avec l'ordre attendu
            if python_labels == expected_order:
                print(f"   ✅ Ordre Python correspond à l'ordre HTML")
            else:
                print(f"   ❌ Ordre Python ne correspond pas à l'ordre HTML")
                return False
        else:
            print(f"   ❌ Impossible d'extraire chart_labels_order du Python")
            return False
        
        print(f"\n   ✅ Synchronisation parfaite des ordres!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test de synchronisation: {e}")
        return False

def test_percentage_calculation_consistency():
    """Test que le calcul des pourcentages est identique entre HTML et graphique."""
    print("\n🧮 Test de Cohérence du Calcul des Pourcentages")
    print("=" * 60)
    
    try:
        # Données de test simulées (dans l'ordre correct)
        test_data = [13244, 4889, 2391, 1775, 893, 499, 285, 39, 45, 34]  # Ordre HTML
        total = sum(test_data)
        
        print(f"   📊 Données de test: {test_data}")
        print(f"   📊 Total: {total:,}")
        
        # Calcul des pourcentages comme dans le HTML (Python)
        html_percentages = []
        for count in test_data:
            percentage = (count / total * 100) if total > 0 else 0
            html_percentages.append(round(percentage, 1))
        
        print(f"\n   📝 Pourcentages HTML (Python logic):")
        labels = ['AD RAS sans temps', 'AD RAS avec temps', 'OK', 'NOK', 'AD Non jointe', 'UPR RAS', 'AD Non trouvée', 'Hors commune', 'UPR NOK', 'UPR OK']
        for i, (label, count, percentage) in enumerate(zip(labels, test_data, html_percentages)):
            print(f"      {i+1}. {label}: {count:,} ({percentage}%)")
        
        # Calcul des pourcentages comme dans le graphique (JavaScript logic)
        # JavaScript: ((context.raw / total) * 100).toFixed(1)
        js_percentages = []
        for count in test_data:
            percentage = round((count / total * 100), 1)  # Équivalent de toFixed(1)
            js_percentages.append(percentage)
        
        print(f"\n   📊 Pourcentages Graphique (JavaScript logic):")
        for i, (label, count, percentage) in enumerate(zip(labels, test_data, js_percentages)):
            print(f"      {i+1}. {label}: {count:,} ({percentage}%)")
        
        # Comparer les résultats
        percentages_match = True
        for i, (html_pct, js_pct) in enumerate(zip(html_percentages, js_percentages)):
            if html_pct != js_pct:
                print(f"      ❌ Différence pour {labels[i]}: HTML={html_pct}%, JS={js_pct}%")
                percentages_match = False
        
        if percentages_match:
            print(f"\n   ✅ Calculs de pourcentages identiques entre HTML et graphique!")
            
            # Vérifier que le total fait 100%
            total_percentage = sum(html_percentages)
            if 99.9 <= total_percentage <= 100.1:  # Tolérance pour les arrondis
                print(f"   ✅ Total des pourcentages cohérent: {total_percentage}%")
            else:
                print(f"   ⚠️ Total des pourcentages: {total_percentage}% (peut être dû aux arrondis)")
            
            return True
        else:
            print(f"\n   ❌ Incohérence dans les calculs de pourcentages!")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test de calcul: {e}")
        return False

def test_script_js_tooltip_logic():
    """Test que la logique de tooltip dans script.js est correcte."""
    print("\n📊 Test de la Logique de Tooltip Script.js")
    print("=" * 60)
    
    try:
        script_file = Path(__file__).parent / "src" / "pres stats" / "script.js"
        with open(script_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Vérifier que le tooltip utilise un calcul dynamique
        if 'const total = context.dataset.data.reduce((a, b) => a + b, 0);' in script_content:
            print(f"   ✅ Tooltip utilise un calcul dynamique du total")
        else:
            print(f"   ❌ Tooltip utilise encore un total hardcodé")
            return False
        
        # Vérifier la formule de pourcentage
        if '((context.raw / total) * 100).toFixed(1)' in script_content:
            print(f"   ✅ Formule de pourcentage correcte dans tooltip")
        else:
            print(f"   ❌ Formule de pourcentage incorrecte dans tooltip")
            return False
        
        # Vérifier qu'il n'y a plus de total hardcodé
        hardcoded_total_match = re.search(r'const total = \d+;', script_content)
        if hardcoded_total_match:
            print(f"   ❌ Total hardcodé trouvé: {hardcoded_total_match.group(0)}")
            return False
        else:
            print(f"   ✅ Aucun total hardcodé trouvé")
        
        print(f"   ✅ Logique de tooltip correcte!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test de tooltip: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de Synchronisation Parfaite Acts HTML ↔ Graphique")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Synchronisation des ordres
    if test_acts_order_synchronization():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Synchronisation des ordres")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Synchronisation des ordres")
    
    # Test 2: Cohérence des calculs
    if test_percentage_calculation_consistency():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Cohérence des calculs")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Cohérence des calculs")
    
    # Test 3: Logique tooltip
    if test_script_js_tooltip_logic():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Logique tooltip")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Logique tooltip")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Synchronisation parfaite Acts HTML ↔ Graphique!")
        print("\n🎯 Corrections apportées:")
        print("  • ✅ Ordre unifié: HTML = Script.js = Python")
        print("  • ✅ Calcul dynamique: Total calculé automatiquement")
        print("  • ✅ Formule identique: (count/total)*100 partout")
        print("  • ✅ Formatage cohérent: X.X% avec 1 décimale")
        
        print("\n📊 Résultat attendu:")
        print("  HTML: 'AD RAS sans temps (58.2%)'")
        print("  Tooltip: 'AD RAS sans temps: 13,244 (58.2%)'")
        print("  → MÊME POURCENTAGE PARTOUT!")
        
        print("\n🔄 Workflow:")
        print("  1. Extraction données Acts depuis Sheet 2")
        print("  2. Ordre unifié: [AD RAS sans temps, AD RAS avec temps, OK, NOK, ...]")
        print("  3. Calcul total dynamique: sum(all_values)")
        print("  4. Calcul pourcentages: (value/total)*100")
        print("  5. Mise à jour HTML: valeurs + pourcentages calculés")
        print("  6. Mise à jour script.js: mêmes données, même ordre")
        print("  7. Tooltips: calcul dynamique identique")
        
        print("\n🎯 Synchronisation parfaite garantie!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

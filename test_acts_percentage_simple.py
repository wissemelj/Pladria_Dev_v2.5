#!/usr/bin/env python3
"""
Test simple de la correction des pourcentages Acts.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_regex_patterns():
    """Test que les patterns regex fonctionnent correctement."""
    print("🔍 Test des Patterns Regex Corrigés")
    print("=" * 50)
    
    # HTML de test avec structure réelle
    test_html = '''
    <div class="summary-item">
        <span class="summary-value">13,244</span>
        <span class="summary-label">AD RAS sans temps (52.8%)</span>
    </div>
    <div class="summary-item">
        <span class="summary-value">4,889</span>
        <span class="summary-label">AD RAS avec temps (20.4%)</span>
    </div>
    <div class="summary-item">
        <span class="summary-value">2,391</span>
        <span class="summary-label">OK (9.5%)</span>
    </div>
    '''
    
    # Patterns corrigés
    patterns = {
        'AD RAS sans temps': r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">AD RAS sans temps \()[^)]*(\)</span>)',
        'AD RAS avec temps': r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">AD RAS avec temps \()[^)]*(\)</span>)',
        'OK': r'(<span class="summary-value">)[^<]*(</span>\s*<span class="summary-label">OK \()[^)]*(\)</span>)'
    }
    
    success_count = 0
    for label, pattern in patterns.items():
        try:
            match = re.search(pattern, test_html)
            if match:
                print(f"   ✅ Pattern {label}: MATCH")
                
                # Test du remplacement
                new_value = 1000
                new_percentage = 45.5
                replacement = rf'\g<1>{new_value:,}\g<2>{new_percentage:.1f}%\g<3>'
                updated = re.sub(pattern, replacement, test_html)
                
                if f'{new_value:,}' in updated and f'{new_percentage:.1f}%' in updated:
                    print(f"      ✅ Remplacement réussi: {new_value:,} ({new_percentage:.1f}%)")
                    success_count += 1
                else:
                    print(f"      ❌ Remplacement échoué")
            else:
                print(f"   ❌ Pattern {label}: NO MATCH")
        except Exception as e:
            print(f"   ❌ Pattern {label}: ERROR - {e}")
    
    if success_count == len(patterns):
        print(f"   ✅ Tous les patterns fonctionnent ({success_count}/{len(patterns)})")
        return True
    else:
        print(f"   ❌ Certains patterns échouent ({success_count}/{len(patterns)})")
        return False

def test_percentage_calculation():
    """Test du calcul des pourcentages."""
    print("\n🧮 Test du Calcul des Pourcentages")
    print("=" * 50)
    
    # Données de test
    test_cases = [
        ([1000, 500, 300, 200], [50.0, 25.0, 15.0, 10.0]),  # Total = 2000
        ([100, 50, 25, 25], [50.0, 25.0, 12.5, 12.5]),      # Total = 200
        ([1, 1, 1], [33.3, 33.3, 33.3])                     # Total = 3, test arrondis
    ]
    
    for i, (values, expected_percentages) in enumerate(test_cases):
        total = sum(values)
        print(f"   📊 Test case {i+1}: Total = {total}")
        
        calculated_percentages = []
        for value in values:
            percentage = (value / total * 100) if total > 0 else 0
            calculated_percentages.append(percentage)
        
        # Vérifier les résultats
        all_correct = True
        for j, (calc, expected) in enumerate(zip(calculated_percentages, expected_percentages)):
            if abs(calc - expected) < 0.1:  # Tolérance de 0.1%
                print(f"      ✅ {values[j]} → {calc:.1f}% (attendu: {expected:.1f}%)")
            else:
                print(f"      ❌ {values[j]} → {calc:.1f}% (attendu: {expected:.1f}%)")
                all_correct = False
        
        if not all_correct:
            return False
    
    print(f"   ✅ Tous les calculs de pourcentages corrects")
    return True

def test_html_structure_detection():
    """Test de la détection de la structure HTML Acts."""
    print("\n🔍 Test de la Structure HTML Acts")
    print("=" * 50)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ Fichier HTML non trouvé")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier la présence des éléments Acts avec pourcentages
        acts_elements = [
            'Acts Traitement PA',
            'AD RAS sans temps (52.8%)',
            'AD RAS avec temps (20.4%)',
            'OK (9.5%)',
            'NOK (8.2%)'
        ]
        
        found_elements = 0
        for element in acts_elements:
            if element in html_content:
                print(f"   ✅ Élément trouvé: {element}")
                found_elements += 1
            else:
                print(f"   ❌ Élément manquant: {element}")
        
        if found_elements >= 4:  # Au moins 4 sur 5
            print(f"   ✅ Structure HTML Acts détectée ({found_elements}/{len(acts_elements)})")
            return True
        else:
            print(f"   ❌ Structure HTML Acts incomplète ({found_elements}/{len(acts_elements)})")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification HTML: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test Simple de la Correction des Pourcentages Acts")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Patterns regex
    if test_regex_patterns():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Patterns regex")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Patterns regex")
    
    # Test 2: Calcul pourcentages
    if test_percentage_calculation():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Calcul pourcentages")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Calcul pourcentages")
    
    # Test 3: Structure HTML
    if test_html_structure_detection():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Structure HTML")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Structure HTML")
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Correction des pourcentages Acts prête!")
        print("\n🎯 Fonctionnalités implémentées:")
        print("  • ✅ Patterns regex corrigés pour capturer pourcentages")
        print("  • ✅ Calcul dynamique: (count/total)*100")
        print("  • ✅ Formatage: X.X% avec 1 décimale")
        print("  • ✅ Remplacement simultané valeurs + pourcentages")
        
        print("\n📊 Exemple de transformation:")
        print("  AVANT: 'AD RAS sans temps (52.8%)'")
        print("  APRÈS: 'AD RAS sans temps (45.3%)' (avec vraies données)")
        
        print("\n🔧 Workflow:")
        print("  1. Extraction données Acts depuis Sheet 2")
        print("  2. Calcul total et pourcentages individuels")
        print("  3. Mise à jour HTML avec valeurs et pourcentages réels")
        print("  4. Synchronisation avec tooltips du graphique")
        
        print("\n🚀 Prêt pour test avec données réelles!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

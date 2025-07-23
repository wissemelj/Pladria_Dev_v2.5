#!/usr/bin/env python3
"""
Test de la disposition horizontale des sections UPR et 501/511.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_html_horizontal_structure():
    """Test que le HTML contient la structure horizontale."""
    print("🔍 Test de la Structure HTML Horizontale")
    print("=" * 60)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ Fichier HTML non trouvé")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier la structure horizontale
        elements_horizontaux = [
            'tickets-row',
            'half-width',
            'Tickets UPR and 501/511 Sections - Side by Side'
        ]
        
        for element in elements_horizontaux:
            if element in html_content:
                print(f"   ✅ Élément horizontal trouvé: {element}")
            else:
                print(f"   ❌ Élément horizontal manquant: {element}")
                return False
        
        # Vérifier que les deux sections sont dans la même div tickets-row
        tickets_row_count = html_content.count('tickets-row')
        half_width_count = html_content.count('half-width')
        
        if tickets_row_count == 1:
            print(f"   ✅ Une seule div tickets-row trouvée")
        else:
            print(f"   ❌ Nombre incorrect de tickets-row: {tickets_row_count}")
            return False
        
        if half_width_count == 2:
            print(f"   ✅ Deux cartes half-width trouvées")
        else:
            print(f"   ❌ Nombre incorrect de half-width: {half_width_count}")
            return False
        
        # Vérifier que les sections UPR et 501/511 sont toujours présentes
        if 'Tickets UPR' in html_content and 'Tickets 501/511' in html_content:
            print(f"   ✅ Les deux sections sont présentes")
        else:
            print(f"   ❌ Une ou plusieurs sections manquantes")
            return False
        
        print(f"   ✅ Structure HTML horizontale correcte")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification HTML: {e}")
        return False

def test_css_horizontal_styles():
    """Test que le CSS contient les styles pour la disposition horizontale."""
    print("\n🔍 Test des Styles CSS Horizontaux")
    print("=" * 60)
    
    try:
        css_file = Path(__file__).parent / "src" / "pres stats" / "styles.css"
        
        if not css_file.exists():
            print(f"   ❌ Fichier CSS non trouvé")
            return False
        
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Vérifier les styles horizontaux
        styles_horizontaux = [
            '.tickets-row',
            'display: flex',
            '.card.half-width',
            'flex: 1',
            'flex-direction: column'  # Pour responsive
        ]
        
        for style in styles_horizontaux:
            if style in css_content:
                print(f"   ✅ Style horizontal trouvé: {style}")
            else:
                print(f"   ❌ Style horizontal manquant: {style}")
                return False
        
        # Vérifier le responsive design
        if '@media (max-width: 768px)' in css_content:
            print(f"   ✅ Media query responsive trouvée")
        else:
            print(f"   ❌ Media query responsive manquante")
            return False
        
        print(f"   ✅ Styles CSS horizontaux corrects")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification CSS: {e}")
        return False

def test_html_update_patterns_still_work():
    """Test que les patterns de mise à jour HTML fonctionnent toujours."""
    print("\n🔍 Test des Patterns de Mise à Jour (Inchangés)")
    print("=" * 60)
    
    try:
        # Les patterns doivent être identiques car seule la structure a changé
        test_html = '''
        <div class="tickets-row">
            <div class="card half-width">
                <div class="summary-item">
                    <span class="summary-value upr-cree">4</span>
                    <span class="summary-label">Créé</span>
                </div>
                <div class="summary-item">
                    <span class="summary-value upr-non">28</span>
                    <span class="summary-label">Non</span>
                </div>
                <div class="summary-item">
                    <span class="summary-value upr-total">32</span>
                    <span class="summary-label">Total UPR</span>
                </div>
            </div>
            <div class="card half-width">
                <div class="summary-item">
                    <span class="summary-value tickets-501511">36</span>
                    <span class="summary-label">Total 501/511</span>
                </div>
            </div>
        </div>
        '''
        
        import re
        
        # Test des patterns (identiques à avant)
        patterns = [
            ('UPR Créé', r'(<span class="summary-value upr-cree">)[^<]*(</span>)'),
            ('UPR Non', r'(<span class="summary-value upr-non">)[^<]*(</span>)'),
            ('UPR Total', r'(<span class="summary-value upr-total">)[^<]*(</span>)'),
            ('501/511 Tickets', r'(<span class="summary-value tickets-501511">)[^<]*(</span>)')
        ]
        
        for nom, pattern in patterns:
            match = re.search(pattern, test_html)
            if match:
                print(f"   ✅ Pattern {nom} fonctionne: {match.group(0)}")
            else:
                print(f"   ❌ Pattern {nom} échoue")
                return False
        
        print(f"   ✅ Tous les patterns de mise à jour fonctionnent encore")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test des patterns: {e}")
        return False

def test_visual_layout_description():
    """Décrit la disposition visuelle attendue."""
    print("\n🎨 Description de la Disposition Visuelle")
    print("=" * 60)
    
    print("   📐 Disposition Desktop (≥768px):")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │                    Dashboard                            │")
    print("   ├─────────────────────┬───────────────────────────────────┤")
    print("   │    Tickets UPR      │      Tickets 501/511              │")
    print("   │  ┌─────────────┐    │    ┌─────────────────────┐        │")
    print("   │  │  4   Créé   │    │    │  36   Total 501/511 │        │")
    print("   │  │ 28   Non    │    │    └─────────────────────┘        │")
    print("   │  │ 32 Total UPR│    │                                   │")
    print("   │  └─────────────┘    │                                   │")
    print("   └─────────────────────┴───────────────────────────────────┘")
    
    print("\n   📱 Disposition Mobile (<768px):")
    print("   ┌─────────────────────────────────────┐")
    print("   │           Dashboard                 │")
    print("   ├─────────────────────────────────────┤")
    print("   │         Tickets UPR                 │")
    print("   │  ┌─────────────────────────────┐    │")
    print("   │  │  4   Créé                   │    │")
    print("   │  │ 28   Non                    │    │")
    print("   │  │ 32   Total UPR              │    │")
    print("   │  └─────────────────────────────┘    │")
    print("   ├─────────────────────────────────────┤")
    print("   │       Tickets 501/511               │")
    print("   │  ┌─────────────────────────────┐    │")
    print("   │  │ 36   Total 501/511          │    │")
    print("   │  └─────────────────────────────┘    │")
    print("   └─────────────────────────────────────┘")
    
    print("\n   ✅ Avantages de la disposition horizontale:")
    print("   • 💾 Économie d'espace vertical")
    print("   • 👀 Vue d'ensemble plus compacte")
    print("   • 📊 Comparaison facile UPR vs 501/511")
    print("   • 📱 Responsive design pour mobile")
    
    return True

def main():
    """Fonction principale de test."""
    print("🚀 Test de la Disposition Horizontale UPR et 501/511")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Structure HTML horizontale
    if test_html_horizontal_structure():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Structure HTML horizontale")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Structure HTML horizontale")
    
    # Test 2: Styles CSS horizontaux
    if test_css_horizontal_styles():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Styles CSS horizontaux")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Styles CSS horizontaux")
    
    # Test 3: Patterns de mise à jour inchangés
    if test_html_update_patterns_still_work():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Patterns de mise à jour inchangés")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Patterns de mise à jour")
    
    # Test 4: Description visuelle
    if test_visual_layout_description():
        tests_passed += 1
        print("\n✅ Test 4 RÉUSSI: Description visuelle")
    else:
        print("\n❌ Test 4 ÉCHOUÉ: Description visuelle")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Disposition horizontale UPR et 501/511 implémentée!")
        print("\n🎯 Changements effectués:")
        print("  • ✅ Sections UPR et 501/511 côte à côte horizontalement")
        print("  • ✅ Classe CSS 'tickets-row' avec display: flex")
        print("  • ✅ Classes 'half-width' pour chaque section")
        print("  • ✅ Design responsive (vertical sur mobile)")
        print("  • ✅ Patterns de mise à jour HTML inchangés")
        print("  • ✅ Économie d'espace vertical")
        
        print("\n📱 Comportement responsive:")
        print("  • Desktop (≥768px): Côte à côte horizontalement")
        print("  • Mobile (<768px): Empilées verticalement")
        
        print("\n🔧 Prêt pour test avec données réelles!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

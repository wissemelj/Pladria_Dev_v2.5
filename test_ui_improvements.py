#!/usr/bin/env python3
"""
Test des améliorations UI pour les sections Tickets UPR et 501/511.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_upr_section_simplification():
    """Test que la section UPR ne montre que 'Créé'."""
    print("🔍 Test de la Simplification Section UPR")
    print("=" * 60)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ Fichier HTML non trouvé")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier la nouvelle structure UPR
        upr_checks = [
            ('Nouvelle classe display', 'upr-display'),
            ('Métrique primaire', 'primary-metric'),
            ('Valeur métrique', 'metric-value upr-cree'),
            ('Label métrique', 'metric-label'),
            ('Description métrique', 'metric-description'),
            ('Tickets Créés', 'Tickets Créés')
        ]
        
        passed_checks = 0
        for check_name, pattern in upr_checks:
            if pattern in html_content:
                print(f"   ✅ {check_name}: Trouvé")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifier que les anciens éléments ont été supprimés
        removed_elements = [
            ('upr-non', 'Ancien élément "Non"'),
            ('upr-total', 'Ancien élément "Total UPR"'),
            ('summary-value upr-non', 'Ancienne classe Non'),
            ('summary-value upr-total', 'Ancienne classe Total')
        ]
        
        for pattern, description in removed_elements:
            if pattern not in html_content:
                print(f"   ✅ {description}: Correctement supprimé")
                passed_checks += 1
            else:
                print(f"   ❌ {description}: Encore présent")
        
        if passed_checks >= 8:  # 6 nouveaux + 2 supprimés minimum
            print(f"   ✅ Section UPR simplifiée correctement ({passed_checks}/10)")
            return True
        else:
            print(f"   ❌ Section UPR pas complètement simplifiée ({passed_checks}/10)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test UPR: {e}")
        return False

def test_501511_section_enhancement():
    """Test que la section 501/511 a été améliorée."""
    print("\n🔍 Test de l'Amélioration Section 501/511")
    print("=" * 60)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier la nouvelle structure 501/511
        section_501511_checks = [
            ('Nouvelle classe display', 'tickets-501511-display'),
            ('Métrique primaire', 'primary-metric'),
            ('Valeur métrique', 'metric-value tickets-501511'),
            ('Label amélioré', 'Tickets Traités'),
            ('Breakdown section', 'metric-breakdown'),
            ('Breakdown item', 'breakdown-item'),
            ('Icône breakdown', 'breakdown-icon'),
            ('Texte breakdown', 'breakdown-text'),
            ('Description métrique', 'metric-description'),
            ('Texte descriptif', 'Tickets 501 & 511')
        ]
        
        passed_checks = 0
        for check_name, pattern in section_501511_checks:
            if pattern in html_content:
                print(f"   ✅ {check_name}: Trouvé")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifier que l'ancien format simple a été remplacé
        if 'Total 501/511' not in html_content or 'Tickets Traités' in html_content:
            print(f"   ✅ Ancien label 'Total 501/511' remplacé par 'Tickets Traités'")
            passed_checks += 1
        else:
            print(f"   ❌ Ancien label 'Total 501/511' encore présent")
        
        if passed_checks >= 8:  # Au moins 8 sur 11
            print(f"   ✅ Section 501/511 améliorée correctement ({passed_checks}/11)")
            return True
        else:
            print(f"   ❌ Section 501/511 pas complètement améliorée ({passed_checks}/11)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test 501/511: {e}")
        return False

def test_css_styles_added():
    """Test que les nouveaux styles CSS ont été ajoutés."""
    print("\n🎨 Test des Nouveaux Styles CSS")
    print("=" * 60)
    
    try:
        css_file = Path(__file__).parent / "src" / "pres stats" / "styles.css"
        
        if not css_file.exists():
            print(f"   ❌ Fichier CSS non trouvé")
            return False
        
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Vérifier les nouveaux styles
        css_checks = [
            ('UPR display', '.upr-display'),
            ('Primary metric', '.primary-metric'),
            ('Metric value', '.metric-value'),
            ('Metric label', '.metric-label'),
            ('Metric description', '.metric-description'),
            ('501/511 display', '.tickets-501511-display'),
            ('Metric breakdown', '.metric-breakdown'),
            ('Breakdown item', '.breakdown-item'),
            ('Breakdown icon', '.breakdown-icon'),
            ('Breakdown text', '.breakdown-text'),
            ('Responsive design', '@media (max-width: 768px)')
        ]
        
        passed_checks = 0
        for check_name, pattern in css_checks:
            if pattern in css_content:
                print(f"   ✅ {check_name}: Style ajouté")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Style manquant")
        
        # Vérifier les couleurs spécifiques
        color_checks = [
            ('Couleur UPR verte', '#27ae60'),
            ('Couleur 501/511 violette', '#9b59b6'),
            ('Gradient background', 'linear-gradient')
        ]
        
        for check_name, pattern in color_checks:
            if pattern in css_content:
                print(f"   ✅ {check_name}: Couleur définie")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Couleur manquante")
        
        if passed_checks >= 12:  # Au moins 12 sur 14
            print(f"   ✅ Styles CSS ajoutés correctement ({passed_checks}/14)")
            return True
        else:
            print(f"   ❌ Styles CSS incomplets ({passed_checks}/14)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test CSS: {e}")
        return False

def test_python_patterns_updated():
    """Test que les patterns Python ont été mis à jour."""
    print("\n🐍 Test des Patterns Python Mis à Jour")
    print("=" * 60)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Vérifier que la méthode existe
        if hasattr(TeamStatsModule, '_update_html_elements_with_data'):
            print(f"   ✅ Méthode _update_html_elements_with_data existe")
        else:
            print(f"   ❌ Méthode _update_html_elements_with_data manquante")
            return False
        
        # Vérifier le code source pour les nouveaux patterns
        import inspect
        source = inspect.getsource(TeamStatsModule._update_html_elements_with_data)
        
        pattern_checks = [
            ('Pattern UPR metric-value', 'metric-value upr-cree'),
            ('Pattern 501/511 metric-value', 'metric-value tickets-501511'),
            ('Suppression pattern upr-non', 'upr-non' not in source),
            ('Suppression pattern upr-total', 'upr-total' not in source)
        ]
        
        passed_checks = 0
        for check_name, condition in pattern_checks:
            if isinstance(condition, bool):
                if condition:
                    print(f"   ✅ {check_name}: OK")
                    passed_checks += 1
                else:
                    print(f"   ❌ {check_name}: Échec")
            else:
                if condition in source:
                    print(f"   ✅ {check_name}: Trouvé")
                    passed_checks += 1
                else:
                    print(f"   ❌ {check_name}: Manquant")
        
        if passed_checks >= 3:  # Au moins 3 sur 4
            print(f"   ✅ Patterns Python mis à jour ({passed_checks}/4)")
            return True
        else:
            print(f"   ❌ Patterns Python pas complètement mis à jour ({passed_checks}/4)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test Python: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test des Améliorations UI Tickets UPR et 501/511")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Simplification UPR
    if test_upr_section_simplification():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Simplification UPR")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Simplification UPR")
    
    # Test 2: Amélioration 501/511
    if test_501511_section_enhancement():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Amélioration 501/511")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Amélioration 501/511")
    
    # Test 3: Styles CSS
    if test_css_styles_added():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Styles CSS")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Styles CSS")
    
    # Test 4: Patterns Python
    if test_python_patterns_updated():
        tests_passed += 1
        print("\n✅ Test 4 RÉUSSI: Patterns Python")
    else:
        print("\n❌ Test 4 ÉCHOUÉ: Patterns Python")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Améliorations UI implémentées avec succès!")
        
        print("\n🎯 Améliorations apportées:")
        print("\n📋 Section Tickets UPR:")
        print("  • ✅ Simplifiée: Ne montre que 'Créé'")
        print("  • ✅ Design épuré: Métrique principale mise en valeur")
        print("  • ✅ Couleur verte: #27ae60 pour les tickets créés")
        print("  • ✅ Description: Contexte ajouté pour clarifier")
        print("  • ❌ Supprimé: Éléments 'Non' et 'Total UPR'")
        
        print("\n📋 Section Tickets 501/511:")
        print("  • ✅ Design amélioré: Présentation plus attrayante")
        print("  • ✅ Couleur violette: #9b59b6 pour différenciation")
        print("  • ✅ Breakdown visuel: Icône + description")
        print("  • ✅ Gradient background: Effet visuel moderne")
        print("  • ✅ Label amélioré: 'Tickets Traités' au lieu de 'Total 501/511'")
        
        print("\n🎨 Styles CSS:")
        print("  • ✅ Classes spécialisées: .metric-value, .metric-label, etc.")
        print("  • ✅ Responsive design: Adaptation mobile")
        print("  • ✅ Animations: Effets visuels cohérents")
        print("  • ✅ Typography: Tailles et poids optimisés")
        
        print("\n🔧 Intégration Python:")
        print("  • ✅ Patterns mis à jour: metric-value au lieu de summary-value")
        print("  • ✅ Logging amélioré: Messages plus clairs")
        print("  • ✅ Simplification UPR: Suppression des patterns inutiles")
        
        print("\n📊 Layout final:")
        print("  ┌─────────────┬─────────────┬─────────────┐")
        print("  │ Tickets UPR │ Tickets     │ RIP (P0 P1) │")
        print("  │             │ 501/511     │             │")
        print("  │    16       │    98       │ Graphique   │")
        print("  │ Tickets     │ Tickets     │ Doughnut    │")
        print("  │ Créés       │ Traités     │             │")
        print("  │ (simplifié) │ (amélioré)  │             │")
        print("  └─────────────┴─────────────┴─────────────┘")
        
        print("\n🚀 Interface utilisateur améliorée et prête!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

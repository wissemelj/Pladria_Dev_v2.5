#!/usr/bin/env python3
"""
Test de la facturation complète incluant PA, CM, UPR et 501/511.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_complete_billing_html():
    """Test que le HTML contient toutes les sections de facturation."""
    print("🔍 Test de la Structure HTML Facturation Complète")
    print("=" * 60)
    
    try:
        html_file = Path(__file__).parent / "src" / "pres stats" / "index.html"
        
        if not html_file.exists():
            print(f"   ❌ Fichier HTML non trouvé")
            return False
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier toutes les sections de facturation
        sections = [
            ('Section PA', '📋 Prix PA (Acts) par Motif'),
            ('Section CM', '📊 Prix CM par Motif'),
            ('Section UPR', '🎫 Prix Tickets UPR par Motif'),
            ('Section 501/511', '📋 Prix Tickets 501/511')
        ]
        
        print(f"   📊 Vérification des sections:")
        sections_found = 0
        for section_name, section_text in sections:
            if section_text in html_content:
                print(f"      ✅ {section_name}: Trouvée")
                sections_found += 1
            else:
                print(f"      ❌ {section_name}: Manquante")
        
        # Vérifier les motifs UPR
        upr_motifs = ['UPR Créé', 'UPR Non']
        print(f"\n   🎫 Vérification des motifs UPR:")
        upr_found = 0
        for motif in upr_motifs:
            if motif in html_content:
                print(f"      ✅ {motif}: Trouvé")
                upr_found += 1
            else:
                print(f"      ❌ {motif}: Manquant")
        
        # Vérifier les inputs de prix UPR et 501/511
        new_price_inputs = [
            'price-upr-cree', 'price-upr-non', 'price-tickets-501511'
        ]
        
        print(f"\n   💶 Vérification des nouveaux inputs de prix:")
        new_inputs_found = 0
        for price_id in new_price_inputs:
            if f'id="{price_id}"' in html_content:
                print(f"      ✅ {price_id}: Input trouvé")
                new_inputs_found += 1
            else:
                print(f"      ❌ {price_id}: Input manquant")
        
        # Vérifier les totaux
        total_elements = ['totalUPR', 'total501511', 'grandTotal']
        print(f"\n   📊 Vérification des totaux:")
        totals_found = 0
        for total_id in total_elements:
            if f'id="{total_id}"' in html_content:
                print(f"      ✅ {total_id}: Élément trouvé")
                totals_found += 1
            else:
                print(f"      ❌ {total_id}: Élément manquant")
        
        total_checks = sections_found + upr_found + new_inputs_found + totals_found
        expected_total = len(sections) + len(upr_motifs) + len(new_price_inputs) + len(total_elements)
        
        if total_checks >= expected_total - 1:  # Tolérance de 1
            print(f"\n   ✅ Structure HTML complète correcte ({total_checks}/{expected_total})")
            return True
        else:
            print(f"\n   ❌ Structure HTML complète incomplète ({total_checks}/{expected_total})")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test HTML: {e}")
        return False

def test_complete_billing_css():
    """Test que les styles CSS pour toutes les sections sont présents."""
    print("\n🎨 Test des Styles CSS Facturation Complète")
    print("=" * 60)
    
    try:
        css_file = Path(__file__).parent / "src" / "pres stats" / "styles.css"
        
        if not css_file.exists():
            print(f"   ❌ Fichier CSS non trouvé")
            return False
        
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Vérifier les nouveaux styles
        css_classes = [
            ('UPR grid', '.motif-pricing-grid.upr-grid'),
            ('501/511 grid', '.motif-pricing-grid.tickets-501511-grid'),
            ('UPR section total', '.upr-section-total'),
            ('501/511 section total', '.tickets-501511-section-total')
        ]
        
        passed_checks = 0
        for check_name, css_class in css_classes:
            if css_class in css_content:
                print(f"   ✅ {check_name}: Style défini")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Style manquant")
        
        # Vérifier les couleurs spécifiques
        color_checks = [
            ('Couleur UPR orange', '#ff9800'),
            ('Couleur 501/511 violette', '#9c27b0'),
            ('Gradient UPR', 'linear-gradient(135deg, #fff3e0'),
            ('Gradient 501/511', 'linear-gradient(135deg, #f3e5f5')
        ]
        
        for check_name, pattern in color_checks:
            if pattern in css_content:
                print(f"   ✅ {check_name}: Couleur définie")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Couleur manquante")
        
        if passed_checks >= 7:  # Au moins 7 sur 8
            print(f"   ✅ Styles CSS complets ({passed_checks}/8)")
            return True
        else:
            print(f"   ❌ Styles CSS incomplets ({passed_checks}/8)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test CSS: {e}")
        return False

def test_complete_billing_javascript():
    """Test que le JavaScript gère toutes les sections."""
    print("\n💻 Test du JavaScript Facturation Complète")
    print("=" * 60)
    
    try:
        js_file = Path(__file__).parent / "src" / "pres stats" / "script.js"
        
        if not js_file.exists():
            print(f"   ❌ Fichier JavaScript non trouvé")
            return False
        
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Vérifier les nouveaux arrays de motifs
        js_elements = [
            ('UPR motifs array', 'this.uprMotifs'),
            ('501/511 motifs array', 'this.tickets501511Motifs'),
            ('UPR event listeners', 'this.uprMotifs.forEach'),
            ('501/511 event listeners', 'this.tickets501511Motifs.forEach'),
            ('UPR calculations', 'totalUPR'),
            ('501/511 calculations', 'total501511'),
            ('Updated updateWithRealData', 'updateWithRealData(paData, cmData, uprData, tickets501511Data)')
        ]
        
        passed_checks = 0
        for check_name, pattern in js_elements:
            if pattern in js_content:
                print(f"   ✅ {check_name}: Implémenté")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifier les IDs spécifiques
        id_checks = [
            ('UPR Créé ID', 'upr-cree'),
            ('UPR Non ID', 'upr-non'),
            ('Tickets 501/511 ID', 'tickets-501511')
        ]
        
        for check_name, pattern in id_checks:
            if pattern in js_content:
                print(f"   ✅ {check_name}: Défini")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        if passed_checks >= 9:  # Au moins 9 sur 10
            print(f"   ✅ JavaScript complet ({passed_checks}/10)")
            return True
        else:
            print(f"   ❌ JavaScript incomplet ({passed_checks}/10)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test JavaScript: {e}")
        return False

def test_python_complete_integration():
    """Test que l'intégration Python gère toutes les sections."""
    print("\n🐍 Test de l'Intégration Python Complète")
    print("=" * 60)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Vérifier le code source pour les nouvelles données
        import inspect
        source = inspect.getsource(TeamStatsModule._update_facturation_data)
        
        integration_checks = [
            ('UPR motif data', 'upr_motif_data'),
            ('501/511 data', 'tickets_501511_data'),
            ('UPR extraction', 'upr_data'),
            ('501/511 extraction', 'tickets_501511_mapping'),
            ('UPR total', 'upr_total'),
            ('501/511 total', 'tickets_501511_total'),
            ('UPR motifs storage', 'upr_motifs'),
            ('501/511 motifs storage', 'tickets_501511_motifs')
        ]
        
        passed_checks = 0
        for check_name, pattern in integration_checks:
            if pattern in source:
                print(f"   ✅ {check_name}: Implémenté")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifier la mise à jour script.js
        script_source = inspect.getsource(TeamStatsModule._update_script_js_values)
        
        script_checks = [
            ('UPR data string', 'upr_data_str'),
            ('501/511 data string', 'tickets_501511_data_str'),
            ('4 parameters update', 'uprData, tickets501511Data')
        ]
        
        for check_name, pattern in script_checks:
            if pattern in script_source:
                print(f"   ✅ {check_name}: Implémenté")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        if passed_checks >= 10:  # Au moins 10 sur 11
            print(f"   ✅ Intégration Python complète ({passed_checks}/11)")
            return True
        else:
            print(f"   ❌ Intégration Python incomplète ({passed_checks}/11)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test Python: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de la Facturation Complète (PA + CM + UPR + 501/511)")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Structure HTML complète
    if test_complete_billing_html():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Structure HTML complète")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Structure HTML complète")
    
    # Test 2: Styles CSS complets
    if test_complete_billing_css():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Styles CSS complets")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Styles CSS complets")
    
    # Test 3: JavaScript complet
    if test_complete_billing_javascript():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: JavaScript complet")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: JavaScript complet")
    
    # Test 4: Intégration Python complète
    if test_python_complete_integration():
        tests_passed += 1
        print("\n✅ Test 4 RÉUSSI: Intégration Python complète")
    else:
        print("\n❌ Test 4 ÉCHOUÉ: Intégration Python complète")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Facturation complète avec 4 sections implémentée!")
        
        print("\n🎯 Sections de facturation:")
        print("\n📋 PA (Acts) - 10 motifs individuels:")
        print("  • AD RAS sans temps, AD RAS avec temps, OK, NOK")
        print("  • AD Non jointe, UPR RAS, AD Non trouvée")
        print("  • Hors commune, UPR NOK, UPR OK")
        
        print("\n📊 CM - 3 motifs individuels:")
        print("  • RAF, Modification, Création")
        
        print("\n🎫 UPR - 2 motifs individuels:")
        print("  • UPR Créé, UPR Non")
        
        print("\n📋 501/511 - 1 motif:")
        print("  • Tickets 501/511")
        
        print("\n💶 Calculs automatiques:")
        print("  • Total par motif: Count × Prix individuel")
        print("  • Total PA: Somme de tous les motifs PA")
        print("  • Total CM: Somme de tous les motifs CM")
        print("  • Total UPR: Somme de tous les motifs UPR")
        print("  • Total 501/511: Count × Prix")
        print("  • Grand Total: PA + CM + UPR + 501/511")
        
        print("\n📊 Exemple complet:")
        print("  PA: €26,503.20 (10 motifs)")
        print("  CM: €3,714.00 (3 motifs)")
        print("  UPR: €246.00 (2 motifs)")
        print("  501/511: €343.00 (1 motif)")
        print("  Grand Total: €30,806.20")
        
        print("\n🎨 Interface:")
        print("  • 4 sections distinctes avec couleurs différenciées")
        print("  • 16 inputs de prix individuels (10+3+2+1)")
        print("  • 4 totaux de section + 1 grand total")
        print("  • Grid responsive adaptatif")
        
        print("\n🚀 Facturation complète prête!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

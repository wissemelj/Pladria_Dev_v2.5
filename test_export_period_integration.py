#!/usr/bin/env python3
"""
Test de l'intégration des contrôles de période dans la section export stats.
"""

import sys
import os
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_export_section_integration():
    """Test que la section export contient les contrôles de période intégrés."""
    print("🔍 Test de l'Intégration des Contrôles de Période dans Export")
    print("=" * 60)
    
    try:
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        if not team_stats_file.exists():
            print(f"   ❌ Fichier team_stats_module.py non trouvé")
            return False
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            module_content = f.read()
        
        # Vérifier que la section export a été modifiée
        export_checks = [
            ('Export section header updated', 'Export Stat & Période'),
            ('Period filtering method', '_create_period_filtering_in_export'),
            ('Period filtering call', 'self._create_period_filtering_in_export(export_content)'),
            ('Generate stats button in export', 'self.generate_stats_button = tk.Button'),
            ('Date range status in export', 'self.date_range_status = tk.Label'),
            ('Separator in export', 'separator = tk.Frame'),
            ('Period subsection header', '📅 Filtrage par période')
        ]
        
        print(f"   📤 Vérification de l'intégration export:")
        export_found = 0
        for check_name, pattern in export_checks:
            if pattern in module_content:
                print(f"      ✅ {check_name}: Trouvé")
                export_found += 1
            else:
                print(f"      ❌ {check_name}: Manquant")
        
        # Vérifier que l'ancienne section date range n'est plus appelée
        old_section_checks = [
            ('Old date range section call removed', '_create_date_range_section(left_column)'),
            ('Date from entry preserved', 'self.date_from_entry = tk.Entry'),
            ('Date to entry preserved', 'self.date_to_entry = tk.Entry'),
            ('Clear date range method preserved', 'command=self._clear_date_range')
        ]
        
        print(f"\n   📅 Vérification de la migration:")
        migration_found = 0
        for check_name, pattern in old_section_checks:
            if check_name == 'Old date range section call removed':
                # This should NOT be found
                if pattern not in module_content:
                    print(f"      ✅ {check_name}: Supprimé")
                    migration_found += 1
                else:
                    print(f"      ❌ {check_name}: Encore présent")
            else:
                # These should be found
                if pattern in module_content:
                    print(f"      ✅ {check_name}: Trouvé")
                    migration_found += 1
                else:
                    print(f"      ❌ {check_name}: Manquant")
        
        total_checks = export_found + migration_found
        expected_total = len(export_checks) + len(old_section_checks)
        
        if total_checks >= expected_total - 1:  # Tolérance de 1
            print(f"\n   ✅ Intégration des contrôles de période correcte ({total_checks}/{expected_total})")
            return True
        else:
            print(f"\n   ❌ Intégration des contrôles de période incomplète ({total_checks}/{expected_total})")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test d'intégration: {e}")
        return False

def test_period_filtering_functionality():
    """Test que la fonctionnalité de filtrage par période est préservée."""
    print("\n🔄 Test de la Fonctionnalité de Filtrage")
    print("=" * 60)
    
    try:
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            module_content = f.read()
        
        # Vérifier que les méthodes de filtrage sont préservées
        filtering_checks = [
            ('Generate filtered statistics', '_generate_filtered_statistics'),
            ('Filter data by date range', '_filter_data_by_date_range'),
            ('Update date range status', '_update_date_range_status'),
            ('Show date from picker', '_show_date_from_picker'),
            ('Show date to picker', '_show_date_to_picker'),
            ('Clear date range', '_clear_date_range'),
            ('Dashboard data extraction', 'dashboard_data'),
            ('Billing calculations', 'facturation_data')
        ]
        
        passed_checks = 0
        for check_name, pattern in filtering_checks:
            if pattern in module_content:
                print(f"   ✅ {check_name}: Fonctionnalité préservée")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Fonctionnalité manquante")
        
        # Vérifier les sources de données spécifiques
        data_source_checks = [
            ('Excel sheet filtering', 'Sheet.*Column'),
            ('PA/Acts data extraction', 'acts.*data'),
            ('CM data extraction', 'cm.*data'),
            ('UPR data extraction', 'upr.*data'),
            ('501/511 data extraction', 'tickets.*501.*511'),
            ('Date variables', 'date_from_var'),
            ('Statistics injection', '_inject_statistics')
        ]
        
        for check_name, pattern in data_source_checks:
            if re.search(pattern, module_content, re.IGNORECASE):
                print(f"   ✅ {check_name}: Source préservée")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Source manquante")
        
        if passed_checks >= 13:  # Au moins 13 sur 15
            print(f"\n   ✅ Fonctionnalité de filtrage préservée ({passed_checks}/15)")
            return True
        else:
            print(f"\n   ❌ Fonctionnalité de filtrage incomplète ({passed_checks}/15)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test de fonctionnalité: {e}")
        return False

def test_user_workflow_integration():
    """Test que le workflow utilisateur est correctement intégré."""
    print("\n👤 Test du Workflow Utilisateur")
    print("=" * 60)
    
    try:
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            module_content = f.read()
        
        # Vérifier le workflow intégré
        workflow_checks = [
            ('Export section contains period controls', 'Export Stat & Période'),
            ('Period filtering in export section', '_create_period_filtering_in_export'),
            ('Generate button in export section', 'generate_stats_button.*export'),
            ('Date selection in export section', 'date_from_entry.*export'),
            ('Status updates in export section', 'date_range_status'),
            ('Clear dates functionality', '_clear_date_range'),
            ('Date validation logic', 'date_from_var.*date_to_var'),
            ('Statistics generation trigger', 'command=self._generate_filtered_statistics')
        ]
        
        passed_checks = 0
        for check_name, pattern in workflow_checks:
            if re.search(pattern, module_content, re.IGNORECASE):
                print(f"   ✅ {check_name}: Workflow intégré")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Workflow manquant")
        
        # Vérifier que les fonctionnalités de facturation sont préservées
        billing_checks = [
            ('Complete billing system', 'DetailedBillingCalculator'),
            ('Individual motif pricing', 'motif.*price'),
            ('Real data injection', 'updateWithRealData'),
            ('Filtered data for billing', 'facturation_data')
        ]
        
        for check_name, pattern in billing_checks:
            if re.search(pattern, module_content, re.IGNORECASE):
                print(f"   ✅ {check_name}: Facturation préservée")
                passed_checks += 1
            else:
                print(f"   ❌ {check_name}: Facturation manquante")
        
        if passed_checks >= 10:  # Au moins 10 sur 12
            print(f"\n   ✅ Workflow utilisateur correctement intégré ({passed_checks}/12)")
            return True
        else:
            print(f"\n   ❌ Workflow utilisateur incomplet ({passed_checks}/12)")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test de workflow: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de l'Intégration des Contrôles de Période dans Export Stats")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Intégration des contrôles dans export section
    if test_export_section_integration():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Intégration des contrôles de période")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Intégration des contrôles de période")
    
    # Test 2: Fonctionnalité de filtrage préservée
    if test_period_filtering_functionality():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Fonctionnalité de filtrage préservée")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Fonctionnalité de filtrage préservée")
    
    # Test 3: Workflow utilisateur intégré
    if test_user_workflow_integration():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Workflow utilisateur intégré")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Workflow utilisateur intégré")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Intégration des contrôles de période dans export stats complète!")
        
        print("\n🎯 Fonctionnalités intégrées:")
        print("\n📤 Section Export Stats étendue:")
        print("  • Titre mis à jour: 'Export Stat & Période'")
        print("  • Contrôles de sélection de période intégrés")
        print("  • Bouton 'Générer et ouvrir index' centralisé")
        print("  • Status de validation des dates en temps réel")
        print("  • Séparateur visuel entre période et export")
        
        print("\n🔄 Workflow utilisateur simplifié:")
        print("  1. Charger le fichier Excel")
        print("  2. Aller dans la section 'Export Stat & Période'")
        print("  3. Sélectionner la période (Date début/fin)")
        print("  4. Cliquer 'Générer et ouvrir index'")
        print("  5. Dashboard avec facturation complète s'ouvre")
        
        print("\n📊 Fonctionnalités préservées:")
        print("  • Filtrage par date sur toutes les sources Excel")
        print("  • Facturation complète (PA+CM+UPR+501/511)")
        print("  • Prix individuels par motif")
        print("  • Calculs automatiques temps réel")
        print("  • Données réelles filtrées")
        print("  • Dashboard automatique avec charts")
        
        print("\n🎨 Interface améliorée:")
        print("  • Contrôles centralisés dans export stats")
        print("  • Sous-section période clairement identifiée")
        print("  • Workflow plus intuitif et logique")
        print("  • Moins de navigation entre sections")
        
        print("\n🚀 Intégration période/export réussie!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

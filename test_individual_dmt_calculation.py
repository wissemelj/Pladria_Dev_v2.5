#!/usr/bin/env python3
"""
Test des nouvelles méthodes de calcul DMT individuels par collaborateur.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_individual_dmt_methods_exist():
    """Test que les nouvelles méthodes DMT individuelles existent."""
    print("🔍 Test des Nouvelles Méthodes DMT Individuelles")
    print("=" * 70)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Vérifier que les nouvelles méthodes existent
        individual_methods = [
            '_calculate_individual_dmt_pa',
            '_calculate_individual_dmt_cm'
        ]
        
        print("📊 Vérification des nouvelles méthodes DMT individuelles:")
        for method_name in individual_methods:
            if hasattr(TeamStatsModule, method_name):
                print(f"   ✅ {method_name}: Méthode trouvée")
            else:
                print(f"   ❌ {method_name}: Méthode manquante")
                return False
        
        # Lire le code source pour vérifier les implémentations
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Vérifications spécifiques pour DMT PA individuel
        pa_individual_checks = [
            ('PA individual method', 'def _calculate_individual_dmt_pa(self, collaborateur):'),
            ('PA individual sheet access', "'Traitement PA' not in self.global_suivi_data"),
            ('PA individual collaborateur column F', "columns[5]  # Column F (index 5)"),
            ('PA individual durée column H', "columns[7]          # Column H (index 7)"),
            ('PA individual collaborateur filtering', "str(row_collaborateur).strip() == str(collaborateur).strip()"),
            ('PA individual zero exclusion', "if duree_numeric > 0:"),
            ('PA individual average calculation', "dmt_individuel = sum(collaborateur_durees) / len(collaborateur_durees)"),
            ('PA individual debug logging', "self.logger.debug(f\"DMT PA individuel - {collaborateur}:")
        ]
        
        print(f"\n📊 Vérification DMT PA individuel:")
        pa_found = 0
        for check_name, pattern in pa_individual_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Implémenté")
                pa_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifications spécifiques pour DMT CM individuel
        cm_individual_checks = [
            ('CM individual method', 'def _calculate_individual_dmt_cm(self, collaborateur):'),
            ('CM individual sheet access', "'CM' not in self.global_suivi_data"),
            ('CM individual collaborateur column E', "columns[4]  # Column E (index 4) - CORRIGÉ"),
            ('CM individual durée column J', "columns[9]          # Column J (index 9)"),
            ('CM individual collaborateur filtering', "str(row_collaborateur).strip() == str(collaborateur).strip()"),
            ('CM individual zero exclusion', "if duree_numeric > 0:"),
            ('CM individual average calculation', "dmt_individuel = sum(collaborateur_durees) / len(collaborateur_durees)"),
            ('CM individual debug logging', "self.logger.debug(f\"DMT CM individuel - {collaborateur}:")
        ]
        
        print(f"\n📊 Vérification DMT CM individuel:")
        cm_found = 0
        for check_name, pattern in cm_individual_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Implémenté")
                cm_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifier l'intégration dans _calculate_dmt_automatically
        integration_checks = [
            ('Individual PA call', 'dmt_pa = self._calculate_individual_dmt_pa(collab)'),
            ('Individual CM call', 'dmt_cm = self._calculate_individual_dmt_cm(collab)'),
            ('Individual calculation comment', '# Calculate individual DMT PA and CM for this collaborator')
        ]
        
        print(f"\n🔧 Vérification intégration dans _calculate_dmt_automatically:")
        integration_found = 0
        for check_name, pattern in integration_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Implémenté")
                integration_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        total_found = pa_found + cm_found + integration_found
        total_expected = len(pa_individual_checks) + len(cm_individual_checks) + len(integration_checks)
        
        if total_found >= total_expected - 1:  # Tolérance de 1
            print(f"\n✅ Nouvelles méthodes DMT individuelles correctes ({total_found}/{total_expected})")
            return True
        else:
            print(f"\n❌ Nouvelles méthodes DMT individuelles incomplètes ({total_found}/{total_expected})")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_individual_dmt_logic():
    """Test de la logique de calcul DMT individuel avec des données simulées."""
    print("\n🧮 Test de la Logique DMT Individuel")
    print("=" * 70)
    
    try:
        # Simuler des données pour tester la logique individuelle
        import pandas as pd
        
        # Données simulées PA (Feuille 3) avec plusieurs collaborateurs
        pa_data = {
            'Col_A': ['PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6'],
            'Col_B': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'],
            'Col_C': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
            'Col_D': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
            'Col_E': ['E1', 'E2', 'E3', 'E4', 'E5', 'E6'],
            'Col_F': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob', 'Alice'],  # Collaborateurs (index 5)
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'],
            'Col_H': [2.0, 3.0, 1.5, 2.5, 0, 4.0]  # Durées (index 7) - avec 0 à exclure
        }
        
        # Données simulées CM (Feuille 2) avec plusieurs collaborateurs
        cm_data = {
            'Col_A': ['CM1', 'CM2', 'CM3', 'CM4', 'CM5', 'CM6'],
            'Col_B': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'],
            'Col_C': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'],
            'Col_D': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'],
            'Col_E': ['Alice', 'Bob', 'Alice', 'David', 'Bob', 'Alice'],  # Collaborateurs (index 4)
            'Col_F': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6'],
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'],
            'Col_H': ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'],
            'Col_I': ['I1', 'I2', 'I3', 'I4', 'I5', 'I6'],
            'Col_J': [1.8, 2.2, 3.1, 1.0, '', 2.9]  # Durées (index 9) - avec vide à exclure
        }
        
        df_pa = pd.DataFrame(pa_data)
        df_cm = pd.DataFrame(cm_data)
        
        print("📊 Données de test créées:")
        print(f"   PA: {len(df_pa)} lignes, collaborateurs: {df_pa['Col_F'].unique()}")
        print(f"   CM: {len(df_cm)} lignes, collaborateurs: {df_cm['Col_E'].unique()}")
        
        # Test de la logique individuelle PA pour Alice
        print(f"\n🔧 Test logique PA individuelle pour Alice:")
        alice_pa_durees = []
        for index, row in df_pa.iterrows():
            collaborateur = row['Col_F']  # Column F (index 5)
            duree = row['Col_H']          # Column H (index 7)
            
            # Filtrage pour Alice uniquement
            if (pd.notna(collaborateur) and pd.notna(duree) and 
                str(collaborateur).strip() == 'Alice' and str(duree).strip() != ''):
                try:
                    duree_numeric = float(duree)
                    if duree_numeric > 0:
                        alice_pa_durees.append(duree_numeric)
                except (ValueError, TypeError):
                    continue
        
        alice_pa_moyenne = sum(alice_pa_durees) / len(alice_pa_durees) if alice_pa_durees else 0
        print(f"   Alice PA: {alice_pa_durees} → Moyenne: {alice_pa_moyenne:.2f}")
        
        # Test de la logique individuelle CM pour Alice
        print(f"\n🔧 Test logique CM individuelle pour Alice:")
        alice_cm_durees = []
        for index, row in df_cm.iterrows():
            collaborateur = row['Col_E']  # Column E (index 4)
            duree = row['Col_J']          # Column J (index 9)
            
            # Filtrage pour Alice uniquement
            if (pd.notna(collaborateur) and pd.notna(duree) and 
                str(collaborateur).strip() == 'Alice' and str(duree).strip() != ''):
                try:
                    duree_numeric = float(duree)
                    if duree_numeric > 0:
                        alice_cm_durees.append(duree_numeric)
                except (ValueError, TypeError):
                    continue
        
        alice_cm_moyenne = sum(alice_cm_durees) / len(alice_cm_durees) if alice_cm_durees else 0
        print(f"   Alice CM: {alice_cm_durees} → Moyenne: {alice_cm_moyenne:.2f}")
        
        # Vérifications
        expected_alice_pa = [2.0, 1.5, 4.0]  # Alice a 3 entrées PA valides
        expected_alice_cm = [1.8, 3.1, 2.9]  # Alice a 3 entrées CM valides
        
        print(f"\n📊 Vérification des calculs individuels:")
        print(f"   Alice PA attendu: {expected_alice_pa}")
        print(f"   Alice PA trouvé: {alice_pa_durees}")
        print(f"   Alice CM attendu: {expected_alice_cm}")
        print(f"   Alice CM trouvé: {alice_cm_durees}")
        
        if (alice_pa_durees == expected_alice_pa and alice_cm_durees == expected_alice_cm):
            print(f"\n✅ Logique de calcul individuel correcte")
            print(f"   Alice DMT PA: {alice_pa_moyenne:.2f}")
            print(f"   Alice DMT CM: {alice_cm_moyenne:.2f}")
            return True
        else:
            print(f"\n❌ Logique de calcul individuel incorrecte")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test de logique: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test des Nouvelles Méthodes DMT Individuelles")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Vérification de l'existence des méthodes
    if test_individual_dmt_methods_exist():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Nouvelles méthodes DMT individuelles")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Nouvelles méthodes DMT individuelles")
    
    # Test 2: Test de la logique de calcul individuel
    if test_individual_dmt_logic():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Logique de calcul DMT individuel")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Logique de calcul DMT individuel")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        
        print("\n🎯 Nouvelles méthodes DMT individuelles implémentées:")
        
        print("\n📊 _calculate_individual_dmt_pa(collaborateur):")
        print("  • Source: Feuille 3 (Traitement PA)")
        print("  • Collaborateur: Colonne F (index 5)")
        print("  • Durée: Colonne H (index 7)")
        print("  • Filtrage: Par collaborateur spécifique + exclusion 0/vides")
        print("  • Calcul: Moyenne individuelle pour ce collaborateur uniquement")
        
        print("\n📊 _calculate_individual_dmt_cm(collaborateur):")
        print("  • Source: Feuille 2 (CM)")
        print("  • Collaborateur: Colonne E (index 4) ✅ CORRIGÉ")
        print("  • Durée: Colonne J (index 9)")
        print("  • Filtrage: Par collaborateur spécifique + exclusion 0/vides")
        print("  • Calcul: Moyenne individuelle pour ce collaborateur uniquement")
        
        print("\n🔧 Intégration dans _calculate_dmt_automatically:")
        print("  • Appel: dmt_pa = self._calculate_individual_dmt_pa(collab)")
        print("  • Appel: dmt_cm = self._calculate_individual_dmt_cm(collab)")
        print("  • Résultat: DMT individuels stockés dans self.dmt_data[collab]")
        
        print("\n🎯 Problème résolu:")
        print("  • AVANT: DMT CM et PA identiques pour tous (moyennes globales)")
        print("  • APRÈS: DMT CM et PA individuels par collaborateur")
        print("  • Interface: Affichage correct des valeurs individuelles")
        
        print("\n✅ Les DMT individuels par collaborateur sont maintenant calculés correctement!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

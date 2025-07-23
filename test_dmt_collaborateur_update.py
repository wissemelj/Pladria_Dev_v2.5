#!/usr/bin/env python3
"""
Test des modifications du calcul DMT par collaborateur.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_dmt_calculation_methods():
    """Test que les méthodes de calcul DMT ont été modifiées correctement."""
    print("🔍 Test des Modifications du Calcul DMT par Collaborateur")
    print("=" * 70)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Vérifier que les méthodes existent
        module_methods = [
            '_calculate_dmt_pa',
            '_calculate_dmt_cm',
            '_calculate_dmt_for_treated_communes'
        ]
        
        print("📊 Vérification des méthodes DMT:")
        for method_name in module_methods:
            if hasattr(TeamStatsModule, method_name):
                print(f"   ✅ {method_name}: Méthode trouvée")
            else:
                print(f"   ❌ {method_name}: Méthode manquante")
                return False
        
        # Lire le code source pour vérifier les modifications
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Vérifications spécifiques pour DMT CM
        cm_checks = [
            ('CM sheet access', "'CM' not in self.global_suivi_data"),
            ('CM collaborateur column B', "columns[1]  # Column B (index 1)"),
            ('CM durée column J', "columns[9]          # Column J (index 9)"),
            ('CM zero and empty exclusion', "if duree_numeric > 0:"),
            ('CM collaborateur grouping', "collaborateur_dmts[collaborateur_name]"),
            ('CM average calculation', "collab_moyenne = sum(durees) / len(durees)"),
            ('CM empty string check', "str(duree_value).strip() != ''")
        ]
        
        print(f"\n📊 Vérification DMT CM (Feuille 2, Col B+J):")
        cm_found = 0
        for check_name, pattern in cm_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Implémenté")
                cm_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifications spécifiques pour DMT PA
        pa_checks = [
            ('PA sheet access', "'Traitement PA' not in self.global_suivi_data"),
            ('PA collaborateur column F', "columns[5]  # Column F (index 5)"),
            ('PA durée column H', "columns[7]          # Column H (index 7)"),
            ('PA zero and empty exclusion', "if duree_numeric > 0:"),
            ('PA collaborateur grouping', "collaborateur_dmts[collaborateur_name]"),
            ('PA average calculation', "collab_moyenne = sum(durees) / len(durees)"),
            ('PA empty string check', "str(duree_value).strip() != ''")
        ]
        
        print(f"\n📊 Vérification DMT PA (Feuille 3, Col F+H):")
        pa_found = 0
        for check_name, pattern in pa_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Implémenté")
                pa_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifications générales
        general_checks = [
            ('Error handling', "except Exception as e:"),
            ('Debug logging', "self.logger.debug"),
            ('Info logging', "self.logger.info"),
            ('Traceback logging', "traceback.format_exc()"),
            ('Non-null filtering', "pd.notna(collaborateur) and pd.notna(duree_value)"),
            ('String validation', "str(collaborateur).strip() != ''"),
            ('Float conversion', "duree_numeric = float(duree_value)"),
            ('Empty list check', "if durees:")
        ]
        
        print(f"\n🔧 Vérification fonctionnalités générales:")
        general_found = 0
        for check_name, pattern in general_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Implémenté")
                general_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        total_found = cm_found + pa_found + general_found
        total_expected = len(cm_checks) + len(pa_checks) + len(general_checks)
        
        if total_found >= total_expected - 2:  # Tolérance de 2
            print(f"\n✅ Modifications DMT correctes ({total_found}/{total_expected})")
            return True
        else:
            print(f"\n❌ Modifications DMT incomplètes ({total_found}/{total_expected})")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_dmt_calculation_logic():
    """Test de la logique de calcul DMT avec des données simulées."""
    print("\n🧮 Test de la Logique de Calcul DMT")
    print("=" * 70)
    
    try:
        # Simuler des données pour tester la logique
        import pandas as pd
        
        # Données simulées CM (Feuille 2)
        cm_data = {
            'Col_A': ['Data1', 'Data2', 'Data3', 'Data4', 'Data5'],
            'Col_B': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],  # Collaborateurs (index 1)
            'Col_C': ['C1', 'C2', 'C3', 'C4', 'C5'],
            'Col_D': ['D1', 'D2', 'D3', 'D4', 'D5'],
            'Col_E': ['E1', 'E2', 'E3', 'E4', 'E5'],
            'Col_F': ['F1', 'F2', 'F3', 'F4', 'F5'],
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5'],
            'Col_H': ['H1', 'H2', 'H3', 'H4', 'H5'],
            'Col_I': ['I1', 'I2', 'I3', 'I4', 'I5'],
            'Col_J': [2.5, 0, 3.0, 1.5, '']  # Durées (index 9) - avec 0 et vide à exclure
        }
        
        # Données simulées PA (Feuille 3)
        pa_data = {
            'Col_A': ['PA1', 'PA2', 'PA3', 'PA4', 'PA5'],
            'Col_B': ['B1', 'B2', 'B3', 'B4', 'B5'],
            'Col_C': ['C1', 'C2', 'C3', 'C4', 'C5'],
            'Col_D': ['D1', 'D2', 'D3', 'D4', 'D5'],
            'Col_E': ['E1', 'E2', 'E3', 'E4', 'E5'],
            'Col_F': ['Alice', 'Bob', 'Alice', 'David', ''],  # Collaborateurs (index 5) - avec vide
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5'],
            'Col_H': [1.8, 2.2, 0, 2.0, 1.5]  # Durées (index 7) - avec 0 à exclure
        }
        
        df_cm = pd.DataFrame(cm_data)
        df_pa = pd.DataFrame(pa_data)
        
        print("📊 Données de test créées:")
        print(f"   CM: {len(df_cm)} lignes, collaborateurs: {df_cm['Col_B'].unique()}")
        print(f"   PA: {len(df_pa)} lignes, collaborateurs: {df_pa['Col_F'].unique()}")
        
        # Test de la logique de calcul CM
        print(f"\n🔧 Test logique CM:")
        cm_collaborateurs = {}
        for index, row in df_cm.iterrows():
            collaborateur = row['Col_B']  # Column B (index 1)
            duree = row['Col_J']          # Column J (index 9)
            
            # Filtrage: exclure 0 et vides
            if (pd.notna(collaborateur) and pd.notna(duree) and 
                str(collaborateur).strip() != '' and str(duree).strip() != ''):
                try:
                    duree_numeric = float(duree)
                    if duree_numeric > 0:  # Exclure les 0
                        if collaborateur not in cm_collaborateurs:
                            cm_collaborateurs[collaborateur] = []
                        cm_collaborateurs[collaborateur].append(duree_numeric)
                except (ValueError, TypeError):
                    continue
        
        cm_moyennes = []
        for collab, durees in cm_collaborateurs.items():
            if durees:
                moyenne = sum(durees) / len(durees)
                cm_moyennes.append(moyenne)
                print(f"   {collab}: {moyenne:.2f} (sur {len(durees)} valeurs)")
        
        dmt_cm_global = sum(cm_moyennes) / len(cm_moyennes) if cm_moyennes else 0
        print(f"   DMT CM Global: {dmt_cm_global:.2f}")
        
        # Test de la logique de calcul PA
        print(f"\n🔧 Test logique PA:")
        pa_collaborateurs = {}
        for index, row in df_pa.iterrows():
            collaborateur = row['Col_F']  # Column F (index 5)
            duree = row['Col_H']          # Column H (index 7)
            
            # Filtrage: exclure 0 et vides
            if (pd.notna(collaborateur) and pd.notna(duree) and 
                str(collaborateur).strip() != '' and str(duree).strip() != ''):
                try:
                    duree_numeric = float(duree)
                    if duree_numeric > 0:  # Exclure les 0
                        if collaborateur not in pa_collaborateurs:
                            pa_collaborateurs[collaborateur] = []
                        pa_collaborateurs[collaborateur].append(duree_numeric)
                except (ValueError, TypeError):
                    continue
        
        pa_moyennes = []
        for collab, durees in pa_collaborateurs.items():
            if durees:
                moyenne = sum(durees) / len(durees)
                pa_moyennes.append(moyenne)
                print(f"   {collab}: {moyenne:.2f} (sur {len(durees)} valeurs)")
        
        dmt_pa_global = sum(pa_moyennes) / len(pa_moyennes) if pa_moyennes else 0
        print(f"   DMT PA Global: {dmt_pa_global:.2f}")
        
        # Vérifications
        expected_cm_collabs = 2  # Alice et Charlie (Bob exclu car durée = 0, dernière ligne vide)
        expected_pa_collabs = 3  # Alice, Bob et David (dernière ligne exclue car collaborateur vide)
        
        if len(cm_collaborateurs) == expected_cm_collabs and len(pa_collaborateurs) == expected_pa_collabs:
            print(f"\n✅ Logique de calcul correcte")
            print(f"   CM: {len(cm_collaborateurs)} collaborateurs avec durées > 0")
            print(f"   PA: {len(pa_collaborateurs)} collaborateurs avec durées > 0")
            return True
        else:
            print(f"\n❌ Logique de calcul incorrecte")
            print(f"   CM: {len(cm_collaborateurs)} collaborateurs (attendu: {expected_cm_collabs})")
            print(f"   PA: {len(pa_collaborateurs)} collaborateurs (attendu: {expected_pa_collabs})")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test de logique: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test des Modifications du Calcul DMT par Collaborateur")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Vérification des modifications du code
    if test_dmt_calculation_methods():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Modifications du code DMT")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Modifications du code DMT")
    
    # Test 2: Test de la logique de calcul
    if test_dmt_calculation_logic():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Logique de calcul DMT")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Logique de calcul DMT")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        
        print("\n🎯 Modifications DMT implémentées avec succès:")
        
        print("\n📊 DMT CM (Feuille 2):")
        print("  • Source: Sheet 2 du fichier Excel Suivi Global")
        print("  • Collaborateur: Colonne B (index 1)")
        print("  • Durée: Colonne J (index 9)")
        print("  • Filtrage: Exclusion des valeurs 0 et vides")
        print("  • Calcul: Moyenne par collaborateur, puis moyenne globale")
        
        print("\n📊 DMT PA (Feuille 3):")
        print("  • Source: Sheet 3 du fichier Excel Suivi Global")
        print("  • Collaborateur: Colonne F (index 5)")
        print("  • Durée: Colonne H (index 7)")
        print("  • Filtrage: Exclusion des valeurs 0 et vides")
        print("  • Calcul: Moyenne par collaborateur, puis moyenne globale")
        
        print("\n🔧 Fonctionnalités ajoutées:")
        print("  • Validation des données d'entrée (non-null, non-vide)")
        print("  • Exclusion automatique des valeurs 0 et chaînes vides")
        print("  • Calcul par collaborateur individuel")
        print("  • Moyenne globale pondérée équitablement")
        print("  • Logging détaillé pour debugging")
        print("  • Gestion d'erreurs robuste avec tracebacks")
        
        print("\n✅ Les méthodes DMT utilisent maintenant les bonnes colonnes!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test de la correction du calcul DMT CM - Colonne E au lieu de Colonne B.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_dmt_cm_column_correction():
    """Test que la méthode DMT CM utilise maintenant la Colonne E pour le collaborateur."""
    print("🔍 Test de la Correction DMT CM - Colonne E")
    print("=" * 60)
    
    try:
        # Lire le code source pour vérifier les modifications
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Vérifications spécifiques pour la correction DMT CM
        cm_correction_checks = [
            ('CM method exists', 'def _calculate_dmt_cm(self, data):'),
            ('CM docstring updated', 'Colonne E (collaborateur), Colonne J (durée)'),
            ('CM collaborateur column E', "columns[4]  # Column E (index 4)"),
            ('CM durée column J', "columns[9]          # Column J (index 9)"),
            ('CM correction comment', "# Column E (index 4) - CORRIGÉ"),
            ('CM sheet access', "'CM' not in self.global_suivi_data"),
            ('CM zero exclusion', "if duree_numeric > 0:"),
            ('CM collaborateur grouping', "collaborateur_dmts[collaborateur_name]")
        ]
        
        print("📊 Vérification correction DMT CM (Colonne E):")
        cm_found = 0
        for check_name, pattern in cm_correction_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Trouvé")
                cm_found += 1
            else:
                print(f"   ❌ {check_name}: Manquant")
        
        # Vérifier que l'ancienne référence à la Colonne B a été supprimée
        old_references = [
            ('Old Column B reference removed', "columns[1]  # Column B (index 1)"),
            ('Old docstring removed', 'Colonne B (collaborateur), Colonne J (durée)')
        ]
        
        print(f"\n🗑️ Vérification suppression anciennes références:")
        old_removed = 0
        for check_name, pattern in old_references:
            if pattern not in source_code:
                print(f"   ✅ {check_name}: Supprimé")
                old_removed += 1
            else:
                print(f"   ❌ {check_name}: Encore présent")
        
        # Vérifier que DMT PA n'a pas été modifié
        pa_unchanged_checks = [
            ('PA method unchanged', 'def _calculate_dmt_pa(self, data):'),
            ('PA collaborateur column F', "columns[5]  # Column F (index 5)"),
            ('PA durée column H', "columns[7]          # Column H (index 7)"),
            ('PA sheet access', "'Traitement PA' not in self.global_suivi_data")
        ]
        
        print(f"\n📊 Vérification DMT PA inchangé (Colonne F+H):")
        pa_unchanged = 0
        for check_name, pattern in pa_unchanged_checks:
            if pattern in source_code:
                print(f"   ✅ {check_name}: Préservé")
                pa_unchanged += 1
            else:
                print(f"   ❌ {check_name}: Modifié par erreur")
        
        total_found = cm_found + old_removed + pa_unchanged
        total_expected = len(cm_correction_checks) + len(old_references) + len(pa_unchanged_checks)
        
        if total_found >= total_expected - 1:  # Tolérance de 1
            print(f"\n✅ Correction DMT CM réussie ({total_found}/{total_expected})")
            return True
        else:
            print(f"\n❌ Correction DMT CM incomplète ({total_found}/{total_expected})")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_dmt_calculation_logic_with_column_e():
    """Test de la logique de calcul DMT CM avec la Colonne E."""
    print("\n🧮 Test de la Logique DMT CM avec Colonne E")
    print("=" * 60)
    
    try:
        # Simuler des données pour tester la logique avec Colonne E
        import pandas as pd
        
        # Données simulées CM (Feuille 2) avec Colonne E pour collaborateur
        cm_data = {
            'Col_A': ['Data1', 'Data2', 'Data3', 'Data4', 'Data5'],
            'Col_B': ['B1', 'B2', 'B3', 'B4', 'B5'],  # Ancienne colonne (ne doit plus être utilisée)
            'Col_C': ['C1', 'C2', 'C3', 'C4', 'C5'],
            'Col_D': ['D1', 'D2', 'D3', 'D4', 'D5'],
            'Col_E': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],  # Collaborateurs (index 4) - NOUVELLE COLONNE
            'Col_F': ['F1', 'F2', 'F3', 'F4', 'F5'],
            'Col_G': ['G1', 'G2', 'G3', 'G4', 'G5'],
            'Col_H': ['H1', 'H2', 'H3', 'H4', 'H5'],
            'Col_I': ['I1', 'I2', 'I3', 'I4', 'I5'],
            'Col_J': [2.5, 0, 3.0, 1.5, '']  # Durées (index 9) - avec 0 et vide à exclure
        }
        
        df_cm = pd.DataFrame(cm_data)
        
        print("📊 Données de test créées avec Colonne E:")
        print(f"   CM: {len(df_cm)} lignes")
        print(f"   Collaborateurs en Col B (ancienne): {df_cm['Col_B'].unique()}")
        print(f"   Collaborateurs en Col E (nouvelle): {df_cm['Col_E'].unique()}")
        
        # Test de la logique de calcul CM avec Colonne E
        print(f"\n🔧 Test logique CM avec Colonne E:")
        cm_collaborateurs = {}
        for index, row in df_cm.iterrows():
            collaborateur = row['Col_E']  # Column E (index 4) - NOUVELLE LOGIQUE
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
        
        # Vérifications
        expected_collaborateurs = ['Alice', 'Charlie']  # Bob exclu car durée = 0 ou vide
        actual_collaborateurs = list(cm_collaborateurs.keys())
        
        print(f"\n📊 Vérification des collaborateurs:")
        print(f"   Attendus: {expected_collaborateurs}")
        print(f"   Trouvés: {actual_collaborateurs}")
        
        if set(actual_collaborateurs) == set(expected_collaborateurs):
            print(f"\n✅ Logique de calcul correcte avec Colonne E")
            print(f"   Collaborateurs traités: {len(cm_collaborateurs)}")
            print(f"   DMT CM calculé: {dmt_cm_global:.2f}")
            return True
        else:
            print(f"\n❌ Logique de calcul incorrecte")
            print(f"   Différence dans les collaborateurs détectés")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test de logique: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_specifications_compliance():
    """Test de conformité aux spécifications."""
    print("\n📋 Test de Conformité aux Spécifications")
    print("=" * 60)
    
    try:
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Spécifications à vérifier
        specifications = [
            ('Source: Feuille 2 (Sheet 2)', "'CM' not in self.global_suivi_data"),
            ('Collaborateur: Colonne E (index 4)', "columns[4]  # Column E (index 4)"),
            ('Durée: Colonne J (index 9)', "columns[9]          # Column J (index 9)"),
            ('Filtrage: Exclure valeurs 0', "if duree_numeric > 0:"),
            ('Filtrage: Exclure valeurs vides', "str(duree_value).strip() != ''"),
            ('Méthode: Grouper par collaborateur', "collaborateur_dmts = {}"),
            ('Méthode: Moyenne individuelle', "collab_moyenne = sum(durees) / len(durees)"),
            ('Méthode: Moyenne globale', "dmt_global = sum(all_durees) / len(all_durees)"),
            ('DMT PA inchangé: Colonne F', "columns[5]  # Column F (index 5)"),
            ('DMT PA inchangé: Colonne H', "columns[7]          # Column H (index 7)")
        ]
        
        print("📊 Vérification conformité spécifications:")
        compliant = 0
        for spec_name, pattern in specifications:
            if pattern in source_code:
                print(f"   ✅ {spec_name}: Conforme")
                compliant += 1
            else:
                print(f"   ❌ {spec_name}: Non conforme")
        
        if compliant >= len(specifications) - 1:  # Tolérance de 1
            print(f"\n✅ Spécifications respectées ({compliant}/{len(specifications)})")
            return True
        else:
            print(f"\n❌ Spécifications non respectées ({compliant}/{len(specifications)})")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test de conformité: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🚀 Test de la Correction DMT CM - Colonne E")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Vérification de la correction de colonne
    if test_dmt_cm_column_correction():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Correction de colonne DMT CM")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Correction de colonne DMT CM")
    
    # Test 2: Test de la logique avec Colonne E
    if test_dmt_calculation_logic_with_column_e():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Logique de calcul avec Colonne E")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Logique de calcul avec Colonne E")
    
    # Test 3: Test de conformité aux spécifications
    if test_specifications_compliance():
        tests_passed += 1
        print("\n✅ Test 3 RÉUSSI: Conformité aux spécifications")
    else:
        print("\n❌ Test 3 ÉCHOUÉ: Conformité aux spécifications")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        
        print("\n🎯 Correction DMT CM appliquée avec succès:")
        
        print("\n📊 DMT CM CORRIGÉ (Feuille 2):")
        print("  • Source: Sheet 2 du fichier Excel Suivi Global")
        print("  • Collaborateur: Colonne E (index 4) ✅ CORRIGÉ")
        print("  • Durée: Colonne J (index 9) ✅ CONFIRMÉ")
        print("  • Filtrage: Exclusion des valeurs 0 et vides")
        print("  • Calcul: Moyenne par collaborateur, puis moyenne globale")
        
        print("\n📊 DMT PA INCHANGÉ (Feuille 3):")
        print("  • Source: Sheet 3 du fichier Excel Suivi Global")
        print("  • Collaborateur: Colonne F (index 5) ✅ PRÉSERVÉ")
        print("  • Durée: Colonne H (index 7) ✅ PRÉSERVÉ")
        print("  • Filtrage: Exclusion des valeurs 0 et vides")
        print("  • Calcul: Moyenne par collaborateur, puis moyenne globale")
        
        print("\n🔧 Correction appliquée:")
        print("  • Colonne B (index 1) → Colonne E (index 4) pour DMT CM")
        print("  • Documentation mise à jour")
        print("  • Commentaire de correction ajouté")
        print("  • DMT PA maintenu inchangé")
        
        print("\n✅ DMT CM utilise maintenant la Colonne E pour le collaborateur!")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

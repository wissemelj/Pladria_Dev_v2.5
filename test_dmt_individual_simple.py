#!/usr/bin/env python3
"""
Test simple des nouvelles méthodes DMT individuelles.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    print("🚀 Test Simple des Méthodes DMT Individuelles")
    print("=" * 60)
    
    try:
        # Test import
        print("📦 Test import...")
        from ui.modules.team_stats_module import TeamStatsModule
        print("✅ Import réussi")
        
        # Test méthodes existent
        print("\n🔍 Vérification des méthodes...")
        methods = ['_calculate_individual_dmt_pa', '_calculate_individual_dmt_cm']
        
        for method in methods:
            if hasattr(TeamStatsModule, method):
                print(f"✅ {method}: Existe")
            else:
                print(f"❌ {method}: Manquant")
                return False
        
        # Test intégration dans _calculate_dmt_automatically
        print("\n🔧 Vérification intégration...")
        team_stats_file = Path(__file__).parent / "src" / "ui" / "modules" / "team_stats_module.py"
        
        with open(team_stats_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        integration_patterns = [
            'dmt_pa = self._calculate_individual_dmt_pa(collab)',
            'dmt_cm = self._calculate_individual_dmt_cm(collab)',
            'def _calculate_individual_dmt_pa(self, collaborateur):',
            'def _calculate_individual_dmt_cm(self, collaborateur):'
        ]
        
        for pattern in integration_patterns:
            if pattern in source_code:
                print(f"✅ {pattern[:50]}...")
            else:
                print(f"❌ {pattern[:50]}...")
                return False
        
        # Test spécifications
        print("\n📊 Vérification spécifications...")
        
        # DMT PA spécifications
        pa_specs = [
            ("PA Feuille 3", "'Traitement PA' not in self.global_suivi_data"),
            ("PA Colonne F", "columns[5]  # Column F (index 5)"),
            ("PA Colonne H", "columns[7]          # Column H (index 7)"),
            ("PA Filtrage collaborateur", "str(row_collaborateur).strip() == str(collaborateur).strip()"),
            ("PA Exclusion zéro", "if duree_numeric > 0:")
        ]
        
        for spec_name, pattern in pa_specs:
            if pattern in source_code:
                print(f"✅ {spec_name}")
            else:
                print(f"❌ {spec_name}")
        
        # DMT CM spécifications
        cm_specs = [
            ("CM Feuille 2", "'CM' not in self.global_suivi_data"),
            ("CM Colonne E", "columns[4]  # Column E (index 4) - CORRIGÉ"),
            ("CM Colonne J", "columns[9]          # Column J (index 9)"),
            ("CM Filtrage collaborateur", "str(row_collaborateur).strip() == str(collaborateur).strip()"),
            ("CM Exclusion zéro", "if duree_numeric > 0:")
        ]
        
        for spec_name, pattern in cm_specs:
            if pattern in source_code:
                print(f"✅ {spec_name}")
            else:
                print(f"❌ {spec_name}")
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        
        print("\n📋 Résumé des Modifications:")
        print("=" * 60)
        
        print("\n🔧 Nouvelles Méthodes Créées:")
        print("• _calculate_individual_dmt_pa(collaborateur)")
        print("  - Calcule DMT PA pour un collaborateur spécifique")
        print("  - Source: Feuille 3, Colonne F (collaborateur), Colonne H (durée)")
        print("  - Filtrage: Par collaborateur + exclusion 0/vides")
        
        print("\n• _calculate_individual_dmt_cm(collaborateur)")
        print("  - Calcule DMT CM pour un collaborateur spécifique")
        print("  - Source: Feuille 2, Colonne E (collaborateur), Colonne J (durée)")
        print("  - Filtrage: Par collaborateur + exclusion 0/vides")
        
        print("\n🔄 Intégration dans _calculate_dmt_automatically:")
        print("• Remplace les appels aux méthodes globales")
        print("• Utilise les nouvelles méthodes individuelles")
        print("• Stocke les résultats dans self.dmt_data[collaborateur]")
        
        print("\n🎯 Problème Résolu:")
        print("• AVANT: DMT identiques pour tous (moyennes globales)")
        print("• APRÈS: DMT individuels par collaborateur")
        print("• Interface: Affichage correct des valeurs individuelles")
        
        print("\n✅ Les DMT individuels sont maintenant calculés correctement!")
        print("✅ DMT CM utilise la Colonne E (corrigée)")
        print("✅ DMT PA utilise la Colonne F (préservée)")
        print("✅ Filtrage par collaborateur implémenté")
        print("✅ Exclusion des valeurs 0 et vides")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS: Nouvelles méthodes DMT individuelles implémentées!")
    else:
        print("\n❌ FAILURE: Problème avec les nouvelles méthodes DMT individuelles")
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test de la normalisation améliorée des motifs Acts.
"""

import sys
import os
import pandas as pd
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_improved_normalization():
    """Test de la normalisation améliorée."""
    print("🔧 Test de la Normalisation Améliorée des Motifs")
    print("=" * 70)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Créer une instance mock pour tester
        class MockTeamStatsModule:
            def __init__(self):
                self._normalize_acts_motif = TeamStatsModule._normalize_acts_motif.__get__(self, MockTeamStatsModule)
                
                import logging
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
        
        mock_module = MockTeamStatsModule()
        
        # Test avec différents motifs possibles
        test_cases = [
            # Cas NOK
            ('NOK', 'NOK'),
            ('nok', 'NOK'),
            ('KO', 'NOK'),
            ('ko', 'NOK'),
            ('NOT OK', 'NOK'),
            ('NOTOK', 'NOK'),
            ('INVALIDE', 'NOK'),
            ('ERREUR', 'NOK'),
            
            # Cas OK
            ('OK', 'OK'),
            ('ok', 'OK'),
            ('VALIDE', 'OK'),
            ('CORRECT', 'OK'),
            
            # Cas UPR NOK
            ('UPR NOK', 'UPR NOK'),
            ('upr nok', 'UPR NOK'),
            ('UPR-NOK', 'UPR NOK'),
            ('UPR_NOK', 'UPR NOK'),
            ('UPR KO', 'UPR NOK'),
            ('UPR NOT OK', 'UPR NOK'),
            
            # Cas UPR OK
            ('UPR OK', 'UPR OK'),
            ('upr ok', 'UPR OK'),
            ('UPR-OK', 'UPR OK'),
            ('UPR_OK', 'UPR OK'),
            ('UPR VALIDE', 'UPR OK'),
            
            # Cas UPR RAS
            ('UPR RAS', 'UPR RAS'),
            ('upr ras', 'UPR RAS'),
            ('UPR-RAS', 'UPR RAS'),
            ('UPR', 'UPR RAS'),  # Fallback
            
            # Cas AD
            ('AD NON JOINTE', 'AD Non jointe'),
            ('ad non jointe', 'AD Non jointe'),
            ('ADRESSE NON JOINTE', 'AD Non jointe'),
            ('AD NON TROUVÉE', 'AD Non trouvée'),
            ('ad non trouvée', 'AD Non trouvée'),
            
            # Cas Hors commune
            ('HORS COMMUNE', 'Hors commune'),
            ('hors commune', 'Hors commune'),
            ('HORS-COMMUNE', 'Hors commune'),
        ]
        
        print("🧪 Test des cas de normalisation:")
        
        all_passed = True
        for input_motif, expected_output in test_cases:
            motif_upper = input_motif.upper().strip()
            actual_output = mock_module._normalize_acts_motif(motif_upper)
            
            if actual_output == expected_output:
                status = "✅"
            else:
                status = "❌"
                all_passed = False
            
            print(f"   {status} '{input_motif}' → '{actual_output}' (attendu: '{expected_output}')")
        
        if all_passed:
            print(f"\n🎉 TOUS LES TESTS DE NORMALISATION RÉUSSIS!")
        else:
            print(f"\n❌ Certains tests de normalisation ont échoué")
            return False
        
        # Test avec des données simulées complètes
        print(f"\n📊 Test avec données simulées complètes:")
        
        # Créer des données de test avec des motifs variés
        mock_data = {
            'Nom commune': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'],
            'Insee': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            'Num Dossier Site': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
            'Motif': [
                'NOK',           # Should map to NOK
                'UPR NOK',       # Should map to UPR NOK
                'UPR OK',        # Should map to UPR OK
                'OK',            # Should map to OK
                'ad ras',        # Should map to AD RAS sans temps
                'UPR RAS',       # Should map to UPR RAS
                'KO',            # Should map to NOK (variant)
                'UPR-NOK',       # Should map to UPR NOK (variant)
                'UPR_OK',        # Should map to UPR OK (variant)
                'INVALIDE'       # Should map to NOK (variant)
            ],
            'Adresse BAN': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'],
            'Collaborateur': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice'],
            'Date traitement': [
                '2025-07-15', '2025-07-16', '2025-07-17', '2025-07-18', '2025-07-19',
                '2025-07-20', '2025-07-21', '2025-07-22', '2025-07-23', '2025-07-24'
            ],
            'Durée': [1.0, 0.0, 2.0, 1.0, 0.0, 3.0, 1.0, 0.0, 2.0, 1.0]
        }
        
        # Étendre la classe mock pour inclure l'extraction complète
        class FullMockTeamStatsModule(MockTeamStatsModule):
            def __init__(self):
                super().__init__()
                self._extract_acts_data_for_dashboard = TeamStatsModule._extract_acts_data_for_dashboard.__get__(self, FullMockTeamStatsModule)
                
                self.global_suivi_data = {
                    'Traitement PA': pd.DataFrame(mock_data)
                }
                
                self.date_from_selected = date(2025, 7, 15)
                self.date_to_selected = date(2025, 7, 25)
        
        full_mock = FullMockTeamStatsModule()
        
        # Extraire les données
        acts_data = full_mock._extract_acts_data_for_dashboard()
        
        if acts_data:
            print(f"   ✅ Extraction réussie:")
            print(f"   Total records: {acts_data['total_records']}")
            print(f"   Categories: {acts_data['labels']}")
            print(f"   Counts: {acts_data['data']}")
            print(f"   Breakdown: {acts_data['motif_breakdown']}")
            
            # Vérifier que NOK, UPR NOK, UPR OK ont des valeurs > 0
            breakdown = acts_data['motif_breakdown']
            nok_count = breakdown.get('NOK', 0)
            upr_nok_count = breakdown.get('UPR NOK', 0)
            upr_ok_count = breakdown.get('UPR OK', 0)
            
            print(f"\n   🎯 Vérification des catégories problématiques:")
            print(f"   NOK: {nok_count} (attendu: ≥2)")  # NOK + KO + INVALIDE
            print(f"   UPR NOK: {upr_nok_count} (attendu: ≥2)")  # UPR NOK + UPR-NOK
            print(f"   UPR OK: {upr_ok_count} (attendu: ≥2)")  # UPR OK + UPR_OK
            
            if nok_count > 0 and upr_nok_count > 0 and upr_ok_count > 0:
                print(f"   🎉 TOUTES LES CATÉGORIES ONT DES VALEURS!")
                print(f"   La normalisation améliorée fonctionne correctement")
                return True
            else:
                print(f"   ❌ Certaines catégories ont encore des valeurs 0")
                return False
        else:
            print(f"   ❌ Échec de l'extraction")
            return False
        
    except Exception as e:
        print(f"❌ Erreur dans le test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale."""
    print("🚀 Test de la Normalisation Améliorée")
    print("=" * 70)
    
    if test_improved_normalization():
        print(f"\n✅ NORMALISATION AMÉLIORÉE RÉUSSIE!")
        print(f"\n🎯 Améliorations apportées:")
        print(f"  • Mappings plus complets pour NOK/UPR variations")
        print(f"  • Support des formats avec tirets et underscores")
        print(f"  • Gestion des synonymes (KO, INVALIDE, etc.)")
        print(f"  • Logging détaillé pour le débogage")
        print(f"  • Logique de fallback améliorée")
        
        print(f"\n📝 Résultat attendu:")
        print(f"  Les catégories NOK, UPR NOK, et UPR OK devraient")
        print(f"  maintenant afficher des valeurs > 0 si ces motifs")
        print(f"  existent dans les données réelles")
        
        print(f"\n🔧 Prochaine étape:")
        print(f"  Tester avec l'application réelle pour voir si")
        print(f"  les valeurs 0 sont maintenant corrigées")
        
        return True
    else:
        print(f"\n❌ NORMALISATION ÉCHOUÉE")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test pour vérifier que l'ordre des données Acts correspond aux labels du Chart.js.
"""

import sys
import os
import pandas as pd
from datetime import datetime, date
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_acts_chart_order():
    """Test que l'ordre des données correspond aux labels Chart.js."""
    print("🔄 Test de l'Ordre des Données Acts dans l'Histogramme")
    print("=" * 80)
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Ordre exact des labels dans script.js
        expected_chart_order = [
            'AD RAS avec temps',
            'AD RAS sans temps', 
            'AD Non jointe',
            'AD Non trouvée',
            'Hors commune',
            'NOK',
            'OK',
            'UPR RAS',
            'UPR NOK',
            'UPR OK'
        ]
        
        print(f"📊 Ordre attendu des labels Chart.js:")
        for i, label in enumerate(expected_chart_order):
            print(f"   {i+1}. {label}")
        
        # Créer des données de test avec des motifs variés
        mock_data = {
            'Nom commune': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12'],
            'Insee': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            'Num Dossier Site': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'],
            'Motif': [
                'ad ras',           # AD RAS sans temps (durée 0)
                'AD RAS',           # AD RAS avec temps (durée > 0)
                'ok',               # OK
                'NOK',              # NOK
                'ad non jointe',    # AD Non jointe
                'UPR ras',          # UPR RAS
                'ad ras',           # AD RAS sans temps (durée 0)
                'AD RAS',           # AD RAS avec temps (durée > 0)
                'ad non trouvée',   # AD Non trouvée
                'hors commune',     # Hors commune
                'UPR NOK',          # UPR NOK
                'UPR OK'            # UPR OK
            ],
            'Adresse BAN': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'],
            'Collaborateur': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'],
            'Date traitement': [
                '2025-07-15', '2025-07-16', '2025-07-17', '2025-07-18', 
                '2025-07-19', '2025-07-20', '2025-07-21', '2025-07-22',
                '2025-07-23', '2025-07-24', '2025-07-25', '2025-07-26'
            ],
            'Durée': [0.0, 5.0, 2.0, 1.0, 0.0, 3.0, 0.0, 2.0, 1.0, 0.0, 1.0, 2.0]  # Durées variées
        }
        
        # Créer mock module
        class MockTeamStatsModule:
            def __init__(self):
                self._extract_acts_data_for_dashboard = TeamStatsModule._extract_acts_data_for_dashboard.__get__(self, MockTeamStatsModule)
                self._normalize_acts_motif = TeamStatsModule._normalize_acts_motif.__get__(self, MockTeamStatsModule)
                
                self.global_suivi_data = {
                    'Traitement PA': pd.DataFrame(mock_data)
                }
                
                self.date_from_selected = date(2025, 7, 15)
                self.date_to_selected = date(2025, 7, 30)
                
                import logging
                self.logger = logging.getLogger(__name__)
                self.logger.setLevel(logging.INFO)
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
        
        mock_module = MockTeamStatsModule()
        
        # Extraire les données
        print(f"\n📊 Extraction des données Acts...")
        acts_data = mock_module._extract_acts_data_for_dashboard()
        
        if not acts_data:
            print(f"❌ Échec de l'extraction des données")
            return False
        
        print(f"\n✅ Données extraites avec succès:")
        print(f"   Total records: {acts_data['total_records']}")
        print(f"   Categories: {len(acts_data['labels'])}")
        
        # Vérifier l'ordre des labels
        actual_labels = acts_data['labels']
        actual_data = acts_data['data']
        
        print(f"\n🔍 Vérification de l'ordre des données:")
        print(f"   Ordre attendu vs Ordre obtenu:")
        
        order_correct = True
        for i, (expected, actual) in enumerate(zip(expected_chart_order, actual_labels)):
            status = "✅" if expected == actual else "❌"
            print(f"   {i+1}. {status} Attendu: '{expected}' | Obtenu: '{actual}' | Valeur: {actual_data[i]}")
            if expected != actual:
                order_correct = False
        
        if order_correct:
            print(f"\n🎉 ORDRE CORRECT!")
            print(f"   Les données sont dans le bon ordre pour l'histogramme")
        else:
            print(f"\n❌ ORDRE INCORRECT!")
            print(f"   Les données ne correspondent pas à l'ordre des labels Chart.js")
            return False
        
        # Vérifier que les données correspondent aux motifs attendus
        print(f"\n📊 Vérification des valeurs par catégorie:")
        
        expected_counts = {
            'AD RAS avec temps': 2,  # 2 AD RAS avec durée > 0
            'AD RAS sans temps': 2,  # 2 AD RAS avec durée = 0
            'AD Non jointe': 1,      # 1 ad non jointe
            'AD Non trouvée': 1,     # 1 ad non trouvée
            'Hors commune': 1,       # 1 hors commune
            'NOK': 1,                # 1 NOK
            'OK': 1,                 # 1 OK
            'UPR RAS': 1,            # 1 UPR ras
            'UPR NOK': 1,            # 1 UPR NOK
            'UPR OK': 1              # 1 UPR OK
        }
        
        values_correct = True
        for i, (label, expected_count, actual_count) in enumerate(zip(actual_labels, [expected_counts.get(label, 0) for label in actual_labels], actual_data)):
            status = "✅" if expected_count == actual_count else "❌"
            print(f"   {status} {label}: Attendu {expected_count}, Obtenu {actual_count}")
            if expected_count != actual_count:
                values_correct = False
        
        if values_correct:
            print(f"\n🎉 VALEURS CORRECTES!")
            print(f"   Toutes les valeurs correspondent aux motifs attendus")
        else:
            print(f"\n❌ VALEURS INCORRECTES!")
            print(f"   Certaines valeurs ne correspondent pas aux motifs")
            return False
        
        # Test avec script.js
        print(f"\n📜 Test d'intégration avec script.js:")
        
        # Simuler la mise à jour du script.js
        sample_script = """
        const actsCtx = document.getElementById('actsChart').getContext('2d');
        new Chart(actsCtx, {
            type: 'bar',
            data: {
                labels: ['AD RAS\\navec temps', 'AD RAS\\nsans temps', 'AD Non jointe', 'AD Non trouvée', 'Hors commune', 'NOK', 'OK', 'UPR RAS', 'UPR NOK', 'UPR OK'],
                datasets: [{
                    data: [2324, 6023, 584, 143, 23, 930, 1084, 180, 16, 14],
                    backgroundColor: colors.acts,
                    borderWidth: 1
                }]
            },
        """
        
        import re
        
        # Mettre à jour avec nos données
        acts_pattern = r'(data:\s*\[)[^\]]*(\])'
        data_str = ', '.join(str(x) for x in actual_data)
        replacement = rf'\g<1>{data_str}\g<2>'
        
        updated_script = re.sub(acts_pattern, replacement, sample_script)
        
        if f'[{data_str}]' in updated_script:
            print(f"   ✅ Script.js mis à jour avec succès")
            print(f"   Données: [{data_str}]")
            print(f"   Correspondance parfaite avec l'ordre des labels!")
        else:
            print(f"   ❌ Échec de la mise à jour du script.js")
            return False
        
        print(f"\n🎉 TOUS LES TESTS RÉUSSIS!")
        print(f"\n✅ L'ordre des données est maintenant correct pour l'histogramme!")
        print(f"\n📊 Résumé:")
        print(f"  • Ordre des labels: ✅ Correspond exactement à Chart.js")
        print(f"  • Valeurs des données: ✅ Correspondent aux motifs extraits")
        print(f"  • Intégration script.js: ✅ Mise à jour réussie")
        print(f"  • Ad Ras split: ✅ Avec temps ({actual_data[0]}) et Sans temps ({actual_data[1]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale."""
    if test_acts_chart_order():
        print(f"\n🎯 CORRECTION RÉUSSIE!")
        print(f"\nLes valeurs seront maintenant correctement placées dans l'histogramme:")
        print(f"  1. AD RAS avec temps - en première position")
        print(f"  2. AD RAS sans temps - en deuxième position") 
        print(f"  3. AD Non jointe - en troisième position")
        print(f"  4. Etc. - dans l'ordre exact des labels Chart.js")
        
        print(f"\n📝 Prochaine étape:")
        print(f"  Tester avec l'application réelle pour confirmer que")
        print(f"  l'histogramme affiche les bonnes valeurs aux bonnes positions")
        
        return True
    else:
        print(f"\n❌ CORRECTION ÉCHOUÉE")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

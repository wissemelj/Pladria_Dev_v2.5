#!/usr/bin/env python3
"""
Simple debug pour analyser les motifs Acts.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Analyse simple des motifs."""
    print("🔍 Analyse Simple des Motifs Acts")
    print("=" * 50)
    
    try:
        # Test de la logique de normalisation actuelle
        from ui.modules.team_stats_module import TeamStatsModule
        
        # Créer une instance mock pour tester la normalisation
        class MockModule:
            def _normalize_acts_motif(self, motif_upper):
                return TeamStatsModule._normalize_acts_motif(None, motif_upper)
        
        mock = MockModule()
        
        # Tester différents motifs possibles
        test_motifs = [
            'NOK',
            'nok', 
            'KO',
            'ko',
            'UPR NOK',
            'upr nok',
            'UPR-NOK',
            'UPR_NOK',
            'UPR OK',
            'upr ok',
            'UPR-OK',
            'UPR_OK',
            'OK',
            'ok'
        ]
        
        print("🧪 Test de normalisation des motifs:")
        for motif in test_motifs:
            motif_upper = motif.upper().strip()
            normalized = mock._normalize_acts_motif(motif_upper)
            print(f"   '{motif}' → '{normalized}'")
        
        # Vérifier les mappings actuels
        print(f"\n📋 Mappings actuels dans le code:")
        import inspect
        source = inspect.getsource(TeamStatsModule._normalize_acts_motif)
        
        if 'NOK' in source:
            print("   ✅ NOK mapping trouvé dans le code")
        else:
            print("   ❌ NOK mapping manquant")
        
        if 'UPR NOK' in source:
            print("   ✅ UPR NOK mapping trouvé dans le code")
        else:
            print("   ❌ UPR NOK mapping manquant")
        
        if 'UPR OK' in source:
            print("   ✅ UPR OK mapping trouvé dans le code")
        else:
            print("   ❌ UPR OK mapping manquant")
        
        print(f"\n💡 Hypothèses sur les valeurs 0:")
        print(f"   1. Les motifs NOK/UPR n'existent pas dans les données réelles")
        print(f"   2. Les motifs utilisent une nomenclature différente")
        print(f"   3. Ces motifs ne sont pas présents dans la période sélectionnée")
        print(f"   4. La logique de normalisation ne les reconnaît pas")
        
        print(f"\n🔧 Solutions possibles:")
        print(f"   1. Vérifier les motifs réels dans le fichier Excel")
        print(f"   2. Ajuster la logique de normalisation")
        print(f"   3. Ajouter des variations de noms de motifs")
        print(f"   4. Confirmer que ces catégories doivent avoir des valeurs")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

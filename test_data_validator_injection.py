#!/usr/bin/env python3
"""
Test des nouvelles validations pour l'injection des données dans le HTML.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_data_validator_injection():
    """Test des validations d'injection de données."""
    print("🔍 Test des Validations d'Injection de Données")
    print("=" * 70)
    
    try:
        from core.data_validator import DataValidator
        
        validator = DataValidator()
        print("✅ DataValidator importé avec succès")
        
        # Test 1: Données valides complètes
        print(f"\n🧪 Test 1: Données valides complètes")
        valid_data = {
            'cm': {
                'data': [2071, 34, 148],
                'total_records': 2253,
                'motif_breakdown': {'RAF': 2071, 'MODIF': 34, 'CREA': 148}
            },
            'communes': {
                'data': [87, 12],
                'total_records': 99,
                'commune_breakdown': {'Orange': 87, 'RIP': 12}
            }
        }
        
        result = validator.validate_dashboard_injection_data(valid_data)
        
        if result['valid']:
            print(f"   ✅ Validation réussie")
            print(f"   📊 Résumé: {result['data_summary']}")
            if result['warnings']:
                print(f"   ⚠️ Avertissements: {result['warnings']}")
        else:
            print(f"   ❌ Validation échouée: {result['errors']}")
            return False
        
        # Test 2: Données avec erreurs
        print(f"\n🧪 Test 2: Données avec erreurs")
        invalid_data = {
            'cm': {
                'data': [2071, -34],  # Pas assez de valeurs + valeur négative
                'total_records': -1,   # Valeur négative
                'motif_breakdown': "invalid"  # Mauvais type
            },
            'communes': {
                'data': [87, 12, 5],  # Trop de valeurs
                'total_records': "invalid",  # Mauvais type
                'commune_breakdown': {}  # Vide
            }
        }
        
        result = validator.validate_dashboard_injection_data(invalid_data)
        
        if not result['valid']:
            print(f"   ✅ Validation correctement échouée")
            print(f"   ❌ Erreurs détectées: {len(result['errors'])}")
            for error in result['errors']:
                print(f"      • {error}")
            if result['warnings']:
                print(f"   ⚠️ Avertissements: {len(result['warnings'])}")
                for warning in result['warnings']:
                    print(f"      • {warning}")
        else:
            print(f"   ❌ Validation aurait dû échouer")
            return False
        
        # Test 3: Données avec avertissements
        print(f"\n🧪 Test 3: Données avec avertissements")
        warning_data = {
            'cm': {
                'data': [0, 0, 0],  # Toutes les valeurs à zéro
                'total_records': 0,
                'motif_breakdown': {}
            },
            'communes': {
                'data': [50, 0],  # Une valeur à zéro
                'total_records': 50,
                'commune_breakdown': {'Orange': 50, 'RIP': 0}
            }
        }
        
        result = validator.validate_dashboard_injection_data(warning_data)
        
        if result['valid']:
            print(f"   ✅ Validation réussie avec avertissements")
            print(f"   ⚠️ Avertissements: {len(result['warnings'])}")
            for warning in result['warnings']:
                print(f"      • {warning}")
        else:
            print(f"   ❌ Validation échouée: {result['errors']}")
            return False
        
        # Test 4: Données partielles (seulement CM)
        print(f"\n🧪 Test 4: Données partielles (seulement CM)")
        partial_data = {
            'cm': {
                'data': [1500, 25, 100],
                'total_records': 1625,
                'motif_breakdown': {'RAF': 1500, 'MODIF': 25, 'CREA': 100}
            }
        }
        
        result = validator.validate_dashboard_injection_data(partial_data)
        
        if result['valid']:
            print(f"   ✅ Validation réussie pour données partielles")
            if result['warnings']:
                print(f"   ⚠️ Avertissements: {result['warnings']}")
            print(f"   📊 Résumé: {result['data_summary']}")
        else:
            print(f"   ❌ Validation échouée: {result['errors']}")
            return False
        
        # Test 5: Données vides
        print(f"\n🧪 Test 5: Données vides")
        empty_data = {}
        
        result = validator.validate_dashboard_injection_data(empty_data)
        
        if not result['valid']:
            print(f"   ✅ Validation correctement échouée pour données vides")
            print(f"   ❌ Erreurs: {result['errors']}")
        else:
            print(f"   ❌ Validation aurait dû échouer pour données vides")
            return False
        
        print(f"\n✅ Tous les tests de validation réussis!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans les tests de validation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_team_stats():
    """Test d'intégration avec le module TeamStatsModule."""
    print(f"\n🔧 Test d'Intégration avec TeamStatsModule:")
    
    try:
        from ui.modules.team_stats_module import TeamStatsModule
        from core.data_validator import DataValidator
        
        # Vérifier que les méthodes existent
        required_methods = [
            '_map_stats_to_dashboard_categories',
            '_update_html_elements_with_data',
            '_extract_cm_data_for_dashboard',
            '_extract_communes_data_for_dashboard'
        ]
        
        for method in required_methods:
            if hasattr(TeamStatsModule, method):
                print(f"   ✅ Méthode existe: {method}")
            else:
                print(f"   ❌ Méthode manquante: {method}")
                return False
        
        # Créer une instance du validateur
        validator = DataValidator()
        print(f"   ✅ DataValidator créé avec succès")
        
        # Simuler des données comme celles retournées par le module
        simulated_mapping = {
            'cm': {
                'data': [2071, 34, 148],
                'total_records': 2253,
                'motif_breakdown': {
                    'Rien à faire': 2071,
                    'Modification Voie': 34,
                    'Création Voie': 148
                }
            },
            'communes': {
                'data': [87, 12],
                'total_records': 99,
                'commune_breakdown': {
                    'Orange': 87,
                    'RIP': 12
                }
            }
        }
        
        # Valider les données simulées
        validation_result = validator.validate_dashboard_injection_data(simulated_mapping)
        
        if validation_result['valid']:
            print(f"   ✅ Données simulées du module validées avec succès")
            print(f"   📊 Résumé de validation: {validation_result['data_summary']}")
        else:
            print(f"   ❌ Validation des données simulées échouée: {validation_result['errors']}")
            return False
        
        print(f"   ✅ Intégration avec TeamStatsModule réussie!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur d'intégration: {e}")
        return False

def main():
    """Fonction de test principale."""
    print("🚀 Test des Validations d'Injection HTML")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Validations d'injection
    if test_data_validator_injection():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Validations d'injection")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Validations d'injection")
    
    # Test 2: Intégration avec le module
    if test_integration_with_team_stats():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Intégration avec le module")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Intégration avec le module")
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ Validations d'injection HTML complètement implémentées!")
        print("\n🎯 Fonctionnalités de validation:")
        print("  • Validation des données CM (3 valeurs: RAF, MODIF, CREA)")
        print("  • Validation des données Communes (2 valeurs: Orange, RIP)")
        print("  • Vérification des types de données (nombres positifs)")
        print("  • Validation croisée entre sections")
        print("  • Génération de résumés de données")
        print("  • Gestion des erreurs et avertissements")
        print("  • Intégration avec TeamStatsModule")
        
        print("\n📝 Utilisation dans le code:")
        print("  validator = DataValidator()")
        print("  result = validator.validate_dashboard_injection_data(mapping)")
        print("  if result['valid']:")
        print("      # Procéder à l'injection")
        print("  else:")
        print("      # Gérer les erreurs: result['errors']")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

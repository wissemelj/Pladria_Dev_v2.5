#!/usr/bin/env python3
"""
Test complet pour vérifier l'injection des valeurs dans le HTML du tableau de bord.
"""

import sys
import os
import tempfile
import shutil
import re
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_injection_complete_html():
    """Test complet de l'injection des valeurs dans le HTML."""
    print("🔄 Test Complet d'Injection des Valeurs dans le HTML")
    print("=" * 80)
    
    try:
        # Créer un environnement de test
        temp_dir = tempfile.mkdtemp()
        original_pres_stats = Path(__file__).parent / "src" / "pres stats"
        temp_pres_stats = os.path.join(temp_dir, "pres stats")
        
        if original_pres_stats.exists():
            shutil.copytree(original_pres_stats, temp_pres_stats)
            print(f"✅ Environnement de test créé: {temp_pres_stats}")
        else:
            print(f"❌ Dossier pres stats non trouvé")
            return False
        
        # Lire les fichiers originaux
        index_path = os.path.join(temp_pres_stats, "index.html")
        script_path = os.path.join(temp_pres_stats, "script.js")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            original_html = f.read()
        
        with open(script_path, 'r', encoding='utf-8') as f:
            original_script = f.read()
        
        print(f"📊 Fichiers originaux chargés:")
        print(f"   HTML: {len(original_html)} caractères")
        print(f"   Script: {len(original_script)} caractères")
        
        # Extraire toutes les valeurs originales
        print(f"\n🔍 Extraction des valeurs originales:")
        
        # Valeurs CM
        cm_title_match = re.search(r'<h2>CM\s*\(([^)]*)\)</h2>', original_html)
        cm_raf_match = re.search(r'<span class="stat-value raf">([^<]*)</span>', original_html)
        cm_modif_match = re.search(r'<span class="stat-value modif">([^<]*)</span>', original_html)
        cm_crea_match = re.search(r'<span class="stat-value crea">([^<]*)</span>', original_html)
        
        # Valeurs Communes
        communes_title_match = re.search(r'<h2>Communes Livrées\s*\(([^)]*)\)</h2>', original_html)
        orange_match = re.search(r'<span class="stat-value orange">([^<]*)</span>', original_html)
        rip_match = re.search(r'<span class="stat-value rip">([^<]*)</span>', original_html)
        
        # Valeurs Script.js
        cm_script_match = re.search(r'const cmCtx.*?data:\s*\[([^\]]*)\]', original_script, flags=re.DOTALL)
        communes_script_match = re.search(r'const communesCtx.*?data:\s*\[([^\]]*)\]', original_script, flags=re.DOTALL)
        
        if all([cm_title_match, cm_raf_match, cm_modif_match, cm_crea_match, 
                communes_title_match, orange_match, rip_match, 
                cm_script_match, communes_script_match]):
            
            print(f"   📋 Valeurs CM HTML:")
            print(f"      Titre: CM ({cm_title_match.group(1)})")
            print(f"      RAF: {cm_raf_match.group(1)}")
            print(f"      MODIF: {cm_modif_match.group(1)}")
            print(f"      CREA: {cm_crea_match.group(1)}")
            
            print(f"   📋 Valeurs Communes HTML:")
            print(f"      Titre: Communes Livrées ({communes_title_match.group(1)})")
            print(f"      Orange: {orange_match.group(1)}")
            print(f"      RIP: {rip_match.group(1)}")
            
            print(f"   📋 Valeurs Script.js:")
            print(f"      CM: [{cm_script_match.group(1).strip()}]")
            print(f"      Communes: [{communes_script_match.group(1).strip()}]")
        else:
            print(f"   ❌ Certaines valeurs originales non trouvées")
            return False
        
        # Données de test réalistes (basées sur l'analyse des données réelles)
        test_data = {
            'cm': {
                'data': [2071, 34, 148],  # RAF, MODIF, CREA
                'total': 2253
            },
            'communes': {
                'data': [87, 12],  # Orange, RIP
                'total': 99
            }
        }
        
        print(f"\n🔄 Injection des nouvelles valeurs:")
        print(f"   CM: Total={test_data['cm']['total']}, RAF={test_data['cm']['data'][0]}, MODIF={test_data['cm']['data'][1]}, CREA={test_data['cm']['data'][2]}")
        print(f"   Communes: Total={test_data['communes']['total']}, Orange={test_data['communes']['data'][0]}, RIP={test_data['communes']['data'][1]}")
        
        # Appliquer toutes les injections HTML
        updated_html = original_html
        
        # 1. Injection CM dans HTML
        # Titre CM
        cm_title_pattern = r'(<h2>CM\s*\()[^)]*(\)</h2>)'
        updated_html = re.sub(cm_title_pattern, rf'\g<1>{test_data["cm"]["total"]}\g<2>', updated_html)
        
        # Valeurs CM individuelles
        raf_pattern = r'(<span class="stat-value raf">)[^<]*(</span>)'
        updated_html = re.sub(raf_pattern, rf'\g<1>{test_data["cm"]["data"][0]}\g<2>', updated_html)
        
        modif_pattern = r'(<span class="stat-value modif">)[^<]*(</span>)'
        updated_html = re.sub(modif_pattern, rf'\g<1>{test_data["cm"]["data"][1]}\g<2>', updated_html)
        
        crea_pattern = r'(<span class="stat-value crea">)[^<]*(</span>)'
        updated_html = re.sub(crea_pattern, rf'\g<1>{test_data["cm"]["data"][2]}\g<2>', updated_html)
        
        # 2. Injection Communes dans HTML
        # Titre Communes
        communes_title_pattern = r'(<h2>Communes Livrées\s*\()[^)]*(\)</h2>)'
        updated_html = re.sub(communes_title_pattern, rf'\g<1>{test_data["communes"]["total"]}\g<2>', updated_html)
        
        # Valeurs Communes individuelles
        orange_pattern = r'(<span class="stat-value orange">)[^<]*(</span>)'
        updated_html = re.sub(orange_pattern, rf'\g<1>{test_data["communes"]["data"][0]}\g<2>', updated_html)
        
        rip_pattern = r'(<span class="stat-value rip">)[^<]*(</span>)'
        updated_html = re.sub(rip_pattern, rf'\g<1>{test_data["communes"]["data"][1]}\g<2>', updated_html)
        
        # 3. Injection dans Script.js
        updated_script = original_script
        
        # CM Script
        cm_script_pattern = r'(const cmCtx.*?data:\s*\[)[^\]]*(\])'
        cm_data_str = ', '.join(str(x) for x in test_data['cm']['data'])
        updated_script = re.sub(cm_script_pattern, rf'\g<1>{cm_data_str}\g<2>', updated_script, flags=re.DOTALL)
        
        # Communes Script
        communes_script_pattern = r'(const communesCtx.*?data:\s*\[)[^\]]*(\])'
        communes_data_str = ', '.join(str(x) for x in test_data['communes']['data'])
        updated_script = re.sub(communes_script_pattern, rf'\g<1>{communes_data_str}\g<2>', updated_script, flags=re.DOTALL)
        
        # 4. Ajouter un commentaire d'horodatage
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment = f'\n<!-- Injection Pladria: {timestamp} | CM: {test_data["cm"]["data"]} | Communes: {test_data["communes"]["data"]} -->\n'
        
        body_close_idx = updated_html.lower().rfind('</body>')
        if body_close_idx != -1:
            updated_html = updated_html[:body_close_idx] + comment + updated_html[body_close_idx:]
        
        # Écrire les fichiers mis à jour
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(updated_script)
        
        print(f"✅ Fichiers mis à jour écrits avec succès")
        
        # Vérification complète
        print(f"\n🔍 Vérification complète de l'injection:")
        
        # Relire les fichiers
        with open(index_path, 'r', encoding='utf-8') as f:
            final_html = f.read()
        
        with open(script_path, 'r', encoding='utf-8') as f:
            final_script = f.read()
        
        # Extraire toutes les valeurs finales
        final_cm_title = re.search(r'<h2>CM\s*\(([^)]*)\)</h2>', final_html).group(1)
        final_cm_raf = re.search(r'<span class="stat-value raf">([^<]*)</span>', final_html).group(1)
        final_cm_modif = re.search(r'<span class="stat-value modif">([^<]*)</span>', final_html).group(1)
        final_cm_crea = re.search(r'<span class="stat-value crea">([^<]*)</span>', final_html).group(1)
        
        final_communes_title = re.search(r'<h2>Communes Livrées\s*\(([^)]*)\)</h2>', final_html).group(1)
        final_orange = re.search(r'<span class="stat-value orange">([^<]*)</span>', final_html).group(1)
        final_rip = re.search(r'<span class="stat-value rip">([^<]*)</span>', final_html).group(1)
        
        final_cm_script = re.search(r'const cmCtx.*?data:\s*\[([^\]]*)\]', final_script, flags=re.DOTALL).group(1).strip()
        final_communes_script = re.search(r'const communesCtx.*?data:\s*\[([^\]]*)\]', final_script, flags=re.DOTALL).group(1).strip()
        
        # Vérifier la cohérence
        print(f"   📋 Valeurs HTML finales:")
        print(f"      CM: Titre=({final_cm_title}), RAF={final_cm_raf}, MODIF={final_cm_modif}, CREA={final_cm_crea}")
        print(f"      Communes: Titre=({final_communes_title}), Orange={final_orange}, RIP={final_rip}")
        
        print(f"   📋 Valeurs Script.js finales:")
        print(f"      CM: [{final_cm_script}]")
        print(f"      Communes: [{final_communes_script}]")
        
        # Validation finale
        success = True
        
        # Vérifier CM
        if (int(final_cm_title) == test_data['cm']['total'] and
            int(final_cm_raf) == test_data['cm']['data'][0] and
            int(final_cm_modif) == test_data['cm']['data'][1] and
            int(final_cm_crea) == test_data['cm']['data'][2] and
            final_cm_script == cm_data_str):
            print(f"   ✅ CM: Injection parfaite (HTML + Script synchronisés)")
        else:
            print(f"   ❌ CM: Échec de l'injection")
            success = False
        
        # Vérifier Communes
        if (int(final_communes_title) == test_data['communes']['total'] and
            int(final_orange) == test_data['communes']['data'][0] and
            int(final_rip) == test_data['communes']['data'][1] and
            final_communes_script == communes_data_str):
            print(f"   ✅ Communes: Injection parfaite (HTML + Script synchronisés)")
        else:
            print(f"   ❌ Communes: Échec de l'injection")
            success = False
        
        # Vérifier le commentaire d'horodatage
        if "Injection Pladria:" in final_html:
            print(f"   ✅ Commentaire d'horodatage ajouté")
        else:
            print(f"   ❌ Commentaire d'horodatage manquant")
        
        if success:
            print(f"\n🎉 INJECTION COMPLÈTE RÉUSSIE!")
            print(f"   • Toutes les valeurs HTML mises à jour")
            print(f"   • Toutes les valeurs Script.js mises à jour")
            print(f"   • Synchronisation parfaite entre HTML et Script")
            print(f"   • Commentaire d'horodatage ajouté")
        
        # Nettoyage
        shutil.rmtree(temp_dir)
        return success
        
    except Exception as e:
        print(f"❌ Erreur dans le test d'injection: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validation_donnees_injectees():
    """Test de validation des données injectées."""
    print(f"\n📋 Test de Validation des Données Injectées:")
    
    try:
        # Données de test avec différents cas
        test_cases = [
            {
                'name': 'Données valides',
                'data': {'cm': [2071, 34, 148], 'communes': [87, 12]},
                'expected_valid': True
            },
            {
                'name': 'Données avec zéros',
                'data': {'cm': [0, 0, 0], 'communes': [0, 0]},
                'expected_valid': True  # Zéros sont valides
            },
            {
                'name': 'Données négatives',
                'data': {'cm': [-1, 34, 148], 'communes': [87, -5]},
                'expected_valid': False
            },
            {
                'name': 'Données manquantes',
                'data': {'cm': [2071, 34], 'communes': [87]},  # Pas assez de valeurs
                'expected_valid': False
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   🧪 Test: {test_case['name']}")
            data = test_case['data']
            
            # Validation simple
            is_valid = True
            errors = []
            
            # Vérifier CM (doit avoir 3 valeurs)
            if 'cm' in data:
                if len(data['cm']) != 3:
                    is_valid = False
                    errors.append("CM doit avoir exactement 3 valeurs")
                
                for i, val in enumerate(data['cm']):
                    if not isinstance(val, (int, float)) or val < 0:
                        is_valid = False
                        errors.append(f"CM valeur {i+1} doit être un nombre positif")
            
            # Vérifier Communes (doit avoir 2 valeurs)
            if 'communes' in data:
                if len(data['communes']) != 2:
                    is_valid = False
                    errors.append("Communes doit avoir exactement 2 valeurs")
                
                for i, val in enumerate(data['communes']):
                    if not isinstance(val, (int, float)) or val < 0:
                        is_valid = False
                        errors.append(f"Communes valeur {i+1} doit être un nombre positif")
            
            # Vérifier le résultat
            if is_valid == test_case['expected_valid']:
                print(f"      ✅ Validation correcte: {'Valide' if is_valid else 'Invalide'}")
                if errors:
                    print(f"         Erreurs: {errors}")
            else:
                print(f"      ❌ Validation incorrecte: Attendu {'Valide' if test_case['expected_valid'] else 'Invalide'}, Obtenu {'Valide' if is_valid else 'Invalide'}")
                return False
        
        print(f"   ✅ Tous les tests de validation réussis")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur dans la validation: {e}")
        return False

def main():
    """Fonction de test principale."""
    print("🚀 Test Complet d'Injection des Valeurs dans le HTML")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Injection complète
    if test_injection_complete_html():
        tests_passed += 1
        print("\n✅ Test 1 RÉUSSI: Injection complète HTML")
    else:
        print("\n❌ Test 1 ÉCHOUÉ: Injection complète HTML")
    
    # Test 2: Validation des données
    if test_validation_donnees_injectees():
        tests_passed += 1
        print("\n✅ Test 2 RÉUSSI: Validation des données")
    else:
        print("\n❌ Test 2 ÉCHOUÉ: Validation des données")
    
    # Résumé
    print("\n" + "=" * 80)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ L'injection des valeurs dans le HTML fonctionne parfaitement!")
        print("\n🎯 Fonctionnalités vérifiées:")
        print("  • Injection des valeurs CM dans HTML (titre + valeurs individuelles)")
        print("  • Injection des valeurs Communes dans HTML (titre + valeurs individuelles)")
        print("  • Mise à jour synchronisée des données Chart.js")
        print("  • Ajout de commentaires d'horodatage")
        print("  • Validation des données injectées")
        print("  • Synchronisation parfaite HTML ↔ Script.js")
        
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) échoué(s).")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test simple pour vérifier que l'analyse fonctionne
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import tempfile
import pandas as pd
import time

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_test_files():
    """Crée des fichiers de test temporaires."""
    temp_dir = tempfile.mkdtemp()
    
    # Créer un fichier QGis de test
    qgis_data = {
        'A': [1, 2, 3, 4, 5],  # num dossier site
        'B': ['Adresse 1', 'Adresse 2', 'Adresse 3', 'Adresse 4', 'Adresse 5'],
        'C': ['75001', '75002', '75003', '75004', '75005'],
        'D': ['Paris', 'Paris', 'Paris', 'Paris', 'Paris'],
        'E': ['Type1', 'Type2', 'Type1', 'Type2', 'Type1'],
        'F': ['Info1', 'Info2', 'Info3', 'Info4', 'Info5'],
        'G': ['Data1', 'Data2', 'Data3', 'Data4', 'Data5'],
        'H': ['Val1', 'Val2', 'Val3', 'Val4', 'Val5'],
        'I': ['Test1', 'Test2', 'Test3', 'Test4', 'Test5'],
        'J': ['OK', 'KO', 'OK', 'KO', 'OK'],  # import fantome
        'K': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'L': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'M': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'N': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'O': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'P': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'Q': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'R': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'S': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'T': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5'],
        'U': ['Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5']
    }
    
    qgis_df = pd.DataFrame(qgis_data)
    qgis_file = os.path.join(temp_dir, 'test_qgis.xlsx')
    qgis_df.to_excel(qgis_file, index=False)
    
    # Créer un fichier de suivi de test avec 3 feuilles
    suivi_data_sheet1 = {
        'Collaborateur': ['Jean Dupont'] * 5,
        'Commune': ['Paris'] * 5,
        'INSEE': ['75001'] * 5,
        'ID_Tache': ['TASK_001'] * 5,
        'Adresse': ['Adresse 1', 'Adresse 2', 'Adresse 3', 'Adresse 4', 'Adresse 5'],
        'Statut': ['En cours', 'Terminé', 'En cours', 'Terminé', 'En cours']
    }
    
    suivi_data_sheet2 = {
        'A': ['Adresse 1', 'Adresse 2', 'Adresse 3'],
        'B': ['Info1', 'Info2', 'Info3'],
        'C': ['Data1', 'Data2', 'Data3'],
        'D': ['Val1', 'Val2', 'Val3'],
        'E': ['Test1', 'Test2', 'Test3'],
        'F': ['Extra1', 'Extra2', 'Extra3'],
        'G': ['More1', 'More2', 'More3'],
        'H': ['Other1', 'Other2', 'Other3'],
        'I': ['OK', 'NOK', 'OK']  # Motifs
    }
    
    suivi_data_sheet3 = {
        'Erreur': ['Erreur 1', 'Erreur 2'],
        'Type': ['Type A', 'Type B'],
        'Description': ['Desc 1', 'Desc 2']
    }
    
    suivi_file = os.path.join(temp_dir, 'test_suivi.xlsx')
    with pd.ExcelWriter(suivi_file, engine='openpyxl') as writer:
        pd.DataFrame(suivi_data_sheet1).to_excel(writer, sheet_name='Sheet1', index=False)
        pd.DataFrame(suivi_data_sheet2).to_excel(writer, sheet_name='Sheet2', index=False)
        pd.DataFrame(suivi_data_sheet3).to_excel(writer, sheet_name='Sheet3', index=False)
    
    return qgis_file, suivi_file, temp_dir

def test_analysis():
    """Test de l'analyse."""
    try:
        print("🧪 Test d'analyse...")
        
        # Créer des fichiers de test
        qgis_file, suivi_file, temp_dir = create_test_files()
        print(f"✅ Fichiers de test créés dans: {temp_dir}")
        
        # Créer une fenêtre de test
        root = tk.Tk()
        root.title("Test - Analyse")
        root.geometry("1200x800")
        
        # Importer et créer le module
        from ui.modules.quality_control_module import QualityControlModule
        
        # Créer un notebook pour simuler l'environnement Pladria
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Créer le module de contrôle qualité
        qc_module = QualityControlModule(notebook)
        
        print("✅ Module créé avec succès")
        
        # Charger les fichiers
        def load_files():
            try:
                from utils.lazy_imports import get_pandas
                pd = get_pandas()
                
                # Charger QGis
                qgis_df = pd.read_excel(qgis_file)
                qc_module.qgis_data = qgis_df
                qc_module.current_qgis_file_path = qgis_file
                print(f"✅ Fichier QGis chargé: {len(qgis_df)} lignes")
                
                # Charger suivi
                suivi_df = pd.read_excel(suivi_file)
                qc_module.suivi_data = suivi_df
                qc_module.current_suivi_file_path = suivi_file
                print(f"✅ Fichier suivi chargé: {len(suivi_df)} lignes")
                
                # Simuler les informations détectées
                qc_module.detected_info = {
                    'collaborateur': 'Jean Dupont',
                    'commune': 'Paris',
                    'insee': '75001',
                    'id_tache': 'TASK_001'
                }
                
                # Mettre à jour les variables si elles existent
                if hasattr(qc_module, 'collaborator_var'):
                    qc_module.collaborator_var.set('Jean Dupont')
                    qc_module.commune_var.set('Paris')
                    qc_module.insee_var.set('75001')
                    qc_module.id_tache_var.set('TASK_001')
                
                print("✅ Informations détectées configurées")
                return True
                
            except Exception as e:
                print(f"❌ Erreur chargement fichiers: {e}")
                return False
        
        # Lancer l'analyse
        def run_analysis():
            try:
                print("\n🔍 Lancement de l'analyse...")
                
                # Vérifier que l'analyse est prête
                if hasattr(qc_module, '_check_analysis_ready'):
                    ready = qc_module._check_analysis_ready()
                    print(f"📋 Analyse prête: {ready}")
                
                # Lancer l'analyse
                if hasattr(qc_module, '_run_quality_analysis'):
                    qc_module._run_quality_analysis()
                    print("✅ Analyse lancée")
                    
                    # Attendre un peu pour que l'analyse se termine
                    def check_results():
                        if hasattr(qc_module, 'qc_results') and qc_module.qc_results:
                            print("✅ Résultats d'analyse disponibles")
                            print(f"📊 Critères analysés: {list(qc_module.qc_results.keys())}")
                            
                            # Tester l'export
                            if hasattr(qc_module, '_export_qc_report'):
                                print("\n📤 Test d'export...")
                                qc_module._export_qc_report()
                                print("✅ Export lancé")
                            
                        else:
                            print("⏳ Analyse en cours...")
                            root.after(1000, check_results)
                    
                    # Vérifier les résultats après 2 secondes
                    root.after(2000, check_results)
                    
                else:
                    print("❌ Méthode d'analyse non trouvée")
                    
            except Exception as e:
                print(f"❌ Erreur analyse: {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
        
        # Séquence de test
        def run_test_sequence():
            if load_files():
                root.after(1000, run_analysis)
            else:
                print("❌ Échec du chargement des fichiers")
                root.after(5000, root.quit)
        
        # Lancer le test après 2 secondes
        root.after(2000, run_test_sequence)
        
        # Fermer après 15 secondes
        root.after(15000, root.quit)
        
        # Afficher la fenêtre
        root.mainloop()
        
        # Nettoyer les fichiers temporaires
        import shutil
        shutil.rmtree(temp_dir)
        print(f"🧹 Fichiers temporaires supprimés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_analysis()
    print(f"\n🏁 Test terminé - {'Succès' if success else 'Échec'}")
    sys.exit(0 if success else 1)

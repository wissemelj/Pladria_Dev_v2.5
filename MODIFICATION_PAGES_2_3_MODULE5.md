# Modifications Pages 2 et 3 - Module 5 Contrôle Qualité

## 🎯 Objectifs des Modifications

### **Page 2 (Controle Qualité CMS)**
- ❌ **Supprimer** le remplissage automatique depuis le fichier suivi commune
- ✅ **Permettre** la saisie manuelle par l'utilisateur

### **Page 3 (Controle Qualité PA)**
- ✅ **Ajouter** une colonne "Batiment" après "Adresse Optimum"
- ✅ **Populer** cette colonne depuis la colonne F page 2 du suivi commune

## 🔧 Modifications Appliquées

### **1. Page 2 - Suppression du Remplissage Automatique**

**Avant :**
```python
# Lecture automatique de la page 1 du suivi commune
suivi_page1_df = pd.read_excel(self.current_suivi_file_path, sheet_name=0, date_format=None)

# Extraction et ajout automatique des données
for index, row in suivi_page1_df.iterrows():
    id_tache = row.iloc[2]      # Colonne C
    voie_demande = row.iloc[3]  # Colonne D  
    motif_voie_initial = row.iloc[4]  # Colonne E
    
    page2_data.append([id_tache, voie_demande, motif_voie_initial, '', ''])
```

**Après :**
```python
# Page 2: Controle Qualité CMS - Structure vide pour saisie manuelle
page2_data = [
    ['ID Tache', 'Voie demandé', 'Motif Voie Initial', 'Etat', 'Commentaire Controleur']
]

# Ajouter des lignes vides pour la saisie manuelle (pas de remplissage automatique)
for i in range(20):  # 20 lignes vides pour saisie manuelle
    page2_data.append([' ', ' ', ' ', ' ', ' '])
```

**Résultat :**
- ✅ Page 2 entièrement vide (sauf en-tête)
- ✅ 20 lignes vides pour saisie manuelle
- ✅ Utilisateur contrôle totalement le contenu

### **2. Page 3 - Ajout Colonne Batiment**

**Structure Avant :**
```
| Num Dossier Site | Adresse Optimum | Adresse BAN | Motif Initial | Etat | Commentaire Controleur |
```

**Structure Après :**
```
| Num Dossier Site | Adresse Optimum | Batiment | Adresse BAN | Motif Initial | Etat | Commentaire Controleur |
```

**Logique de Population :**
```python
# Créer un dictionnaire pour mapper les codes IMB aux données de bâtiment
imb_to_batiment = {}

# Lire la page 2 (index 1) du fichier suivi commune
suivi_page2_df = pd.read_excel(self.current_suivi_file_path, sheet_name=1, date_format=None)

# Extraire les données des colonnes A (IMB) et F (Batiment)
for index, row in suivi_page2_df.iterrows():
    imb_code = str(row.iloc[0]).strip()    # Colonne A: IMB
    batiment = str(row.iloc[5]).strip()    # Colonne F: Batiment
    
    if imb_code and imb_code not in ['', 'nan', 'IMB', 'Num Dossier Site']:
        imb_to_batiment[imb_code] = batiment

# Lors de l'ajout des erreurs à la page 3
for erreur in toutes_erreurs_detectees:
    imb_code = erreur.get('imb_code', '')
    batiment = imb_to_batiment.get(imb_code, '') if imb_code else ''
    
    page3_data.append([
        imb_code,                             # Colonne A: Num Dossier Site
        erreur.get('adresse_optimum', ''),    # Colonne B: Adresse Optimum
        batiment,                             # Colonne C: Batiment (NOUVEAU)
        erreur.get('adresse_ban', ''),        # Colonne D: Adresse BAN
        motif_initial,                        # Colonne E: Motif Initial
        '',                                   # Colonne F: Etat
        '',                                   # Colonne G: Commentaire Controleur
        ''                                    # Colonne H: Supplémentaire
    ])
```

## 📊 Mapping des Données

### **Source des Données Batiment**
- **Fichier** : Suivi commune (même fichier que les autres données)
- **Page** : Page 2 (index 1)
- **Colonne Source** : F (Batiment)
- **Colonne Clé** : A (Code IMB)

### **Processus de Mapping**
1. **Lecture** : Page 2 du suivi commune
2. **Extraction** : Colonne A (IMB) → Colonne F (Batiment)
3. **Stockage** : Dictionnaire `imb_to_batiment`
4. **Application** : Lors de l'ajout des erreurs à la page 3

### **Exemple de Mapping**
```python
imb_to_batiment = {
    'IMB/62148/X/000F': 'Bâtiment A',
    'IMB/62148/X/003U': 'Bâtiment B',
    'IMB/62148/X/003H': 'Résidence C'
}
```

## 🎨 Impact sur l'Interface

### **Page 2 - Controle Qualité CMS**
- ✅ **Flexibilité** : Utilisateur saisit manuellement les données
- ✅ **Contrôle** : Pas de données pré-remplies automatiquement
- ✅ **Simplicité** : Structure claire avec 20 lignes vides

### **Page 3 - Controle Qualité PA**
- ✅ **Information enrichie** : Colonne Batiment ajoutée
- ✅ **Données automatiques** : Batiment populé depuis suivi commune
- ✅ **Cohérence** : Mapping basé sur les codes IMB

## 🔍 Détails Techniques

### **Fichier Modifié**
- **Chemin** : `src/ui/modules/quality_control_module.py`
- **Méthode** : `_prepare_excel_data()`

### **Changements Spécifiques**

**1. Page 2 (Lignes 2540-2548)**
- Suppression de la logique de lecture automatique
- Simplification avec 20 lignes vides

**2. Page 3 (Lignes 2550-2630)**
- Ajout de l'en-tête "Batiment" 
- Création du mapping IMB→Batiment
- Modification de l'ajout des erreurs pour inclure Batiment
- Ajustement du nombre de colonnes (7→8)

**3. DataFrame (Ligne 2656)**
- Ajustement pour 8 colonnes au lieu de 7

## ✅ Avantages des Modifications

### **1. Flexibilité Page 2**
- Utilisateur contrôle entièrement le contenu
- Pas de données automatiques non désirées
- Saisie manuelle selon les besoins

### **2. Enrichissement Page 3**
- Information Batiment disponible automatiquement
- Mapping intelligent basé sur les codes IMB
- Cohérence avec les données du suivi commune

### **3. Robustesse**
- Gestion des erreurs de lecture
- Mapping sécurisé (vérification des clés)
- Fallback en cas de données manquantes

## 🔍 Validation

### **Test Page 2**
1. Générer un rapport de contrôle qualité
2. Vérifier que la page 2 est vide (sauf en-tête)
3. Confirmer 20 lignes vides pour saisie

### **Test Page 3**
1. Vérifier la présence de la colonne "Batiment"
2. Confirmer que les données Batiment sont populées
3. Valider le mapping IMB→Batiment

### **Cas de Test**
```
Si suivi commune page 2 contient:
- Ligne X: IMB/62148/X/000F | ... | ... | ... | ... | Bâtiment A

Alors page 3 rapport devrait afficher:
- IMB/62148/X/000F | Adresse... | Bâtiment A | Adresse BAN... | ...
```

Ces modifications améliorent la flexibilité de la page 2 et enrichissent les informations de la page 3 avec les données de bâtiment.

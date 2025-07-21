# 📊 Feuille "Ecart" Améliorée - Module 5 Contrôle Qualité

## 🎯 Objectif

La feuille **"Ecart"** améliorée du Module 5 offre une analyse complète et détaillée des écarts entre les fichiers **QGis** et **Suivi Commune**, incluant une comparaison au niveau des codes IMB individuels.

## 🆕 Fonctionnalités Améliorées

### ✨ **Feuille Excel "Ecart" (Page 4) - Version Améliorée**
- **Nom de la feuille** : `Ecart`
- **Position** : 4ème feuille du fichier Excel généré
- **Objectif** : Analyse complète des écarts avec deux niveaux de détail :
  1. **Résumé par motif** : Vue d'ensemble des écarts par type de motif
  2. **Analyse détaillée par IMB** : Comparaison individuelle de chaque code IMB

### 📋 **Structure de la Feuille Améliorée**

#### **Section 1: Résumé par Motif**
| Colonne | Nom | Description |
|---------|-----|-------------|
| **A** | Type d'Écart | Le motif analysé (ex: "Motif: AD RAS") |
| **B** | Fichier QGis | Nombre d'occurrences dans QGis |
| **C** | Suivi Commune | Nombre d'occurrences dans Suivi Commune |
| **D** | Différence | Écart calculé (QGis - Suivi) |
| **E** | Détails | Description de l'écart |
| **F** | Statut | Indicateur visuel (✅ OK / ❌ ÉCART) |

#### **Section 2: Analyse Détaillée par IMB**
| Colonne | Nom | Description |
|---------|-----|-------------|
| **A** | Code IMB | Code IMB individuel analysé |
| **B** | Motif QGis | Motif trouvé dans le fichier QGis |
| **C** | Motif Suivi | Motif trouvé dans le fichier Suivi Commune |
| **D** | Statut Comparaison | Résultat de la comparaison (✅ MATCH / ❌ MISMATCH / ⚠️ MANQUANT) |
| **E** | Détails | Description détaillée de l'écart ou du problème |
| **F** | Action | Action recommandée pour corriger l'écart |

### 🔍 **Motifs Analysés**

La feuille analyse les motifs suivants :
- **AD RAS**
- **OK**
- **NOK**
- **UPR RAS**
- **UPR OK**
- **UPR NOK**
- **HORS COMMUNE**

### 🎨 **Mise en Forme**

#### **Couleurs et Styles**
- **Titre** : Fond gris foncé, texte blanc, police Arial 14pt
- **En-têtes** : Fond bleu acier, texte blanc, police Arial 11pt
- **🟢 Vert** : ✅ MATCH (correspondances parfaites)
- **🟡 Jaune** : ⚠️ MATCH+DOUBLONS (correspondances avec doublons détectés)
- **🟠 Orangé** : ❌ MISMATCH (motifs différents nécessitant correction)
- **🔴 Rouge** : ⚠️ MANQUANT (enregistrements manquants dans un des fichiers)

#### **Largeurs de Colonnes**
- **Type d'Écart** : 25 caractères
- **Fichier QGis** : 15 caractères
- **Suivi Commune** : 15 caractères
- **Différence** : 12 caractères
- **Détails** : 25 caractères
- **Statut** : 15 caractères

## 🔧 **Implémentation Technique**

### **Fichiers Modifiés**
- `src/ui/modules/quality_control_module.py`

### **Nouvelles Fonctions**
1. **`_prepare_ecart_data()`** : Prépare les données de la feuille Ecart avec les deux sections
2. **`_analyze_imb_level_gaps()`** : ⭐ **NOUVEAU** - Analyse détaillée au niveau des codes IMB individuels
3. **`_format_page4_ecart()`** : Applique la mise en forme améliorée à la feuille

### **Modifications Existantes**
- **`_prepare_excel_data()`** : Retourne maintenant 4 feuilles au lieu de 3
- **`_write_excel_file()`** : Accepte et traite 4 paramètres de données
- **`_generate_excel_report()`** : Gère la création de 4 feuilles

### **🔍 Logique d'Analyse IMB Détaillée**

#### **Extraction des Données**
1. **Fichier QGis** :
   - Codes IMB : Colonne A (Num Dossier Site)
   - Motifs : Colonne J (Import Fantome)

2. **Fichier Suivi Commune** :
   - Codes IMB : Page 2, Colonne C
   - Motifs : Page 2, Colonne I (Motif)

#### **Logique de Comparaison**
```python
Pour chaque code IMB trouvé dans les deux fichiers:
    Si IMB présent dans QGis ET Suivi:
        Si motifs identiques → ✅ MATCH
        Si motifs différents → ❌ MISMATCH
        Si doublons détectés → ⚠️ MATCH+DOUBLONS

    Si IMB présent seulement dans QGis:
        → ⚠️ MANQUANT SUIVI

    Si IMB présent seulement dans Suivi:
        → ⚠️ MANQUANT QGIS
```

#### **Gestion des Cas Particuliers**
- **Doublons** : Détection des codes IMB multiples dans un même fichier
- **Valeurs vides** : Gestion des motifs ou codes IMB manquants
- **Normalisation** : Conversion en majuscules et suppression des espaces

## 📊 **Exemple de Données Améliorées**

### **Section 1: Résumé par Motif**
```
=== SECTION 1: RÉSUMÉ PAR MOTIF ===

Type d'Écart        | QGis | Suivi | Diff | Détails        | Statut
--------------------|------|-------|------|----------------|----------
Motif: AD RAS       | 10   | 12    | -2   | -2 dans QGis   | ❌ ÉCART
Motif: OK           | 25   | 25    | 0    | Aucun écart    | ✅ OK
Motif: NOK          | 5    | 3     | 2    | +2 dans QGis   | ❌ ÉCART
Motif: UPR OK       | 8    | 8     | 0    | Aucun écart    | ✅ OK

RÉSUMÉ MOTIFS       | Total écarts détectés: 2              | ❌ ATTENTION
```

### **Section 2: Analyse Détaillée par IMB**
```
=== SECTION 2: ANALYSE DÉTAILLÉE PAR IMB ===

Code IMB | Motif QGis | Motif Suivi | Statut        | Détails                    | Action
---------|------------|-------------|---------------|----------------------------|------------------
IMB001   | AD RAS     | AD RAS      | ✅ MATCH      | Motifs identiques          | Aucune
IMB002   | OK         | NOK         | ❌ MISMATCH   | Motifs différents          | Vérifier et corriger
IMB003   | NOK        | ABSENT      | ⚠️ MANQUANT   | Absent du Suivi Commune    | Ajouter dans Suivi
IMB004   | ABSENT     | UPR OK      | ⚠️ MANQUANT   | Absent du fichier QGis     | Ajouter dans QGis

=== RÉSUMÉ ANALYSE IMB ===
Total IMB analysés: 4
✅ Matches: 1
❌ Mismatches: 1
⚠️ Manquants QGis: 1
⚠️ Manquants Suivi: 1
```

## 🚀 **Utilisation**

### **Étapes pour Générer la Feuille Ecart**

1. **Lancer Pladria** : Exécutez `LAUNCH_PLADRIA.bat` ou `python src/launch_app.py`
2. **Accéder au Module 5** : Sélectionnez "Module 5 - Contrôle Qualité"
3. **Charger les Fichiers** :
   - Fichier QGis (format Excel)
   - Fichier Suivi Commune (format Excel)
4. **Lancer l'Analyse** : Cliquez sur "Analyser"
5. **Exporter le Rapport** : Cliquez sur "Exporter Rapport"
6. **Vérifier la Feuille** : Ouvrez le fichier Excel généré et consultez la feuille "Ecart"

### **Interprétation des Résultats**

- **✅ OK** : Aucun écart détecté pour ce motif
- **❌ ÉCART** : Différence détectée entre les deux fichiers
- **⚠️ ATTENTION** : Résumé indiquant des écarts globaux

## 🔍 **Cas d'Usage**

### **Détection d'Erreurs de Saisie**
- Identifier les incohérences entre les fichiers
- Localiser les motifs mal saisis
- Quantifier les écarts par type

### **Contrôle Qualité**
- Valider la cohérence des données
- Générer des rapports d'audit
- Faciliter les corrections

### **Suivi des Performances**
- Mesurer la qualité de saisie
- Identifier les tendances d'erreurs
- Améliorer les processus

## 🧪 **Test de la Fonctionnalité**

Un script de test `test_ecart_sheet.py` a été créé pour valider l'implémentation :

```bash
python test_ecart_sheet.py
```

## 📝 **Notes Techniques**

- La feuille utilise les données du **Critère 0** (Écart Plan Adressage)
- Compatible avec la structure Excel existante
- Gestion d'erreurs intégrée
- Logs détaillés pour le débogage

## 🎉 **Résultat Final**

Le fichier Excel généré contient maintenant **4 feuilles** :
1. **Etat de lieu** (Page 1)
2. **Controle Qualité CMS** (Page 2)
3. **Controle Qualité PA** (Page 3)
4. **Ecart** (Page 4) ← **NOUVEAU !**

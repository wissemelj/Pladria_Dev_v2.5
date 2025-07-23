# Pladria v2.5 - Système de Contrôle Qualité

## 📋 Description
Pladria est un système complet de contrôle qualité développé par Sofrecom pour l'analyse et la validation des données de plan d'adressage.

## 🚀 Modules Disponibles

### Module 1: Générateur de Suivi
- Traitement des fichiers MOAI et QGis
- Génération automatique des suivis de communes

### Module 2: Suivi Global
- Agrégation des suivis de communes
- Vue d'ensemble des tickets

### Module 3: Statistiques Équipe
- Tableau de bord des performances
- Analyse des métriques d'équipe

### Module 4: Visualiseur de Données
- Visualisation des données global tickets
- Filtres avancés et tri

### Module 5: Contrôle Qualité
- Système d'analyse et validation qualité
- 5 critères de contrôle automatisés
- Génération de rapports Excel détaillés

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Windows 10/11 (64-bit)

### Dépendances
```bash
pip install -r Package/requirements.txt
```

## 🎯 Utilisation

### Lancement de l'application
```bash
# Méthode 1: Script batch
LAUNCH_PLADRIA.bat

# Méthode 2: Python direct
python src/main.py
```

### Navigation
- Interface graphique intuitive
- Navigation par onglets
- Raccourcis clavier disponibles

## 📊 Module 5 - Contrôle Qualité

### Critères de Contrôle
1. **Écart Plan Adressage** - Compare les motifs entre QGis et Suivi Commune
2. **Oubli Ticket UPR et 501/511** - Vérifie les tickets requis
3. **Contrôle IMB Doublons** - Détecte les doublons suspects
4. **Détection "AD à Analyser"** - Identifie les entrées à analyser
5. **Motif Incorrect** - Détecte les motifs non autorisés

### Fonctionnalités
- ✅ Import automatique des fichiers Excel
- ✅ Analyse selon 5 critères de qualité
- ✅ Calcul de scores et pourcentages de conformité
- ✅ Génération de rapports Excel détaillés
- ✅ Visualiseur intégré avec filtres
- ✅ Évaluation automatique du statut commune (OK/KO)

## 🔧 Configuration

### Structure des Fichiers
```
Pladria_Dev_v2.5/
├── src/                    # Code source
├── Package/               # Scripts de build
├── logs/                  # Fichiers de logs
├── config/               # Configuration
└── README.md            # Ce fichier
```

### Teams Integration
Le système s'intègre avec Microsoft Teams pour la gestion des fichiers et dossiers de communes.

## 📝 Logs
Les logs sont automatiquement générés dans le dossier `logs/` avec rotation quotidienne.

## 🏗️ Build
```bash
# Build simple
Package/BUILD_SIMPLE.bat

# Build rapide
Package/BUILD_QUICK.bat

# Build depuis l'explorateur
Package/BUILD_FROM_EXPLORER.bat
```

## 📄 Licence
© 2024 Sofrecom - Tous droits réservés

## 🤝 Support
Pour toute question ou problème, contactez l'équipe de développement Sofrecom.

---
**Pladria v2.5** - Système de Contrôle Qualité Professionnel

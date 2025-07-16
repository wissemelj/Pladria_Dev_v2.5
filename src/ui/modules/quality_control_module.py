"""
Module 5: Contrôle Qualité - Pladria v3.0
Système de contrôle qualité pour l'analyse et la validation des données.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple

# Import des utilitaires Pladria
from config.constants import COLORS, AppInfo, TeamsConfig, UIConfig
from utils.logging_config import setup_logging
from utils.lazy_imports import get_pandas
from utils.performance import run_async_task
from utils.file_utils import check_file_access


class QualityControlModule:
    """Module de contrôle qualité pour Pladria v3.0."""
    
    def __init__(self, parent: tk.Widget, navigation_manager=None):
        """
        Initialise le module de contrôle qualité.

        Args:
            parent: Widget parent (fenêtre principale)
            navigation_manager: Gestionnaire de navigation (optionnel)
        """
        self.parent = parent
        self.navigation_manager = navigation_manager
        self.logger = logging.getLogger(__name__)

        # Variables de données
        self.qgis_data = None  # Données du fichier résultats QGis
        self.suivi_data = None  # Données du fichier suivi commune
        self.qc_results = None  # Résultats de l'analyse qualité
        self.current_qgis_file_path = None
        self.current_suivi_file_path = None

        # Variables d'interface
        self.main_frame = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None

        # Variables de sélection
        self.collaborator_var = tk.StringVar()
        self.commune_var = tk.StringVar()
        self.insee_var = tk.StringVar()
        self.id_tache_var = tk.StringVar()

        # Données détectées
        self.detected_info = {}

        # Configuration Teams
        self.teams_folder_path = TeamsConfig.get_teams_base_path()

        # Configuration
        self.setup_ui()

        self.logger.info("Module Contrôle Qualité initialisé")
    
    def setup_ui(self):
        """Configure l'interface utilisateur ultra-compacte sans scrolling."""
        try:
            # Frame principal direct sans scrolling - ultra compact
            self.main_frame = tk.Frame(self.parent, bg=COLORS['BG'])
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

            # Layout en grille pour maximiser l'espace
            self.main_frame.grid_rowconfigure(0, weight=0)  # Header compact
            self.main_frame.grid_rowconfigure(1, weight=1)  # Contenu principal
            self.main_frame.grid_rowconfigure(2, weight=0)  # Status compact
            self.main_frame.grid_columnconfigure(0, weight=1)

            # Header ultra-compact
            self._create_ultra_compact_header()

            # Contenu principal en grille 2x2
            self._create_compact_main_content()

            # Status bar ultra-compact
            self._create_ultra_compact_status()

            self.logger.info("Interface utilisateur ultra-compacte créée avec succès")

        except Exception as e:
            self.logger.error(f"Erreur lors de la création de l'interface QC: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            messagebox.showerror("Erreur", f"Impossible de créer l'interface du module:\n{e}")

    def _create_ultra_compact_header(self):
        """Crée un header ultra-compact en une seule ligne."""
        header_frame = tk.Frame(self.main_frame, bg=COLORS['CARD'], height=35)
        header_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=1)
        header_frame.pack_propagate(False)
        header_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Contenu en ligne horizontale
        content = tk.Frame(header_frame, bg=COLORS['CARD'])
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=3)

        # Icône et titre
        tk.Label(content, text="🔍", font=("Segoe UI", 12),
                fg=COLORS['PRIMARY'], bg=COLORS['CARD']).pack(side=tk.LEFT)

        tk.Label(content, text="Module 5 - Contrôle Qualité",
                font=("Segoe UI", 10, "bold"), fg=COLORS['PRIMARY'],
                bg=COLORS['CARD']).pack(side=tk.LEFT, padx=(5, 15))

        # Indicateurs de statut en ligne
        self._create_inline_status_indicators(content)

    def _create_inline_status_indicators(self, parent: tk.Widget):
        """Crée les indicateurs de statut en ligne."""
        # Séparateur
        tk.Label(parent, text="|", font=("Segoe UI", 10),
                fg=COLORS['BORDER'], bg=COLORS['CARD']).pack(side=tk.LEFT, padx=5)

        # Indicateur fichiers
        self.files_status = tk.Label(parent, text="📁 Fichiers: En attente",
                                   font=("Segoe UI", 8), fg=COLORS['INFO'],
                                   bg=COLORS['CARD'])
        self.files_status.pack(side=tk.LEFT, padx=5)

        # Indicateur analyse
        self.analysis_status = tk.Label(parent, text="🔍 Analyse: Non effectuée",
                                      font=("Segoe UI", 8), fg=COLORS['TEXT_SECONDARY'],
                                      bg=COLORS['CARD'])
        self.analysis_status.pack(side=tk.LEFT, padx=5)

        # Indicateur rapport
        self.report_status = tk.Label(parent, text="📊 Rapport: Non généré",
                                    font=("Segoe UI", 8), fg=COLORS['TEXT_SECONDARY'],
                                    bg=COLORS['CARD'])
        self.report_status.pack(side=tk.LEFT, padx=5)

    def _create_compact_main_content(self):
        """Crée le contenu principal en grille 2x2 ultra-compacte."""
        main_content = tk.Frame(self.main_frame, bg=COLORS['BG'])
        main_content.grid(row=1, column=0, sticky="nsew", padx=2, pady=1)

        # Configuration de la grille 2x2
        main_content.grid_rowconfigure(0, weight=1)
        main_content.grid_rowconfigure(1, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Quadrant 1: Fichiers (haut gauche)
        self._create_files_quadrant(main_content, 0, 0)

        # Quadrant 2: Informations détectées (haut droite)
        self._create_info_quadrant(main_content, 0, 1)

        # Quadrant 3: Analyse et critères (bas gauche)
        self._create_analysis_quadrant(main_content, 1, 0)

        # Quadrant 4: Résultats (bas droite)
        self._create_results_quadrant(main_content, 1, 1)

    def _create_files_quadrant(self, parent: tk.Widget, row: int, col: int):
        """Quadrant 1: Chargement des fichiers ultra-compact."""
        frame = tk.Frame(parent, bg=COLORS['CARD'], relief='flat', bd=1)
        frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Titre compact
        title_frame = tk.Frame(frame, bg=COLORS['ACCENT'], height=25)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="📁 Chargement Fichiers",
                font=("Segoe UI", 9, "bold"), fg=COLORS['PRIMARY'],
                bg=COLORS['ACCENT']).pack(pady=3)

        # Contenu
        content = tk.Frame(frame, bg=COLORS['CARD'])
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # QGis file - ultra compact
        qgis_frame = tk.Frame(content, bg=COLORS['CARD'])
        qgis_frame.pack(fill=tk.X, pady=1)

        tk.Label(qgis_frame, text="🗺️ QGis:", font=("Segoe UI", 8, "bold"),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['CARD']).pack(anchor=tk.W)

        from tkinter import ttk
        self.load_qgis_button = ttk.Button(qgis_frame, text="📂 Importer QGis",
                                         command=self._load_qgis_file, style='Compact.TButton')
        self.load_qgis_button.pack(anchor=tk.W, pady=1)

        self.qgis_info_label = tk.Label(qgis_frame, text="❌ Non chargé",
                                      font=("Segoe UI", 7), fg=COLORS['TEXT_SECONDARY'],
                                      bg=COLORS['CARD'])
        self.qgis_info_label.pack(anchor=tk.W)

        # Séparateur mini
        tk.Frame(content, height=1, bg=COLORS['BORDER']).pack(fill=tk.X, pady=2)

        # Suivi file - ultra compact
        suivi_frame = tk.Frame(content, bg=COLORS['CARD'])
        suivi_frame.pack(fill=tk.X, pady=1)

        tk.Label(suivi_frame, text="📋 Suivi:", font=("Segoe UI", 8, "bold"),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['CARD']).pack(anchor=tk.W)

        self.load_suivi_button = ttk.Button(suivi_frame, text="📂 Importer Suivi",
                                          command=self._load_suivi_file, style='Compact.TButton')
        self.load_suivi_button.pack(anchor=tk.W, pady=1)

        self.suivi_info_label = tk.Label(suivi_frame, text="❌ Non chargé",
                                       font=("Segoe UI", 7), fg=COLORS['TEXT_SECONDARY'],
                                       bg=COLORS['CARD'])
        self.suivi_info_label.pack(anchor=tk.W)

    def _create_info_quadrant(self, parent: tk.Widget, row: int, col: int):
        """Quadrant 2: Informations détectées ultra-compact."""
        frame = tk.Frame(parent, bg=COLORS['CARD'], relief='flat', bd=1)
        frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Titre compact
        title_frame = tk.Frame(frame, bg=COLORS['ACCENT'], height=25)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="📋 Informations Détectées",
                font=("Segoe UI", 9, "bold"), fg=COLORS['PRIMARY'],
                bg=COLORS['ACCENT']).pack(pady=3)

        # Contenu en grille 2x2
        content = tk.Frame(frame, bg=COLORS['CARD'])
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # Ligne 1
        self._create_mini_info_field(content, 0, 0, "👤", "Collaborateur", self.collaborator_var)
        self._create_mini_info_field(content, 0, 1, "🏘️", "Commune", self.commune_var)

        # Ligne 2
        self._create_mini_info_field(content, 1, 0, "🏛️", "INSEE", self.insee_var)
        self._create_mini_info_field(content, 1, 1, "🆔", "ID Tâche", self.id_tache_var)

        # Note ultra-compacte
        note = tk.Label(content, text="ℹ️ Auto-détection depuis fichier suivi",
                       font=("Segoe UI", 7), fg=COLORS['INFO'], bg=COLORS['CARD'])
        note.grid(row=2, column=0, columnspan=2, sticky="w", pady=(3, 0))

    def _create_mini_info_field(self, parent: tk.Widget, row: int, col: int,
                               icon: str, label: str, var: tk.StringVar):
        """Crée un champ d'information mini."""
        field_frame = tk.Frame(parent, bg=COLORS['CARD'])
        field_frame.grid(row=row, column=col, sticky="ew", padx=2, pady=1)

        # Header en ligne
        header = tk.Frame(field_frame, bg=COLORS['CARD'])
        header.pack(fill=tk.X)

        tk.Label(header, text=icon, font=("Segoe UI", 8),
                fg=COLORS['SECONDARY'], bg=COLORS['CARD']).pack(side=tk.LEFT)

        tk.Label(header, text=f"{label}:", font=("Segoe UI", 7, "bold"),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['CARD']).pack(side=tk.LEFT, padx=(2, 0))

        # Valeur
        value_label = tk.Label(field_frame, textvariable=var, font=("Segoe UI", 7),
                              fg=COLORS['INFO'], bg=COLORS['CARD'], anchor='w')
        value_label.pack(fill=tk.X)

        # Stocker pour mise à jour
        if not hasattr(self, 'info_displays'):
            self.info_displays = {}
        self.info_displays[label.lower()] = value_label

    def _create_analysis_quadrant(self, parent: tk.Widget, row: int, col: int):
        """Quadrant 3: Analyse et critères ultra-compact."""
        frame = tk.Frame(parent, bg=COLORS['CARD'], relief='flat', bd=1)
        frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Titre compact
        title_frame = tk.Frame(frame, bg=COLORS['ACCENT'], height=25)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="🔍 Analyse Qualité",
                font=("Segoe UI", 9, "bold"), fg=COLORS['PRIMARY'],
                bg=COLORS['ACCENT']).pack(pady=3)

        # Contenu
        content = tk.Frame(frame, bg=COLORS['CARD'])
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # Critères ultra-compacts
        criteria_frame = tk.Frame(content, bg=COLORS['LIGHT'], relief='flat', bd=1)
        criteria_frame.pack(fill=tk.X, pady=(0, 3))
        criteria_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        criteria_content = tk.Frame(criteria_frame, bg=COLORS['LIGHT'])
        criteria_content.pack(fill=tk.X, padx=3, pady=2)

        # Critère 0
        c0_frame = tk.Frame(criteria_content, bg=COLORS['LIGHT'])
        c0_frame.pack(fill=tk.X, pady=1)

        tk.Label(c0_frame, text="0", font=("Segoe UI", 7, "bold"),
                fg='white', bg=COLORS['SECONDARY'], padx=3, pady=1).pack(side=tk.LEFT)
        tk.Label(c0_frame, text="Incohérences fichiers", font=("Segoe UI", 7),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

        # Critère 1
        c1_frame = tk.Frame(criteria_content, bg=COLORS['LIGHT'])
        c1_frame.pack(fill=tk.X, pady=1)

        tk.Label(c1_frame, text="1", font=("Segoe UI", 7, "bold"),
                fg='white', bg=COLORS['SECONDARY'], padx=3, pady=1).pack(side=tk.LEFT)
        tk.Label(c1_frame, text="Doublons IMB", font=("Segoe UI", 7),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

        # Critère 3
        c3_frame = tk.Frame(criteria_content, bg=COLORS['LIGHT'])
        c3_frame.pack(fill=tk.X, pady=1)
        tk.Label(c3_frame, text="CRITÈRE 3", font=("Segoe UI", 7, "bold"),
                fg='white', bg=COLORS['SECONDARY'], padx=3, pady=1).pack(side=tk.LEFT)
        tk.Label(c3_frame, text="Contrôle IMB Doublons", font=("Segoe UI", 7),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

        # Critère 4
        c4_frame = tk.Frame(criteria_content, bg=COLORS['LIGHT'])
        c4_frame.pack(fill=tk.X, pady=1)
        tk.Label(c4_frame, text="CRITÈRE 4", font=("Segoe UI", 7, "bold"),
                fg='white', bg=COLORS['SECONDARY'], padx=3, pady=1).pack(side=tk.LEFT)
        tk.Label(c4_frame, text="AD à Analyser", font=("Segoe UI", 7),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

        # Boutons d'action
        buttons_frame = tk.Frame(content, bg=COLORS['CARD'])
        buttons_frame.pack(fill=tk.X, pady=(3, 0))

        from tkinter import ttk
        self.analyze_button = ttk.Button(buttons_frame, text="🔍 Analyser",
                                       command=self._run_quality_analysis,
                                       style='CompactWarning.TButton', state='disabled')
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 3))

        self.export_button = ttk.Button(buttons_frame, text="📤 Exporter",
                                      command=self._export_qc_report,
                                      style='Compact.TButton', state='disabled')
        self.export_button.pack(side=tk.LEFT)

    def _create_results_quadrant(self, parent: tk.Widget, row: int, col: int):
        """Quadrant 4: Résultats ultra-compact."""
        frame = tk.Frame(parent, bg=COLORS['CARD'], relief='flat', bd=1)
        frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Titre compact
        title_frame = tk.Frame(frame, bg=COLORS['ACCENT'], height=25)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="📊 Résultats",
                font=("Segoe UI", 9, "bold"), fg=COLORS['PRIMARY'],
                bg=COLORS['ACCENT']).pack(pady=3)

        # Zone de résultats
        self.results_frame = tk.Frame(frame, bg=COLORS['CARD'])
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # Message initial ultra-compact
        self.results_label = tk.Label(
            self.results_frame,
            text="⏳ En attente\n\nChargez les fichiers\net lancez l'analyse",
            font=("Segoe UI", 8),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD'],
            justify=tk.CENTER
        )
        self.results_label.pack(expand=True)

    def _create_ultra_compact_status(self):
        """Crée la barre de statut ultra-compacte."""
        status_frame = tk.Frame(self.main_frame, bg=COLORS['LIGHT'], height=25)
        status_frame.grid(row=2, column=0, sticky="ew", padx=2, pady=1)
        status_frame.pack_propagate(False)
        status_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Contenu en ligne
        content = tk.Frame(status_frame, bg=COLORS['LIGHT'])
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Progress bar mini
        from tkinter import ttk
        self.progress_var = tk.DoubleVar()

        tk.Label(content, text="Progression:", font=("Segoe UI", 8),
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(content, variable=self.progress_var,
                                          maximum=100, length=150)
        self.progress_bar.pack(side=tk.LEFT, padx=(5, 10))

        # Status label
        self.status_label = tk.Label(content, text="Prêt - En attente des fichiers",
                                   font=("Segoe UI", 8), fg=COLORS['INFO'],
                                   bg=COLORS['LIGHT'])
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Créer un status_icon factice pour compatibilité
        self.status_icon = self.status_label
    
    def _create_modern_header(self, parent: tk.Widget):
        """Crée l'en-tête moderne du module avec style Sofrecom."""
        try:
            from ui.styles import create_sofrecom_card

            # Conteneur principal pour l'en-tête
            header_container = tk.Frame(parent, bg=COLORS['BG'])
            header_container.pack(fill=tk.X, pady=(0, 20))

            # Carte d'en-tête avec style Sofrecom
            header_card = create_sofrecom_card(
                header_container,
                title="Module 5 - Contrôle Qualité",
                subtitle="Système d'Analyse et de Validation de la Qualité des Données",
                description="Comparez les fichiers QGis et Teams pour détecter les incohérences et doublons automatiquement",
                icon="🔍",
                clickable=False
            )
            header_card.pack(fill=tk.X, padx=5, pady=5)

            # Indicateurs de statut rapide
            self._create_quick_status_indicators(header_container)

        except Exception as e:
            self.logger.warning(f"Fallback to basic header: {e}")
            # Fallback to basic header
            header_frame = tk.Frame(parent, bg=COLORS['CARD'])
            header_frame.pack(fill=tk.X, pady=(0, 20))

            title_label = tk.Label(
                header_frame,
                text="🔍 Module 5 - Contrôle Qualité",
                font=("Segoe UI", 16, "bold"),
                fg=COLORS['PRIMARY'],
                bg=COLORS['CARD']
            )
            title_label.pack(pady=10)

            desc_label = tk.Label(
                header_frame,
                text="Système d'analyse et de validation de la qualité des données",
                font=("Segoe UI", 10),
                fg=COLORS['TEXT_SECONDARY'],
                bg=COLORS['CARD']
            )
            desc_label.pack(pady=(0, 10))
    
    def _create_modern_data_loading_section(self, parent: tk.Widget):
        """Crée la section moderne de chargement des données avec cartes."""
        from ui.styles import create_sofrecom_card

        # Conteneur principal
        section_container = tk.Frame(parent, bg=COLORS['BG'])
        section_container.pack(fill=tk.X, pady=(0, 20))

        # Titre de section
        section_title = tk.Label(
            section_container,
            text="📁 Chargement des Données",
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        section_title.pack(anchor=tk.W, padx=5, pady=(0, 10))

        # Grille pour les cartes de fichiers
        files_grid = tk.Frame(section_container, bg=COLORS['BG'])
        files_grid.pack(fill=tk.X, padx=5)
        files_grid.grid_columnconfigure(0, weight=1)
        files_grid.grid_columnconfigure(1, weight=1)

        # Carte 1: Fichier QGis
        self._create_qgis_file_card(files_grid)

        # Carte 2: Fichier Suivi
        self._create_suivi_file_card(files_grid)

    def _create_quick_status_indicators(self, parent: tk.Widget):
        """Crée les indicateurs de statut rapide."""
        try:
            indicators_frame = tk.Frame(parent, bg=COLORS['BG'])
            indicators_frame.pack(fill=tk.X, padx=5, pady=(10, 0))

            # Grille pour les indicateurs
            indicators_frame.grid_columnconfigure(0, weight=1)
            indicators_frame.grid_columnconfigure(1, weight=1)
            indicators_frame.grid_columnconfigure(2, weight=1)

            # Indicateur 1: Fichiers chargés
            self.files_indicator = self._create_status_card(
                indicators_frame, 0, 0, "📁", "Fichiers", "En attente", COLORS['INFO']
            )

            # Indicateur 2: Analyse
            self.analysis_indicator = self._create_status_card(
                indicators_frame, 0, 1, "🔍", "Analyse", "Non effectuée", COLORS['TEXT_SECONDARY']
            )

            # Indicateur 3: Rapport
            self.report_indicator = self._create_status_card(
                indicators_frame, 0, 2, "📊", "Rapport", "Non généré", COLORS['TEXT_SECONDARY']
            )
        except Exception as e:
            self.logger.warning(f"Could not create status indicators: {e}")
            # Create dummy indicators to avoid errors
            self.files_indicator = tk.Frame(parent)
            self.analysis_indicator = tk.Frame(parent)
            self.report_indicator = tk.Frame(parent)

    def _create_status_card(self, parent: tk.Widget, row: int, col: int,
                           icon: str, title: str, status: str, color: str) -> tk.Frame:
        """Crée une carte d'indicateur de statut."""
        card_frame = tk.Frame(parent, bg=COLORS['CARD'], relief='flat', bd=1)
        card_frame.grid(row=row, column=col, sticky="ew", padx=3, pady=3)
        card_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Contenu de la carte
        content = tk.Frame(card_frame, bg=COLORS['CARD'])
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # Icône et titre
        header = tk.Frame(content, bg=COLORS['CARD'])
        header.pack(fill=tk.X)

        icon_label = tk.Label(header, text=icon, font=("Segoe UI", 12),
                             fg=color, bg=COLORS['CARD'])
        icon_label.pack(side=tk.LEFT)

        title_label = tk.Label(header, text=title, font=UIConfig.FONT_SUBTITLE,
                              fg=COLORS['TEXT_PRIMARY'], bg=COLORS['CARD'])
        title_label.pack(side=tk.LEFT, padx=(5, 0))

        # Statut
        status_label = tk.Label(content, text=status, font=UIConfig.FONT_SMALL,
                               fg=color, bg=COLORS['CARD'])
        status_label.pack(anchor=tk.W, pady=(2, 0))

        # Stocker les labels pour mise à jour
        card_frame.icon_label = icon_label
        card_frame.status_label = status_label

        return card_frame

    def _create_qgis_file_card(self, parent: tk.Widget):
        """Crée la carte pour le fichier QGis."""
        from ui.styles import create_card_frame

        # Carte QGis
        qgis_card = create_card_frame(parent, shadow=True)
        qgis_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Contenu de la carte
        card_content = qgis_card.winfo_children()[0] if qgis_card.winfo_children() else qgis_card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # En-tête avec icône
        header_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            header_frame,
            text="🗺️",
            font=("Segoe UI", 16),
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text="Fichier Résultats QGis",
            font=UIConfig.FONT_CARD_TITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Description
        desc_label = tk.Label(
            content_frame,
            text="Fichier Excel contenant les résultats d'analyse QGis\n(Colonnes A-J requises)",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD'],
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, pady=(0, 15))

        # Bouton d'import moderne
        from tkinter import ttk
        self.load_qgis_button = ttk.Button(
            content_frame,
            text="📂 Importer Fichier QGis",
            command=self._load_qgis_file,
            style='Primary.TButton'
        )
        self.load_qgis_button.pack(anchor=tk.W, pady=(0, 10))

        # Statut du fichier
        self.qgis_info_label = tk.Label(
            content_frame,
            text="❌ Aucun fichier QGis chargé",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD']
        )
        self.qgis_info_label.pack(anchor=tk.W)

    def _create_suivi_file_card(self, parent: tk.Widget):
        """Crée la carte pour le fichier Suivi."""
        from ui.styles import create_card_frame

        # Carte Suivi
        suivi_card = create_card_frame(parent, shadow=True)
        suivi_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Contenu de la carte
        card_content = suivi_card.winfo_children()[0] if suivi_card.winfo_children() else suivi_card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # En-tête avec icône
        header_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            header_frame,
            text="📋",
            font=("Segoe UI", 16),
            fg=COLORS['SUCCESS'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text="Fichier Suivi Commune",
            font=UIConfig.FONT_CARD_TITLE,
            fg=COLORS['SUCCESS'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Description
        desc_label = tk.Label(
            content_frame,
            text="Fichier de suivi commune Teams\n(Feuille 3 utilisée pour l'analyse)",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD'],
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, pady=(0, 15))

        # Bouton d'import moderne
        from tkinter import ttk
        self.load_suivi_button = ttk.Button(
            content_frame,
            text="📂 Importer Fichier Suivi",
            command=self._load_suivi_file,
            style='Success.TButton'
        )
        self.load_suivi_button.pack(anchor=tk.W, pady=(0, 10))

        # Statut du fichier
        self.suivi_info_label = tk.Label(
            content_frame,
            text="❌ Aucun fichier suivi chargé",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD']
        )
        self.suivi_info_label.pack(anchor=tk.W)
    
    def _create_modern_info_section(self, parent: tk.Widget):
        """Crée la section moderne d'informations détectées."""
        from ui.styles import create_card_frame

        # Conteneur principal
        section_container = tk.Frame(parent, bg=COLORS['BG'])
        section_container.pack(fill=tk.X, pady=(0, 20))

        # Titre de section
        section_title = tk.Label(
            section_container,
            text="📋 Informations Détectées Automatiquement",
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        section_title.pack(anchor=tk.W, padx=5, pady=(0, 10))

        # Carte d'informations
        info_card = create_card_frame(section_container, shadow=True)
        info_card.pack(fill=tk.X, padx=5, pady=5)

        # Contenu de la carte
        card_content = info_card.winfo_children()[0] if info_card.winfo_children() else info_card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Grille pour les informations
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # Informations détectées
        self._create_info_field(content_frame, 0, 0, "👤", "Collaborateur", self.collaborator_var)
        self._create_info_field(content_frame, 0, 1, "🏘️", "Commune", self.commune_var)
        self._create_info_field(content_frame, 1, 0, "🏛️", "Code INSEE", self.insee_var)
        self._create_info_field(content_frame, 1, 1, "🆔", "ID Tâche", self.id_tache_var)

        # Note explicative
        note_label = tk.Label(
            content_frame,
            text="ℹ️ Ces informations sont extraites automatiquement du fichier de suivi commune",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['CARD']
        )
        note_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(15, 0))

    def _create_info_field(self, parent: tk.Widget, row: int, col: int,
                          icon: str, label: str, var: tk.StringVar):
        """Crée un champ d'information moderne."""
        field_frame = tk.Frame(parent, bg=COLORS['CARD'])
        field_frame.grid(row=row, column=col, sticky="ew", padx=10, pady=8)

        # En-tête avec icône
        header_frame = tk.Frame(field_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X)

        icon_label = tk.Label(
            header_frame,
            text=icon,
            font=("Segoe UI", 12),
            fg=COLORS['SECONDARY'],
            bg=COLORS['CARD']
        )
        icon_label.pack(side=tk.LEFT)

        label_text = tk.Label(
            header_frame,
            text=label,
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['TEXT_PRIMARY'],
            bg=COLORS['CARD']
        )
        label_text.pack(side=tk.LEFT, padx=(5, 0))

        # Valeur détectée
        value_label = tk.Label(
            field_frame,
            textvariable=var,
            font=UIConfig.FONT_SMALL,
            fg=COLORS['INFO'],
            bg=COLORS['CARD'],
            anchor='w'
        )
        value_label.pack(fill=tk.X, pady=(3, 0))

        # Stocker pour mise à jour
        if not hasattr(self, 'info_displays'):
            self.info_displays = {}
        self.info_displays[label.lower()] = value_label

    def _create_modern_analysis_section(self, parent: tk.Widget):
        """Crée la section moderne d'analyse et résultats."""
        from ui.styles import create_card_frame

        # Conteneur principal
        section_container = tk.Frame(parent, bg=COLORS['BG'])
        section_container.pack(fill=tk.X, pady=(0, 20))

        # Titre de section
        section_title = tk.Label(
            section_container,
            text="🔍 Analyse de Contrôle Qualité",
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        section_title.pack(anchor=tk.W, padx=5, pady=(0, 10))

        # Carte d'analyse
        analysis_card = create_card_frame(section_container, shadow=True)
        analysis_card.pack(fill=tk.X, padx=5, pady=5)

        # Contenu de la carte
        card_content = analysis_card.winfo_children()[0] if analysis_card.winfo_children() else analysis_card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Description des critères
        criteria_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        criteria_frame.pack(fill=tk.X, pady=(0, 15))

        criteria_title = tk.Label(
            criteria_frame,
            text="Critères d'Analyse",
            font=UIConfig.FONT_CARD_TITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        criteria_title.pack(anchor=tk.W, pady=(0, 8))

        # Critère 0
        self._create_criteria_info(criteria_frame, "0", "Écart Plan Adressage",
                                  "Compare les motifs spécifiques: AD RAS, OK, NOK, UPR RAS, UPR OK, UPR NOK, Hors Commune")

        # Critère 2
        self._create_criteria_info(criteria_frame, "2", "Oubli Ticket UPR et 501/511",
                                  "Vérifie si les tickets UPR et 501/511 ont été déposés selon les motifs")

        # Critère 3
        self._create_criteria_info(criteria_frame, "3", "Contrôle IMB Doublons",
                                  "Détecte les doublons IMB suspects avec motifs identiques et adresses BAN différentes")

        # Critère 4
        self._create_criteria_info(criteria_frame, "4", "Détection AD à Analyser",
                                  "Détecte les motifs 'ad à analyser' avec IMB présent pour analyse approfondie")

        # Critère 5
        self._create_criteria_info(criteria_frame, "5", "Motif Incorrect",
                                  "Détecte les motifs non conformes (différents des 7 motifs autorisés)")

        # Bouton d'analyse moderne
        button_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        button_frame.pack(fill=tk.X, pady=(15, 0))

        from tkinter import ttk
        self.analyze_button = ttk.Button(
            button_frame,
            text="🔍 Lancer Analyse Qualité",
            command=self._run_quality_analysis,
            style='CompactWarning.TButton',
            state='disabled'
        )
        self.analyze_button.pack(side=tk.LEFT)

        # Bouton d'export
        self.export_button = ttk.Button(
            button_frame,
            text="📤 Exporter Rapport",
            command=self._export_qc_report,
            style='Compact.TButton',
            state='disabled'
        )
        self.export_button.pack(side=tk.LEFT, padx=(10, 0))

        # Zone de résultats
        self._create_results_display(content_frame)

    def _create_criteria_info(self, parent: tk.Widget, number: str, title: str, description: str):
        """Crée l'affichage d'un critère d'analyse."""
        criteria_frame = tk.Frame(parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        criteria_frame.pack(fill=tk.X, pady=3)
        criteria_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        content = tk.Frame(criteria_frame, bg=COLORS['LIGHT'])
        content.pack(fill=tk.X, padx=10, pady=8)

        # En-tête
        header = tk.Frame(content, bg=COLORS['LIGHT'])
        header.pack(fill=tk.X)

        # Badge du critère
        badge = tk.Label(
            header,
            text=f"CRITÈRE {number}",
            font=("Segoe UI", 8, "bold"),
            fg='white',
            bg=COLORS['SECONDARY'],
            padx=6,
            pady=2
        )
        badge.pack(side=tk.LEFT)

        # Titre
        title_label = tk.Label(
            header,
            text=title,
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['TEXT_PRIMARY'],
            bg=COLORS['LIGHT']
        )
        title_label.pack(side=tk.LEFT, padx=(8, 0))

        # Description
        desc_label = tk.Label(
            content,
            text=description,
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['LIGHT']
        )
        desc_label.pack(anchor=tk.W, pady=(5, 0))

    def _create_results_display(self, parent: tk.Widget):
        """Crée la zone d'affichage des résultats."""
        # Séparateur
        separator = tk.Frame(parent, height=1, bg=COLORS['BORDER'])
        separator.pack(fill=tk.X, pady=(20, 15))

        # Titre des résultats
        results_title = tk.Label(
            parent,
            text="📊 Résultats de l'Analyse",
            font=UIConfig.FONT_CARD_TITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        results_title.pack(anchor=tk.W, pady=(0, 10))

        # Zone de résultats (sera remplie après analyse)
        self.results_frame = tk.Frame(parent, bg=COLORS['CARD'])
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # Message initial
        self.results_label = tk.Label(
            self.results_frame,
            text="⏳ Aucune analyse effectuée\n\nChargez les fichiers requis et cliquez sur 'Lancer Analyse Qualité'",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['CARD'],
            justify=tk.CENTER
        )
        self.results_label.pack(expand=True, pady=20)

    def _create_modern_status_section(self, parent: tk.Widget):
        """Crée la section moderne de statut et progression."""
        try:
            from ui.styles import create_status_indicator

            # Conteneur de statut
            status_container = tk.Frame(parent, bg=COLORS['BG'])
            status_container.pack(fill=tk.X, pady=(10, 0))

            # Carte de statut
            status_card = tk.Frame(status_container, bg=COLORS['LIGHT'], relief='flat', bd=1)
            status_card.pack(fill=tk.X, padx=5, pady=5)
            status_card.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

            # Contenu de la carte de statut
            status_content = tk.Frame(status_card, bg=COLORS['LIGHT'])
            status_content.pack(fill=tk.X, padx=15, pady=10)

            # Barre de progression moderne
            from tkinter import ttk
            self.progress_var = tk.DoubleVar()

            progress_frame = tk.Frame(status_content, bg=COLORS['LIGHT'])
            progress_frame.pack(fill=tk.X, pady=(0, 8))

            progress_label = tk.Label(
                progress_frame,
                text="Progression:",
                font=UIConfig.FONT_SMALL,
                fg=COLORS['TEXT_PRIMARY'],
                bg=COLORS['LIGHT']
            )
            progress_label.pack(side=tk.LEFT)

            self.progress_bar = ttk.Progressbar(
                progress_frame,
                variable=self.progress_var,
                maximum=100,
                length=300
            )
            self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))

            # Indicateur de statut moderne
            self.status_icon, self.status_label = create_status_indicator(status_content, COLORS['LIGHT'])

            # Initialiser le statut
            self._update_status("waiting", "Prêt - En attente des fichiers")

        except Exception as e:
            self.logger.warning(f"Fallback to basic status section: {e}")
            # Fallback to basic status section
            status_frame = tk.Frame(parent, bg=COLORS['CARD'])
            status_frame.pack(fill=tk.X, pady=(10, 0))

            # Barre de progression
            self.progress_var = tk.DoubleVar()
            self.progress_bar = ttk.Progressbar(
                status_frame,
                variable=self.progress_var,
                maximum=100,
                length=400
            )
            self.progress_bar.pack(pady=(0, 5))

            # Label de statut
            self.status_label = tk.Label(
                status_frame,
                text="Prêt - En attente des fichiers",
                font=("Segoe UI", 9),
                fg=COLORS['TEXT_SECONDARY'],
                bg=COLORS['CARD']
            )
            self.status_label.pack()

            # Créer un status_icon factice pour éviter les erreurs
            self.status_icon = self.status_label
    
    def _update_status(self, status_type: str, message: str):
        """Met à jour l'indicateur de statut moderne."""
        try:
            from ui.styles import update_status_indicator
            if hasattr(self, 'status_icon') and hasattr(self, 'status_label'):
                update_status_indicator(self.status_icon, self.status_label, status_type, message)
        except Exception as e:
            # Fallback to basic status update
            if hasattr(self, 'status_label'):
                self.status_label.config(text=message)
            self.logger.debug(f"Status update fallback: {e}")

    def _update_file_indicators(self):
        """Met à jour les indicateurs de fichiers."""
        qgis_loaded = self.qgis_data is not None
        suivi_loaded = self.suivi_data is not None

        if hasattr(self, 'files_status'):
            if qgis_loaded and suivi_loaded:
                self.files_status.config(text="📁 Fichiers: ✅ Tous chargés", fg=COLORS['SUCCESS'])
            elif qgis_loaded or suivi_loaded:
                self.files_status.config(text="📁 Fichiers: ⚠️ Partiels", fg=COLORS['WARNING'])
            else:
                self.files_status.config(text="📁 Fichiers: En attente", fg=COLORS['INFO'])

    def _update_status_card(self, card: tk.Frame, icon: str, title: str, status: str, color: str):
        """Met à jour une carte d'indicateur de statut."""
        if hasattr(card, 'icon_label') and hasattr(card, 'status_label'):
            card.icon_label.config(text=icon, fg=color)
            card.status_label.config(text=status, fg=color)
    
    def _load_qgis_file(self):
        """Charge un fichier résultats QGis pour analyse."""
        try:
            # Ouvrir dialogue de sélection de fichier
            file_path = filedialog.askopenfilename(
                title="Sélectionner le fichier Résultats QGis",
                filetypes=[
                    ("Fichiers Excel", "*.xlsx *.xls"),
                    ("Tous les fichiers", "*.*")
                ]
            )

            if not file_path:
                return

            self._update_status("waiting", "Chargement du fichier QGis...")
            self.progress_var.set(10)

            def load_qgis():
                pd = get_pandas()

                # Lire le fichier Excel
                df = pd.read_excel(file_path, date_format=None)

                # Vérifier les colonnes requises
                required_columns = ['A', 'J']  # num dossier site, import fantome
                if len(df.columns) < 10:  # Au moins 10 colonnes (A-J)
                    raise ValueError("Le fichier ne contient pas assez de colonnes (minimum A-J requis)")

                return df

            def on_success(df):
                self.qgis_data = df
                self.current_qgis_file_path = file_path
                filename = os.path.basename(file_path)
                self.qgis_info_label.config(
                    text=f"✅ {filename} ({len(df)} lignes)",
                    fg=COLORS['SUCCESS']
                )
                self._update_status("success", "Fichier QGis chargé avec succès")
                self.progress_var.set(0)
                self._update_file_indicators()
                self._check_analysis_ready()
                self.logger.info(f"Fichier QGis chargé: {filename}")

            def on_error(error):
                self.qgis_info_label.config(
                    text="❌ Erreur de chargement",
                    fg=COLORS['ERROR']
                )
                self._update_status("error", "Erreur lors du chargement QGis")
                self.progress_var.set(0)
                self._update_file_indicators()
                messagebox.showerror("Erreur", f"Impossible de charger le fichier QGis:\n{error}")
                self.logger.error(f"Erreur chargement QGis: {error}")

            # Charger de manière asynchrone
            run_async_task(load_qgis, on_success, on_error, "Chargement QGis")

        except Exception as e:
            self.logger.error(f"Erreur lors de la sélection du fichier QGis: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la sélection du fichier:\n{e}")

    def _load_suivi_file(self):
        """Charge le fichier de suivi commune et détecte automatiquement les informations."""
        try:
            # Ouvrir dialogue de sélection de fichier
            file_path = filedialog.askopenfilename(
                title="Sélectionner le fichier Suivi Commune",
                filetypes=[
                    ("Fichiers Excel", "*.xlsx *.xls"),
                    ("Tous les fichiers", "*.*")
                ]
            )

            if not file_path:
                return

            self._update_status("waiting", "Chargement du fichier suivi...")
            self.progress_var.set(10)

            def load_suivi():
                pd = get_pandas()

                # Lire la feuille 3 (index 2) du fichier de suivi
                df = pd.read_excel(file_path, sheet_name=2, date_format=None)

                # Détecter automatiquement les informations
                detected_info = self._detect_info_from_suivi(df, file_path)

                return df, detected_info

            def on_success(result):
                df, detected_info = result
                self.suivi_data = df
                self.current_suivi_file_path = file_path
                self.detected_info = detected_info

                # Mettre à jour l'affichage des informations détectées
                self.collaborator_var.set(detected_info.get('collaborateur', 'Non détecté'))
                self.commune_var.set(detected_info.get('commune', 'Non détecté'))
                self.insee_var.set(detected_info.get('insee', 'Non détecté'))
                self.id_tache_var.set(detected_info.get('id_tache', 'Non détecté'))

                filename = os.path.basename(file_path)
                self.suivi_info_label.config(
                    text=f"✅ {filename} ({len(df)} lignes)",
                    fg=COLORS['SUCCESS']
                )
                self._update_status("success", "Fichier suivi chargé avec succès")
                self.progress_var.set(0)
                self._update_file_indicators()
                self._check_analysis_ready()
                self.logger.info(f"Fichier suivi chargé: {filename}")
                self.logger.info(f"Informations détectées: {detected_info}")

            def on_error(error):
                self.suivi_info_label.config(
                    text="❌ Erreur de chargement",
                    fg=COLORS['ERROR']
                )
                self._update_status("error", "Erreur lors du chargement suivi")
                self.progress_var.set(0)
                self._update_file_indicators()
                messagebox.showerror("Erreur", f"Impossible de charger le fichier suivi:\n{error}")
                self.logger.error(f"Erreur chargement suivi: {error}")

            # Charger de manière asynchrone
            run_async_task(load_suivi, on_success, on_error, "Chargement suivi")

        except Exception as e:
            self.logger.error(f"Erreur lors de la sélection du fichier suivi: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la sélection du fichier:\n{e}")

    def _detect_info_from_suivi(self, df, file_path: str) -> Dict[str, str]:
        """Détecte automatiquement les informations depuis le fichier de suivi."""
        try:
            pd = get_pandas()
            detected = {}

            # 1. Détecter le nom de la commune depuis la colonne A (index 0) - Page 3
            if len(df.columns) >= 1:
                commune_column = df.iloc[:, 0]  # Colonne A
                # Chercher le premier nom de commune non vide
                for commune in commune_column:
                    if pd.notna(commune) and str(commune).strip() and str(commune).strip() not in ['Commune', 'Nom commune']:
                        detected['commune'] = str(commune).strip()
                        break

            # 2. Détecter le collaborateur depuis la colonne U (index 20) - Page 3
            if len(df.columns) >= 21:
                collab_column = df.iloc[:, 20]  # Colonne U
                # Chercher le premier collaborateur non vide
                for collab in collab_column:
                    if pd.notna(collab) and str(collab).strip() and str(collab).strip() != 'Collaborateur U':
                        detected['collaborateur'] = str(collab).strip()
                        break

            # 3. Détecter l'INSEE depuis la colonne C (index 2) - Page 3
            if len(df.columns) >= 3:
                insee_column = df.iloc[:, 2]  # Colonne C
                # Chercher le premier code INSEE valide (5 chiffres)
                for insee in insee_column:
                    if pd.notna(insee):
                        insee_str = str(insee).strip()
                        # Vérifier si c'est un code INSEE (5 chiffres)
                        if insee_str.isdigit() and len(insee_str) == 5:
                            detected['insee'] = insee_str
                            break

            # 4. Détecter l'ID Tâche depuis la colonne B (index 1) - Page 3
            if len(df.columns) >= 2:
                id_tache_column = df.iloc[:, 1]  # Colonne B
                # Chercher le premier ID tâche valide
                for id_tache in id_tache_column:
                    if pd.notna(id_tache):
                        id_tache_str = str(id_tache).strip()
                        # Vérifier si c'est un ID tâche valide (numérique, pas l'en-tête)
                        if id_tache_str.isdigit() and len(id_tache_str) >= 3 and id_tache_str != 'ID Tache':
                            detected['id_tache'] = id_tache_str
                            break

            # 5. Détecter le domaine depuis la colonne D (index 3) - Page 3
            if len(df.columns) >= 4 and len(df) > 0:
                # Essayer ligne 1 d'abord (index 0)
                if pd.notna(df.iloc[0, 3]):
                    domaine_val = str(df.iloc[0, 3]).strip()
                    if domaine_val not in ['Domaine', 'Domain', 'nan', ''] and len(domaine_val) > 1:
                        detected['domaine'] = domaine_val
                        self.logger.info(f"Domaine détecté ligne 1: {domaine_val}")

                # Si pas trouvé, essayer ligne 2 (index 1)
                if 'domaine' not in detected and len(df) > 1:
                    if pd.notna(df.iloc[1, 3]):
                        domaine_val = str(df.iloc[1, 3]).strip()
                        if domaine_val not in ['Domaine', 'Domain', 'nan', ''] and len(domaine_val) > 1:
                            detected['domaine'] = domaine_val
                            self.logger.info(f"Domaine détecté ligne 2: {domaine_val}")

                # Si pas trouvé, essayer ligne 3 (index 2)
                if 'domaine' not in detected and len(df) > 2:
                    if pd.notna(df.iloc[2, 3]):
                        domaine_val = str(df.iloc[2, 3]).strip()
                        if domaine_val not in ['Domaine', 'Domain', 'nan', ''] and len(domaine_val) > 1:
                            detected['domaine'] = domaine_val
                            self.logger.info(f"Domaine détecté ligne 3: {domaine_val}")

                # Si pas trouvé, chercher dans toutes les lignes
                if 'domaine' not in detected:
                    domaine_column = df.iloc[:, 3]  # Colonne D
                    for i, domaine in enumerate(domaine_column):
                        if pd.notna(domaine) and str(domaine).strip():
                            domaine_val = str(domaine).strip()
                            if domaine_val not in ['Domaine', 'Domain', 'nan', ''] and len(domaine_val) > 1:
                                detected['domaine'] = domaine_val
                                self.logger.info(f"Domaine détecté ligne {i+1}: {domaine_val}")
                                break

            # 6. Détecter Nbr voies CMS Total depuis la colonne G (index 6) - Page 3
            if len(df.columns) >= 7 and len(df) > 0:
                # Essayer ligne 1 d'abord (index 0)
                if pd.notna(df.iloc[0, 6]):
                    cms_str = str(df.iloc[0, 6]).strip()
                    try:
                        cms_num = float(cms_str)
                        if cms_num >= 0 and cms_str not in ['CMS', 'Total', 'Nbr', '0.0']:
                            # Correction pour les erreurs de précision flottante
                            if abs(cms_num - round(cms_num)) < 1e-10:
                                detected['cms_total'] = str(int(round(cms_num)))
                            else:
                                detected['cms_total'] = cms_str
                            self.logger.info(f"CMS Total détecté ligne 1: {detected['cms_total']}")
                    except ValueError:
                        pass

                # Si pas trouvé, essayer ligne 2 (index 1)
                if 'cms_total' not in detected and len(df) > 1:
                    if pd.notna(df.iloc[1, 6]):
                        cms_str = str(df.iloc[1, 6]).strip()
                        try:
                            cms_num = float(cms_str)
                            if cms_num >= 0 and cms_str not in ['CMS', 'Total', 'Nbr', '0.0']:
                                # Correction pour les erreurs de précision flottante
                                if abs(cms_num - round(cms_num)) < 1e-10:
                                    detected['cms_total'] = str(int(round(cms_num)))
                                else:
                                    detected['cms_total'] = cms_str
                                self.logger.info(f"CMS Total détecté ligne 2: {detected['cms_total']}")
                        except ValueError:
                            pass

                # Si pas trouvé, essayer ligne 3 (index 2)
                if 'cms_total' not in detected and len(df) > 2:
                    if pd.notna(df.iloc[2, 6]):
                        cms_str = str(df.iloc[2, 6]).strip()
                        try:
                            cms_num = float(cms_str)
                            if cms_num >= 0 and cms_str not in ['CMS', 'Total', 'Nbr', '0.0']:
                                # Correction pour les erreurs de précision flottante
                                if abs(cms_num - round(cms_num)) < 1e-10:
                                    detected['cms_total'] = str(int(round(cms_num)))
                                else:
                                    detected['cms_total'] = cms_str
                                self.logger.info(f"CMS Total détecté ligne 3: {detected['cms_total']}")
                        except ValueError:
                            pass

                # Si pas trouvé, chercher dans toutes les lignes
                if 'cms_total' not in detected:
                    cms_column = df.iloc[:, 6]  # Colonne G
                    for i, cms in enumerate(cms_column):
                        if pd.notna(cms):
                            cms_str = str(cms).strip()
                            try:
                                cms_num = float(cms_str)
                                if cms_num >= 0 and cms_str not in ['CMS', 'Total', 'Nbr', '0.0']:
                                    # Correction pour les erreurs de précision flottante
                                    if abs(cms_num - round(cms_num)) < 1e-10:
                                        detected['cms_total'] = str(int(round(cms_num)))
                                    else:
                                        detected['cms_total'] = cms_str
                                    self.logger.info(f"CMS Total détecté ligne {i+1}: {detected['cms_total']}")
                                    break
                            except ValueError:
                                continue

            # 7. Détecter Nbr IMB PA Total depuis la colonne H (index 7) - Page 3
            if len(df.columns) >= 8 and len(df) > 0:
                # Essayer ligne 1 d'abord (index 0)
                if pd.notna(df.iloc[0, 7]):
                    pa_str = str(df.iloc[0, 7]).strip()
                    try:
                        pa_num = float(pa_str)
                        if pa_num >= 0 and pa_str not in ['PA', 'Total', 'Nbr', '0.0']:
                            # Correction pour les erreurs de précision flottante
                            # Arrondir à l'entier le plus proche si très proche d'un entier
                            if abs(pa_num - round(pa_num)) < 1e-10:
                                detected['pa_total'] = str(int(round(pa_num)))
                            else:
                                detected['pa_total'] = pa_str
                            self.logger.info(f"PA Total détecté ligne 1: {detected['pa_total']}")
                    except ValueError:
                        pass

                # Si pas trouvé, essayer ligne 2 (index 1)
                if 'pa_total' not in detected and len(df) > 1:
                    if pd.notna(df.iloc[1, 7]):
                        pa_str = str(df.iloc[1, 7]).strip()
                        try:
                            pa_num = float(pa_str)
                            if pa_num >= 0 and pa_str not in ['PA', 'Total', 'Nbr', '0.0']:
                                # Correction pour les erreurs de précision flottante
                                # Arrondir à l'entier le plus proche si très proche d'un entier
                                if abs(pa_num - round(pa_num)) < 1e-10:
                                    detected['pa_total'] = str(int(round(pa_num)))
                                else:
                                    detected['pa_total'] = pa_str
                                self.logger.info(f"PA Total détecté ligne 2: {detected['pa_total']}")
                        except ValueError:
                            pass

                # Si pas trouvé, essayer ligne 3 (index 2)
                if 'pa_total' not in detected and len(df) > 2:
                    if pd.notna(df.iloc[2, 7]):
                        pa_str = str(df.iloc[2, 7]).strip()
                        try:
                            pa_num = float(pa_str)
                            if pa_num >= 0 and pa_str not in ['PA', 'Total', 'Nbr', '0.0']:
                                # Correction pour les erreurs de précision flottante
                                # Arrondir à l'entier le plus proche si très proche d'un entier
                                if abs(pa_num - round(pa_num)) < 1e-10:
                                    detected['pa_total'] = str(int(round(pa_num)))
                                else:
                                    detected['pa_total'] = pa_str
                                self.logger.info(f"PA Total détecté ligne 3: {detected['pa_total']}")
                        except ValueError:
                            pass

                # Si pas trouvé, chercher dans toutes les lignes
                if 'pa_total' not in detected:
                    pa_column = df.iloc[:, 7]  # Colonne H
                    for i, pa in enumerate(pa_column):
                        if pd.notna(pa):
                            pa_str = str(pa).strip()
                            try:
                                pa_num = float(pa_str)
                                if pa_num >= 0 and pa_str not in ['PA', 'Total', 'Nbr', '0.0']:
                                    # Correction pour les erreurs de précision flottante
                                    # Arrondir à l'entier le plus proche si très proche d'un entier
                                    if abs(pa_num - round(pa_num)) < 1e-10:
                                        detected['pa_total'] = str(int(round(pa_num)))
                                    else:
                                        detected['pa_total'] = pa_str
                                    self.logger.info(f"PA Total détecté ligne {i+1}: {detected['pa_total']}")
                                    break
                            except ValueError:
                                continue

            # 8. Détecter le collaborateur depuis la colonne U (index 20) - Page 3
            if len(df.columns) >= 21 and len(df) > 0:
                # Essayer ligne 1 d'abord (index 0)
                if pd.notna(df.iloc[0, 20]):
                    collab_val = str(df.iloc[0, 20]).strip()
                    if collab_val not in ['Collaborateur', 'Affectation', 'nan', ''] and len(collab_val) > 1:
                        detected['collaborateur'] = collab_val
                        self.logger.info(f"Collaborateur détecté ligne 1: {collab_val}")

                # Si pas trouvé, essayer ligne 2 (index 1)
                if 'collaborateur' not in detected and len(df) > 1:
                    if pd.notna(df.iloc[1, 20]):
                        collab_val = str(df.iloc[1, 20]).strip()
                        if collab_val not in ['Collaborateur', 'Affectation', 'nan', ''] and len(collab_val) > 1:
                            detected['collaborateur'] = collab_val
                            self.logger.info(f"Collaborateur détecté ligne 2: {collab_val}")

                # Si pas trouvé, essayer ligne 3 (index 2)
                if 'collaborateur' not in detected and len(df) > 2:
                    if pd.notna(df.iloc[2, 20]):
                        collab_val = str(df.iloc[2, 20]).strip()
                        if collab_val not in ['Collaborateur', 'Affectation', 'nan', ''] and len(collab_val) > 1:
                            detected['collaborateur'] = collab_val
                            self.logger.info(f"Collaborateur détecté ligne 3: {collab_val}")

                # Si pas trouvé, chercher dans toutes les lignes
                if 'collaborateur' not in detected:
                    collab_column = df.iloc[:, 20]  # Colonne U
                    for i, collab in enumerate(collab_column):
                        if pd.notna(collab) and str(collab).strip():
                            collab_val = str(collab).strip()
                            if collab_val not in ['Collaborateur', 'Affectation', 'nan', ''] and len(collab_val) > 1:
                                detected['collaborateur'] = collab_val
                                self.logger.info(f"Collaborateur détecté ligne {i+1}: {collab_val}")
                                break

            # 9. Valeurs par défaut si non détectées
            if 'commune' not in detected:
                detected['commune'] = 'Non détecté'
            if 'collaborateur' not in detected:
                detected['collaborateur'] = 'Non détecté'
            if 'insee' not in detected:
                detected['insee'] = 'Non détecté'
            if 'id_tache' not in detected:
                detected['id_tache'] = 'Non détecté'
            if 'domaine' not in detected:
                detected['domaine'] = ''
            if 'cms_total' not in detected:
                detected['cms_total'] = ''
            if 'pa_total' not in detected:
                detected['pa_total'] = ''

            # Log des informations détectées pour vérification
            self.logger.info("=== INFORMATIONS DÉTECTÉES ===")
            self.logger.info(f"Nom de commune (Col A): {detected.get('commune', 'N/A')}")
            self.logger.info(f"ID tâche (Col B): {detected.get('id_tache', 'N/A')}")
            self.logger.info(f"Code INSEE (Col C): {detected.get('insee', 'N/A')}")
            self.logger.info(f"Domaine (Col D): {detected.get('domaine', 'N/A')}")
            self.logger.info(f"Collaborateur (Col U): {detected.get('collaborateur', 'N/A')}")
            self.logger.info(f"CMS Total (Col G): {detected.get('cms_total', 'N/A')}")
            self.logger.info(f"PA Total (Col H): {detected.get('pa_total', 'N/A')}")
            self.logger.info("==============================")



            # Log détaillé des colonnes pour debug si des valeurs sont manquantes
            if not detected.get('domaine') or not detected.get('cms_total') or not detected.get('pa_total'):
                self.logger.info("=== DEBUG COLONNES MANQUANTES ===")
                if len(df.columns) >= 4:
                    self.logger.info(f"Colonne D (Domaine) - premières valeurs: {df.iloc[:5, 3].tolist()}")
                if len(df.columns) >= 7:
                    self.logger.info(f"Colonne G (CMS) - premières valeurs: {df.iloc[:5, 6].tolist()}")
                if len(df.columns) >= 8:
                    self.logger.info(f"Colonne H (PA) - premières valeurs: {df.iloc[:5, 7].tolist()}")
                self.logger.info("===================================")

            # Log détaillé spécifique pour ligne 2 (index 1)
            self.logger.info("=== DEBUG LIGNE 2 (INDEX 1) ===")
            if len(df) > 1:
                if len(df.columns) >= 4:
                    self.logger.info(f"Ligne 2, Colonne D (Domaine): '{df.iloc[1, 3]}'")
                if len(df.columns) >= 7:
                    self.logger.info(f"Ligne 2, Colonne G (CMS): '{df.iloc[1, 6]}'")
                if len(df.columns) >= 8:
                    self.logger.info(f"Ligne 2, Colonne H (PA): '{df.iloc[1, 7]}'")
            self.logger.info("===============================")

            return detected

        except Exception as e:
            self.logger.error(f"Erreur détection informations: {e}")
            return {
                'commune': 'Erreur détection',
                'collaborateur': 'Erreur détection',
                'insee': 'Erreur détection',
                'id_tache': 'Erreur détection'
            }
    
    def _check_analysis_ready(self):
        """Vérifie si tous les éléments sont prêts pour lancer l'analyse."""
        ready = (
            self.qgis_data is not None and
            self.suivi_data is not None and
            self.detected_info.get('collaborateur', '') != 'Non détecté' and
            self.detected_info.get('commune', '') != 'Non détecté'
        )

        if ready:
            self.analyze_button.config(state='normal')
            self._update_status("success", "Prêt pour l'analyse qualité")
        else:
            self.analyze_button.config(state='disabled')

        return ready
    
    def _run_quality_analysis(self):
        """Lance l'analyse de contrôle qualité."""
        if not self._check_analysis_ready():
            messagebox.showwarning("Attention", "Veuillez charger tous les fichiers requis avant de lancer l'analyse.")
            return

        try:
            self._update_status("waiting", "Analyse en cours...")
            self.progress_var.set(10)

            def run_analysis():
                results = {
                    'critere_0': self._analyze_critere_0(),
                    'critere_2': self._analyze_critere_2(),
                    'critere_3': self._analyze_critere_3(),
                    'critere_4': self._analyze_critere_4(),
                    'critere_5': self._analyze_critere_5(),
                    'summary': {}
                }

                # Calculer le résumé
                results['summary'] = self._calculate_summary(results)

                return results

            def on_success(results):
                self.qc_results = results
                self._display_compact_results(results)
                self.export_button.config(state='normal')
                self._update_status("success", "Analyse terminée avec succès")

                # Mettre à jour les indicateurs de statut
                if hasattr(self, 'analysis_status'):
                    self.analysis_status.config(text="🔍 Analyse: ✅ Terminée", fg=COLORS['SUCCESS'])
                if hasattr(self, 'report_status'):
                    self.report_status.config(text="📊 Rapport: ⚠️ Prêt", fg=COLORS['WARNING'])

                self.progress_var.set(100)
                self.logger.info("Analyse qualité terminée")

            def on_error(error):
                self._update_status("error", "Erreur lors de l'analyse")
                if hasattr(self, 'analysis_status'):
                    self.analysis_status.config(text="🔍 Analyse: ❌ Erreur", fg=COLORS['ERROR'])
                self.progress_var.set(0)
                messagebox.showerror("Erreur", f"Erreur lors de l'analyse:\n{error}")
                self.logger.error(f"Erreur analyse qualité: {error}")

            # Lancer l'analyse de manière asynchrone
            run_async_task(run_analysis, on_success, on_error, "Analyse qualité")

        except Exception as e:
            self.logger.error(f"Erreur lors du lancement de l'analyse: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du lancement:\n{e}")

    def _analyze_critere_0(self) -> Dict[str, Any]:
        """
        Critère 0: Incohérence entre fichier Résultats QGis et suivi commune.
        Compare le nombre des motifs spécifiés dans les deux fichiers.
        Motifs à vérifier: AD RAS, OK, NOK, UPR RAS, UPR OK, UPR NOK, Hors Commune
        """
        try:
            pd = get_pandas()

            # Motifs spécifiques à analyser pour l'écart Plan Adressage
            motifs_plan_adressage = [
                'AD RAS', 'OK', 'NOK', 'UPR RAS', 'UPR OK', 'UPR NOK', 'HORS COMMUNE'
            ]

            # Extraire les motifs du fichier QGis (colonne J - index 9)
            qgis_motifs = []
            if len(self.qgis_data.columns) > 9:
                qgis_motifs_column = self.qgis_data.iloc[:, 9]  # Colonne J (import fantome)
                qgis_motifs = [str(motif).strip().upper() for motif in qgis_motifs_column if pd.notna(motif) and str(motif).strip()]

            # Extraire les motifs du fichier suivi commune (colonne I - index 8) depuis la PAGE 2
            suivi_motifs = []
            try:
                # Lire spécifiquement la page 2 (index 1) pour les motifs
                pd = get_pandas()
                if hasattr(self, 'current_suivi_file_path') and self.current_suivi_file_path:
                    suivi_page2_df = pd.read_excel(self.current_suivi_file_path, sheet_name=1, date_format=None)  # Page 2
                    if len(suivi_page2_df.columns) > 8:
                        suivi_motifs_column = suivi_page2_df.iloc[:, 8]  # Colonne I (Motif)
                        suivi_motifs = [str(motif).strip().upper() for motif in suivi_motifs_column if pd.notna(motif) and str(motif).strip()]
                        self.logger.info(f"Motifs extraits de la page 2, colonne I: {len(suivi_motifs)} motifs trouvés")
                else:
                    self.logger.warning("Chemin du fichier suivi non disponible, impossible de lire la page 2")
            except Exception as e:
                self.logger.error(f"Erreur lors de la lecture de la page 2 pour les motifs: {e}")
                # Fallback: essayer avec les données actuelles (page 3)
                if len(self.suivi_data.columns) > 8:
                    suivi_motifs_column = self.suivi_data.iloc[:, 8]  # Colonne I (Motif)
                    suivi_motifs = [str(motif).strip().upper() for motif in suivi_motifs_column if pd.notna(motif) and str(motif).strip()]

            # Compter les occurrences de chaque motif spécifique
            qgis_counts = {}
            suivi_counts = {}

            # Initialiser tous les motifs à 0
            for motif in motifs_plan_adressage:
                qgis_counts[motif] = 0
                suivi_counts[motif] = 0

            # Compter les motifs QGis
            for motif in qgis_motifs:
                if motif in motifs_plan_adressage:
                    qgis_counts[motif] += 1

            # Compter les motifs Suivi
            for motif in suivi_motifs:
                if motif in motifs_plan_adressage:
                    suivi_counts[motif] += 1

            # Détecter les incohérences pour les motifs Plan Adressage
            incoherences = []
            ecart_plan_adressage = {}

            for motif in motifs_plan_adressage:
                qgis_count = qgis_counts[motif]
                suivi_count = suivi_counts[motif]
                difference = qgis_count - suivi_count

                # Stocker les données pour l'écart Plan Adressage
                ecart_plan_adressage[motif] = {
                    'suivi_count': suivi_count,
                    'qgis_count': qgis_count,
                    'difference': difference,
                    'has_ecart': difference != 0
                }

                # Ajouter aux incohérences si différence détectée
                if difference != 0:
                    incoherences.append({
                        'motif': motif,
                        'qgis_count': qgis_count,
                        'suivi_count': suivi_count,
                        'difference': difference,
                        'type': 'ECART_PLAN_ADRESSAGE',
                        'description': f"Écart détecté: {suivi_count} (Suivi) vs {qgis_count} (QGis) = {difference:+d}"
                    })

            # Calculer les totaux
            total_qgis = sum(qgis_counts.values())
            total_suivi = sum(suivi_counts.values())

            return {
                'status': 'COMPLETE',
                'total_incoherences': len(incoherences),
                'incoherences': incoherences,
                'ecart_plan_adressage': ecart_plan_adressage,
                'qgis_motifs_total': total_qgis,
                'suivi_motifs_total': total_suivi,
                'qgis_counts': qgis_counts,
                'suivi_counts': suivi_counts,
                'motifs_analyses': motifs_plan_adressage
            }

        except Exception as e:
            self.logger.error(f"Erreur dans l'analyse du critère 0: {e}")
            return {
                'status': 'ERROR',
                'error': str(e),
                'total_incoherences': 0,
                'incoherences': [],
                'ecart_plan_adressage': {}
            }
    


    def _analyze_critere_2(self) -> Dict[str, Any]:
        """
        Critère 2: Oubli Ticket UPR et 501/511
        Vérifie si les collaborateurs ont déposé les tickets requis selon les motifs utilisés.

        Règles:
        1. UPR OK (page 2, col I) -> doit avoir ticket UPR (page 3, col T)
        2. Création/Modification Voie (page 1, col E) OU OK (page 2, col I) -> doit avoir ticket 501/511 (page 3, col Q)
        """
        try:
            pd = get_pandas()

            # Initialiser les résultats
            ticket_upr_status = "N/A"
            ticket_501_511_status = "N/A"
            errors = []

            # Variables pour stocker les données des différentes pages
            page1_data = None
            page2_data = None
            page3_data = self.suivi_data  # Page 3 déjà chargée

            # Lire les pages 1 et 2 du fichier suivi commune
            if hasattr(self, 'current_suivi_file_path') and self.current_suivi_file_path:
                try:
                    # Page 1 pour vérifier colonne E (Motif Voie)
                    page1_data = pd.read_excel(self.current_suivi_file_path, sheet_name=0, date_format=None)
                    # Page 2 pour vérifier colonne I (Motif) - déjà utilisée dans critère 0
                    page2_data = pd.read_excel(self.current_suivi_file_path, sheet_name=1, date_format=None)

                    self.logger.info("Pages 1, 2 et 3 du fichier suivi chargées pour analyse critère 2")

                except Exception as e:
                    self.logger.error(f"Erreur lecture pages suivi pour critère 2: {e}")
                    return {
                        'status': 'ERROR',
                        'error': f'Impossible de lire les pages du fichier suivi: {e}',
                        'ticket_upr_status': 'ERROR',
                        'ticket_501_511_status': 'ERROR',
                        'errors': []
                    }
            else:
                return {
                    'status': 'ERROR',
                    'error': 'Chemin du fichier suivi non disponible',
                    'ticket_upr_status': 'ERROR',
                    'ticket_501_511_status': 'ERROR',
                    'errors': []
                }

            # VÉRIFICATION 1: Ticket UPR
            # Si UPR OK dans page 2, colonne I -> doit avoir ID dans page 3, colonne T
            upr_ok_found = False
            if page2_data is not None and len(page2_data.columns) > 8:
                motifs_page2 = page2_data.iloc[:, 8]  # Colonne I
                for motif in motifs_page2:
                    if pd.notna(motif) and str(motif).strip().upper() == 'UPR OK':
                        upr_ok_found = True
                        break

            if upr_ok_found:
                # Vérifier si ticket UPR déposé (page 3, colonne T - index 19)
                ticket_upr_deposited = False
                if len(page3_data.columns) > 19:
                    id_upr_column = page3_data.iloc[:, 19]  # Colonne T
                    for id_upr in id_upr_column:
                        if pd.notna(id_upr) and str(id_upr).strip() and str(id_upr).strip() not in ['', 'nan', 'ID UPR', 'Ticket UPR']:
                            ticket_upr_deposited = True
                            break

                ticket_upr_status = "OK" if ticket_upr_deposited else "NOK"
                if not ticket_upr_deposited:
                    errors.append({
                        'type': 'TICKET_UPR_MANQUANT',
                        'description': 'Motif UPR OK détecté mais aucun ticket UPR déposé (colonne T vide)',
                        'page': 'Page 2 -> Page 3',
                        'colonnes': 'I -> T'
                    })
            else:
                ticket_upr_status = "N/A"  # Pas de UPR OK, donc pas de ticket requis

            # VÉRIFICATION 2: Ticket 501/511
            # Si Création/Modification Voie (page 1, col E) OU OK (page 2, col I) -> doit avoir ID dans page 3, col Q
            ticket_501_511_required = False

            # Vérifier page 1, colonne E (Motif Voie)
            if page1_data is not None and len(page1_data.columns) > 4:
                motifs_voie = page1_data.iloc[:, 4]  # Colonne E
                for motif in motifs_voie:
                    if pd.notna(motif):
                        motif_str = str(motif).strip()
                        if motif_str in ['Création Voie', 'Modification Voie']:
                            ticket_501_511_required = True
                            break

            # Vérifier page 2, colonne I (motif OK)
            if not ticket_501_511_required and page2_data is not None and len(page2_data.columns) > 8:
                motifs_page2 = page2_data.iloc[:, 8]  # Colonne I
                for motif in motifs_page2:
                    if pd.notna(motif) and str(motif).strip().upper() == 'OK':
                        ticket_501_511_required = True
                        break

            if ticket_501_511_required:
                # Vérifier si ticket 501/511 déposé (page 3, colonne Q - index 16)
                ticket_501_511_deposited = False
                if len(page3_data.columns) > 16:
                    id_501_511_column = page3_data.iloc[:, 16]  # Colonne Q
                    for id_ticket in id_501_511_column:
                        if pd.notna(id_ticket) and str(id_ticket).strip() and str(id_ticket).strip() not in ['', 'nan', 'ID 501/511', 'Ticket 501/511']:
                            ticket_501_511_deposited = True
                            break

                ticket_501_511_status = "OK" if ticket_501_511_deposited else "NOK"
                if not ticket_501_511_deposited:
                    errors.append({
                        'type': 'TICKET_501_511_MANQUANT',
                        'description': 'Motif Création/Modification Voie ou OK détecté mais aucun ticket 501/511 déposé (colonne Q vide)',
                        'page': 'Page 1/2 -> Page 3',
                        'colonnes': 'E/I -> Q'
                    })
            else:
                ticket_501_511_status = "N/A"  # Pas de motif requis, donc pas de ticket nécessaire

            return {
                'status': 'COMPLETE',
                'ticket_upr_status': ticket_upr_status,
                'ticket_501_511_status': ticket_501_511_status,
                'total_errors': len(errors),
                'errors': errors,
                'upr_ok_found': upr_ok_found,
                'ticket_501_511_required': ticket_501_511_required
            }

        except Exception as e:
            self.logger.error(f"Erreur dans l'analyse du critère 2: {e}")
            return {
                'status': 'ERROR',
                'error': str(e),
                'ticket_upr_status': 'ERROR',
                'ticket_501_511_status': 'ERROR',
                'total_errors': 0,
                'errors': []
            }

    def _analyze_critere_3(self) -> Dict[str, Any]:
        """
        Critère 3: Contrôle IMB Doublons
        Détecte les doublons suspects dans le fichier Résultats QGis en identifiant
        les codes IMB identiques ayant le même motif de traitement avec des adresses BAN différentes.

        Colonnes analysées:
        - A: Num Dossier Site (codes IMB)
        - B: Numero Voie Site
        - C: Repondant Voie Site
        - D: Libelle Voie Site
        - J: Import Fantome (motifs)
        - U: Adresse BAN
        """
        try:
            pd = get_pandas()

            # Vérifier que les colonnes requises existent
            required_columns = ['A', 'B', 'C', 'D', 'J', 'U']  # Colonnes A, B, C, D, J, U
            if len(self.qgis_data.columns) < 21:  # Au moins 21 colonnes (A-U)
                raise ValueError("Le fichier QGis ne contient pas assez de colonnes (minimum A-U requis)")

            # Extraire les données des colonnes requises
            df = self.qgis_data.copy()

            # Renommer les colonnes pour faciliter le travail
            df_work = pd.DataFrame({
                'imb_code': df.iloc[:, 0],  # Colonne A - Num Dossier Site
                'numero_voie': df.iloc[:, 1],  # Colonne B - Numero Voie Site
                'repondant_voie': df.iloc[:, 2],  # Colonne C - Repondant Voie Site
                'libelle_voie': df.iloc[:, 3],  # Colonne D - Libelle Voie Site
                'motif': df.iloc[:, 9],  # Colonne J - Import Fantome
                'adresse_ban': df.iloc[:, 20]  # Colonne U - Adresse BAN
            })

            # Nettoyer les données
            df_work = df_work.dropna(subset=['imb_code'])  # Supprimer les lignes sans code IMB
            df_work['imb_code'] = df_work['imb_code'].astype(str).str.strip()
            df_work['motif'] = df_work['motif'].astype(str).str.strip().str.upper()
            df_work['adresse_ban'] = df_work['adresse_ban'].astype(str).str.strip()

            # Construire l'adresse optimum (B + C + D) en gérant les valeurs vides
            def construct_adresse_optimum(row):
                """Construit l'adresse optimum en gérant les valeurs vides et numériques."""
                # Nettoyer et convertir les valeurs
                numero = str(row['numero_voie']).strip() if pd.notna(row['numero_voie']) else ''
                repondant = str(row['repondant_voie']).strip() if pd.notna(row['repondant_voie']) else ''
                libelle = str(row['libelle_voie']).strip() if pd.notna(row['libelle_voie']) else ''

                # Nettoyer les valeurs numériques (enlever .0)
                if numero and numero != 'nan':
                    try:
                        # Si c'est un nombre entier, enlever les décimales
                        if '.' in numero and numero.replace('.', '').replace('-', '').isdigit():
                            numero = str(int(float(numero)))
                    except:
                        pass

                # Construire l'adresse selon les règles :
                # - Si C est vide : B + D uniquement
                # - Si B ou C est vide : D uniquement
                # - Sinon : B + C + D

                parts = []

                if numero and numero != 'nan':
                    parts.append(numero)

                if repondant and repondant != 'nan':
                    parts.append(repondant)

                if libelle and libelle != 'nan':
                    parts.append(libelle)

                # Appliquer les règles spécifiques
                if not repondant or repondant == 'nan':
                    # Si C est vide : B + D uniquement (ou D si B est vide)
                    if numero and numero != 'nan' and libelle and libelle != 'nan':
                        return f"{numero} {libelle}".strip()
                    elif libelle and libelle != 'nan':
                        return libelle.strip()
                    elif numero and numero != 'nan':
                        return numero.strip()
                    else:
                        return ''
                else:
                    # Cas normal : B + C + D
                    return ' '.join(parts).strip()

            df_work['adresse_optimum'] = df_work.apply(construct_adresse_optimum, axis=1)

            # Identifier les doublons IMB
            imb_counts = df_work['imb_code'].value_counts()
            doublons_imb = imb_counts[imb_counts > 1].index.tolist()

            doublons_suspects = []
            doublons_details = []
            erreurs_motif_ok = []
            ad_a_analyser = []
            lignes_deja_ajoutees = set()  # Pour éviter les doublons

            # ÉTAPE 1: Détecter les erreurs de motif "OK" avec adresses identiques (tous les IMB)
            for index, row in df_work.iterrows():
                motif = str(row['motif']).strip().upper()
                adresse_optimum = str(row['adresse_optimum']).strip()
                adresse_ban = str(row['adresse_ban']).strip()

                # Debug: Log pour vérifier les comparaisons
                self.logger.debug(f"Vérification motif OK - IMB: {row['imb_code']}, Motif: '{motif}', Adresse Opt: '{adresse_optimum}', Adresse BAN: '{adresse_ban}'")

                # Vérifier si motif = "OK" et adresses identiques
                if (motif == 'OK' and
                    adresse_optimum and adresse_optimum != '' and adresse_optimum != 'nan' and
                    adresse_ban and adresse_ban != '' and adresse_ban != 'nan' and
                    adresse_optimum == adresse_ban):

                    # Créer une clé unique pour cette ligne
                    ligne_key = f"{row['imb_code']}_{adresse_optimum}_{adresse_ban}_{motif}"

                    if ligne_key not in lignes_deja_ajoutees:
                        erreur_info = {
                            'imb_code': row['imb_code'],
                            'adresse_optimum': adresse_optimum,
                            'motif_initial': motif,
                            'adresse_ban': adresse_ban,
                            'type': 'ERREUR_MOTIF_OK_ADRESSE_IDENTIQUE',
                            'description': f"IMB {row['imb_code']} - Motif 'OK' mais adresse optimum = adresse BAN (erreur de saisie)"
                        }
                        erreurs_motif_ok.append(erreur_info)
                        doublons_details.append(erreur_info)
                        lignes_deja_ajoutees.add(ligne_key)

                        # Log pour confirmer la détection
                        self.logger.info(f"ERREUR MOTIF OK DÉTECTÉE - IMB: {row['imb_code']}, Adresse: '{adresse_optimum}'")

            # ÉTAPE 2: Analyser chaque groupe de doublons IMB
            for imb_code in doublons_imb:
                groupe_doublons = df_work[df_work['imb_code'] == imb_code].copy()

                # Vérifier s'il y a des motifs identiques avec des adresses BAN différentes
                for motif in groupe_doublons['motif'].unique():
                    if pd.isna(motif) or motif == '' or motif.upper() == 'NAN':
                        continue

                    lignes_meme_motif = groupe_doublons[groupe_doublons['motif'] == motif]

                    if len(lignes_meme_motif) > 1:
                        # Vérifier si les adresses BAN sont différentes
                        adresses_ban_uniques = lignes_meme_motif['adresse_ban'].unique()
                        adresses_ban_uniques = [addr for addr in adresses_ban_uniques
                                              if pd.notna(addr) and str(addr).strip() != '' and str(addr).upper() != 'NAN']

                        if len(adresses_ban_uniques) > 1:
                            # Doublon suspect détecté !
                            for _, ligne in lignes_meme_motif.iterrows():
                                # Créer une clé unique pour cette ligne
                                ligne_key = f"{ligne['imb_code']}_{ligne['adresse_optimum']}_{ligne['adresse_ban']}_{ligne['motif']}"

                                # Ajouter seulement si pas déjà ajoutée
                                if ligne_key not in lignes_deja_ajoutees:
                                    doublon_info = {
                                        'imb_code': ligne['imb_code'],
                                        'adresse_optimum': ligne['adresse_optimum'],
                                        'motif_initial': ligne['motif'],
                                        'adresse_ban': ligne['adresse_ban'],
                                        'type': 'DOUBLON_IMB_SUSPECT',
                                        'description': f"IMB {ligne['imb_code']} - Motif '{ligne['motif']}' avec adresses BAN différentes"
                                    }
                                    doublons_suspects.append(doublon_info)
                                    doublons_details.append(doublon_info)
                                    lignes_deja_ajoutees.add(ligne_key)

            # Calculer les statistiques
            total_doublons_imb = len(doublons_imb)
            total_doublons_suspects = len(doublons_suspects)
            total_erreurs_motif_ok = len(erreurs_motif_ok)
            total_erreurs_detectees = total_doublons_suspects + total_erreurs_motif_ok

            return {
                'status': 'COMPLETE',
                'total_doublons_imb': total_doublons_imb,
                'total_doublons_suspects': total_doublons_suspects,
                'total_erreurs_motif_ok': total_erreurs_motif_ok,
                'total_erreurs_detectees': total_erreurs_detectees,
                'doublons_suspects': doublons_suspects,
                'erreurs_motif_ok': erreurs_motif_ok,
                'doublons_details': doublons_details,
                'doublons_imb_codes': doublons_imb,
                'total_records_analyzed': len(df_work)
            }

        except Exception as e:
            self.logger.error(f"Erreur dans l'analyse du critère 3: {e}")
            return {
                'status': 'ERROR',
                'error': str(e),
                'total_doublons_imb': 0,
                'total_doublons_suspects': 0,
                'total_erreurs_motif_ok': 0,
                'total_erreurs_detectees': 0,
                'doublons_suspects': [],
                'erreurs_motif_ok': [],
                'doublons_details': []
            }

    def _analyze_critere_4(self) -> Dict[str, Any]:
        """
        Critère 4: Détection "ad à analyser"
        Détecte les entrées avec motif "ad à analyser" qui ont un IMB présent dans la colonne A.

        Colonnes analysées:
        - A: Num Dossier Site (codes IMB) - OBLIGATOIRE
        - B: Numero Voie Site
        - C: Repondant Voie Site
        - D: Libelle Voie Site
        - J: Import Fantome (motifs)
        - U: Adresse BAN
        """
        try:
            pd = get_pandas()

            # Vérifier que les colonnes requises existent
            if len(self.qgis_data.columns) < 21:  # Au moins 21 colonnes (A-U)
                raise ValueError("Le fichier QGis ne contient pas assez de colonnes (minimum A-U requis)")

            # Extraire les données des colonnes requises
            df = self.qgis_data.copy()

            # Renommer les colonnes pour faciliter le travail
            df_work = pd.DataFrame({
                'imb_code': df.iloc[:, 0],  # Colonne A - Num Dossier Site
                'numero_voie': df.iloc[:, 1],  # Colonne B - Numero Voie Site
                'repondant_voie': df.iloc[:, 2],  # Colonne C - Repondant Voie Site
                'libelle_voie': df.iloc[:, 3],  # Colonne D - Libelle Voie Site
                'motif': df.iloc[:, 9],  # Colonne J - Import Fantome
                'adresse_ban': df.iloc[:, 20]  # Colonne U - Adresse BAN
            })

            # Nettoyer les données
            df_work['imb_code'] = df_work['imb_code'].astype(str).str.strip()
            df_work['motif'] = df_work['motif'].astype(str).str.strip().str.upper()
            df_work['adresse_ban'] = df_work['adresse_ban'].astype(str).str.strip()

            # Construire l'adresse optimum (même logique que critère 3)
            def construct_adresse_optimum(row):
                """Construit l'adresse optimum en gérant les valeurs vides et numériques."""
                numero = str(row['numero_voie']).strip() if pd.notna(row['numero_voie']) else ''
                repondant = str(row['repondant_voie']).strip() if pd.notna(row['repondant_voie']) else ''
                libelle = str(row['libelle_voie']).strip() if pd.notna(row['libelle_voie']) else ''

                # Nettoyer les valeurs numériques (enlever .0)
                if numero and numero != 'nan':
                    try:
                        if '.' in numero and numero.replace('.', '').replace('-', '').isdigit():
                            numero = str(int(float(numero)))
                    except:
                        pass

                # Appliquer les règles de construction d'adresse
                if not repondant or repondant == 'nan':
                    if numero and numero != 'nan' and libelle and libelle != 'nan':
                        return f"{numero} {libelle}".strip()
                    elif libelle and libelle != 'nan':
                        return libelle.strip()
                    elif numero and numero != 'nan':
                        return numero.strip()
                    else:
                        return ''
                else:
                    parts = []
                    if numero and numero != 'nan':
                        parts.append(numero)
                    if repondant and repondant != 'nan':
                        parts.append(repondant)
                    if libelle and libelle != 'nan':
                        parts.append(libelle)
                    return ' '.join(parts).strip()

            df_work['adresse_optimum'] = df_work.apply(construct_adresse_optimum, axis=1)

            # Détecter les entrées "ad à analyser" avec IMB présent
            ad_a_analyser_entries = []

            for _, row in df_work.iterrows():
                motif = str(row['motif']).strip().upper()
                imb_code = str(row['imb_code']).strip()

                # Vérifier si motif = "AD À ANALYSER" et IMB présent
                if (motif == 'AD À ANALYSER' and
                    imb_code and imb_code != '' and imb_code != 'nan' and imb_code.upper() != 'NAN'):

                    entry_info = {
                        'imb_code': imb_code,
                        'adresse_optimum': row['adresse_optimum'],
                        'motif_initial': 'ad à analyser',
                        'adresse_ban': row['adresse_ban'],
                        'type': 'AD_A_ANALYSER_AVEC_IMB',
                        'description': f"IMB {imb_code} - Motif 'ad à analyser' nécessitant une analyse"
                    }
                    ad_a_analyser_entries.append(entry_info)

                    # Log pour confirmer la détection
                    self.logger.info(f"AD À ANALYSER DÉTECTÉ - IMB: {imb_code}, Adresse: '{row['adresse_optimum']}'")

            # Calculer les statistiques
            total_ad_a_analyser = len(ad_a_analyser_entries)

            return {
                'status': 'COMPLETE',
                'total_ad_a_analyser': total_ad_a_analyser,
                'ad_a_analyser_entries': ad_a_analyser_entries,
                'total_records_analyzed': len(df_work)
            }

        except Exception as e:
            self.logger.error(f"Erreur dans l'analyse du critère 4: {e}")
            return {
                'status': 'ERROR',
                'error': str(e),
                'total_ad_a_analyser': 0,
                'ad_a_analyser_entries': []
            }

    def _analyze_critere_5(self) -> Dict[str, Any]:
        """
        Critère 5: Motif Incorrect
        Détecte les motifs non conformes dans le fichier Résultats QGis (colonne J)
        qui ne correspondent pas aux 7 motifs autorisés.

        Colonnes analysées:
        - A: Num Dossier Site (codes IMB)
        - B: Numero Voie Site
        - C: Repondant Voie Site
        - D: Libelle Voie Site
        - J: Import Fantome (motifs à vérifier)
        - U: Adresse BAN
        """
        try:
            pd = get_pandas()

            # Motifs autorisés (liste de référence)
            motifs_autorises = [
                'AD RAS', 'OK', 'NOK', 'UPR RAS', 'UPR OK', 'UPR NOK', 'HORS COMMUNE'
            ]

            # Vérifier que les colonnes requises existent
            if len(self.qgis_data.columns) < 21:  # Au moins 21 colonnes (A-U)
                raise ValueError("Le fichier QGis ne contient pas assez de colonnes (minimum A-U requis)")

            # Extraire les données des colonnes requises
            df = self.qgis_data.copy()

            # Renommer les colonnes pour faciliter le travail
            df_work = pd.DataFrame({
                'imb_code': df.iloc[:, 0],  # Colonne A - Num Dossier Site
                'numero_voie': df.iloc[:, 1],  # Colonne B - Numero Voie Site
                'repondant_voie': df.iloc[:, 2],  # Colonne C - Repondant Voie Site
                'libelle_voie': df.iloc[:, 3],  # Colonne D - Libelle Voie Site
                'motif': df.iloc[:, 9],  # Colonne J - Import Fantome (index 9 pour colonne J)
                'adresse_ban': df.iloc[:, 20]  # Colonne U - Adresse BAN
            })

            # Nettoyer les données
            df_work = df_work.dropna(subset=['imb_code'])  # Supprimer les lignes sans code IMB
            df_work['imb_code'] = df_work['imb_code'].astype(str).str.strip()
            df_work['motif'] = df_work['motif'].astype(str).str.strip().str.upper()
            df_work['adresse_ban'] = df_work['adresse_ban'].astype(str).str.strip()

            # Construire l'adresse optimum (même logique que critère 3)
            def construct_adresse_optimum(row):
                """Construit l'adresse optimum en gérant les valeurs vides et numériques."""
                numero = str(row['numero_voie']).strip() if pd.notna(row['numero_voie']) else ''
                repondant = str(row['repondant_voie']).strip() if pd.notna(row['repondant_voie']) else ''
                libelle = str(row['libelle_voie']).strip() if pd.notna(row['libelle_voie']) else ''

                # Nettoyer les valeurs numériques (enlever .0)
                if numero and numero != 'nan':
                    try:
                        if '.' in numero and numero.replace('.', '').replace('-', '').isdigit():
                            numero = str(int(float(numero)))
                    except:
                        pass

                # Construire l'adresse selon les règles du critère 3
                parts = []
                if numero and numero != 'nan':
                    parts.append(numero)
                if repondant and repondant != 'nan':
                    parts.append(repondant)
                if libelle and libelle != 'nan':
                    parts.append(libelle)

                # Appliquer les règles spécifiques
                if not repondant or repondant == 'nan':
                    if numero and numero != 'nan' and libelle and libelle != 'nan':
                        return f"{numero} {libelle}".strip()
                    elif libelle and libelle != 'nan':
                        return libelle.strip()
                    elif numero and numero != 'nan':
                        return numero.strip()
                    else:
                        return ''
                else:
                    return ' '.join(parts).strip()

            df_work['adresse_optimum'] = df_work.apply(construct_adresse_optimum, axis=1)

            motifs_incorrects_entries = []

            # Analyser chaque ligne pour détecter les motifs incorrects
            for index, row in df_work.iterrows():
                motif = str(row['motif']).strip().upper()
                imb_code = str(row['imb_code']).strip()

                # Ignorer les lignes avec motifs vides ou NaN
                if not motif or motif == '' or motif.upper() == 'NAN':
                    continue

                # Vérifier si le motif n'est pas dans la liste autorisée
                if motif not in motifs_autorises:
                    entry_info = {
                        'imb_code': imb_code,
                        'adresse_optimum': row['adresse_optimum'],
                        'motif_incorrect': motif,
                        'adresse_ban': row['adresse_ban'],
                        'type': 'MOTIF_INCORRECT',
                        'description': f"IMB {imb_code} - Motif '{motif}' non autorisé"
                    }
                    motifs_incorrects_entries.append(entry_info)

                    # Log pour confirmer la détection
                    self.logger.info(f"MOTIF INCORRECT DÉTECTÉ - IMB: {imb_code}, Motif: '{motif}'")

            # Calculer les statistiques
            total_motifs_incorrects = len(motifs_incorrects_entries)

            return {
                'status': 'COMPLETE',
                'total_motifs_incorrects': total_motifs_incorrects,
                'motifs_incorrects_entries': motifs_incorrects_entries,
                'total_records_analyzed': len(df_work)
            }

        except Exception as e:
            self.logger.error(f"Erreur dans l'analyse du critère 5: {e}")
            return {
                'status': 'ERROR',
                'error': str(e),
                'total_motifs_incorrects': 0,
                'motifs_incorrects_entries': []
            }

    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule le résumé des résultats d'analyse."""
        try:
            critere_0 = results.get('critere_0', {})
            critere_2 = results.get('critere_2', {})
            critere_3 = results.get('critere_3', {})
            critere_4 = results.get('critere_4', {})
            critere_5 = results.get('critere_5', {})

            total_errors = (
                critere_0.get('total_incoherences', 0) +
                critere_2.get('total_errors', 0) +
                critere_3.get('total_erreurs_detectees', 0) +
                critere_4.get('total_ad_a_analyser', 0) +
                critere_5.get('total_motifs_incorrects', 0)
            )

            return {
                'total_errors': total_errors,
                'critere_0_errors': critere_0.get('total_incoherences', 0),
                'critere_2_errors': critere_2.get('total_errors', 0),
                'critere_3_errors': critere_3.get('total_erreurs_detectees', 0),
                'critere_3_doublons_suspects': critere_3.get('total_doublons_suspects', 0),
                'critere_3_erreurs_motif_ok': critere_3.get('total_erreurs_motif_ok', 0),
                'critere_4_errors': critere_4.get('total_ad_a_analyser', 0),
                'critere_5_errors': critere_5.get('total_motifs_incorrects', 0),
                'ticket_upr_status': critere_2.get('ticket_upr_status', 'N/A'),
                'ticket_501_511_status': critere_2.get('ticket_501_511_status', 'N/A'),
                'total_doublons_imb': critere_3.get('total_doublons_imb', 0),
                'total_doublons_suspects': critere_3.get('total_doublons_suspects', 0),
                'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'commune': self.detected_info.get('commune', 'Non détecté'),
                'collaborateur': self.detected_info.get('collaborateur', 'Non détecté'),
                'insee': self.detected_info.get('insee', 'Non détecté'),
                'id_tache': self.detected_info.get('id_tache', 'Non détecté'),
                'domaine': self.detected_info.get('domaine', ''),
                'cms_total': self.detected_info.get('cms_total', ''),
                'pa_total': self.detected_info.get('pa_total', '')
            }

        except Exception as e:
            self.logger.error(f"Erreur calcul résumé: {e}")
            return {'total_errors': 0}

    def _export_qc_report(self):
        """Exporte le rapport de contrôle qualité."""
        if not self.qc_results:
            messagebox.showwarning("Attention", "Aucune analyse à exporter. Veuillez d'abord lancer l'analyse.")
            return

        try:
            # Générer le nom de fichier depuis les informations détectées
            commune = self.detected_info.get('commune', 'Commune')
            insee = self.detected_info.get('insee', 'INSEE')
            collaborateur = self.detected_info.get('collaborateur', 'Collaborateur')

            # Nettoyer les noms pour le fichier (enlever caractères spéciaux)
            commune_clean = "".join(c for c in commune if c.isalnum() or c in (' ', '-', '_')).strip()
            collaborateur_clean = "".join(c for c in collaborateur if c.isalnum() or c in (' ', '-', '_')).strip()

            filename = f"Etat_De_Lieu_{commune_clean}_{insee}_{collaborateur_clean}.xlsx"

            # Demander où sauvegarder avec paramètres compatibles
            file_path = filedialog.asksaveasfilename(
                title="Sauvegarder le rapport de contrôle qualité",
                initialfile=filename,
                defaultextension=".xlsx",
                filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")]
            )

            if not file_path:
                return

            self._update_status("waiting", "Génération du rapport...")
            self.progress_var.set(50)

            def generate_report():
                return self._generate_excel_report(file_path)

            def on_success(success):
                if success:
                    self._update_status("success", "Rapport exporté avec succès")
                    if hasattr(self, 'report_status'):
                        self.report_status.config(text="📊 Rapport: ✅ Exporté", fg=COLORS['SUCCESS'])
                    self.progress_var.set(100)
                    messagebox.showinfo("Succès", f"Rapport exporté vers:\n{file_path}")
                    self.logger.info(f"Rapport exporté: {file_path}")
                else:
                    self._update_status("error", "Erreur lors de l'export")
                    self.progress_var.set(0)
                    messagebox.showerror("Erreur", "Échec de la génération du rapport Excel.\nVérifiez les logs pour plus de détails.")

            def on_error(error):
                self._update_status("error", "Erreur lors de l'export")
                self.progress_var.set(0)
                error_msg = f"Erreur lors de l'export:\n{str(error)}"
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + "...\n\nVoir les logs pour plus de détails."
                messagebox.showerror("Erreur", error_msg)
                self.logger.error(f"Erreur export rapport: {error}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")

            # Générer de manière asynchrone
            run_async_task(generate_report, on_success, on_error, "Export rapport")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'export: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{e}")
    
    def _generate_excel_report(self, file_path: str) -> bool:
        """Génère le rapport Excel avec 2 feuilles."""
        try:
            self.logger.info(f"Début génération rapport Excel: {file_path}")

            # Vérifier que les résultats QC existent
            if not self.qc_results:
                raise ValueError("Aucun résultat d'analyse disponible pour l'export")

            # Nettoyer le chemin du fichier
            file_path = os.path.abspath(file_path)
            self.logger.info(f"Chemin absolu du fichier: {file_path}")

            # Vérifier que le répertoire existe
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"Répertoire créé: {directory}")

            # Générer les données des 3 feuilles d'abord
            page1_data, page2_data, page3_data = self._prepare_excel_data()
            self.logger.info("Données Excel préparées pour 3 feuilles")

            # Créer le fichier Excel de manière isolée
            success = self._write_excel_file(file_path, page1_data, page2_data, page3_data)

            if success:
                # Vérifier que le fichier a été créé
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    self.logger.info(f"Fichier créé avec succès: {file_path} ({file_size} bytes)")
                    return True
                else:
                    raise FileNotFoundError(f"Le fichier n'a pas été créé: {file_path}")
            else:
                return False

        except Exception as e:
            self.logger.error(f"Erreur génération rapport Excel: {e}")
            import traceback
            self.logger.error(f"Traceback complet: {traceback.format_exc()}")
            return False

    def _prepare_excel_data(self):
        """Prépare les données pour les 3 feuilles Excel selon la nouvelle structure."""
        try:
            summary = self.qc_results.get('summary', {})
            commune = summary.get('commune', 'COMMUNE')
            collaborateur = summary.get('collaborateur', 'COLLABORATEUR')
            insee = summary.get('insee', 'INSEE')
            id_tache = summary.get('id_tache', 'ID_TACHE')
            domaine = summary.get('domaine', '')
            cms_total = summary.get('cms_total', '')
            pa_total = summary.get('pa_total', '')

            # Page 1: Structure selon le nouveau modèle avec sections étendues
            page1_data = [
                # En-tête principal (ligne 1-2)
                ['Nom de commune', 'ID tâche Plan Adressage', 'Code INSEE', 'Domaine', 'AFFECTATION', 'Controleur', '', '', '', ''],
                [commune, id_tache, insee, domaine, collaborateur, '', '', '', '', ''],  # Collaborateur depuis colonne U, Contrôleur vide
                ['', '', '', '', '', '', '', '', '', ''],  # Ligne vide

                # Section CMS (lignes 4-5) - Avec formules Excel dynamiques
                ['Nbr voies CMS Total', 'Nbr voies CMS Controllé', 'Nbr voies KO', '% Erreur CMS', '', '', '', '', '', ''],
                [cms_total, '', '=SUMPRODUCT(--(\'Controle Qualité CMS\'!A2:A1000<>""))', '=IF(A5=0,0,C5/A5)', '', '', '', '', '', ''],  # Formules dynamiques - SUMPRODUCT compte seulement les cellules vraiment non vides
                ['', '', '', '', '', '', '', '', '', ''],  # Ligne vide

                # Section PA (lignes 7-8)
                ['Nbr IMB PA Total', 'Nbr IMB PA Controllé', 'Nbr IMB PA KO', '% Erreur PA', '', '', '', '', '', ''],
                [pa_total, '', '=SUMPRODUCT(--(\'Controle Qualité PA\'!A2:A1000<>""))', '=IF(A8=0,0,C8/A8)', '', '', '', '', '', ''],  # Total PA depuis colonne H + formule pour compter seulement les codes IMB vraiment présents de la page 3 + formule % Erreur PA
                ['', '', '', '', '', '', '', '', '', ''],  # Ligne vide

                # Section Tickets (lignes 10-11)
                ['Ticket 501/511', 'Ticket UPR', '% Erreur Banbou', '', '', '', '', '', '', ''],
            ]

            # Calculer les pourcentages avec pondérations (pour les valeurs statiques)
            resume_erreurs_data = self._calculate_resume_erreurs()

            # Remplir les statuts des tickets et calculer % Erreur Banbou
            if self.qc_results and 'critere_2' in self.qc_results:
                critere_2 = self.qc_results['critere_2']
                ticket_501_511_status = critere_2.get('ticket_501_511_status', '')
                ticket_upr_status = critere_2.get('ticket_upr_status', '')

                # Calculer le % Erreur Banbou
                erreur_banbou_percentage = self._calculate_erreur_banbou_percentage()
                erreur_banbou_str = f"{erreur_banbou_percentage:.0f}%"

                page1_data.append([ticket_501_511_status, ticket_upr_status, erreur_banbou_str, '', '', '', 'Résumé Erreurs', '', '', ''])
            else:
                # Pas de données d'analyse, afficher vides
                page1_data.append(['', '', '', '', '', '', 'Résumé Erreurs', '', '', ''])

            # Préparer les données d'écart Plan Adressage
            motifs_data = []
            if self.qc_results and 'critere_0' in self.qc_results:
                critere_0 = self.qc_results['critere_0']
                ecart_data = critere_0.get('ecart_plan_adressage', {})

                # Motifs dans l'ordre d'affichage
                motifs_ordre = ['AD RAS', 'OK', 'NOK', 'UPR RAS', 'UPR OK', 'UPR NOK', 'HORS COMMUNE']

                for motif in motifs_ordre:
                    if motif in ecart_data:
                        data = ecart_data[motif]
                        suivi_count = data['suivi_count']
                        qgis_count = data['qgis_count']
                        motif_display = motif.title() if motif != 'HORS COMMUNE' else 'Hors Commune'
                        motifs_data.append([motif_display, str(suivi_count), str(qgis_count)])
                    else:
                        motif_display = motif.title() if motif != 'HORS COMMUNE' else 'Hors Commune'
                        motifs_data.append([motif_display, '', ''])
            else:
                # Pas de données d'analyse, afficher les motifs vides
                motifs_ordre = ['AD RAS', 'OK', 'NOK', 'UPR RAS', 'UPR OK', 'UPR NOK', 'Hors Commune']
                for motif in motifs_ordre:
                    motifs_data.append([motif, '', ''])

            # Section Ecart Plan Adressage et résumé erreurs intégrés avec formules Excel dynamiques
            page1_data.extend([
                ['', '', '', '', '', '', '% Erreur Par Catégorie', '% Brut', 'Pondération', 'Taux'],  # Ligne 12 - En-tête avec nouvelle colonne
                ['Ecart Plan Adressage', '', '', '', '', '', '% Erreur CMS', '=D5', resume_erreurs_data['ponderation_cms'], '=H13*I13'],  # Ligne 13 - Formule pour % CMS
                ['Motif', 'Suivi', 'Resultats Qgis', '', '', '', '% Erreur PA', '=D8', resume_erreurs_data['ponderation_pa'], '=H14*I14'],  # Ligne 14 - Formule pour référencer % Erreur PA
                [motifs_data[0][0], motifs_data[0][1], motifs_data[0][2], '', '', '', '% Erreur Banbou', resume_erreurs_data['pourcentage_banbou_brut'], resume_erreurs_data['ponderation_banbou'], '=H15*I15'],  # Ligne 15 - Ad Ras
                [motifs_data[1][0], motifs_data[1][1], motifs_data[1][2], '', '', '', '% Ecart Plan Adressage', resume_erreurs_data['pourcentage_ecart_brut'], resume_erreurs_data['ponderation_ecart'], '=H16*I16'],  # Ligne 16 - Ok
                [motifs_data[2][0], motifs_data[2][1], motifs_data[2][2], '', '', '', '% Total', '', '', '=J13+J14+J15+J16'],  # Ligne 17 - Nok (formule pour total)
                [motifs_data[3][0], motifs_data[3][1], motifs_data[3][2], '', '', '', '', '', '', ''],  # Ligne 18 - Upr Ras
                [motifs_data[4][0], motifs_data[4][1], motifs_data[4][2], '', '', '', '', '', '', ''],  # Ligne 19 - Upr Ok
                [motifs_data[5][0], motifs_data[5][1], motifs_data[5][2], '', '', '', '', '', '', ''],  # Ligne 20 - Upr Nok
                [motifs_data[6][0], motifs_data[6][1], motifs_data[6][2], '', '', '', '', '', '', ''],  # Ligne 21 - Hors Commune
            ])

            # Ajouter la ligne % Ecart Plan Adressage directement sous le tableau (ligne 22)
            page1_data.extend([
                ['% Ecart Plan Adressage', '=H16', '', '', '', '', '', '', '', ''],  # Ligne 22 - Formule référençant H16 (% Brut Ecart Plan Adressage)
                ['', '', '', '', '', '', '', '', '', ''],  # Ligne vide finale
            ])

            # Page 2: Controle Qualité CMS - Structure vide pour saisie manuelle
            page2_data = [
                # En-tête avec les colonnes spécifiées
                ['ID Tache', 'Voie demandé', 'Motif Voie Initial', 'Etat', 'Commentaire Controleur']
            ]

            # Ajouter des lignes vides pour la saisie manuelle (pas de remplissage automatique)
            for i in range(20):  # 20 lignes vides pour saisie manuelle
                page2_data.append([' ', ' ', ' ', ' ', ' '])  # Espaces au lieu de chaînes vides (5 colonnes)

            # Page 3: Controle Qualité PA - Structure avec colonnes spécifiées + colonne Batiment
            page3_data = [
                # En-tête avec les colonnes spécifiées + nouvelle colonne Batiment après Adresse Optimum
                ['Num Dossier Site', 'Adresse Optimum', 'Batiment', 'Adresse BAN', 'Motif Initial', 'Etat', 'Commentaire Controleur', '']
            ]

            # Créer un dictionnaire pour mapper les codes IMB aux données de bâtiment (colonne F page 2 suivi commune)
            imb_to_batiment = {}
            if hasattr(self, 'current_suivi_file_path') and self.current_suivi_file_path:
                try:
                    pd = get_pandas()
                    # Lire la page 2 (index 1) du fichier suivi commune pour récupérer les données de bâtiment
                    suivi_page2_df = pd.read_excel(self.current_suivi_file_path, sheet_name=1, date_format=None)

                    self.logger.info(f"Page 2 suivi commune chargée pour bâtiments: {suivi_page2_df.shape}")

                    # Extraire les données des colonnes A (IMB) et F (Batiment)
                    if len(suivi_page2_df.columns) >= 6:  # Au moins 6 colonnes (A-F)
                        for index, row in suivi_page2_df.iterrows():
                            imb_code = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''  # Colonne A: IMB
                            batiment = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ''  # Colonne F: Batiment

                            # Ajouter au dictionnaire si les deux valeurs sont présentes
                            if imb_code and imb_code not in ['', 'nan', 'IMB', 'Num Dossier Site']:
                                imb_to_batiment[imb_code] = batiment

                    self.logger.info(f"Mapping IMB->Batiment créé: {len(imb_to_batiment)} entrées")

                except Exception as e:
                    self.logger.error(f"Erreur lecture page 2 suivi commune pour bâtiments: {e}")
                    imb_to_batiment = {}

            # Ajouter les données des CRITÈRES 3, 4 et 5 si disponibles
            toutes_erreurs_detectees = []

            # CRITÈRE 3: Doublons IMB et erreurs motif OK
            if self.qc_results and 'critere_3' in self.qc_results:
                critere_3 = self.qc_results['critere_3']
                doublons_suspects = critere_3.get('doublons_suspects', [])
                erreurs_motif_ok = critere_3.get('erreurs_motif_ok', [])
                toutes_erreurs_detectees.extend(doublons_suspects + erreurs_motif_ok)

            # CRITÈRE 4: AD à analyser
            if self.qc_results and 'critere_4' in self.qc_results:
                critere_4 = self.qc_results['critere_4']
                ad_a_analyser_entries = critere_4.get('ad_a_analyser_entries', [])
                toutes_erreurs_detectees.extend(ad_a_analyser_entries)

            # CRITÈRE 5: Motifs incorrects
            if self.qc_results and 'critere_5' in self.qc_results:
                critere_5 = self.qc_results['critere_5']
                motifs_incorrects_entries = critere_5.get('motifs_incorrects_entries', [])
                toutes_erreurs_detectees.extend(motifs_incorrects_entries)

            if toutes_erreurs_detectees:
                # Compter par type
                c3_doublons = len([e for e in toutes_erreurs_detectees if e.get('type') == 'DOUBLON_IMB_SUSPECT'])
                c3_motif_ok = len([e for e in toutes_erreurs_detectees if e.get('type') == 'ERREUR_MOTIF_OK_ADRESSE_IDENTIQUE'])
                c4_ad_analyser = len([e for e in toutes_erreurs_detectees if e.get('type') == 'AD_A_ANALYSER_AVEC_IMB'])
                c5_motifs_incorrects = len([e for e in toutes_erreurs_detectees if e.get('type') == 'MOTIF_INCORRECT'])

                self.logger.info(f"Ajout de {len(toutes_erreurs_detectees)} erreurs à la page 3 (C3: {c3_doublons} doublons + {c3_motif_ok} motif OK, C4: {c4_ad_analyser} ad à analyser, C5: {c5_motifs_incorrects} motifs incorrects)")

                for erreur in toutes_erreurs_detectees:
                    # Pour le critère 5 (motifs incorrects), utiliser le motif incorrect comme motif initial
                    motif_initial = erreur.get('motif_incorrect', '') if erreur.get('type') == 'MOTIF_INCORRECT' else erreur.get('motif_initial', '')

                    # Récupérer les données de bâtiment depuis le mapping IMB->Batiment
                    imb_code = erreur.get('imb_code', '')
                    batiment = imb_to_batiment.get(imb_code, '') if imb_code else ''

                    page3_data.append([
                        imb_code,                             # Colonne A: Num Dossier Site
                        erreur.get('adresse_optimum', ''),    # Colonne B: Adresse Optimum
                        batiment,                             # Colonne C: Batiment (depuis colonne F page 2 suivi commune)
                        erreur.get('adresse_ban', ''),        # Colonne D: Adresse BAN
                        motif_initial,                        # Colonne E: Motif Initial (ou motif incorrect pour C5)
                        '',                                    # Colonne F: Etat (vide pour saisie avec validation Nok-Mineure/Nok Majeure)
                        '',                                    # Colonne G: Commentaire Controleur (vide pour saisie)
                        ''                                     # Colonne H: Supplémentaire
                    ])

            # Ajouter des lignes vides supplémentaires pour la saisie manuelle
            lignes_vides_necessaires = max(0, 20 - (len(page3_data) - 1))  # -1 pour l'en-tête
            for i in range(lignes_vides_necessaires):
                page3_data.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])  # Espaces au lieu de chaînes vides (8 colonnes maintenant)

            return page1_data, page2_data, page3_data

        except Exception as e:
            self.logger.error(f"Erreur préparation données Excel: {e}")
            raise

    def _write_excel_file(self, file_path: str, page1_data: list, page2_data: list, page3_data: list) -> bool:
        """Écrit le fichier Excel avec 3 feuilles et mise en forme."""
        try:
            pd = get_pandas()

            # Obtenir les informations pour les noms de feuilles
            summary = self.qc_results.get('summary', {}) if self.qc_results else {}
            commune = summary.get('commune', 'Commune')
            collaborateur = summary.get('collaborateur', 'Collaborateur')

            # Créer les DataFrames avec colonnes appropriées
            df_page1 = pd.DataFrame(page1_data, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7', 'Col8', 'Col9', 'Col10'])
            df_page2 = pd.DataFrame(page2_data, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5'])  # 5 colonnes maintenant
            df_page3 = pd.DataFrame(page3_data, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7', 'Col8'])  # 8 colonnes maintenant (ajout colonne Batiment)

            self.logger.info("DataFrames créés pour 3 feuilles")

            # Noms des feuilles selon la nouvelle structure
            sheet1_name = f"Etat de lieu {commune}_{collaborateur}"
            sheet2_name = "Controle Qualité CMS"
            sheet3_name = "Controle Qualité PA"

            # Limiter la longueur des noms de feuilles (Excel limite à 31 caractères)
            if len(sheet1_name) > 31:
                sheet1_name = f"Etat de lieu {commune[:10]}_{collaborateur[:10]}"
                if len(sheet1_name) > 31:
                    sheet1_name = "Etat de lieu"

            # Écrire le fichier Excel avec mise en forme
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Page 1: Etat de lieu avec mise en forme
                df_page1.to_excel(writer, sheet_name=sheet1_name, index=False, header=False)

                # Appliquer la mise en forme à la page 1
                self._format_page1(writer.sheets[sheet1_name])

                # Page 2: Controle Qualité CMS (avec structure)
                df_page2.to_excel(writer, sheet_name=sheet2_name, index=False, header=False)

                # Appliquer la mise en forme à la page 2
                self._format_page2(writer.sheets[sheet2_name])

                # Page 3: Controle Qualité PA (avec structure)
                # S'assurer que toutes les lignes ont 7 colonnes
                page3_data_fixed = []
                for row in page3_data:
                    row_copy = row.copy() if isinstance(row, list) else list(row)
                    if len(row_copy) < 7:
                        row_copy.extend([' '] * (7 - len(row_copy)))  # Ajouter des espaces si nécessaire
                    page3_data_fixed.append(row_copy[:7])  # Limiter à 7 colonnes

                df_page3_fixed = pd.DataFrame(page3_data_fixed, columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7'])
                df_page3_fixed.to_excel(writer, sheet_name=sheet3_name, index=False, header=False)

                # Appliquer la mise en forme à la page 3
                self._format_page3(writer.sheets[sheet3_name])

                self.logger.info(f"3 feuilles Excel écrites: {sheet1_name}, {sheet2_name}, {sheet3_name}")

            self.logger.info("Fichier Excel écrit avec succès avec mise en forme")
            return True

        except Exception as e:
            self.logger.error(f"Erreur écriture fichier Excel: {e}")
            return False

    def _format_page1(self, worksheet):
        """Applique la mise en forme à la page 1 selon le modèle (avec bordures)."""
        try:
            from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

            # Définir les couleurs selon votre modèle
            blue_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            green_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
            orange_fill = PatternFill(start_color="C65911", end_color="C65911", fill_type="solid")

            # Police blanche pour les en-têtes (Calibri 11)
            white_font = Font(color="FFFFFF", bold=True, size=11, name="Calibri")
            bold_font = Font(bold=True, size=11, name="Calibri")
            normal_font = Font(size=11, name="Calibri")

            # Alignement centré
            center_alignment = Alignment(horizontal="center", vertical="center")

            # Définir les bordures
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

            # Appliquer la mise en forme selon les sections (AVEC BORDURES)

            # En-tête principal (ligne 1) - Bleu avec bordures
            for col in range(1, 7):  # A1:F1
                cell = worksheet.cell(row=1, column=col)
                cell.fill = blue_fill
                cell.font = white_font
                cell.alignment = center_alignment
                cell.border = thin_border

            # Section CMS (lignes 4-5) - Vert avec bordures
            for row in range(4, 6):  # Lignes 4-5
                for col in range(1, 5):  # A4:D5
                    cell = worksheet.cell(row=row, column=col)
                    if row == 4:  # En-tête
                        cell.fill = green_fill
                        cell.font = white_font
                    cell.alignment = center_alignment
                    cell.border = thin_border

            # Section PA (lignes 7-8) - Orange avec bordures
            for row in range(7, 9):  # Lignes 7-8
                for col in range(1, 5):  # A7:D8
                    cell = worksheet.cell(row=row, column=col)
                    if row == 7:  # En-tête
                        cell.fill = orange_fill
                        cell.font = white_font
                    cell.alignment = center_alignment
                    cell.border = thin_border

            # Section Tickets (lignes 10-11) - Bleu avec bordures
            for row in range(10, 12):  # Lignes 10-11
                for col in range(1, 4):  # A10:C11
                    cell = worksheet.cell(row=row, column=col)
                    if row == 10:  # En-tête
                        cell.fill = blue_fill
                        cell.font = white_font
                    cell.alignment = center_alignment
                    cell.border = thin_border

            # Section Résumé Erreurs (G11:J17) - Bleu avec bordures - Consécutif (ajout colonne % Brut)
            for row in range(11, 18):  # Lignes 11-17 (tableau consécutif)
                for col in range(7, 11):  # G11:J17 (ajout colonne J pour % Brut)
                    cell = worksheet.cell(row=row, column=col)
                    if row == 11 or row == 12:  # En-têtes (Résumé Erreurs + % Erreur Par Catégorie)
                        cell.fill = blue_fill
                        cell.font = white_font
                    cell.alignment = center_alignment
                    cell.border = thin_border

            # Section Ecart Plan Adressage (lignes 13-21) - Bleu avec bordures
            for row in range(13, 22):  # Lignes 13-21
                for col in range(1, 4):  # A13:C21
                    cell = worksheet.cell(row=row, column=col)
                    if row == 13 or row == 14:  # En-têtes
                        cell.fill = blue_fill
                        cell.font = white_font
                    cell.alignment = center_alignment
                    cell.border = thin_border

            # Section % Ecart Plan Adressage sous le tableau (ligne 22) - Bleu avec bordures
            for col in range(1, 3):  # A22:B22 (seulement 2 colonnes)
                cell = worksheet.cell(row=22, column=col)
                cell.fill = blue_fill
                cell.font = white_font
                cell.alignment = center_alignment
                cell.border = thin_border

            # Ajuster la largeur des colonnes
            worksheet.column_dimensions['A'].width = 20
            worksheet.column_dimensions['B'].width = 25
            worksheet.column_dimensions['C'].width = 15
            worksheet.column_dimensions['D'].width = 15
            worksheet.column_dimensions['E'].width = 15
            worksheet.column_dimensions['F'].width = 15
            worksheet.column_dimensions['G'].width = 20
            worksheet.column_dimensions['H'].width = 10
            worksheet.column_dimensions['I'].width = 12
            worksheet.column_dimensions['J'].width = 10

            # Appliquer l'alignement centré aux cellules de données
            # Centrer toutes les cellules de données, y compris les motifs
            for row in range(1, 25):  # Lignes 1 à 24 (pour couvrir tous les motifs)
                for col in range(1, 11):  # Colonnes A à J
                    cell = worksheet.cell(row=row, column=col)
                    # Appliquer l'alignement centré à toutes les cellules
                    cell.alignment = center_alignment
                    # Appliquer la police Calibri 11 à toutes les cellules
                    if not cell.font.bold:  # Ne pas changer la police des en-têtes en gras
                        cell.font = normal_font

            # Ajouter une validation des données pour la cellule Contrôleur (F2)
            self._add_controleur_validation(worksheet)

            # Appliquer le formatage des pourcentages aux cellules avec formules
            self._apply_percentage_formatting(worksheet)

            self.logger.info("Mise en forme appliquée à la page 1 (avec bordures)")

        except Exception as e:
            self.logger.warning(f"Erreur lors de la mise en forme: {e}")
            # Continue sans mise en forme si erreur

    def _add_controleur_validation(self, worksheet):
        """Ajoute une validation des données pour la cellule Contrôleur."""
        try:
            from openpyxl.worksheet.datavalidation import DataValidation

            # Importer la liste des collaborateurs depuis constants.py
            from config.constants import VALIDATION_LISTS
            collaborateurs_list = VALIDATION_LISTS.get("Collaborateur", [])

            if not collaborateurs_list:
                self.logger.warning("Liste des collaborateurs vide, validation ignorée")
                return

            # Créer une feuille cachée pour la liste des collaborateurs
            # Cela évite les problèmes avec les formules longues
            if 'ValidationData' not in [ws.title for ws in worksheet.parent.worksheets]:
                validation_sheet = worksheet.parent.create_sheet('ValidationData')
                validation_sheet.sheet_state = 'hidden'

                # Écrire la liste des collaborateurs dans la feuille cachée
                for i, collab in enumerate(collaborateurs_list, 1):
                    validation_sheet.cell(row=i, column=1, value=collab)

                # Créer la validation des données avec référence à la feuille cachée
                range_ref = f"ValidationData!$A$1:$A${len(collaborateurs_list)}"
                dv = DataValidation(
                    type="list",
                    formula1=range_ref,
                    allow_blank=True
                )
            else:
                # Si la feuille existe déjà, utiliser la référence existante
                range_ref = f"ValidationData!$A$1:$A${len(collaborateurs_list)}"
                dv = DataValidation(
                    type="list",
                    formula1=range_ref,
                    allow_blank=True
                )

            dv.error = "Veuillez sélectionner un contrôleur dans la liste."
            dv.errorTitle = "Contrôleur invalide"
            dv.prompt = "Sélectionnez un contrôleur dans la liste déroulante."
            dv.promptTitle = "Sélection du contrôleur"

            # Appliquer la validation à la cellule F2 (Contrôleur)
            dv.add('F2')
            worksheet.add_data_validation(dv)

            self.logger.info("Validation des données ajoutée pour le contrôleur")

        except Exception as e:
            self.logger.warning(f"Erreur lors de l'ajout de la validation des données: {e}")
            # Continue sans validation si erreur

    def _apply_percentage_formatting(self, worksheet):
        """Applique le formatage des pourcentages aux cellules contenant des formules de pourcentage."""
        try:
            from openpyxl.styles import NamedStyle

            # Créer un style de pourcentage si il n'existe pas
            try:
                percentage_style = worksheet.parent.named_styles['Percentage']
            except KeyError:
                percentage_style = NamedStyle(name='Percentage', number_format='0%')
                worksheet.parent.add_named_style(percentage_style)

            # Appliquer le formatage des pourcentages aux cellules avec formules de pourcentage
            percentage_cells = [
                'D5',   # % Erreur CMS
                'D8',   # % Erreur PA
                'H13',  # % Brut CMS (Résumé Erreurs)
                'H14',  # % Brut PA (Résumé Erreurs)
                'H15',  # % Brut Banbou (Résumé Erreurs)
                'H16',  # % Brut Ecart Plan Adressage (Résumé Erreurs)
                'J13',  # Taux CMS (Résumé Erreurs)
                'J14',  # Taux PA (Résumé Erreurs)
                'J15',  # Taux Banbou (Résumé Erreurs)
                'J16',  # Taux Ecart Plan Adressage (Résumé Erreurs)
                'J17',  # % Total (Résumé Erreurs)
                'B22'   # % Ecart Plan Adressage final
            ]

            for cell_ref in percentage_cells:
                cell = worksheet[cell_ref]
                cell.number_format = '0%'

            self.logger.info("Formatage des pourcentages appliqué")

        except Exception as e:
            self.logger.warning(f"Erreur lors du formatage des pourcentages: {e}")
            # Continue sans formatage si erreur

    def _format_page3(self, worksheet):
        """Applique la mise en forme à la page 3 - Contrôle Qualité PA."""
        try:
            from openpyxl.styles import PatternFill, Font, Alignment

            # Définir les styles
            blue_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            white_font = Font(color="FFFFFF", bold=True, size=11, name="Calibri")
            center_alignment = Alignment(horizontal="center", vertical="center")

            # Mise en forme de l'en-tête (ligne 1)
            header_columns = ['A', 'B', 'C', 'D', 'E', 'F']
            for col_letter in header_columns:
                cell = worksheet[f"{col_letter}1"]
                cell.fill = blue_fill
                cell.font = white_font
                cell.alignment = center_alignment

            # Ajuster la largeur des colonnes selon le contenu
            worksheet.column_dimensions['A'].width = 18  # Num Dossier Site
            worksheet.column_dimensions['B'].width = 25  # Adresse Optimum
            worksheet.column_dimensions['C'].width = 25  # Adresse BAN
            worksheet.column_dimensions['D'].width = 15  # Motif Initial
            worksheet.column_dimensions['E'].width = 15  # Etat
            worksheet.column_dimensions['F'].width = 20  # Commentaire Controleur
            worksheet.column_dimensions['G'].width = 10  # Colonne supplémentaire

            # Ajouter la validation de données pour la colonne E (Etat)
            from openpyxl.worksheet.datavalidation import DataValidation
            validation_options = '"Nok-Mineure,Nok Majeure"'
            dv = DataValidation(type="list", formula1=validation_options, allow_blank=True)
            dv.error = "Veuillez sélectionner une option valide"
            dv.errorTitle = "Valeur incorrecte"
            dv.prompt = "Sélectionnez: Nok-Mineure ou Nok Majeure"
            dv.promptTitle = "Etat"

            # Appliquer la validation aux lignes 2 à 22 (données + lignes vides)
            dv.add(f"E2:E22")
            worksheet.add_data_validation(dv)

            # Appliquer l'alignement centré à toutes les cellules de données
            for row in range(1, 22):  # Lignes 1 à 21 (en-tête + 20 lignes de données)
                for col in range(1, 8):  # Colonnes A à G
                    cell = worksheet.cell(row=row, column=col)
                    cell.alignment = center_alignment

            self.logger.info("Mise en forme appliquée à la page 3 - Contrôle Qualité PA")

        except Exception as e:
            self.logger.warning(f"Erreur lors de la mise en forme de la page 3: {e}")
            # Continue sans mise en forme si erreur

    def _format_page2(self, worksheet):
        """Applique la mise en forme à la page 2 - Contrôle Qualité CMS."""
        try:
            from openpyxl.styles import PatternFill, Font, Alignment
            from openpyxl.worksheet.datavalidation import DataValidation

            # Définir les styles
            blue_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            white_font = Font(color="FFFFFF", bold=True, size=11, name="Calibri")
            center_alignment = Alignment(horizontal="center", vertical="center")

            # Mise en forme de l'en-tête (ligne 1) - 5 colonnes seulement
            header_columns = ['A', 'B', 'C', 'D', 'E']
            for col_letter in header_columns:
                cell = worksheet[f"{col_letter}1"]
                cell.fill = blue_fill
                cell.font = white_font
                cell.alignment = center_alignment

            # Ajuster la largeur des colonnes selon le contenu
            worksheet.column_dimensions['A'].width = 15  # ID Tache
            worksheet.column_dimensions['B'].width = 30  # Voie demandé
            worksheet.column_dimensions['C'].width = 20  # Motif Voie Initial
            worksheet.column_dimensions['D'].width = 20  # Etat (élargie pour validation)
            worksheet.column_dimensions['E'].width = 25  # Commentaire Controleur

            # Ajouter la validation de données pour la colonne D (Etat)
            validation_options = '"Nok-Mineure,Nok Majeure"'
            dv = DataValidation(type="list", formula1=validation_options, allow_blank=True)
            dv.error = "Veuillez sélectionner une option valide"
            dv.errorTitle = "Valeur incorrecte"
            dv.prompt = "Sélectionnez: Nok-Mineure ou Nok Majeure"
            dv.promptTitle = "Etat"

            # Appliquer la validation aux lignes 2 à 22 (données + lignes vides)
            dv.add(f"D2:D22")
            worksheet.add_data_validation(dv)

            # Appliquer l'alignement centré à toutes les cellules de données
            for row in range(1, 22):  # Lignes 1 à 21 (en-tête + 20 lignes de données)
                for col in range(1, 6):  # Colonnes A à E (5 colonnes)
                    cell = worksheet.cell(row=row, column=col)
                    cell.alignment = center_alignment

            self.logger.info("Mise en forme de la page 2 appliquée avec validation de données")

        except Exception as e:
            self.logger.warning(f"Erreur lors de la mise en forme de la page 2: {e}")
            # Continue sans mise en forme si erreur





    def _calculate_error_percentage(self) -> float:
        """Calcule le pourcentage d'erreur."""
        try:
            summary = self.qc_results.get('summary', {})
            total_errors = summary.get('total_errors', 0)

            # Base de calcul (nombre total d'enregistrements analysés)
            total_records = 0
            if self.qgis_data is not None:
                total_records += len(self.qgis_data)
            if self.suivi_data is not None:
                total_records += len(self.suivi_data)

            if total_records > 0:
                return (total_errors / total_records) * 100
            return 0.0

        except Exception:
            return 0.0

    def _calculate_erreur_banbou_percentage(self) -> float:
        """
        Calcule le % Erreur Banbou basé sur les statuts des tickets UPR et 501/511.

        Logique:
        - Si les deux tickets sont OK ou N/A → 0%
        - Si les deux tickets sont NOK → 100%
        - Si un OK et un NOK → 50%

        Returns:
            float: Pourcentage d'erreur Banbou (0.0 à 100.0)
        """
        try:
            if not self.qc_results or 'critere_2' not in self.qc_results:
                return 0.0

            critere_2 = self.qc_results['critere_2']
            ticket_upr_status = critere_2.get('ticket_upr_status', 'N/A')
            ticket_501_511_status = critere_2.get('ticket_501_511_status', 'N/A')

            # Compter les tickets NOK
            nok_count = 0
            total_tickets = 0

            # Analyser ticket UPR
            if ticket_upr_status in ['OK', 'NOK']:
                total_tickets += 1
                if ticket_upr_status == 'NOK':
                    nok_count += 1

            # Analyser ticket 501/511
            if ticket_501_511_status in ['OK', 'NOK']:
                total_tickets += 1
                if ticket_501_511_status == 'NOK':
                    nok_count += 1

            # Calculer le pourcentage
            if total_tickets == 0:
                # Aucun ticket requis (tous N/A) → 0% d'erreur
                percentage = 0.0
            else:
                # Pourcentage = (nombre de NOK / total de tickets) * 100
                percentage = (nok_count / total_tickets) * 100.0

            self.logger.info(f"Calcul % Erreur Banbou: UPR={ticket_upr_status}, 501/511={ticket_501_511_status}, "
                           f"NOK={nok_count}/{total_tickets}, Résultat={percentage}%")

            return percentage

        except Exception as e:
            self.logger.error(f"Erreur calcul % Erreur Banbou: {e}")
            return 0.0

    def _calculate_resume_erreurs(self) -> Dict[str, str]:
        """Calcule les pourcentages du résumé erreurs avec pondérations."""
        try:
            # Pondérations fixes (constantes)
            ponderation_cms = "0,3"
            ponderation_pa = "0,6"
            ponderation_banbou = "0,05"
            ponderation_ecart = "0,05"

            # Calculer les pourcentages bruts
            pourcentage_cms_brut = 0.0  # À calculer selon vos critères CMS
            pourcentage_pa_brut = 0.0   # À calculer selon vos critères PA
            pourcentage_banbou_brut = self._calculate_erreur_banbou_percentage()  # Calculé selon les tickets
            pourcentage_ecart_brut = self._calculate_ecart_plan_adressage_percentage()

            # Convertir en pourcentage (diviser par 100 pour avoir une valeur sous 1)
            pourcentage_ecart_decimal = pourcentage_ecart_brut / 100.0

            # Calculer les taux pondérés (pourcentage décimal * pondération)
            taux_cms = pourcentage_cms_brut * 0.3
            taux_pa = pourcentage_pa_brut * 0.6
            taux_banbou = pourcentage_banbou_brut * 0.05
            taux_ecart = pourcentage_ecart_decimal * 0.05

            # Calculer le total
            total = taux_cms + taux_pa + taux_banbou + taux_ecart

            # Formater avec points comme séparateurs décimaux (pas de virgules)
            return {
                'ponderation_cms': ponderation_cms,
                'ponderation_pa': ponderation_pa,
                'ponderation_banbou': ponderation_banbou,
                'ponderation_ecart': ponderation_ecart,
                # Pourcentages bruts (avant pondération)
                'pourcentage_cms_brut': f"{pourcentage_cms_brut:.1f}%",
                'pourcentage_pa_brut': f"{pourcentage_pa_brut:.1f}%",
                'pourcentage_banbou_brut': f"{pourcentage_banbou_brut:.0f}%",
                'pourcentage_ecart_brut': f"{pourcentage_ecart_brut:.1f}%",
                # Taux pondérés (après multiplication par pondération) - Format sans décimales
                'taux_cms': f"{taux_cms:.0f}%",
                'taux_pa': f"{taux_pa:.0f}%",
                'taux_banbou': f"{taux_banbou:.0f}%",
                'taux_ecart': f"{taux_ecart:.0f}%",
                'total': f"{total:.0f}%",
                # Données supplémentaires pour compatibilité
                'pourcentage_ecart_brut_percent': f"{pourcentage_ecart_brut:.2f}%",
                'pourcentage_banbou_brut_percent': f"{pourcentage_banbou_brut:.0f}%"
            }

        except Exception as e:
            self.logger.error(f"Erreur calcul résumé erreurs: {e}")
            return {
                'ponderation_cms': "0,3",
                'ponderation_pa': "0,6",
                'ponderation_banbou': "0,05",
                'ponderation_ecart': "0,05",
                'taux_cms': "0,000",
                'taux_pa': "0,000",
                'taux_banbou': "0,000",
                'taux_ecart': "0,000",
                'total': "0,000",
                'pourcentage_ecart_brut': "0,00",
                'pourcentage_ecart_brut_percent': "0,00%"
            }

    def _calculate_ecart_plan_adressage_percentage(self) -> float:
        """Calcule le pourcentage d'erreur spécifique à l'écart Plan Adressage."""
        try:
            if not self.qc_results or 'critere_0' not in self.qc_results:
                return 0.0

            critere_0 = self.qc_results['critere_0']
            ecart_data = critere_0.get('ecart_plan_adressage', {})

            total_ecarts = 0
            total_motifs = 0

            # Debug: afficher les données pour comprendre le calcul
            self.logger.debug("Calcul pourcentage écart Plan Adressage:")

            for motif, data in ecart_data.items():
                suivi_count = data.get('suivi_count', 0)
                qgis_count = data.get('qgis_count', 0)
                difference = data.get('difference', 0)
                has_ecart = data.get('has_ecart', False)

                # Utiliser le maximum comme base de calcul
                base_count = max(suivi_count, qgis_count)
                total_motifs += base_count

                # Ajouter l'écart absolu si il y en a un
                if has_ecart:
                    ecart_abs = abs(difference)
                    total_ecarts += ecart_abs
                    self.logger.debug(f"  {motif}: Suivi={suivi_count}, QGis={qgis_count}, Écart={difference:+d}, Base={base_count}")
                else:
                    self.logger.debug(f"  {motif}: Suivi={suivi_count}, QGis={qgis_count}, Pas d'écart, Base={base_count}")

            self.logger.debug(f"  Total écarts: {total_ecarts}, Total motifs: {total_motifs}")

            if total_motifs > 0:
                pourcentage = (total_ecarts / total_motifs) * 100
                self.logger.debug(f"  Pourcentage calculé: {pourcentage:.2f}%")
                return pourcentage
            return 0.0

        except Exception as e:
            self.logger.warning(f"Erreur calcul pourcentage écart Plan Adressage: {e}")
            return 0.0

    def _display_modern_results(self, results: Dict[str, Any]):
        """Affiche les résultats de l'analyse avec un design moderne."""
        try:
            # Effacer les résultats précédents
            for widget in self.results_frame.winfo_children():
                widget.destroy()

            summary = results.get('summary', {})
            critere_0 = results.get('critere_0', {})
            critere_1 = results.get('critere_1', {})

            total_errors = summary.get('total_errors', 0)

            # Carte de résumé principal
            self._create_summary_card(summary, total_errors)

            # Cartes de détails par critère
            critere_2 = results.get('critere_2', {})
            critere_3 = results.get('critere_3', {})
            critere_4 = results.get('critere_4', {})
            self._create_criteria_results_cards(critere_0, critere_2, critere_3, critere_4)

            # Informations de contexte
            self._create_context_info_card(summary)

        except Exception as e:
            self.logger.error(f"Erreur affichage résultats modernes: {e}")

    def _display_compact_results(self, results: Dict[str, Any]):
        """Affiche les résultats de l'analyse de manière ultra-compacte."""
        try:
            # Effacer les résultats précédents
            for widget in self.results_frame.winfo_children():
                widget.destroy()

            summary = results.get('summary', {})
            critere_0 = results.get('critere_0', {})
            critere_2 = results.get('critere_2', {})
            critere_3 = results.get('critere_3', {})

            total_errors = summary.get('total_errors', 0)

            # Statut principal ultra-compact
            status_frame = tk.Frame(self.results_frame, bg=COLORS['CARD'])
            status_frame.pack(fill=tk.X, pady=(0, 3))

            status_icon = "✅" if total_errors == 0 else "⚠️" if total_errors < 5 else "❌"
            status_color = COLORS['SUCCESS'] if total_errors == 0 else COLORS['WARNING'] if total_errors < 5 else COLORS['ERROR']

            tk.Label(status_frame, text=f"{status_icon} {total_errors} erreur(s)",
                    font=("Segoe UI", 9, "bold"), fg=status_color,
                    bg=COLORS['CARD']).pack()

            # Détails par critère ultra-compacts
            details_frame = tk.Frame(self.results_frame, bg=COLORS['LIGHT'], relief='flat', bd=1)
            details_frame.pack(fill=tk.X, pady=2)
            details_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

            details_content = tk.Frame(details_frame, bg=COLORS['LIGHT'])
            details_content.pack(fill=tk.X, padx=3, pady=2)

            # Critère 0
            c0_errors = critere_0.get('total_incoherences', 0)
            c0_color = COLORS['SUCCESS'] if c0_errors == 0 else COLORS['ERROR']
            c0_frame = tk.Frame(details_content, bg=COLORS['LIGHT'])
            c0_frame.pack(fill=tk.X, pady=1)

            tk.Label(c0_frame, text="0", font=("Segoe UI", 7, "bold"),
                    fg='white', bg=c0_color, padx=2).pack(side=tk.LEFT)
            tk.Label(c0_frame, text=f"Incohérences: {c0_errors}",
                    font=("Segoe UI", 7), fg=COLORS['TEXT_PRIMARY'],
                    bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

            # Critère 2
            c2_errors = critere_2.get('total_errors', 0)
            c2_color = COLORS['SUCCESS'] if c2_errors == 0 else COLORS['ERROR']
            c2_frame = tk.Frame(details_content, bg=COLORS['LIGHT'])
            c2_frame.pack(fill=tk.X, pady=1)

            tk.Label(c2_frame, text="2", font=("Segoe UI", 7, "bold"),
                    fg='white', bg=c2_color, padx=2).pack(side=tk.LEFT)
            tk.Label(c2_frame, text=f"Tickets: {c2_errors}",
                    font=("Segoe UI", 7), fg=COLORS['TEXT_PRIMARY'],
                    bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

            # Critère 3
            c3_errors = critere_3.get('total_erreurs_detectees', 0)
            c3_doublons = critere_3.get('total_doublons_suspects', 0)
            c3_motif_ok = critere_3.get('total_erreurs_motif_ok', 0)
            c3_color = COLORS['SUCCESS'] if c3_errors == 0 else COLORS['ERROR']
            c3_frame = tk.Frame(details_content, bg=COLORS['LIGHT'])
            c3_frame.pack(fill=tk.X, pady=1)

            tk.Label(c3_frame, text="3", font=("Segoe UI", 7, "bold"),
                    fg='white', bg=c3_color, padx=2).pack(side=tk.LEFT)
            tk.Label(c3_frame, text=f"IMB: {c3_doublons}+{c3_motif_ok}={c3_errors}",
                    font=("Segoe UI", 7), fg=COLORS['TEXT_PRIMARY'],
                    bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

            # Critère 4
            critere_4 = results.get('critere_4', {})
            c4_errors = critere_4.get('total_ad_a_analyser', 0)
            c4_color = COLORS['SUCCESS'] if c4_errors == 0 else COLORS['ERROR']
            c4_frame = tk.Frame(details_content, bg=COLORS['LIGHT'])
            c4_frame.pack(fill=tk.X, pady=1)

            tk.Label(c4_frame, text="4", font=("Segoe UI", 7, "bold"),
                    fg='white', bg=c4_color, padx=2).pack(side=tk.LEFT)
            tk.Label(c4_frame, text=f"AD à analyser: {c4_errors}",
                    font=("Segoe UI", 7), fg=COLORS['TEXT_PRIMARY'],
                    bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(3, 0))

            # Informations contextuelles ultra-compactes
            context_frame = tk.Frame(self.results_frame, bg=COLORS['CARD'])
            context_frame.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

            context_text = f"📅 {summary.get('analysis_date', 'N/A')[:16]}\n"
            context_text += f"📊 Taux erreur: {self._calculate_error_percentage():.1f}%\n"
            context_text += f"📄 Rapport: 3 feuilles vides prêtes"

            tk.Label(context_frame, text=context_text, font=("Segoe UI", 7),
                    fg=COLORS['TEXT_SECONDARY'], bg=COLORS['CARD'],
                    justify=tk.LEFT).pack(expand=True)

        except Exception as e:
            self.logger.error(f"Erreur affichage résultats compacts: {e}")
            # Fallback simple
            tk.Label(self.results_frame, text="❌ Erreur affichage",
                    font=("Segoe UI", 8), fg=COLORS['ERROR'],
                    bg=COLORS['CARD']).pack(expand=True)

    def _create_summary_card(self, summary: Dict[str, Any], total_errors: int):
        """Crée la carte de résumé principal."""
        from ui.styles import create_card_frame

        summary_card = create_card_frame(self.results_frame, shadow=True)
        summary_card.pack(fill=tk.X, pady=(0, 10))

        card_content = summary_card.winfo_children()[0] if summary_card.winfo_children() else summary_card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.X, padx=20, pady=15)

        # En-tête avec statut
        header_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X, pady=(0, 10))

        status_icon = "✅" if total_errors == 0 else "⚠️" if total_errors < 5 else "❌"
        status_color = COLORS['SUCCESS'] if total_errors == 0 else COLORS['WARNING'] if total_errors < 5 else COLORS['ERROR']

        tk.Label(
            header_frame,
            text=status_icon,
            font=("Segoe UI", 20),
            fg=status_color,
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text=f"Analyse Terminée - {total_errors} erreur(s) détectée(s)",
            font=UIConfig.FONT_CARD_TITLE,
            fg=status_color,
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Métriques
        metrics_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        metrics_frame.pack(fill=tk.X)
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)

        # Pourcentage d'erreur
        error_percentage = self._calculate_error_percentage()
        self._create_metric_display(metrics_frame, 0, 0, "📊", "Taux d'erreur", f"{error_percentage:.1f}%")

        # Date d'analyse
        analysis_date = summary.get('analysis_date', 'N/A')
        self._create_metric_display(metrics_frame, 0, 1, "📅", "Date d'analyse", analysis_date)

    def _create_metric_display(self, parent: tk.Widget, row: int, col: int,
                              icon: str, label: str, value: str):
        """Crée un affichage de métrique."""
        metric_frame = tk.Frame(parent, bg=COLORS['LIGHT'], relief='flat', bd=1)
        metric_frame.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        metric_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        content = tk.Frame(metric_frame, bg=COLORS['LIGHT'])
        content.pack(fill=tk.X, padx=10, pady=8)

        # Icône et label
        header = tk.Frame(content, bg=COLORS['LIGHT'])
        header.pack(fill=tk.X)

        tk.Label(header, text=icon, font=("Segoe UI", 12),
                fg=COLORS['SECONDARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT)

        tk.Label(header, text=label, font=UIConfig.FONT_SMALL,
                fg=COLORS['TEXT_SECONDARY'], bg=COLORS['LIGHT']).pack(side=tk.LEFT, padx=(5, 0))

        # Valeur
        tk.Label(content, text=value, font=UIConfig.FONT_SUBTITLE,
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['LIGHT']).pack(anchor=tk.W, pady=(3, 0))

    def _create_criteria_results_cards(self, critere_0: Dict[str, Any], critere_2: Dict[str, Any], critere_3: Dict[str, Any], critere_4: Dict[str, Any]):
        """Crée les cartes de résultats par critère."""
        from ui.styles import create_card_frame

        # Conteneur pour les cartes de critères
        criteria_container = tk.Frame(self.results_frame, bg=COLORS['CARD'])
        criteria_container.pack(fill=tk.X, pady=(0, 10))
        criteria_container.grid_columnconfigure(0, weight=1)
        criteria_container.grid_columnconfigure(1, weight=1)
        criteria_container.grid_columnconfigure(2, weight=1)
        criteria_container.grid_columnconfigure(3, weight=1)

        # Carte Critère 0 - Écart Plan Adressage
        self._create_single_criteria_card(criteria_container, 0, 0, "0", "Écart Plan Adressage",
                                         critere_0.get('total_incoherences', 0),
                                         critere_0.get('incoherences', []))

        # Carte Critère 2 - Oubli Tickets
        self._create_single_criteria_card(criteria_container, 0, 1, "2", "Oubli Tickets",
                                         critere_2.get('total_errors', 0),
                                         critere_2.get('errors', []))

        # Carte Critère 3 - Contrôle IMB
        total_c3_errors = critere_3.get('total_erreurs_detectees', 0)
        all_c3_details = critere_3.get('doublons_details', [])
        self._create_single_criteria_card(criteria_container, 0, 2, "3", "Contrôle IMB",
                                         total_c3_errors, all_c3_details)

        # Carte Critère 4 - AD à Analyser
        total_c4_errors = critere_4.get('total_ad_a_analyser', 0)
        all_c4_details = critere_4.get('ad_a_analyser_entries', [])
        self._create_single_criteria_card(criteria_container, 0, 3, "4", "AD à Analyser",
                                         total_c4_errors, all_c4_details)

    def _create_single_criteria_card(self, parent: tk.Widget, row: int, col: int,
                                    number: str, title: str, count: int, details: list):
        """Crée une carte pour un critère spécifique."""
        from ui.styles import create_card_frame

        card = create_card_frame(parent, shadow=True)
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        card_content = card.winfo_children()[0] if card.winfo_children() else card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # En-tête
        header_frame = tk.Frame(content_frame, bg=COLORS['CARD'])
        header_frame.pack(fill=tk.X, pady=(0, 8))

        # Badge
        badge_color = COLORS['SUCCESS'] if count == 0 else COLORS['WARNING'] if count < 3 else COLORS['ERROR']
        badge = tk.Label(
            header_frame,
            text=f"CRITÈRE {number}",
            font=("Segoe UI", 8, "bold"),
            fg='white',
            bg=badge_color,
            padx=6,
            pady=2
        )
        badge.pack(side=tk.LEFT)

        # Titre
        tk.Label(
            header_frame,
            text=title,
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['TEXT_PRIMARY'],
            bg=COLORS['CARD']
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Compteur
        count_color = COLORS['SUCCESS'] if count == 0 else COLORS['ERROR']
        tk.Label(
            content_frame,
            text=f"{count} erreur(s) détectée(s)",
            font=UIConfig.FONT_CARD_SUBTITLE,
            fg=count_color,
            bg=COLORS['CARD']
        ).pack(anchor=tk.W, pady=(0, 5))

        # Détails spécifiques pour le Critère 0 (Écart Plan Adressage)
        if number == "0" and details and count > 0:
            # Afficher les écarts détectés
            ecarts_text = "Écarts détectés:\n"
            for detail in details[:3]:  # Limiter à 3 exemples
                motif = detail.get('motif', 'N/A')
                suivi = detail.get('suivi_count', 0)
                qgis = detail.get('qgis_count', 0)
                diff = detail.get('difference', 0)
                ecarts_text += f"• {motif}: {suivi} vs {qgis} ({diff:+d})\n"

            if len(details) > 3:
                ecarts_text += f"... et {len(details) - 3} autre(s) écart(s)"

            details_label = tk.Label(
                content_frame,
                text=ecarts_text.strip(),
                font=UIConfig.FONT_SMALL,
                fg=COLORS['TEXT_SECONDARY'],
                bg=COLORS['CARD'],
                justify=tk.LEFT
            )
            details_label.pack(anchor=tk.W, pady=(5, 0))

        # Détails spécifiques pour le Critère 2 (Oubli Tickets)
        elif number == "2":
            # Récupérer les statuts des tickets depuis les résultats
            if hasattr(self, 'qc_results') and self.qc_results and 'critere_2' in self.qc_results:
                critere_2 = self.qc_results['critere_2']
                ticket_upr_status = critere_2.get('ticket_upr_status', 'N/A')
                ticket_501_511_status = critere_2.get('ticket_501_511_status', 'N/A')

                # Afficher les statuts des tickets
                tickets_text = f"Statuts des tickets:\n"
                tickets_text += f"• Ticket UPR: {ticket_upr_status}\n"
                tickets_text += f"• Ticket 501/511: {ticket_501_511_status}"

                # Couleur selon les statuts
                status_color = COLORS['SUCCESS']
                if ticket_upr_status == 'NOK' or ticket_501_511_status == 'NOK':
                    status_color = COLORS['ERROR']
                elif ticket_upr_status == 'N/A' and ticket_501_511_status == 'N/A':
                    status_color = COLORS['TEXT_SECONDARY']

                tickets_label = tk.Label(
                    content_frame,
                    text=tickets_text,
                    font=UIConfig.FONT_SMALL,
                    fg=status_color,
                    bg=COLORS['CARD'],
                    justify=tk.LEFT
                )
                tickets_label.pack(anchor=tk.W, pady=(5, 0))

                # Afficher les erreurs détectées si présentes
                if details and count > 0:
                    errors_text = "\nErreurs détectées:\n"
                    for detail in details[:2]:  # Limiter à 2 exemples
                        error_type = detail.get('type', 'N/A')
                        description = detail.get('description', 'N/A')
                        if error_type == 'TICKET_UPR_MANQUANT':
                            errors_text += "• Ticket UPR manquant\n"
                        elif error_type == 'TICKET_501_511_MANQUANT':
                            errors_text += "• Ticket 501/511 manquant\n"

                    if len(details) > 2:
                        errors_text += f"... et {len(details) - 2} autre(s) erreur(s)"

                    errors_label = tk.Label(
                        content_frame,
                        text=errors_text.strip(),
                        font=UIConfig.FONT_SMALL,
                        fg=COLORS['ERROR'],
                        bg=COLORS['CARD'],
                        justify=tk.LEFT
                    )
                    errors_label.pack(anchor=tk.W, pady=(2, 0))

        # Détails génériques pour les autres critères
        elif details and count > 0:
            details_text = f"Exemples: {len(details[:3])} élément(s) affichés"
            if len(details) > 3:
                details_text += f" (+ {len(details) - 3} autres)"

            tk.Label(
                content_frame,
                text=details_text,
                font=UIConfig.FONT_SMALL,
                fg=COLORS['TEXT_SECONDARY'],
                bg=COLORS['CARD']
            ).pack(anchor=tk.W)

    def _create_context_info_card(self, summary: Dict[str, Any]):
        """Crée la carte d'informations de contexte."""
        from ui.styles import create_card_frame

        context_card = create_card_frame(self.results_frame, shadow=True)
        context_card.pack(fill=tk.X)

        card_content = context_card.winfo_children()[0] if context_card.winfo_children() else context_card
        content_frame = tk.Frame(card_content, bg=COLORS['CARD'])
        content_frame.pack(fill=tk.X, padx=20, pady=15)

        # Titre
        tk.Label(
            content_frame,
            text="📋 Informations de Contexte",
            font=UIConfig.FONT_CARD_TITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        ).pack(anchor=tk.W, pady=(0, 10))

        # Grille d'informations
        info_grid = tk.Frame(content_frame, bg=COLORS['CARD'])
        info_grid.pack(fill=tk.X)
        info_grid.grid_columnconfigure(0, weight=1)
        info_grid.grid_columnconfigure(1, weight=1)

        # Informations
        self._create_context_item(info_grid, 0, 0, "🏘️", "Commune", summary.get('commune', 'N/A'))
        self._create_context_item(info_grid, 0, 1, "👤", "Collaborateur", summary.get('collaborateur', 'N/A'))
        self._create_context_item(info_grid, 1, 0, "🏛️", "Code INSEE", summary.get('insee', 'N/A'))
        self._create_context_item(info_grid, 1, 1, "🆔", "ID Tâche", summary.get('id_tache', 'N/A'))

    def _create_context_item(self, parent: tk.Widget, row: int, col: int,
                            icon: str, label: str, value: str):
        """Crée un élément d'information de contexte."""
        item_frame = tk.Frame(parent, bg=COLORS['CARD'])
        item_frame.grid(row=row, column=col, sticky="w", padx=10, pady=3)

        # Icône et label
        header = tk.Frame(item_frame, bg=COLORS['CARD'])
        header.pack(anchor=tk.W)

        tk.Label(header, text=icon, font=("Segoe UI", 10),
                fg=COLORS['SECONDARY'], bg=COLORS['CARD']).pack(side=tk.LEFT)

        tk.Label(header, text=f"{label}:", font=UIConfig.FONT_SMALL,
                fg=COLORS['TEXT_SECONDARY'], bg=COLORS['CARD']).pack(side=tk.LEFT, padx=(3, 0))

        # Valeur
        tk.Label(item_frame, text=value, font=UIConfig.FONT_SUBTITLE,
                fg=COLORS['TEXT_PRIMARY'], bg=COLORS['CARD']).pack(anchor=tk.W, pady=(2, 0))

    def show(self):
        """Affiche le module."""
        if self.main_frame:
            self.main_frame.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        """Cache le module."""
        if self.main_frame:
            self.main_frame.grid_forget()

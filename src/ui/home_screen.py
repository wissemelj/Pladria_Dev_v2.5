"""
Home screen for the Suivi Generator platform.
Central navigation hub for all application features.
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Optional

from config.constants import COLORS, UIConfig, AppInfo
from ui.styles import create_card_frame, create_section_header, create_sofrecom_card
from ui.navigation import NavigationState

logger = logging.getLogger(__name__)


class HomeScreen:
    """Home screen with feature navigation."""
    
    def __init__(self, parent: tk.Widget, navigation_manager=None):
        """
        Initialize the home screen.
        
        Args:
            parent: Parent widget
            navigation_manager: Navigation manager instance
        """
        self.parent = parent
        self.navigation_manager = navigation_manager
        self.logger = logging.getLogger(__name__)
        
        self._create_home_screen()
    
    def _create_home_screen(self):
        """Create the home screen interface."""
        # Main container
        main_container = tk.Frame(self.parent, bg=COLORS['BG'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome section
        self._create_welcome_section(main_container)
        
        # Features grid
        self._create_features_section(main_container)
        
        # Quick stats/info section
        self._create_info_section(main_container)
    
    def _create_welcome_section(self, parent: tk.Widget):
        """Create the welcome section - Sofrecom inspired, compact."""
        # Hero section with gradient-like background - COMPACT
        hero_frame = tk.Frame(parent, bg=COLORS['ACCENT'], relief='flat', bd=0)
        hero_frame.pack(fill=tk.X, pady=(0, 20))  # Reduced padding

        # Add subtle border
        hero_frame.config(highlightbackground=COLORS['PRIMARY'], highlightthickness=1)

        # Welcome content - COMPACT
        welcome_content = tk.Frame(hero_frame, bg=COLORS['ACCENT'])
        welcome_content.pack(fill=tk.X, padx=30, pady=20)  # Reduced padding

        # Main title with Sofrecom logo - COMPACT
        title_frame = tk.Frame(welcome_content, bg=COLORS['ACCENT'])
        title_frame.pack(anchor=tk.W, pady=(0, 5))

        # Try to load Sofrecom logo for title
        try:
            from utils.file_utils import get_resource_path
            from PIL import Image, ImageTk
            import os

            logo_path = get_resource_path("logo_Sofrecom.png")
            if os.path.exists(logo_path):
                # Load and resize logo for title - ENLARGED
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((120, 36), Image.Resampling.LANCZOS)  # Much larger logo
                logo_photo = ImageTk.PhotoImage(logo_image)

                logo_label = tk.Label(
                    title_frame,
                    image=logo_photo,
                    bg=COLORS['ACCENT']
                )
                logo_label.image = logo_photo  # Keep a reference
                logo_label.pack(side=tk.LEFT, padx=(0, 15))  # More spacing

        except Exception as e:
            # Fallback to icon if logo fails - ENLARGED
            logo_fallback = tk.Label(
                title_frame,
                text="🔷",
                font=("Segoe UI", 24),  # Larger fallback icon
                fg=COLORS['PRIMARY'],
                bg=COLORS['ACCENT']
            )
            logo_fallback.pack(side=tk.LEFT, padx=(0, 15))  # More spacing

        # Main title text - ENLARGED
        title_label = tk.Label(
            title_frame,
            text="Pladria",
            font=UIConfig.FONT_LARGE,  # Back to large font for prominence
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        title_label.pack(side=tk.LEFT)

        # Subtitle with professional styling - COMPACT
        subtitle_label = tk.Label(
            welcome_content,
            text="Solutions de traitement et génération de données",
            font=UIConfig.FONT_SUBTITLE,  # Reduced size
            fg=COLORS['INFO'],
            bg=COLORS['ACCENT']
        )
        subtitle_label.pack(anchor=tk.W, pady=(5, 15))  # Reduced padding

        # Description with better typography - COMPACT
        description_label = tk.Label(
            welcome_content,
            text="Bienvenue sur Pladria développé Pour l'activité CMS adr_Plan Adressage. ",
            font=UIConfig.FONT_SMALL,  # Reduced size
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['ACCENT'],
            wraplength=700,
            justify=tk.LEFT
        )
        description_label.pack(anchor=tk.W)

        # Add Sofrecom branding - COMPACT (text only)
        brand_frame = tk.Frame(welcome_content, bg=COLORS['ACCENT'])
        brand_frame.pack(anchor=tk.W, pady=(10, 0))  # Reduced padding

        # Team branding text only
        brand_label = tk.Label(
            brand_frame,
            text="Équipe Plan Adressage - Sofrecom Tunisie",
            font=("Segoe UI", 8, "bold"),  # Reduced font size
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        brand_label.pack(side=tk.LEFT)
    
    def _create_features_section(self, parent: tk.Widget):
        """Create the features/modules section - Sofrecom inspired, optimized."""
        # Section header - COMPACT
        header_frame = tk.Frame(parent, bg=COLORS['BG'])
        header_frame.pack(fill=tk.X, pady=(0, 15))  # Reduced padding

        header_label = tk.Label(
            header_frame,
            text="Modules",
            font=UIConfig.FONT_TITLE,  # Reduced from FONT_HEADER
            fg=COLORS['INFO'],
            bg=COLORS['BG']
        )
        header_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(
            header_frame,
            text="  Choisissez un module pour commencer",
            font=UIConfig.FONT_SMALL,  # Reduced size
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['BG']
        )
        subtitle_label.pack(anchor=tk.W, pady=(3, 0))  # Reduced padding

        # Features grid with Sofrecom cards - OPTIMIZED
        features_grid = tk.Frame(parent, bg=COLORS['BG'])
        features_grid.pack(fill=tk.BOTH, expand=True, pady=(0, 15))  # Reduced padding

        # Configure grid
        features_grid.grid_columnconfigure(0, weight=1)
        features_grid.grid_columnconfigure(1, weight=1)
        features_grid.grid_rowconfigure(0, weight=1)
        features_grid.grid_rowconfigure(1, weight=1)
        features_grid.grid_rowconfigure(2, weight=1)

        # Feature 1: Suivi Generator
        card1 = create_sofrecom_card(
            features_grid,
            title="Générateur De Suivi Production",
            subtitle="Un Fichier Excel Par Commune",
            icon="📊",
            clickable=True,
            command=self._open_suivi_generator
        )
        card1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Feature 2: Suivi Global Tickets
        card2 = create_sofrecom_card(
            features_grid,
            title="Suivi Global Tickets",
            subtitle="Générez et MàJ Votre Suivi Global Des Tickets",
            icon="🌐",
            clickable=True,
            command=self._open_suivi_global
        )
        card2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Feature 3: Team Statistics
        card3 = create_sofrecom_card(
            features_grid,
            title="Statistiques Équipe",
            subtitle="Jetez Un Coeup d'oeil Sur Les Performances Globales De L'équipe",
            icon="📈",
            clickable=True,
            command=self._open_team_stats
        )
        card3.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Feature 4: Data Viewer - Visualize global tickets data
        card4 = create_sofrecom_card(
            features_grid,
            title="Visualiseur de Données",
            subtitle="Visualisation des Données Global Tickets",
            icon="📊",
            clickable=True,
            command=self._open_data_viewer
        )
        card4.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Feature 5: Quality Control - New module
        card5 = create_sofrecom_card(
            features_grid,
            title="Contrôle Qualité",
            subtitle="Système d'Analyse et de Validation de la Qualité des Données",
            icon="🔍",
            clickable=True,
            command=self._open_quality_control
        )
        card5.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Teams link section
        teams_frame = tk.Frame(parent, bg=COLORS['BG'])
        teams_frame.pack(fill=tk.X, pady=(20, 0))

        teams_link = tk.Label(
            teams_frame,
            text="🗂️ Ouvrir Canal Teams",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG'],
            cursor="hand2"
        )
        teams_link.pack()

        # Bind click event
        teams_link.bind("<Button-1>", lambda e: self._open_teams_folder_directly())

        # Add hover effects
        def on_enter(event):
            teams_link.config(fg=COLORS['SECONDARY'])

        def on_leave(event):
            teams_link.config(fg=COLORS['PRIMARY'])

        teams_link.bind("<Enter>", on_enter)
        teams_link.bind("<Leave>", on_leave)



    def _create_info_section(self, parent: tk.Widget):
        """Create the information section - Sofrecom inspired, compact."""
        # Footer-style info section - COMPACT
        footer_frame = tk.Frame(parent, bg=COLORS['ACCENT'], relief='flat', bd=0)
        footer_frame.pack(fill=tk.X, pady=(15, 0))  # Reduced padding

        # Add subtle border
        footer_frame.config(highlightbackground=COLORS['BORDER'], highlightthickness=1)

        # Footer content - COMPACT
        footer_content = tk.Frame(footer_frame, bg=COLORS['ACCENT'])
        footer_content.pack(fill=tk.X, padx=30, pady=15)  # Reduced padding

        # Configure grid
        footer_content.grid_columnconfigure(0, weight=1)
        footer_content.grid_columnconfigure(1, weight=1)
        footer_content.grid_columnconfigure(2, weight=1)

        # Quick stats cards with modern styling
        self._create_modern_info_card(
            footer_content, 0, 0,
            "Version",
            AppInfo.VERSION,
            "Version actuelle",
            "🔖"
        )

        self._create_modern_info_card(
            footer_content, 0, 1,
            "Équipe",
            "Plan Adressage",
            "Développé par",
            "👥"
        )

        self._create_modern_info_card(
            footer_content, 0, 2,
            "Plateforme",
            "Pladria",
            "Solution complète",
            "🚀"
        )


    def _create_modern_info_card(self, parent: tk.Widget, row: int, col: int,
                                title: str, value: str, description: str, icon: str):
        """Create a modern information card."""
        # Card container
        card_container = tk.Frame(parent, bg=COLORS['ACCENT'])
        card_container.grid(row=row, column=col, sticky="ew", padx=15, pady=5)

        # Card content with horizontal layout
        content = tk.Frame(card_container, bg=COLORS['ACCENT'])
        content.pack(fill=tk.X)

        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 14),
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 12))

        # Text content
        text_frame = tk.Frame(content, bg=COLORS['ACCENT'])
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Title
        title_label = tk.Label(
            text_frame,
            text=title,
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['INFO'],
            bg=COLORS['ACCENT']
        )
        title_label.pack(anchor=tk.W)

        # Value
        value_label = tk.Label(
            text_frame,
            text=value,
            font=("Segoe UI", 9, "bold"),
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        value_label.pack(anchor=tk.W)

        # Description
        desc_label = tk.Label(
            text_frame,
            text=description,
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['ACCENT']
        )
        desc_label.pack(anchor=tk.W)
    
    def _open_suivi_generator(self):
        """Open the Suivi Generator module."""
        try:
            self.logger.info("User clicked Suivi Generator button")
            if self.navigation_manager:
                self.navigation_manager.navigate_to(NavigationState.SUIVI_GENERATOR)
            else:
                self.logger.error("Navigation manager not available")
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", "Gestionnaire de navigation non disponible")
        except Exception as e:
            self.logger.error(f"Error opening Suivi Generator: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le Générateur Suivi:\n{e}")

    def _open_suivi_global(self):
        """Open the Suivi Global Tickets module."""
        try:
            self.logger.info("User clicked Suivi Global Tickets button")
            if self.navigation_manager:
                self.navigation_manager.navigate_to(NavigationState.SUIVI_GLOBAL)
            else:
                self.logger.error("Navigation manager not available")
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", "Gestionnaire de navigation non disponible")
        except Exception as e:
            self.logger.error(f"Error opening Suivi Global Tickets: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le Suivi Global Tickets:\n{e}")

    def _open_team_stats(self):
        """Open the Team Statistics module."""
        try:
            self.logger.info("User clicked Team Statistics button")
            if self.navigation_manager:
                self.navigation_manager.navigate_to(NavigationState.TEAM_STATS)
            else:
                self.logger.error("Navigation manager not available")
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", "Gestionnaire de navigation non disponible")
        except Exception as e:
            self.logger.error(f"Error opening Team Statistics: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erreur", f"Impossible d'ouvrir les Statistiques Équipe:\n{e}")

    def _open_data_viewer(self):
        """Open the Data Viewer module."""
        try:
            if self.navigation_manager:
                self.navigation_manager.navigate_to(NavigationState.DATA_VIEWER)
            else:
                self.logger.error("Navigation manager not available")
        except Exception as e:
            self.logger.error(f"Error opening Data Viewer: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le Visualiseur de Données:\n{e}")

    def _open_quality_control(self):
        """Open the Quality Control module."""
        try:
            self.logger.info("User clicked Quality Control button")
            if self.navigation_manager:
                self.navigation_manager.navigate_to(NavigationState.QUALITY_CONTROL)
            else:
                self.logger.error("Navigation manager not available")
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur", "Gestionnaire de navigation non disponible")
        except Exception as e:
            self.logger.error(f"Error opening Quality Control: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le Contrôle Qualité:\n{e}")

    def _open_teams_folder_directly(self):
        """Open the Teams folder directly in Windows Explorer."""
        try:
            import subprocess
            import getpass
            import os
            import tkinter.messagebox as messagebox
            from config.constants import AccessControl

            self.logger.info("User clicked Teams folder button - opening directly")

            # Get dynamic Teams path using AccessControl (handles special cases like m.benali)
            username = getpass.getuser()
            teams_path = AccessControl.get_teams_path_for_user(username)

            if os.path.exists(teams_path):
                # Open in Windows Explorer (don't check return code as explorer can return non-zero even on success)
                subprocess.run(['explorer', teams_path])
                self.logger.info(f"Opened Teams folder: {teams_path}")
            else:
                self.logger.warning(f"Teams path does not exist: {teams_path}")
                messagebox.showerror(
                    "Dossier Teams Inaccessible",
                    f"Le dossier Teams n'existe pas ou n'est pas accessible:\n\n{teams_path}\n\n"
                    f"Utilisateur: {username}\n\n"
                    "Vérifiez que Microsoft Teams est synchronisé et que vous avez accès au canal."
                )

        except Exception as e:
            self.logger.error(f"Error opening Teams folder: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ouvrir le dossier Teams:\n\n{e}"
            )

    def refresh(self, **kwargs):
        """Refresh the home screen."""
        # Home screen doesn't need refreshing, but method is required for consistency
        pass

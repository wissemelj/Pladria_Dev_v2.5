"""
Modern Home screen for the Pladria platform.
Professional central navigation hub with modern UI design.
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Optional
import math
import time

from config.constants import COLORS, UIConfig, AppInfo
from ui.styles import create_card_frame, create_section_header, create_sofrecom_card
from ui.navigation import NavigationState

logger = logging.getLogger(__name__)


class HomeScreen:
    """Modern home screen with professional feature navigation."""

    def __init__(self, parent: tk.Widget, navigation_manager=None):
        """
        Initialize the modern home screen.

        Args:
            parent: Parent widget
            navigation_manager: Navigation manager instance
        """
        self.parent = parent
        self.navigation_manager = navigation_manager
        self.logger = logging.getLogger(__name__)

        # Animation and interaction state
        self.hover_animations = {}
        self.card_widgets = []

        self._create_modern_home_screen()
    
    def _create_modern_home_screen(self):
        """Create the modern home screen interface with professional design."""
        # Main scrollable container with modern styling - no padding
        self.main_container = tk.Frame(self.parent, bg=COLORS['BG'], bd=0, highlightthickness=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0, ipady=0, ipadx=0)

        # Create scrollable canvas for better UX - no padding
        self.canvas = tk.Canvas(self.main_container, bg=COLORS['BG'], highlightthickness=0, bd=0, relief='flat')
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS['BG'], bd=0, highlightthickness=0)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Ensure scrollable frame takes full width
        def configure_scrollable_frame(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas.find_all()[0], width=canvas_width)

        self.canvas.bind('<Configure>', configure_scrollable_frame)

        # Pack scrollable components - no padding
        self.canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0, ipady=0, ipadx=0)
        self.scrollbar.pack(side="right", fill="y")

        # Hero section first - absolutely full width without any padding
        self._create_modern_hero_section(self.scrollable_frame)

        # Content container with modern padding for other sections
        content_container = tk.Frame(self.scrollable_frame, bg=COLORS['BG'])
        content_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        # Modern features grid
        self._create_modern_features_section(content_container)

        # Footer section removed for cleaner interface

        # Bind mouse wheel to canvas
        self._bind_mousewheel()
    
    def _create_modern_hero_section(self, parent: tk.Widget):
        """Create a modern hero section with background image taking absolute full width."""
        # Get the root window to access full window width
        root_window = parent.winfo_toplevel()

        # Hero section taking absolute full width - no padding, no margins
        hero_card = tk.Frame(parent, relief='flat', bd=0, highlightthickness=0, bg=COLORS['BG'])
        hero_card.pack(fill=tk.X, pady=0, padx=0, ipady=0, ipadx=0)

        # Force the hero to extend beyond any container constraints
        hero_card.pack_propagate(False)

        # Ensure hero takes full parent width immediately
        def ensure_full_width():
            try:
                parent.update_idletasks()
                parent_width = parent.winfo_width()
                if parent_width > 1:
                    hero_card.configure(width=parent_width)
            except:
                pass

        parent.after(10, ensure_full_width)

        # Store reference to adjust width dynamically
        self.hero_card = hero_card

        # Set background image and get canvas
        canvas = self._set_hero_background(hero_card, root_window)

        if canvas:
            # Create content frame on the canvas - inherit canvas background
            hero_content = tk.Frame(canvas)
            # Make the frame transparent by not setting any background
            hero_content.configure(bg=canvas.cget('bg'))
            # Place the content frame on the canvas - centered horizontally and vertically
            canvas_window = canvas.create_window(100, 80, anchor=tk.NW, window=hero_content)

            # Function to center content when canvas resizes
            def center_content(event):
                canvas_width = event.width
                # Center the content horizontally with some left margin
                x_pos = max(50, (canvas_width - 800) // 2)  # 800px content width, min 50px margin
                canvas.coords(canvas_window, x_pos, 80)

            canvas.bind('<Configure>', center_content)
        else:
            # Fallback: create content frame directly on hero_card
            hero_content = tk.Frame(hero_card, bg=COLORS['PRIMARY'])
            hero_content.pack(fill=tk.X, padx=50, pady=40)

        # Create hero content
        self._create_hero_content(hero_content)

    def _create_hero_content(self, hero_content):
        """Create the content for the hero section."""
        # No content - just pure image background
        pass

    def _set_hero_background(self, hero_card, root_window=None):
        """Set the background image for the hero section."""
        try:
            from PIL import Image, ImageTk
            import os

            # Path to the background image
            background_path = os.path.join("src", "background.png")

            if os.path.exists(background_path):
                # Load the background image
                bg_image = Image.open(background_path)

                # Get actual window width for true full-width hero
                if root_window:
                    try:
                        # Get the actual window width
                        root_window.update_idletasks()
                        hero_width = max(1920, root_window.winfo_width())  # At least Full HD, or window width
                    except:
                        hero_width = 1920  # Fallback
                else:
                    hero_width = 1920  # Fallback

                hero_height = 400  # Even taller height for better visual impact

                # Resize image to fit hero section
                bg_image = bg_image.resize((hero_width, hero_height), Image.Resampling.LANCZOS)

                # Convert to PhotoImage
                self.hero_bg_photo = ImageTk.PhotoImage(bg_image)

                # Debug: Print image dimensions
                self.logger.info(f"Hero image resized to: {hero_width}x{hero_height}")

                # Set the background image directly on the hero card
                hero_card.configure(bg='white')  # Fallback color

                # Create a canvas to display the background image - absolute full width
                canvas = tk.Canvas(
                    hero_card,
                    highlightthickness=0,
                    bd=0,
                    relief='flat',
                    width=hero_width,
                    height=hero_height
                )
                canvas.pack(fill=tk.BOTH, expand=True, padx=0, pady=0, ipady=0, ipadx=0)

                # Force canvas to use the full width and height
                canvas.pack_propagate(False)

                # Ensure the hero_card has the right height
                hero_card.configure(height=hero_height)

                self.logger.info(f"Canvas created with dimensions: {hero_width}x{hero_height}")

                # Add the background image to the canvas, centered both horizontally and vertically
                image_id = canvas.create_image(hero_width//2, hero_height//2, anchor=tk.CENTER, image=self.hero_bg_photo)
                self.logger.info(f"Image added to canvas with ID: {image_id} at position ({hero_width//2}, {hero_height//2})")

                # Bind canvas resize to update image position and extend beyond scrollbar
                def on_canvas_configure(event):
                    canvas_width = event.width
                    # Get the actual window width to extend beyond scrollbar
                    try:
                        window_width = hero_card.winfo_toplevel().winfo_width()
                        # Extend canvas to full window width
                        canvas.configure(width=window_width)
                        # Center the image both horizontally and vertically
                        canvas.coords(canvas.find_all()[0], window_width//2, hero_height//2)
                    except:
                        # Fallback to canvas width
                        canvas.coords(canvas.find_all()[0], canvas_width//2, hero_height//2)

                canvas.bind('<Configure>', on_canvas_configure)

                # Also bind to window resize - with error handling
                def on_window_resize(event):
                    try:
                        # Check if widgets still exist
                        if not hero_card.winfo_exists():
                            return
                        if event.widget == hero_card.winfo_toplevel():
                            window_width = event.width
                            # Make sure canvas takes full window width
                            if canvas.winfo_exists():
                                canvas.configure(width=window_width)
                            # Update hero_card width as well
                            if hero_card.winfo_exists():
                                hero_card.configure(width=window_width)
                            if canvas.winfo_exists() and canvas.find_all():
                                canvas.coords(canvas.find_all()[0], window_width//2, hero_height//2)
                    except Exception as e:
                        # Silently ignore errors when widgets are destroyed
                        pass

                try:
                    hero_card.winfo_toplevel().bind('<Configure>', on_window_resize)
                except:
                    pass

                # Store canvas reference for content placement
                self.hero_canvas = canvas

                # Force initial width update after a short delay
                def update_initial_width():
                    try:
                        root = hero_card.winfo_toplevel()
                        root.update_idletasks()
                        window_width = root.winfo_width()
                        if window_width > 1:  # Valid width
                            canvas.configure(width=window_width)
                            hero_card.configure(width=window_width)
                            if canvas.find_all():
                                canvas.coords(canvas.find_all()[0], window_width//2, hero_height//2)
                    except:
                        pass

                # Schedule the width update
                hero_card.after(100, update_initial_width)

                self.logger.info("Background image loaded successfully on canvas")
                return canvas

            else:
                # Fallback to solid color if image not found
                hero_card.configure(bg=COLORS['PRIMARY'])
                self.logger.warning(f"Background image not found at {background_path}, using solid color")
                return None

        except Exception as e:
            # Fallback to solid color if any error occurs
            hero_card.configure(bg=COLORS['PRIMARY'])
            self.logger.error(f"Error loading background image: {e}")
            return None
    
    def _create_modern_features_section(self, parent: tk.Widget):
        """Create modern features section with professional card design."""
        # Modern section header
        header_section = tk.Frame(parent, bg=COLORS['BG'])
        header_section.pack(fill=tk.X, pady=(0, 30))

        # Section title with modern typography
        title_frame = tk.Frame(header_section, bg=COLORS['BG'])
        title_frame.pack(anchor=tk.W)

        header_label = tk.Label(
            title_frame,
            text="Modules Disponibles",
            font=("Segoe UI", 22, "bold"),
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        header_label.pack(side=tk.LEFT)

        # Modern accent line
        accent_line = tk.Frame(title_frame, bg=COLORS['SECONDARY'], height=4, width=60)
        accent_line.pack(side=tk.LEFT, padx=(15, 0), anchor=tk.CENTER)

        subtitle_label = tk.Label(
            header_section,
            text="Sélectionnez un module pour accéder aux fonctionnalités avancées",
            font=("Segoe UI", 12),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['BG']
        )
        subtitle_label.pack(anchor=tk.W, pady=(8, 0))

        # Modern features grid with enhanced cards
        features_container = tk.Frame(parent, bg=COLORS['BG'])
        features_container.pack(fill=tk.BOTH, expand=True, pady=(0, 30))

        # Configure horizontal grid (5 columns, 1 row)
        for i in range(5):
            features_container.grid_columnconfigure(i, weight=1)
        features_container.grid_rowconfigure(0, weight=1)

        # Modern feature cards with enhanced design
        modules_data = [
            {
                'title': 'Générateur Suivi Production',
                'subtitle': 'Génération automatisée de fichiers Excel par commune',
                'icon': '📊',
                'color': COLORS['PRIMARY'],
                'command': self._open_suivi_generator,
                'features': ['Excel automatisé', 'Multi-communes', 'Templates avancés']
            },
            {
                'title': 'Suivi Global Tickets',
                'subtitle': 'Gestion centralisée et mise à jour du suivi global',
                'icon': '🌐',
                'color': COLORS['SUCCESS'],
                'command': self._open_suivi_global,
                'features': ['Vue globale', 'Synchronisation', 'Reporting avancé']
            },
            {
                'title': 'Statistiques Équipe',
                'subtitle': 'Analyse des performances et métriques d\'équipe',
                'icon': '📈',
                'color': COLORS['SECONDARY'],
                'command': self._open_team_stats,
                'features': ['Analytics avancés', 'Tableaux de bord', 'KPIs temps réel']
            },
            {
                'title': 'Visualiseur de Données',
                'subtitle': 'Exploration interactive des données Global Tickets',
                'icon': '📊',
                'color': COLORS['INFO'],
                'command': self._open_data_viewer,
                'features': ['Visualisation interactive', 'Filtres avancés', 'Export données']
            },
            {
                'title': 'Contrôle Qualité',
                'subtitle': 'Système d\'analyse et validation qualité des données',
                'icon': '🔍',
                'color': COLORS['DANGER'],
                'command': self._open_quality_control,
                'features': ['Validation automatique', 'Rapports qualité', 'Analyses critères'],
                'span': True
            }
        ]

        # Create modern cards in horizontal layout
        for i, module in enumerate(modules_data):
            card = self._create_modern_feature_card(
                features_container,
                module['title'],
                module['subtitle'],
                module['icon'],
                module['color'],
                module['command'],
                module['features']
            )

            # Place all cards in a single row
            card.grid(row=0, column=i, sticky="nsew", padx=8, pady=15)
            self.card_widgets.append(card)

        # Modern Teams access section
        self._create_modern_teams_section(parent)

    def _create_modern_feature_card(self, parent, title, subtitle, icon, color, command, features):
        """Create a modern feature card with enhanced design and animations."""
        # Card container with shadow effect
        card_container = tk.Frame(parent, bg=COLORS['BG'])

        # Main card with modern styling
        card = tk.Frame(card_container, bg=COLORS['WHITE'], relief='flat', bd=0)
        card.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Add shadow effect
        shadow = tk.Frame(card_container, bg='#E0E0E0', height=2)
        shadow.pack(fill=tk.X, side=tk.BOTTOM)

        # Card header with colored accent
        header = tk.Frame(card, bg=color, height=6)
        header.pack(fill=tk.X)

        # Card content with smaller padding for horizontal layout
        content = tk.Frame(card, bg=COLORS['WHITE'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Icon and title section with smaller spacing
        title_section = tk.Frame(content, bg=COLORS['WHITE'])
        title_section.pack(fill=tk.X, pady=(0, 10))

        # Smaller modern icon for horizontal layout
        icon_label = tk.Label(
            title_section,
            text=icon,
            font=("Segoe UI", 24),
            fg=color,
            bg=COLORS['WHITE']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))

        # Title and subtitle
        text_section = tk.Frame(title_section, bg=COLORS['WHITE'])
        text_section.pack(side=tk.LEFT, fill=tk.X, expand=True)

        title_label = tk.Label(
            text_section,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg=COLORS['TEXT_PRIMARY'],
            bg=COLORS['WHITE'],
            anchor=tk.W
        )
        title_label.pack(fill=tk.X)

        subtitle_label = tk.Label(
            text_section,
            text=subtitle,
            font=("Segoe UI", 8),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['WHITE'],
            anchor=tk.W,
            wraplength=180,
            justify=tk.LEFT
        )
        subtitle_label.pack(fill=tk.X, pady=(3, 0))

        # Features list with smaller text
        features_frame = tk.Frame(content, bg=COLORS['WHITE'])
        features_frame.pack(fill=tk.X, pady=(8, 12))

        for feature in features:
            feature_label = tk.Label(
                features_frame,
                text=f"• {feature}",
                font=("Segoe UI", 7),
                fg=COLORS['INFO'],
                bg=COLORS['WHITE'],
                anchor=tk.W
            )
            feature_label.pack(fill=tk.X, pady=1)

        # Action button
        button_frame = tk.Frame(content, bg=COLORS['WHITE'])
        button_frame.pack(fill=tk.X)

        action_button = tk.Button(
            button_frame,
            text="Ouvrir",
            font=("Segoe UI", 8, "bold"),
            bg=color,
            fg=COLORS['WHITE'],
            relief='flat',
            bd=0,
            padx=15,
            pady=6,
            cursor='hand2',
            command=command
        )
        action_button.pack(anchor=tk.E)

        # Add hover effects
        self._add_card_hover_effects(card_container, card, action_button, color)

        return card_container

    def _add_card_hover_effects(self, container, card, button, color):
        """Add modern hover effects to cards."""
        def on_enter(event):
            card.config(bg=COLORS['CARD_HOVER'])
            container.config(bg=COLORS['ACCENT'])
            button.config(bg=self._darken_color(color))

        def on_leave(event):
            card.config(bg=COLORS['WHITE'])
            container.config(bg=COLORS['BG'])
            button.config(bg=color)

        # Bind to all card elements
        for widget in [container, card]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e: button.invoke())

    def _darken_color(self, color):
        """Darken a color for hover effects."""
        color_map = {
            COLORS['PRIMARY']: COLORS['PRIMARY_DARK'],
            COLORS['SUCCESS']: '#1E7E34',
            COLORS['SECONDARY']: '#E55A00',
            COLORS['INFO']: '#343A40',
            COLORS['DANGER']: '#C82333'
        }
        return color_map.get(color, color)

    def _add_shadow_effect(self, container, element):
        """Add shadow effect to elements."""
        shadow1 = tk.Frame(container, bg='#F0F0F0', height=1)
        shadow1.pack(fill=tk.X, pady=(11, 0))

        shadow2 = tk.Frame(container, bg='#E8E8E8', height=1)
        shadow2.pack(fill=tk.X)

    def _create_modern_teams_section(self, parent):
        """Create modern Teams access section."""
        teams_container = tk.Frame(parent, bg=COLORS['BG'])
        teams_container.pack(fill=tk.X, pady=(20, 0))

        # Modern Teams card
        teams_card = tk.Frame(teams_container, bg=COLORS['ACCENT'], relief='flat', bd=0)
        teams_card.pack(fill=tk.X, padx=20, pady=10)

        teams_content = tk.Frame(teams_card, bg=COLORS['ACCENT'])
        teams_content.pack(fill=tk.X, padx=30, pady=20)

        # Teams icon and text
        teams_header = tk.Frame(teams_content, bg=COLORS['ACCENT'])
        teams_header.pack(fill=tk.X)

        teams_icon = tk.Label(
            teams_header,
            text="🗂️",
            font=("Segoe UI", 24),
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        teams_icon.pack(side=tk.LEFT, padx=(0, 15))

        teams_text_frame = tk.Frame(teams_header, bg=COLORS['ACCENT'])
        teams_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        teams_title = tk.Label(
            teams_text_frame,
            text="Accès Direct au Canal Teams",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        teams_title.pack(anchor=tk.W)

        teams_subtitle = tk.Label(
            teams_text_frame,
            text="Ouvrir le dossier Teams synchronisé pour accéder aux fichiers partagés",
            font=("Segoe UI", 8),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['ACCENT']
        )
        teams_subtitle.pack(anchor=tk.W, pady=(2, 0))

        # Modern Teams button
        teams_button = tk.Button(
            teams_header,
            text="Ouvrir Teams",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['PRIMARY'],
            fg=COLORS['WHITE'],
            relief='flat',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self._open_teams_folder_directly
        )
        teams_button.pack(side=tk.RIGHT, padx=(20, 0))

        # Add hover effect to Teams button
        def on_teams_enter(event):
            teams_button.config(bg=COLORS['PRIMARY_DARK'])

        def on_teams_leave(event):
            teams_button.config(bg=COLORS['PRIMARY'])

        teams_button.bind("<Enter>", on_teams_enter)
        teams_button.bind("<Leave>", on_teams_leave)



    def _create_modern_footer_section(self, parent: tk.Widget):
        """Create modern footer section with enhanced information display."""
        # Modern footer container
        footer_container = tk.Frame(parent, bg=COLORS['BG'])
        footer_container.pack(fill=tk.X, pady=(30, 0))

        # Footer card with modern design
        footer_card = tk.Frame(footer_container, bg=COLORS['LIGHT'], relief='flat', bd=0)
        footer_card.pack(fill=tk.X, padx=20, pady=10)

        # Footer content
        footer_content = tk.Frame(footer_card, bg=COLORS['LIGHT'])
        footer_content.pack(fill=tk.X, padx=40, pady=25)

        # Configure responsive grid
        footer_content.grid_columnconfigure(0, weight=1)
        footer_content.grid_columnconfigure(1, weight=1)
        footer_content.grid_columnconfigure(2, weight=1)
        footer_content.grid_columnconfigure(3, weight=1)

        # Modern info cards with enhanced design
        info_data = [
            {
                'title': 'Version',
                'value': AppInfo.VERSION,
                'description': 'Version actuelle',
                'icon': '🔖',
                'color': COLORS['PRIMARY']
            },
            {
                'title': 'Équipe',
                'value': 'Plan Adressage',
                'description': 'Développé par',
                'icon': '👥',
                'color': COLORS['SUCCESS']
            },
            {
                'title': 'Plateforme',
                'value': 'Pladria',
                'description': 'Solution complète',
                'icon': '🚀',
                'color': COLORS['SECONDARY']
            },
            {
                'title': 'Statut',
                'value': 'Opérationnel',
                'description': 'Système actif',
                'icon': '✅',
                'color': COLORS['SUCCESS']
            }
        ]

        for i, info in enumerate(info_data):
            self._create_enhanced_info_card(
                footer_content, 0, i,
                info['title'], info['value'], info['description'],
                info['icon'], info['color']
            )

    def _create_enhanced_info_card(self, parent: tk.Widget, row: int, col: int,
                                  title: str, value: str, description: str,
                                  icon: str, color: str):
        """Create an enhanced modern information card."""
        # Card container with modern styling
        card_container = tk.Frame(parent, bg=COLORS['LIGHT'])
        card_container.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)

        # Card content with vertical layout
        content = tk.Frame(card_container, bg=COLORS['LIGHT'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Icon with colored background
        icon_frame = tk.Frame(content, bg=color, width=50, height=50)
        icon_frame.pack(pady=(0, 10))
        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=("Segoe UI", 14),
            fg=COLORS['WHITE'],
            bg=color
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Value (main text)
        value_label = tk.Label(
            content,
            text=value,
            font=("Segoe UI", 10, "bold"),
            fg=COLORS['TEXT_PRIMARY'],
            bg=COLORS['LIGHT']
        )
        value_label.pack(pady=(0, 2))

        # Title
        title_label = tk.Label(
            content,
            text=title,
            font=("Segoe UI", 8),
            fg=color,
            bg=COLORS['LIGHT']
        )
        title_label.pack(pady=(0, 2))

        # Description
        desc_label = tk.Label(
            content,
            text=description,
            font=("Segoe UI", 7),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['LIGHT']
        )
        desc_label.pack()

    def _bind_mousewheel(self):
        """Bind mouse wheel scrolling to canvas."""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")

        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)
    
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

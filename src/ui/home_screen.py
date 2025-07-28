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
        hero_card = tk.Frame(parent, relief='flat', bd=0, highlightthickness=0, bg=COLORS['BG'], height=400)
        hero_card.pack(fill=tk.X, pady=0, padx=0, ipady=0, ipadx=0)
        hero_card.pack_propagate(False)  # Maintain fixed height

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
            # Add overlay content on the background image with a small delay
            canvas.after(100, lambda: self._create_hero_overlay_content(canvas, hero_card))

        else:
            # Fallback: create content frame directly on hero_card
            hero_content = tk.Frame(hero_card, bg=COLORS['PRIMARY'])
            hero_content.pack(fill=tk.X, padx=50, pady=40)
            # Create hero content for fallback only
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

            # Path to the background image - check multiple locations
            import os
            current_dir = os.getcwd()
            self.logger.info(f"Current working directory: {current_dir}")

            background_paths = [
                "Background.png",  # Root directory
                "../Background.png",  # Parent directory (since we're in src)
                os.path.join("..", "Background.png"),  # Explicit parent
                os.path.join("src", "background.png"),  # Original location
                "background.png"  # Current directory fallback
            ]

            background_path = None
            for path in background_paths:
                abs_path = os.path.abspath(path)
                self.logger.info(f"Checking background path: {path} -> {abs_path} (exists: {os.path.exists(path)})")
                if os.path.exists(path):
                    background_path = path
                    self.logger.info(f"Found background image at: {background_path}")
                    break

            if background_path and os.path.exists(background_path):
                self.logger.info(f"Loading background image from: {background_path}")
                # Load the background image
                bg_image = Image.open(background_path)
                self.logger.info(f"Image loaded successfully. Original size: {bg_image.size}")

                # Get the original image dimensions
                img_width, img_height = bg_image.size
                self.logger.info(f"Original image size: {img_width}x{img_height}")

                # Get actual window dimensions for full coverage
                if root_window:
                    try:
                        # Get the actual window dimensions
                        root_window.update_idletasks()
                        window_width = root_window.winfo_width()
                        window_height = root_window.winfo_height()

                        # Leave 15cm (approximately 567px at 96 DPI) for content below
                        cm_to_pixels = 567  # 15 cm ≈ 567 pixels at standard 96 DPI
                        max_hero_height = window_height - cm_to_pixels

                        # Use full window dimensions for target area
                        target_width = window_width
                        target_height = max_hero_height

                        # Calculate scaling to fill entire area (crop to fill approach)
                        scale_x = target_width / img_width
                        scale_y = target_height / img_height
                        scale = max(scale_x, scale_y)  # Use larger scale to fill entire area

                        # Calculate new dimensions after scaling
                        scaled_width = int(img_width * scale)
                        scaled_height = int(img_height * scale)

                        # Resize image with scaling that fills the area
                        bg_image_scaled = bg_image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

                        # Crop to exact target dimensions if needed (center crop)
                        if scaled_width > target_width or scaled_height > target_height:
                            left = (scaled_width - target_width) // 2
                            top = (scaled_height - target_height) // 2
                            right = left + target_width
                            bottom = top + target_height
                            bg_image = bg_image_scaled.crop((left, top, right, bottom))
                        else:
                            bg_image = bg_image_scaled

                    except:
                        # Fallback: use window dimensions or defaults
                        target_width = window_width if window_width > 0 else 1400
                        target_height = (window_height - 567) if window_height > 567 else 600

                        # Apply same crop-to-fill logic for fallback
                        scale_x = target_width / img_width
                        scale_y = target_height / img_height
                        scale = max(scale_x, scale_y)

                        scaled_width = int(img_width * scale)
                        scaled_height = int(img_height * scale)
                        bg_image_scaled = bg_image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

                        if scaled_width > target_width or scaled_height > target_height:
                            left = (scaled_width - target_width) // 2
                            top = (scaled_height - target_height) // 2
                            right = left + target_width
                            bottom = top + target_height
                            bg_image = bg_image_scaled.crop((left, top, right, bottom))
                        else:
                            bg_image = bg_image_scaled
                else:
                    # Fallback: use window dimensions or defaults
                    target_width = window_width if window_width > 0 else 1400
                    target_height = (window_height - 567) if window_height > 567 else 600

                    # Apply same crop-to-fill logic for fallback
                    scale_x = target_width / img_width
                    scale_y = target_height / img_height
                    scale = max(scale_x, scale_y)

                    scaled_width = int(img_width * scale)
                    scaled_height = int(img_height * scale)
                    bg_image_scaled = bg_image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

                    if scaled_width > target_width or scaled_height > target_height:
                        left = (scaled_width - target_width) // 2
                        top = (scaled_height - target_height) // 2
                        right = left + target_width
                        bottom = top + target_height
                        bg_image = bg_image_scaled.crop((left, top, right, bottom))
                    else:
                        bg_image = bg_image_scaled

                # Store the PIL image for glassmorphism effects
                self.hero_image_pil = bg_image.copy()

                # Convert to PhotoImage
                self.hero_bg_photo = ImageTk.PhotoImage(bg_image)

                # Debug: Print image dimensions
                self.logger.info(f"Hero image processed to: {bg_image.width}x{bg_image.height} (crop-to-fill applied)")

                # Set the background image directly on the hero card
                hero_card.configure(bg='white')  # Fallback color

                # Create a canvas to display the background image - absolute full width
                canvas = tk.Canvas(
                    hero_card,
                    highlightthickness=0,
                    bd=0,
                    relief='flat',
                    width=target_width,
                    height=target_height,
                    bg='white'  # Set a background color to ensure visibility
                )
                canvas.pack(fill=tk.BOTH, expand=True, padx=0, pady=0, ipady=0, ipadx=0)

                # Force canvas to use the full width and height
                canvas.pack_propagate(False)

                # Ensure the hero_card has the right height
                hero_card.configure(height=target_height)

                self.logger.info(f"Canvas created with dimensions: {target_width}x{target_height}")

                # Add the background image to the canvas, centered both horizontally and vertically
                image_id = canvas.create_image(target_width//2, target_height//2, anchor=tk.CENTER, image=self.hero_bg_photo)
                self.logger.info(f"Image added to canvas with ID: {image_id} at position ({target_width//2}, {target_height//2})")

                # Ensure the image is visible by bringing it to front
                canvas.tag_lower(image_id)  # Put image at the back so content can go on top

                # Force canvas update
                canvas.update_idletasks()

                # Bind canvas resize to update image position and extend beyond scrollbar
                def on_canvas_configure(event):
                    canvas_width = event.width
                    # Get the actual window width to extend beyond scrollbar
                    try:
                        window_width = hero_card.winfo_toplevel().winfo_width()
                        # Extend canvas to full window width
                        canvas.configure(width=window_width)
                        # Center the image both horizontally and vertically
                        canvas.coords(canvas.find_all()[0], window_width//2, target_height//2)
                    except:
                        # Fallback to canvas width
                        canvas.coords(canvas.find_all()[0], canvas_width//2, target_height//2)

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
                                canvas.coords(canvas.find_all()[0], window_width//2, target_height//2)
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
                                canvas.coords(canvas.find_all()[0], window_width//2, max_hero_height//2)
                    except:
                        pass

                # Schedule the width update
                hero_card.after(100, update_initial_width)

                self.logger.info("Background image loaded successfully on canvas")
                return canvas

            else:
                # Fallback to solid color if image not found
                hero_card.configure(bg=COLORS['PRIMARY'])
                self.logger.warning(f"Background image not found at any of the expected locations: {background_paths}, using solid color")
                return None

        except Exception as e:
            # Fallback to solid color if any error occurs
            hero_card.configure(bg=COLORS['PRIMARY'])
            self.logger.error(f"Error loading background image: {e}")
            return None

    def _create_hero_overlay_content(self, canvas, hero_card):
        """Create overlay content on the hero background image."""
        try:
            from config.constants import COLORS, UIConfig, AppInfo

            # Get canvas dimensions with better fallback
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            # Use more reliable dimensions
            if canvas_width <= 1:
                canvas_width = 1200  # Default width
            if canvas_height <= 1:
                canvas_height = 226  # Default height

            # Calculate center position first (needed for glassmorphism calculations)
            center_x = max(canvas_width // 2, 300)  # Ensure minimum positioning
            center_y = max(canvas_height // 2, 100)  # Ensure minimum positioning

            # Create a glassmorphism overlay with transparent background
            overlay_frame = tk.Frame(
                canvas,
                bg='#FFFFFF',  # White background for glassmorphism
                relief='flat',
                bd=0,
                highlightthickness=0
            )

            # Create a glassmorphism background using PIL for better transparency simulation
            try:
                from PIL import Image, ImageDraw, ImageFilter, ImageTk

                # Try to create a true glassmorphism effect with background blur
                if hasattr(self, 'hero_image_pil') and self.hero_image_pil:
                    # Calculate the region of the background image that will be behind the overlay
                    overlay_x = max(0, center_x - 225)  # Half of overlay width (450/2)
                    overlay_y = max(0, center_y - 70)   # Half of overlay height (140/2)

                    # Ensure coordinates are within image bounds
                    img_width, img_height = self.hero_image_pil.size
                    overlay_x = min(overlay_x, img_width - 450) if img_width > 450 else 0
                    overlay_y = min(overlay_y, img_height - 140) if img_height > 140 else 0

                    # Extract the region that will be behind the overlay
                    try:
                        # Ensure we don't go beyond image boundaries
                        crop_right = min(overlay_x + 450, img_width)
                        crop_bottom = min(overlay_y + 140, img_height)

                        region = self.hero_image_pil.crop((
                            overlay_x, overlay_y,
                            crop_right, crop_bottom
                        ))

                        # Resize to exact overlay dimensions
                        region = region.resize((450, 140), Image.Resampling.LANCZOS)

                        # Apply blur effect for glassmorphism
                        blurred_region = region.filter(ImageFilter.GaussianBlur(radius=15))

                        # Create a glassmorphism overlay with proper transparency
                        # Use a more sophisticated gradient for better glassmorphism effect
                        glass_overlay = Image.new('RGBA', (450, 140), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(glass_overlay)

                        # Create a radial gradient effect for glassmorphism
                        for y in range(140):
                            for x in range(450):
                                # Calculate distance from center for radial effect
                                center_dist = ((x - 225) ** 2 + (y - 70) ** 2) ** 0.5
                                max_dist = (225 ** 2 + 70 ** 2) ** 0.5

                                # Create gradient based on distance from center
                                gradient_factor = 1 - min(center_dist / max_dist, 1)

                                # Base alpha with gradient
                                alpha = int(80 + (gradient_factor * 60))  # 80-140 alpha range
                                alpha = max(60, min(140, alpha))

                                # Add some noise for more realistic glass effect
                                noise = (x + y) % 3 - 1  # Simple noise pattern
                                alpha += noise * 5
                                alpha = max(50, min(150, alpha))

                                draw.point((x, y), fill=(255, 255, 255, alpha))

                        # Add subtle border for definition
                        draw.rectangle([0, 0, 449, 139], outline=(255, 255, 255, 120), width=1)

                        # Add inner highlight for glass effect
                        draw.rectangle([1, 1, 448, 138], outline=(255, 255, 255, 80), width=1)

                        # Composite the blurred background with the glass overlay
                        glassmorphism_bg = Image.alpha_composite(
                            blurred_region.convert('RGBA'),
                            glass_overlay
                        )

                        # Convert to PhotoImage
                        glass_photo = ImageTk.PhotoImage(glassmorphism_bg)

                        # Create background label with glassmorphism
                        glass_bg = tk.Label(overlay_frame, image=glass_photo, bd=0, highlightthickness=0)
                        glass_bg.place(x=0, y=0, relwidth=1, relheight=1)

                        # Store reference to prevent garbage collection
                        overlay_frame.glass_photo = glass_photo

                        # NOW ADD TEXT DIRECTLY ON TOP OF THE GLASS BACKGROUND
                        self._add_text_to_glass_overlay(overlay_frame)

                        self.logger.info("Advanced glassmorphism effect applied successfully")

                    except Exception as crop_error:
                        self.logger.warning(f"Advanced glassmorphism failed: {crop_error}, using simple version")
                        raise Exception(f"Crop error: {crop_error}")

                else:
                    # Create a simple gradient glassmorphism background when no background image
                    self._create_simple_glassmorphism(overlay_frame)

            except Exception as e:
                # Fallback: create simple glassmorphism effect
                self.logger.info(f"Advanced glassmorphism failed, using simple version: {e}")
                self._create_simple_glassmorphism(overlay_frame)

            self.logger.info("About to create overlay window...")

            # Position the overlay frame in the center of the main canvas
            overlay_window = canvas.create_window(
                center_x, center_y,  # Center positioning
                window=overlay_frame,
                anchor=tk.CENTER,
                width=450,  # Fixed width for consistency
                height=140   # Fixed height for consistency
            )

            self.logger.info(f"Overlay window created with ID: {overlay_window}")
            self.logger.info("Glassmorphism overlay positioned successfully")

            # Store overlay reference for potential updates
            self.hero_overlay = overlay_window

            self.logger.info("Hero overlay content created successfully")

        except Exception as e:
            self.logger.error(f"Error creating hero overlay content: {e}")
            import traceback
            traceback.print_exc()

    def _create_simple_glassmorphism(self, overlay_frame):
        """Create a simple glassmorphism effect when advanced version fails."""
        try:
            from PIL import Image, ImageDraw, ImageTk

            # Create a simple gradient glassmorphism background
            glass_img = Image.new('RGBA', (450, 140), (0, 0, 0, 0))
            draw = ImageDraw.Draw(glass_img)

            # Create a subtle gradient effect
            for y in range(140):
                # Create vertical gradient
                alpha = int(120 - (y * 0.2))  # Subtle gradient
                alpha = max(80, min(140, alpha))  # Keep in visible range

                # Add horizontal variation for more realistic effect
                for x in range(450):
                    x_factor = abs(x - 225) / 225  # Distance from center horizontally
                    final_alpha = int(alpha * (1 - x_factor * 0.2))  # Slight horizontal fade
                    final_alpha = max(70, min(130, final_alpha))

                    draw.point((x, y), fill=(255, 255, 255, final_alpha))

            # Add subtle border
            draw.rectangle([0, 0, 449, 139], outline=(255, 255, 255, 100), width=1)

            # Add inner highlight
            draw.rectangle([2, 2, 447, 137], outline=(255, 255, 255, 60), width=1)

            # Convert to PhotoImage
            glass_photo = ImageTk.PhotoImage(glass_img)

            # Create background label with glassmorphism
            glass_bg = tk.Label(overlay_frame, image=glass_photo, bd=0, highlightthickness=0)
            glass_bg.place(x=0, y=0, relwidth=1, relheight=1)

            # Store reference to prevent garbage collection
            overlay_frame.glass_photo = glass_photo

            # NOW ADD TEXT DIRECTLY ON TOP OF THE GLASS BACKGROUND
            self._add_text_to_glass_overlay(overlay_frame)

            self.logger.info("Simple glassmorphism effect applied successfully")

        except Exception as e:
            self.logger.warning(f"Simple glassmorphism also failed: {e}")
            # Ultimate fallback: semi-transparent white background
            overlay_frame.configure(bg='#FFFFFF')  # Solid white fallback
            # Still add text even with fallback
            self._add_text_to_glass_overlay(overlay_frame)

    def _add_text_to_glass_overlay(self, overlay_frame):
        """Add only title and subtitle text floating over glassmorphism - no background cards."""
        try:
            # Create title label - pure text floating over glass, no background
            title_label = tk.Label(
                overlay_frame,
                text="Bienvenue sur Pladria",
                font=("Segoe UI", 16, "bold"),
                fg="#000000",  # Black text
                relief='flat',
                bd=0,
                highlightthickness=0
            )
            title_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

            # Create subtitle label - pure text floating over glass, no background
            subtitle_label = tk.Label(
                overlay_frame,
                text="Système de contrôle qualité pour l'activité Plan Adressage",
                font=("Segoe UI", 10, "normal"),
                fg="#333333",  # Dark gray for subtitle
                relief='flat',
                bd=0,
                highlightthickness=0,
                wraplength=400
            )
            subtitle_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

            self.logger.info("Pure floating text added to glassmorphism overlay successfully")

        except Exception as e:
            self.logger.error(f"Error adding text to glassmorphism overlay: {e}")
            # Fallback: create a simple text label
            fallback_label = tk.Label(
                overlay_frame,
                text="Bienvenue sur Pladria",
                font=("Segoe UI", 14, "bold"),
                fg="#000000",  # Black text
                relief='flat',
                bd=0,
                highlightthickness=0
            )
            fallback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _create_modern_features_section(self, parent: tk.Widget):
        """Create modern features section with professional card design."""
        # Modern section header
        header_section = tk.Frame(parent, bg=COLORS['BG'])
        header_section.pack(fill=tk.X, pady=(0, 30))

        # Title and subtitle removed as requested

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
        """Create a modern feature card with enhanced design and glassmorphism effects."""
        # Card container with enhanced shadow effect
        card_container = tk.Frame(parent, bg=COLORS['BG'])

        # Main card with modern glassmorphism styling
        card = tk.Frame(card_container, bg=COLORS['WHITE'], relief='solid', bd=1)
        card.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Enhanced shadow effect with gradient-like appearance
        shadow1 = tk.Frame(card_container, bg='#D0D0D0', height=1)
        shadow1.pack(fill=tk.X, side=tk.BOTTOM)
        shadow2 = tk.Frame(card_container, bg='#E8E8E8', height=1)
        shadow2.pack(fill=tk.X, side=tk.BOTTOM)

        # Card header with colored accent and gradient effect
        header = tk.Frame(card, bg=color, height=8)
        header.pack(fill=tk.X)

        # Add a subtle accent line below the header
        accent_frame = tk.Frame(card, bg=COLORS['LIGHT'], height=1)
        accent_frame.pack(fill=tk.X)

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
        """Create modern Teams access section with compact design."""
        teams_container = tk.Frame(parent, bg=COLORS['BG'])
        teams_container.pack(pady=(20, 0))

        # Compact Teams card with fixed width
        teams_card = tk.Frame(teams_container, bg=COLORS['ACCENT'], relief='flat', bd=0, width=600, height=80)
        teams_card.pack(padx=20, pady=10)
        teams_card.pack_propagate(False)  # Maintain fixed size

        teams_content = tk.Frame(teams_card, bg=COLORS['ACCENT'])
        teams_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Teams icon and text in horizontal layout
        teams_header = tk.Frame(teams_content, bg=COLORS['ACCENT'])
        teams_header.pack(fill=tk.X)

        # Smaller icon
        teams_icon = tk.Label(
            teams_header,
            text="🗂️",
            font=("Segoe UI", 18),
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        teams_icon.pack(side=tk.LEFT, padx=(0, 12))

        # Compact text section
        teams_text_frame = tk.Frame(teams_header, bg=COLORS['ACCENT'])
        teams_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        teams_title = tk.Label(
            teams_text_frame,
            text="Accès Direct au Canal Teams",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS['PRIMARY'],
            bg=COLORS['ACCENT']
        )
        teams_title.pack(anchor=tk.W)

        teams_subtitle = tk.Label(
            teams_text_frame,
            text="Ouvrir le dossier Teams synchronisé",
            font=("Segoe UI", 7),
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['ACCENT']
        )
        teams_subtitle.pack(anchor=tk.W, pady=(1, 0))

        # Compact Teams button
        teams_button = tk.Button(
            teams_header,
            text="Ouvrir Teams",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS['PRIMARY'],
            fg=COLORS['WHITE'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self._open_teams_folder_directly
        )
        teams_button.pack(side=tk.RIGHT, padx=(15, 0))

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

"""
Data Viewer Module for Pladria.
Visualizes the content of the first sheet of "Suivis Global Tickets CMS Adr_PA.xlsx" from Teams.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
from datetime import datetime

class DatePickerPopup:
    """Popup calendar for date selection like web interfaces."""

    def __init__(self, parent, initial_date=None, callback=None):
        self.parent = parent
        self.callback = callback
        self.selected_date = initial_date or datetime.now().date()
        self.popup = None

    def show(self):
        """Show the calendar popup."""
        if not CALENDAR_AVAILABLE:
            return

        # Create popup window
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Sélectionner une date")
        self.popup.geometry("300x280")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()

        # Center the popup
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.popup.winfo_screenheight() // 2) - (280 // 2)
        self.popup.geometry(f"300x280+{x}+{y}")

        # Create calendar
        self.calendar = Calendar(
            self.popup,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            background='#2E86AB',
            foreground='white',
            bordercolor='#2E86AB',
            headersbackground='#1B5E7A',
            headersforeground='white',
            selectbackground='#A23B72',
            selectforeground='white',
            weekendbackground='#F18F01',
            weekendforeground='white',
            othermonthbackground='#E8E8E8',
            othermonthforeground='gray',
            normalbackground='white',
            normalforeground='black'
        )
        self.calendar.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Set initial date
        self.calendar.selection_set(self.selected_date)

        # Buttons frame
        buttons_frame = tk.Frame(self.popup, bg='white')
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # OK button
        ok_button = tk.Button(
            buttons_frame,
            text="✓ OK",
            command=self._on_ok,
            bg='#2E86AB',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=5
        )
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Cancel button
        cancel_button = tk.Button(
            buttons_frame,
            text="✗ Annuler",
            command=self._on_cancel,
            bg='#6C757D',
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            padx=20,
            pady=5
        )
        cancel_button.pack(side=tk.RIGHT)

        # Today button
        today_button = tk.Button(
            buttons_frame,
            text="📅 Aujourd'hui",
            command=self._on_today,
            bg='#F18F01',
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            padx=15,
            pady=5
        )
        today_button.pack(side=tk.LEFT)

        # Bind double-click on calendar
        self.calendar.bind("<<CalendarSelected>>", self._on_date_selected)

        # Bind escape key
        self.popup.bind('<Escape>', lambda e: self._on_cancel())
        self.popup.bind('<Return>', lambda e: self._on_ok())

        # Focus on popup
        self.popup.focus_set()

    def _on_date_selected(self, event=None):
        """Handle date selection (double-click)."""
        # Auto-close on double-click
        self.popup.after(100, self._on_ok)

    def _on_today(self):
        """Set calendar to today's date."""
        today = datetime.now().date()
        self.calendar.selection_set(today)

    def _on_ok(self):
        """Handle OK button click."""
        try:
            self.selected_date = self.calendar.selection_get()
            if self.callback:
                self.callback(self.selected_date)
        except Exception as e:
            print(f"Error getting selected date: {e}")
        finally:
            self._close_popup()

    def _on_cancel(self):
        """Handle Cancel button click."""
        self._close_popup()

    def _close_popup(self):
        """Close the popup window."""
        if self.popup:
            self.popup.grab_release()
            self.popup.destroy()
            self.popup = None
from typing import Optional, Dict, Any, List
from pathlib import Path

# Import tkcalendar for date picker
try:
    from tkcalendar import DateEntry, Calendar
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False
    Calendar = None

from config.constants import COLORS, UIConfig, TeamsConfig
from utils.file_utils import get_icon_path
from utils.lazy_imports import get_pandas
from utils.performance import run_async_task

from ui.styles import StyleManager, create_card_frame, create_section_header
from ui.keyboard_shortcuts import KeyboardShortcutManager

logger = logging.getLogger(__name__)


class DataViewerModule:
    """Data Viewer module for visualizing global tickets data."""
    
    def __init__(self, parent, navigation_manager=None):
        """
        Initialize the Data Viewer module.
        
        Args:
            parent: Parent widget
            navigation_manager: Navigation manager instance
        """
        self.parent = parent
        self.navigation_manager = navigation_manager
        self.logger = logging.getLogger(__name__)
        
        # Module data
        self.data_df = None
        self.filtered_data = None
        self.global_excel_path = None
        
        # Get Teams path
        self.teams_folder_path = TeamsConfig.get_global_teams_path()
        self.global_excel_filename = "Suivis Global Tickets CMS Adr_PA.xlsx"
        
        # UI components
        self.main_frame = None
        self.tree = None
        self.filter_frame = None
        self.commune_search_var = None  # Added Commune search variable
        self.search_var = None
        self.insee_search_var = None  # Added INSEE search variable
        self.domaine_filter_var = None  # Added Domaine filter variable
        self.date_filter_var = None
        self.collaborateur_filter_var = None
        self.etat_filter_var = None
        self.status_label = None
        self.refresh_button = None
        
        # Keyboard shortcuts (will be initialized later)
        self.keyboard_manager = None
        
        # Create UI
        self._create_ui()
        
        # Initialize optional features after UI is ready
        self.parent.after(100, self._initialize_optional_features)
    
    def _create_ui(self):
        """Create the user interface."""
        try:
            # Main container - Ultra minimal
            self.main_frame = tk.Frame(self.parent, bg=COLORS['BG'])
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)  # Ultra minimal padding
            
            # Header
            self._create_header()
            
            # Filters section
            self._create_filters_section()
            
            # Data table
            self._create_data_table()
            
            # Status bar
            self._create_status_bar()
            
            # Load data initially
            self._load_data()
            
            self.logger.info("Data Viewer module UI created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating Data Viewer UI: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la création de l'interface: {e}")
    
    def _create_header(self):
        """Create the header section."""
        header_frame = tk.Frame(self.main_frame, bg=COLORS['BG'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Home button (left)
        home_button = tk.Button(
            header_frame,
            text="🏠 Retour Accueil",
            font=UIConfig.FONT_BUTTON,
            bg=COLORS['SECONDARY'],
            fg=COLORS['WHITE'],
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._go_home
        )
        home_button.pack(side=tk.LEFT)

        # Title (center)
        title_label = tk.Label(
            header_frame,
            text="📊 Visualiseur de Données Global",
            font=UIConfig.FONT_HEADER,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        title_label.pack(side=tk.LEFT, padx=(20, 0))

        # Refresh button (right)
        self.refresh_button = tk.Button(
            header_frame,
            text="🔄 Actualiser",
            font=UIConfig.FONT_BUTTON,
            bg=COLORS['PRIMARY'],
            fg=COLORS['WHITE'],
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._refresh_data
        )
        self.refresh_button.pack(side=tk.RIGHT)
    
    def _create_filters_section(self):
        """Create the filters section."""
        # Filters frame - Reduced padding
        self.filter_frame = create_card_frame(self.main_frame)
        self.filter_frame.pack(fill=tk.X, pady=(0, 5))  # Reduced from 15 to 5

        # Filters header - Reduced padding
        filters_header_frame = tk.Frame(self.filter_frame, bg=COLORS['CARD'])
        filters_header_frame.pack(fill=tk.X, padx=15, pady=(10, 5))  # Reduced padding

        filters_header_label = tk.Label(
            filters_header_frame,
            text="🔍 Filtres et Recherche",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        filters_header_label.pack(side=tk.LEFT)

        # Filters container - Reduced padding
        filters_container = tk.Frame(self.filter_frame, bg=COLORS['CARD'])
        filters_container.pack(fill=tk.X, padx=15, pady=(0, 10))  # Reduced from 15 to 10

        # Configure grid - 8 columns for all filters in one single row (added Commune + Domaine)
        filters_container.grid_columnconfigure(0, weight=1)
        filters_container.grid_columnconfigure(1, weight=1)
        filters_container.grid_columnconfigure(2, weight=1)
        filters_container.grid_columnconfigure(3, weight=1)
        filters_container.grid_columnconfigure(4, weight=1)
        filters_container.grid_columnconfigure(5, weight=1)
        filters_container.grid_columnconfigure(6, weight=1)
        filters_container.grid_columnconfigure(7, weight=1)  # 8 columns total

        # Search by Nom Commune (Column A) - Column 0 (NEW)
        commune_label = tk.Label(
            filters_container,
            text="Nom Commune:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        commune_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 3), pady=1)

        self.commune_search_var = tk.StringVar()
        self.commune_search_var.trace('w', self._on_filter_change)
        commune_entry = tk.Entry(
            filters_container,
            textvariable=self.commune_search_var,
            font=UIConfig.FONT_SUBTITLE,
            width=8
        )
        commune_entry.grid(row=1, column=0, sticky=tk.W+tk.E, padx=(0, 3), pady=1)

        # Search by ID Commune (Column B) - Column 1 (moved from column 0)
        search_label = tk.Label(
            filters_container,
            text="ID Commune:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        search_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 3), pady=1)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_filter_change)
        search_entry = tk.Entry(
            filters_container,
            textvariable=self.search_var,
            font=UIConfig.FONT_SUBTITLE,
            width=8
        )
        search_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=(0, 3), pady=1)

        # Search by Code INSEE (Column C) - Column 2 (moved from column 1)
        insee_label = tk.Label(
            filters_container,
            text="Code INSEE:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        insee_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 3), pady=1)

        self.insee_search_var = tk.StringVar()
        self.insee_search_var.trace('w', self._on_filter_change)
        insee_entry = tk.Entry(
            filters_container,
            textvariable=self.insee_search_var,
            font=UIConfig.FONT_SUBTITLE,
            width=8
        )
        insee_entry.grid(row=1, column=2, sticky=tk.W+tk.E, padx=(0, 3), pady=1)
        
        # Date filter range (Column O) - From - Column 3 (moved from column 2)
        date_from_label = tk.Label(
            filters_container,
            text="📅 Date de:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        date_from_label.grid(row=0, column=3, sticky=tk.W, padx=(0, 3), pady=1)

        # Date from selection - Web-style button
        self.date_from_selected = None
        self.date_from_button = tk.Button(
            filters_container,
            text="📅 De",
            command=self._show_date_from_picker,
            bg=COLORS['PRIMARY'],
            fg='white',
            font=UIConfig.FONT_SUBTITLE,
            relief='flat',
            padx=3,
            pady=1,
            cursor='hand2'
        )
        self.date_from_button.grid(row=1, column=3, sticky=tk.W+tk.E, padx=(0, 3), pady=1)

        # Date filter range (Column O) - To - Column 4
        date_to_label = tk.Label(
            filters_container,
            text="📅 Date à:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        date_to_label.grid(row=0, column=4, sticky=tk.W, padx=(0, 3), pady=1)

        # Date to selection - Web-style button
        self.date_to_selected = None
        self.date_to_button = tk.Button(
            filters_container,
            text="📅 À",
            command=self._show_date_to_picker,
            bg=COLORS['PRIMARY'],
            fg='white',
            font=UIConfig.FONT_SUBTITLE,
            relief='flat',
            padx=3,
            pady=1,
            cursor='hand2'
        )
        self.date_to_button.grid(row=1, column=4, sticky=tk.W+tk.E, padx=(0, 3), pady=1)

        # Domaine filter (Column D) - Column 5 (moved after dates as requested)
        domaine_label = tk.Label(
            filters_container,
            text="Domaine:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        domaine_label.grid(row=0, column=5, sticky=tk.W, padx=(0, 3), pady=1)

        self.domaine_filter_var = tk.StringVar()
        self.domaine_filter_var.trace('w', self._on_filter_change)
        domaine_combo = ttk.Combobox(
            filters_container,
            textvariable=self.domaine_filter_var,
            font=UIConfig.FONT_SUBTITLE,
            width=8,
            state="readonly"
        )
        domaine_combo.grid(row=1, column=5, sticky=tk.W+tk.E, padx=(0, 3), pady=1)
        self.domaine_combo = domaine_combo
        
        # État filter (Column P) - Column 6 (moved after Domaine as requested)
        etat_label = tk.Label(
            filters_container,
            text="État:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        etat_label.grid(row=0, column=6, sticky=tk.W, padx=(0, 3), pady=1)

        self.etat_filter_var = tk.StringVar()
        self.etat_filter_var.trace('w', self._on_filter_change)
        etat_combo = ttk.Combobox(
            filters_container,
            textvariable=self.etat_filter_var,
            font=UIConfig.FONT_SUBTITLE,
            width=8,
            state="readonly"
        )
        etat_combo.grid(row=1, column=6, sticky=tk.W+tk.E, padx=(0, 3), pady=1)
        self.etat_combo = etat_combo

        # Collaborateur filter (Column U) - Column 7 (moved to last position as requested)
        collab_label = tk.Label(
            filters_container,
            text="Collaborateur:",
            font=UIConfig.FONT_SUBTITLE,
            bg=COLORS['CARD'],
            fg=COLORS['TEXT_SECONDARY']
        )
        collab_label.grid(row=0, column=7, sticky=tk.W, padx=(0, 3), pady=1)

        self.collaborateur_filter_var = tk.StringVar()
        self.collaborateur_filter_var.trace('w', self._on_filter_change)
        collab_combo = ttk.Combobox(
            filters_container,
            textvariable=self.collaborateur_filter_var,
            font=UIConfig.FONT_SUBTITLE,
            width=8,
            state="readonly"
        )
        collab_combo.grid(row=1, column=7, sticky=tk.W+tk.E, padx=(0, 3), pady=1)
        self.collaborateur_combo = collab_combo

        # Clear filters button - positioned below all filters
        clear_button = tk.Button(
            filters_container,
            text="🗑️ Effacer",
            font=UIConfig.FONT_BUTTON,
            bg=COLORS['TEXT_SECONDARY'],
            fg=COLORS['WHITE'],
            relief=tk.FLAT,
            padx=10,  # Reduced padding
            pady=3,   # Reduced padding
            command=self._clear_filters
        )
        clear_button.grid(row=2, column=0, columnspan=8, pady=(5, 0))  # Updated columnspan to 8, reduced padding
    
    def _create_data_table(self):
        """Create the data table."""
        # Table frame - Reduced spacing
        table_frame = create_card_frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))  # No top padding to reduce space

        # Table header - Reduced padding
        table_header_frame = tk.Frame(table_frame, bg=COLORS['CARD'])
        table_header_frame.pack(fill=tk.X, padx=15, pady=(10, 5))  # Reduced padding

        table_header_label = tk.Label(
            table_header_frame,
            text="📋 Données Global Tickets",
            font=UIConfig.FONT_SUBTITLE,
            fg=COLORS['PRIMARY'],
            bg=COLORS['CARD']
        )
        table_header_label.pack(side=tk.LEFT)

        # Treeview container - Ultra minimal
        tree_container = tk.Frame(table_frame, bg=COLORS['CARD'])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=3, pady=(0, 3))  # Ultra minimal padding
        
        # Define columns (A, B, C, D, I, N, O, P, U) - Added column C for Code INSEE
        columns = ('A', 'B', 'C', 'D', 'I', 'N', 'O', 'P', 'U')
        column_names = {
            'A': '🏘️ Commune',
            'B': '🆔 ID Tâche',
            'C': '📍 INSEE',
            'D': '🏢 Domaine',
            'I': '📅 Affectation',
            'N': '⏱️ Durée',
            'O': '📦 Livraison',
            'P': '📋 État',
            'U': '👤 Collaborateur'
        }
        
        # Create Treeview
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings', height=15)
        
        # Configure columns with sorting
        self.sort_column = None
        self.sort_reverse = False

        for col in columns:
            self.tree.heading(col, text=column_names[col],
                            command=lambda c=col: self._sort_treeview(c))
            if col in ['A', 'U']:  # Wider columns for names
                self.tree.column(col, width=150, minwidth=100)
            elif col in ['B']:  # ID Tâche column
                self.tree.column(col, width=130, minwidth=100)
            elif col in ['C']:  # Code INSEE column
                self.tree.column(col, width=90, minwidth=70)
            elif col in ['I', 'O']:  # Date columns
                self.tree.column(col, width=120, minwidth=100)
            else:
                self.tree.column(col, width=100, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)

        # Configure grid weights
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Bind double-click event to open Excel file
        self.tree.bind("<Double-1>", self._on_double_click)

        # Bind right-click event for context menu
        self.tree.bind("<Button-3>", self._on_right_click)

        # Create context menu
        self._create_context_menu()
    
    def _create_status_bar(self):
        """Create the enhanced status bar - Ultra compact."""
        status_frame = tk.Frame(self.main_frame, bg=COLORS['BG'])
        status_frame.pack(fill=tk.X, pady=(3, 0))  # Ultra minimal spacing

        # Status label with icon
        self.status_label = tk.Label(
            status_frame,
            text="📊 Prêt à charger les données",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['TEXT_SECONDARY'],
            bg=COLORS['BG']
        )
        self.status_label.pack(side=tk.LEFT)

        # Data info label (will show count and filter info)
        self.data_info_label = tk.Label(
            status_frame,
            text="",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        self.data_info_label.pack(side=tk.LEFT, padx=(20, 0))

        # Add instruction for double-click
        instruction_label = tk.Label(
            status_frame,
            text="💡 Double-cliquez sur une ligne pour ouvrir le fichier Excel de la commune",
            font=UIConfig.FONT_SMALL,
            fg=COLORS['PRIMARY'],
            bg=COLORS['BG']
        )
        instruction_label.pack(side=tk.RIGHT)

    def _create_context_menu(self):
        """Create simplified context menu for right-click operations."""
        try:
            self.context_menu = tk.Menu(self.parent, tearoff=0)

            # Copy commune name
            self.context_menu.add_command(
                label="🏘️ Copier le nom de commune",
                command=self._copy_commune_name
            )

            # Copy ID tâche
            self.context_menu.add_command(
                label="🆔 Copier l'ID tâche",
                command=self._copy_id_tache
            )

            # Copy code INSEE
            self.context_menu.add_command(
                label="📍 Copier le code INSEE",
                command=self._copy_code_insee
            )

        except Exception as e:
            self.logger.error(f"Error creating context menu: {e}")

    def _initialize_optional_features(self):
        """Initialize optional features after UI is ready."""
        try:
            # Setup keyboard shortcuts
            if self.navigation_manager and hasattr(self.navigation_manager, 'root'):
                self.keyboard_manager = KeyboardShortcutManager(self.navigation_manager.root)
                self._setup_module_shortcuts()

            self.logger.info("Optional features initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing optional features: {e}")
    
    def _setup_module_shortcuts(self):
        """Setup keyboard shortcuts for this module."""
        try:
            if self.keyboard_manager:
                self.keyboard_manager.bind_key('<F5>', self._refresh_data)
                self.keyboard_manager.bind_key('<Control-r>', self._refresh_data)
                self.keyboard_manager.bind_key('<Control-f>', lambda: self.search_var.set(''))
                
        except Exception as e:
            self.logger.error(f"Error setting up keyboard shortcuts: {e}")
    
    def _load_data(self):
        """Load data from the global Excel file."""
        try:
            self._update_status("Chargement des données...")
            
            # Construct path to global Excel file
            self.global_excel_path = os.path.join(self.teams_folder_path, self.global_excel_filename)
            
            if not os.path.exists(self.global_excel_path):
                self._update_status("Fichier global non trouvé")
                messagebox.showwarning(
                    "Fichier non trouvé",
                    f"Le fichier '{self.global_excel_filename}' n'a pas été trouvé dans:\n{self.teams_folder_path}\n\n"
                    "Assurez-vous que le module Suivi Global a été exécuté au moins une fois."
                )
                return
            
            # Load data using pandas
            pd = get_pandas()
            
            # Read first sheet (Suivi Tickets)
            self.data_df = pd.read_excel(
                self.global_excel_path,
                sheet_name=0,  # First sheet
                dtype={'Code INSEE': str, 'ID tâche Plan Adressage': str},
                date_format=None  # CRITICAL: Prevent automatic date parsing to avoid date inversion
            )

            # Format all date columns for better display
            date_columns = []
            for col in self.data_df.columns:
                if 'date' in col.lower() or col in ['Date Affectation', 'Date Livraison']:
                    date_columns.append(col)

            # Format dates for better readability in ISO format (YYYY-MM-DD)
            for col in date_columns:
                if col in self.data_df.columns:
                    self.data_df[col] = self.data_df[col].apply(self._format_date_for_display)

            for col in date_columns:
                try:
                    # Convert to datetime and then format as YYYY-MM-DD (ISO format)
                    self.data_df[col] = pd.to_datetime(self.data_df[col], errors='coerce')
                    self.data_df[col] = self.data_df[col].dt.strftime('%Y-%m-%d')
                    # Replace NaT with empty string
                    self.data_df[col] = self.data_df[col].fillna('')
                except Exception as e:
                    self.logger.warning(f"Could not format date column {col}: {e}")
            
            if self.data_df is None or self.data_df.empty:
                self._update_status("Aucune donnée trouvée")
                return
            
            # Update filter options
            self._update_filter_options()
            
            # Apply filters and display data
            self._apply_filters()
            
            self._update_status(f"Données chargées: {len(self.data_df)} lignes")
            self.logger.info(f"Data loaded successfully: {len(self.data_df)} rows")
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            self._update_status("Erreur lors du chargement")
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données:\n{e}")
    
    def _update_filter_options(self):
        """Update filter dropdown options based on loaded data."""
        try:
            if self.data_df is None or self.data_df.empty:
                return
            
            # Get column names (may vary)
            columns = list(self.data_df.columns)
            
            # Find collaborateur column (usually last or contains 'Collaborateur')
            collaborateur_col = None
            for col in columns:
                if 'Collaborateur' in str(col) or col == columns[-1]:
                    collaborateur_col = col
                    break
            
            # Find domaine column (usually contains 'Domaine')
            domaine_col = None
            for col in columns:
                if 'Domaine' in str(col):
                    domaine_col = col
                    break

            # Find état column (usually contains 'Etat' or 'État')
            etat_col = None
            for col in columns:
                if 'Etat' in str(col) or 'État' in str(col) or 'STATUT' in str(col):
                    etat_col = col
                    break

            # Update collaborateur options
            if collaborateur_col and collaborateur_col in self.data_df.columns:
                collaborateurs = [''] + sorted(self.data_df[collaborateur_col].dropna().unique().tolist())
                if hasattr(self, 'collaborateur_combo') and self.collaborateur_combo:
                    self.collaborateur_combo['values'] = collaborateurs

            # Update domaine options
            if domaine_col and domaine_col in self.data_df.columns:
                domaines = [''] + sorted(self.data_df[domaine_col].dropna().unique().tolist())
                if hasattr(self, 'domaine_combo') and self.domaine_combo:
                    self.domaine_combo['values'] = domaines

            # Update état options
            if etat_col and etat_col in self.data_df.columns:
                etats = [''] + sorted(self.data_df[etat_col].dropna().unique().tolist())
                if hasattr(self, 'etat_combo') and self.etat_combo:
                    self.etat_combo['values'] = etats
                
        except Exception as e:
            self.logger.error(f"Error updating filter options: {e}")
    
    def _apply_filters(self):
        """Apply current filters to the data."""
        try:
            if self.data_df is None or self.data_df.empty:
                return
            
            # Start with all data
            filtered_df = self.data_df.copy()
            
            # Get column mappings
            columns = list(self.data_df.columns)
            
            # Map to expected columns (A, B, C, D, I, N, O, P, U)
            col_mapping = {}
            if len(columns) >= 21:  # Ensure we have enough columns
                col_mapping = {
                    'A': columns[0],   # Nom Commune
                    'B': columns[1],   # ID Tâche
                    'C': columns[2] if len(columns) > 2 else None,   # Code INSEE
                    'D': columns[3] if len(columns) > 3 else None,   # Domaine
                    'I': columns[8] if len(columns) > 8 else None,   # Date Affectation
                    'N': columns[13] if len(columns) > 13 else None, # Durée Finale
                    'O': columns[14] if len(columns) > 14 else None, # Date Livraison
                    'P': columns[15] if len(columns) > 15 else None, # État Ticket
                    'U': columns[20] if len(columns) > 20 else None  # Collaborateur
                }
            
            # Apply commune search filter (Nom Commune - Column A)
            commune_text = self.commune_search_var.get().strip()
            if commune_text and col_mapping.get('A'):
                filtered_df = filtered_df[
                    filtered_df[col_mapping['A']].astype(str).str.contains(commune_text, case=False, na=False)
                ]

            # Apply search filter (ID Commune - Column B)
            search_text = self.search_var.get().strip()
            if search_text and col_mapping.get('B'):
                filtered_df = filtered_df[
                    filtered_df[col_mapping['B']].astype(str).str.contains(search_text, case=False, na=False)
                ]

            # Apply INSEE search filter (Code INSEE - Column C)
            insee_text = self.insee_search_var.get().strip()
            if insee_text and col_mapping.get('C'):
                filtered_df = filtered_df[
                    filtered_df[col_mapping['C']].astype(str).str.contains(insee_text, case=False, na=False)
                ]

            # Apply domaine filter (Column D)
            domaine_text = self.domaine_filter_var.get().strip()
            if domaine_text and col_mapping.get('D'):
                filtered_df = filtered_df[filtered_df[col_mapping['D']] == domaine_text]

            # Apply date range filter (Column O) using selected dates
            date_from_obj = self.date_from_selected
            date_to_obj = self.date_to_selected

            if (date_from_obj or date_to_obj) and col_mapping.get('O'):
                date_col = col_mapping['O']

                # Convert date column to datetime for proper comparison
                try:
                    pd = get_pandas()
                    filtered_df[date_col] = pd.to_datetime(filtered_df[date_col], errors='coerce')

                    if date_from_obj:
                        # Convert date object to pandas datetime
                        date_from_dt = pd.to_datetime(date_from_obj)
                        filtered_df = filtered_df[filtered_df[date_col] >= date_from_dt]

                    if date_to_obj:
                        # Convert date object to pandas datetime
                        date_to_dt = pd.to_datetime(date_to_obj)
                        filtered_df = filtered_df[filtered_df[date_col] <= date_to_dt]

                except Exception as e:
                    self.logger.error(f"Error filtering by date range: {e}")
                    # If filtering fails, show all data
                    pass
            
            # Apply collaborateur filter (Column U)
            collab_text = self.collaborateur_filter_var.get().strip()
            if collab_text and col_mapping.get('U'):
                filtered_df = filtered_df[filtered_df[col_mapping['U']] == collab_text]
            
            # Apply état filter (Column P)
            etat_text = self.etat_filter_var.get().strip()
            if etat_text and col_mapping.get('P'):
                filtered_df = filtered_df[filtered_df[col_mapping['P']] == etat_text]
            
            # Store filtered data
            self.filtered_data = filtered_df
            
            # Update display
            self._update_table_display()
            
        except Exception as e:
            self.logger.error(f"Error applying filters: {e}")
            self._update_status("Erreur lors du filtrage")
    
    def _update_table_display(self):
        """Update the table display with filtered data."""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if self.filtered_data is None or self.filtered_data.empty:
                self._update_status("Aucune donnée à afficher")
                return
            
            # Get column mappings
            columns = list(self.data_df.columns)
            col_mapping = {}
            if len(columns) >= 21:
                col_mapping = {
                    'A': columns[0],   # Nom Commune
                    'B': columns[1],   # ID Tâche
                    'C': columns[2] if len(columns) > 2 else None,   # Code INSEE
                    'D': columns[3] if len(columns) > 3 else None,   # Domaine
                    'I': columns[8] if len(columns) > 8 else None,   # Date Affectation
                    'N': columns[13] if len(columns) > 13 else None, # Durée Finale
                    'O': columns[14] if len(columns) > 14 else None, # Date Livraison
                    'P': columns[15] if len(columns) > 15 else None, # État Ticket
                    'U': columns[20] if len(columns) > 20 else None  # Collaborateur
                }
            
            # Add filtered data to tree
            for index, row in self.filtered_data.iterrows():
                values = []
                for col_key in ['A', 'B', 'C', 'D', 'I', 'N', 'O', 'P', 'U']:
                    col_name = col_mapping.get(col_key)
                    if col_name and col_name in row:
                        pd = get_pandas()
                        value = str(row[col_name]) if pd.notna(row[col_name]) else ""

                        # Format dates to YYYY-MM-DD (ISO format) if it's a date column
                        if col_key in ['I', 'O'] and value and value != "":
                            try:
                                # Try to parse and format the date
                                date_obj = pd.to_datetime(value, errors='coerce')
                                if pd.notna(date_obj):
                                    value = date_obj.strftime("%Y-%m-%d")
                            except:
                                pass  # Keep original value if parsing fails
                    else:
                        value = ""
                    values.append(value)

                self.tree.insert('', 'end', values=values)
            
            # Update status with enhanced information
            total_rows = len(self.data_df) if self.data_df is not None else 0
            filtered_rows = len(self.filtered_data)

            if filtered_rows == total_rows:
                self._update_status(f"📊 {filtered_rows} ligne(s) affichée(s)")
                self._update_data_info("")
            else:
                self._update_status(f"🔍 {filtered_rows} ligne(s) filtrée(s)")
                self._update_data_info(f"sur {total_rows} total")

        except Exception as e:
            self.logger.error(f"Error updating table display: {e}")
            self._update_status("❌ Erreur lors de l'affichage")
            self._update_data_info("")
    
    def _on_filter_change(self, *args):
        """Handle filter changes."""
        self._apply_filters()

    def _show_date_from_picker(self):
        """Show date picker popup for 'Date de' filter."""
        try:
            if not CALENDAR_AVAILABLE:
                messagebox.showwarning(
                    "Calendrier non disponible",
                    "Le module de calendrier n'est pas installé.\nVeuillez installer tkcalendar."
                )
                return

            picker = DatePickerPopup(
                self.main_frame,
                initial_date=self.date_from_selected,
                callback=self._on_date_from_selected
            )
            picker.show()
        except Exception as e:
            self.logger.error(f"Error showing date from picker: {e}")

    def _show_date_to_picker(self):
        """Show date picker popup for 'Date à' filter."""
        try:
            if not CALENDAR_AVAILABLE:
                messagebox.showwarning(
                    "Calendrier non disponible",
                    "Le module de calendrier n'est pas installé.\nVeuillez installer tkcalendar."
                )
                return

            picker = DatePickerPopup(
                self.main_frame,
                initial_date=self.date_to_selected,
                callback=self._on_date_to_selected
            )
            picker.show()
        except Exception as e:
            self.logger.error(f"Error showing date to picker: {e}")

    def _on_date_from_selected(self, selected_date):
        """Handle date selection from 'Date de' picker."""
        try:
            self.date_from_selected = selected_date
            # Update button text to show selected date in ISO format
            date_str = selected_date.strftime("%Y-%m-%d")
            self.date_from_button.config(text=f"📅 {date_str}")
            # Apply filters
            self._apply_filters()
        except Exception as e:
            self.logger.error(f"Error handling date from selection: {e}")

    def _on_date_to_selected(self, selected_date):
        """Handle date selection from 'Date à' picker."""
        try:
            self.date_to_selected = selected_date
            # Update button text to show selected date in ISO format
            date_str = selected_date.strftime("%Y-%m-%d")
            self.date_to_button.config(text=f"📅 {date_str}")
            # Apply filters
            self._apply_filters()
        except Exception as e:
            self.logger.error(f"Error handling date to selection: {e}")

    def _format_date_for_display(self, date_value):
        """Format date for display in ISO format (YYYY-MM-DD) for better sorting and consistency."""
        try:
            if not date_value or str(date_value).strip() == '' or str(date_value).lower() in ['nan', 'none', 'null']:
                return ''

            date_str = str(date_value).strip()

            # If it's already in ISO format (YYYY-MM-DD), format for display
            if '-' in date_str and len(date_str.split('-')) == 3:
                parts = date_str.split('-')
                if len(parts[0]) == 4 and len(parts[1]) <= 2 and len(parts[2]) <= 2:
                    year, month, day = parts
                    # Return in a more readable format but still sortable
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            # If it's in dd/mm/yyyy format, convert to ISO for consistency
            if '/' in date_str and len(date_str.split('/')) == 3:
                parts = date_str.split('/')
                if len(parts[0]) <= 2 and len(parts[1]) <= 2 and len(parts[2]) == 4:
                    day, month, year = parts
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            # Return as-is if format is not recognized
            return date_str

        except Exception as e:
            self.logger.error(f"Error formatting date for display: {date_value} - {e}")
            return str(date_value) if date_value is not None else ''

    def _on_date_change(self, event=None):
        """Handle date picker changes."""
        try:
            # Apply filters directly when calendar dates change
            self._apply_filters()
        except Exception as e:
            self.logger.error(f"Error handling date change: {e}")

    def _sort_treeview(self, col):
        """Sort treeview by column."""
        try:
            # Get all items
            items = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

            # Determine if we need to reverse the sort
            if self.sort_column == col:
                self.sort_reverse = not self.sort_reverse
            else:
                self.sort_reverse = False
                self.sort_column = col

            # Sort items with consistent type handling
            def sort_key(item):
                value = item[0]

                # Handle empty values first
                if not value or str(value).strip() == '':
                    return (0, '')  # Empty values sort first

                value_str = str(value).strip()

                # Try to convert to number for numeric sorting
                try:
                    numeric_value = float(value_str.replace(',', '.'))
                    return (1, numeric_value)  # Numbers sort second
                except:
                    pass

                # For dates, try to parse them (both ISO and dd/mm/yyyy formats)
                if ('-' in value_str and len(value_str.split('-')) == 3) or ('/' in value_str and len(value_str.split('/')) == 3):
                    try:
                        pd = get_pandas()
                        # Try ISO format first (YYYY-MM-DD)
                        if '-' in value_str and len(value_str.split('-')) == 3:
                            parts = value_str.split('-')
                            if len(parts[0]) == 4:  # YYYY-MM-DD format
                                date_obj = pd.to_datetime(value_str, format='%Y-%m-%d', errors='coerce')
                                if pd.notna(date_obj):
                                    return (2, date_obj.timestamp())  # Dates sort third
                        # Try dd/mm/yyyy format
                        elif '/' in value_str and len(value_str.split('/')) == 3:
                            date_obj = pd.to_datetime(value_str, format='%d/%m/%Y', errors='coerce')
                            if pd.notna(date_obj):
                                return (2, date_obj.timestamp())  # Dates sort third
                    except:
                        pass

                # Default to string sorting
                return (3, value_str.lower())  # Strings sort last

            items.sort(key=sort_key, reverse=self.sort_reverse)

            # Rearrange items in sorted positions
            for index, (val, child) in enumerate(items):
                self.tree.move(child, '', index)

            # Update column headers to show sort direction
            columns = ('A', 'B', 'C', 'D', 'I', 'N', 'O', 'P', 'U')
            column_names = {
                'A': '🏘️ Commune',
                'B': '🆔 ID Tâche',
                'C': '📍 INSEE',
                'D': '🏢 Domaine',
                'I': '📅 Affectation',
                'N': '⏱️ Durée',
                'O': '📦 Livraison',
                'P': '📋 État',
                'U': '👤 Collaborateur'
            }

            for column in columns:
                if column == col:
                    # Add sort indicator
                    indicator = " ↓" if self.sort_reverse else " ↑"
                    self.tree.heading(column, text=column_names[column] + indicator)
                else:
                    # Remove sort indicator
                    self.tree.heading(column, text=column_names[column])

        except Exception as e:
            self.logger.error(f"Error sorting column {col}: {e}")

    def _on_double_click(self, event):
        """Handle double-click on table row to open Excel file."""
        try:
            # Get selected item
            selection = self.tree.selection()
            if not selection:
                return

            # Get item values
            item = selection[0]
            values = self.tree.item(item, 'values')

            if not values or len(values) < 2:
                return

            # Extract commune name and ID tache (columns A and B)
            nom_commune = values[0].strip()  # Column A
            id_tache = values[1].strip()     # Column B

            if not nom_commune or not id_tache:
                messagebox.showwarning(
                    "Information manquante",
                    "Impossible d'ouvrir le fichier : nom de commune ou ID tâche manquant."
                )
                return

            # Construct file path
            self._open_commune_excel_file(nom_commune, id_tache)

        except Exception as e:
            self.logger.error(f"Error handling double-click: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du fichier:\n{e}")

    def _on_right_click(self, event):
        """Handle right-click on table row to show context menu."""
        try:
            # Get the item under the cursor
            item = self.tree.identify_row(event.y)
            if item:
                # Select the item
                self.tree.selection_set(item)
                self.tree.focus(item)

                # Store the clicked item for context menu actions
                self.clicked_item = item

                # Show context menu
                self.context_menu.post(event.x_root, event.y_root)

        except Exception as e:
            self.logger.error(f"Error handling right-click: {e}")



    def _copy_commune_name(self):
        """Copy the commune name to clipboard."""
        try:
            if not hasattr(self, 'clicked_item') or not self.clicked_item:
                return

            values = self.tree.item(self.clicked_item, 'values')
            if values and len(values) > 0:
                commune_name = values[0]  # Column A
                self._copy_to_clipboard(commune_name)
                self._update_status(f"Nom de commune copié: {commune_name}")

        except Exception as e:
            self.logger.error(f"Error copying commune name: {e}")

    def _copy_id_tache(self):
        """Copy the ID tâche to clipboard."""
        try:
            if not hasattr(self, 'clicked_item') or not self.clicked_item:
                return

            values = self.tree.item(self.clicked_item, 'values')
            if values and len(values) > 1:
                id_tache = values[1]  # Column B
                self._copy_to_clipboard(id_tache)
                self._update_status(f"ID tâche copié: {id_tache}")

        except Exception as e:
            self.logger.error(f"Error copying ID tâche: {e}")

    def _copy_code_insee(self):
        """Copy the code INSEE to clipboard."""
        try:
            if not hasattr(self, 'clicked_item') or not self.clicked_item:
                return

            values = self.tree.item(self.clicked_item, 'values')
            if values and len(values) > 2:
                code_insee = values[2]  # Column C
                self._copy_to_clipboard(code_insee)
                self._update_status(f"Code INSEE copié: {code_insee}")

        except Exception as e:
            self.logger.error(f"Error copying code INSEE: {e}")



    def _copy_to_clipboard(self, text):
        """Copy text to system clipboard."""
        try:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(str(text))
            self.parent.update()  # Ensure clipboard is updated

        except Exception as e:
            self.logger.error(f"Error copying to clipboard: {e}")
            # Fallback: show the text in a dialog for manual copying
            messagebox.showinfo(
                "Copie manuelle",
                f"Impossible de copier automatiquement.\nVeuillez copier manuellement:\n\n{text}"
            )

    def _open_commune_excel_file(self, nom_commune: str, id_tache: str):
        """Open the Excel file for a specific commune in Teams."""
        try:
            import subprocess
            import os

            # Get Teams base path for individual files
            teams_base_path = TeamsConfig.get_teams_base_path()

            # Construct folder name using the pattern: {nom_commune}_{id_tache}
            folder_name = f"{nom_commune}_{id_tache}"

            # Construct full folder path
            folder_path = os.path.join(teams_base_path, folder_name)

            # Expected Excel file name
            excel_filename = f"Suivi_{nom_commune}.xlsx"
            excel_file_path = os.path.join(folder_path, excel_filename)

            # Check if file exists
            if os.path.exists(excel_file_path):
                # Open the Excel file directly
                try:
                    os.startfile(excel_file_path)
                    self._update_status(f"Ouverture du fichier: {excel_filename}")
                    self.logger.info(f"Opened Excel file: {excel_file_path}")

                    # Show success message
                    messagebox.showinfo(
                        "Fichier ouvert",
                        f"Le fichier Excel pour '{nom_commune}' a été ouvert dans Excel."
                    )
                except Exception as e:
                    self.logger.error(f"Error opening Excel file with startfile: {e}")
                    # Fallback to subprocess
                    subprocess.run(['start', '', excel_file_path], shell=True, check=True)
                    self._update_status(f"Ouverture du fichier: {excel_filename}")

            elif os.path.exists(folder_path):
                # File doesn't exist but folder does - look for any Excel file in folder
                excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') and 'Suivi' in f]

                if excel_files:
                    # Found Excel file(s), open the first one
                    found_excel = excel_files[0]
                    found_excel_path = os.path.join(folder_path, found_excel)

                    try:
                        os.startfile(found_excel_path)
                        self._update_status(f"Ouverture du fichier: {found_excel}")
                        self.logger.info(f"Opened Excel file: {found_excel_path}")

                        messagebox.showinfo(
                            "Fichier trouvé et ouvert",
                            f"Le fichier '{found_excel}' a été ouvert dans Excel."
                        )
                    except Exception as e:
                        self.logger.error(f"Error opening found Excel file: {e}")
                        # Fallback to opening folder
                        subprocess.run(['explorer', folder_path], check=True)
                        messagebox.showwarning(
                            "Erreur d'ouverture",
                            f"Impossible d'ouvrir le fichier '{found_excel}'.\n"
                            f"Le dossier '{folder_name}' a été ouvert à la place."
                        )
                else:
                    # No Excel file found, open folder
                    subprocess.run(['explorer', folder_path], check=True)
                    self._update_status(f"Dossier ouvert: {folder_name}")

                    messagebox.showwarning(
                        "Fichier non trouvé",
                        f"Aucun fichier Excel de suivi trouvé dans le dossier '{folder_name}'.\n"
                        f"Le dossier a été ouvert pour vérification manuelle."
                    )

            else:
                # Neither file nor folder exists
                messagebox.showerror(
                    "Dossier non trouvé",
                    f"Le dossier '{folder_name}' n'existe pas dans Teams.\n\n"
                    f"Chemin attendu:\n{folder_path}\n\n"
                    f"Assurez-vous que le suivi pour cette commune a été généré."
                )

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error opening file/folder: {e}")
            messagebox.showerror(
                "Erreur d'ouverture",
                f"Impossible d'ouvrir le fichier ou dossier:\n{e}"
            )

        except Exception as e:
            self.logger.error(f"Error opening commune Excel file: {e}")
            messagebox.showerror(
                "Erreur",
                f"Erreur lors de l'ouverture du fichier:\n{e}"
            )

    def _clear_filters(self):
        """Clear all filters."""
        self.commune_search_var.set('')  # Clear Commune filter
        self.search_var.set('')
        self.insee_search_var.set('')  # Clear INSEE filter
        self.domaine_filter_var.set('')  # Clear Domaine filter
        self.etat_filter_var.set('')
        self.collaborateur_filter_var.set('')

        # Reset date selections
        try:
            self.date_from_selected = None
            self.date_to_selected = None

            # Reset button texts
            if hasattr(self, 'date_from_button'):
                self.date_from_button.config(text="📅 De")
            if hasattr(self, 'date_to_button'):
                self.date_to_button.config(text="📅 À")

            # Apply filters after clearing
            self._apply_filters()
        except Exception as e:
            self.logger.error(f"Error clearing date filters: {e}")
    
    def _go_home(self):
        """Navigate back to home screen."""
        try:
            if self.navigation_manager:
                from ui.navigation import NavigationState
                self.navigation_manager.navigate_to(NavigationState.HOME)
            else:
                self.logger.error("Navigation manager not available")
        except Exception as e:
            self.logger.error(f"Error navigating to home: {e}")

    def _refresh_data(self):
        """Refresh data from file."""
        self._load_data()

    def _update_status(self, message: str):
        """Update status bar message."""
        if self.status_label:
            self.status_label.config(text=message)

    def _update_data_info(self, message: str):
        """Update data info label."""
        if hasattr(self, 'data_info_label') and self.data_info_label:
            self.data_info_label.config(text=message)
    
    def cleanup(self):
        """Clean up resources when module is closed."""
        try:
            self.logger.info("Data Viewer module cleaned up")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

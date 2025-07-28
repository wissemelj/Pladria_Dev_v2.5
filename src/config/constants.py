"""
Configuration constants for the Suivi Generator application.
Centralized configuration management for colors, validation lists, and UI settings.
"""

# Color scheme for the application - Inspired by Sofrecom design language
COLORS = {
    'PRIMARY': "#0066CC",       # Bleu Sofrecom principal
    'PRIMARY_LIGHT': "#3385D6", # Bleu clair
    'PRIMARY_DARK': "#004499",  # Bleu foncé
    'SECONDARY': "#FF6600",     # Orange Sofrecom (accent)
    'SECONDARY_LIGHT': "#FF8533", # Orange clair
    'SUCCESS': "#28A745",       # Vert moderne
    'WARNING': "#FFC107",       # Jaune d'avertissement
    'DANGER': "#DC3545",        # Rouge d'erreur
    'ERROR': "#DC3545",         # Rouge d'erreur (alias pour DANGER)
    'INFO': "#495057",          # Gris informatif plus foncé
    'TEXT_PRIMARY': "#212529",  # Texte principal (noir doux)
    'TEXT_SECONDARY': "#6C757D", # Texte secondaire
    'TEXT_MUTED': "#ADB5BD",    # Texte atténué
    'LIGHT': "#F8F9FA",         # Gris très clair
    'WHITE': "#FFFFFF",         # Blanc pur
    'BORDER': "#E9ECEF",        # Bordure subtile
    'SHADOW': "#00000015",      # Ombre légère
    'BG': "#FFFFFF",           # Arrière-plan principal blanc
    'CARD': "#FFFFFF",         # Arrière-plan des cartes
    'CARD_HOVER': "#F8F9FA",   # Arrière-plan des cartes au hover
    'ACCENT': "#E3F2FD",       # Bleu très clair pour les accents
    'GRADIENT_START': "#0066CC", # Début du gradient
    'GRADIENT_END': "#004499"   # Fin du gradient
}

# Validation lists for dropdown menus
VALIDATION_LISTS = {
    "Domaine": ["Orange", "RIP"],
    "Type de Commune": ["Classique", "Fusionné"],
    "Type de base": ["Mono-Base", "Multi-Base"],
    "Motif Voie": ["Création Voie", "Modification Voie", "Rien à faire"],
    "STATUT Ticket": ["Traité", "En Cours", "En Attente", "Bloqué", "Rejeté"],
    "Etat": ["Traité", "En Cours", "En Attente", "Bloqué", "Rejeté"],
    "Depose Ticket UPR": ["Non Créé", "Créé"],
    "PC Status": ["PC trouvé sur la voie", "PC fictif ajouté"],
    "XY Status": ["RAS", "MàJ XY effectué dans Oras", "Modification libélle 42C"],
    "Collaborateur": [
        "ATTAFI Aya",
        "AZIZA Ala",
        "BACHOUEL Iheb",
        "BEN ALI Mariem",
        "BEN HADJ HSSINE Arij",
        "BOUOKKEZ Achraf",
        "BOUTEJ Yosr",
        "CHAOUCH Yasmine",
        "CHERNI Louay",
        "DAKHLI Shady",
        "ELJ Wissem",
        "FRIGUI Rayene",
        "KHCHIMI Ghada",
        "KORBI Zaineb",
        "MADHBOUH Roua",
        "NOUIRA Iyed",
        "OUESLATI Mohamed Amine",
        "REZGUI Ichrak",
        "SAHLI Nadine",
        "SAMAALI Fatma",
        "SOUISSI Takoua",
        "WARDI Aymen",
        "ZAOUGA Wissem",
        "ZARROUK Mariem",
        "ZGOLLI Iheb"
    ]

}

# UI Configuration
class UIConfig:
    """UI configuration constants with responsive font support"""

    # Window settings - Ultra minimal for maximum compatibility
    WINDOW_TITLE = "Pladria - Activité Plan Adressage"
    WINDOW_MIN_SIZE = "550x400"  # Further reduced for ultra minimal fit
    WINDOW_DEFAULT_SIZE = "600x450"  # Further reduced for ultra minimal default

    # Base font sizes (will be scaled by ResponsiveManager) - Ultra minimal
    BASE_FONT_SIZES = {
        'title': 5,          # Ultra minimal for title
        'subtitle': 4,       # Ultra minimal for subtitle
        'button': 4,         # Ultra minimal for buttons
        'header': 6,         # Ultra minimal for headers
        'subheader': 5,      # Ultra minimal for subheaders
        'small': 4,          # Ultra minimal for small text
        'large': 7,          # Ultra minimal for large text
        'card_title': 5,     # Ultra minimal for card titles
        'card_subtitle': 4,  # Ultra minimal for card subtitles
        'card_description': 4 # Ultra minimal for card descriptions
    }

    # Typography - Sofrecom inspired, professional and readable
    # These will be dynamically updated by ResponsiveManager
    FONT_TITLE = ("Segoe UI", 11, "bold")
    FONT_SUBTITLE = ("Segoe UI", 9)
    FONT_BUTTON = ("Segoe UI", 9, "bold")
    FONT_HEADER = ("Segoe UI", 14, "bold")
    FONT_SUBHEADER = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 8)
    FONT_LARGE = ("Segoe UI", 16, "bold")
    FONT_CARD_TITLE = ("Segoe UI", 12, "bold")
    FONT_CARD_SUBTITLE = ("Segoe UI", 9)
    FONT_CARD_DESCRIPTION = ("Segoe UI", 8)

    @classmethod
    def update_responsive_fonts(cls, responsive_manager):
        """Update font configurations with responsive scaling."""
        try:
            cls.FONT_TITLE = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['title'], "bold")
            cls.FONT_SUBTITLE = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['subtitle'])
            cls.FONT_BUTTON = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['button'], "bold")
            cls.FONT_HEADER = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['header'], "bold")
            cls.FONT_SUBHEADER = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['subheader'])
            cls.FONT_SMALL = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['small'])
            cls.FONT_LARGE = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['large'], "bold")
            cls.FONT_CARD_TITLE = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['card_title'], "bold")
            cls.FONT_CARD_SUBTITLE = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['card_subtitle'])
            cls.FONT_CARD_DESCRIPTION = responsive_manager.get_responsive_font("Segoe UI", cls.BASE_FONT_SIZES['card_description'])
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to update responsive fonts: {e}")

# File processing configuration
class FileConfig:
    """File processing configuration"""
    
    # QGis columns to import
    QGIS_COLUMNS = "A,B,C,D,G,J,O,P,Q,R"
    QGIS_COLUMNS_WITH_U = "A,B,C,D,G,J,O,P,Q,R,U"
    
    # Supported file types
    EXCEL_FILETYPES = [("Fichiers Excel", "*.xlsx *.xls")]
    
    # Column mappings for Plan Adressage
    PLAN_ADRESSAGE_COLUMNS = [
        'Num Dossier Site',      # Colonne A du fichier source
        'Num Voie Site',         # Colonne B du fichier source
        'Comp Voie Site',        # Colonne C du fichier source
        'Libelle Voie Site',     # Colonne D du fichier source
        'Batiment IMB',          # Colonne G du fichier source
        'Motif',                 # Colonne J du fichier source
        'Même Adresse',          # Colonne O du fichier source
        'Numero Voie BAN',       # Colonne P du fichier source
        'Repondant Voie BAN',    # Colonne Q du fichier source
        'Libelle Voie BAN'       # Colonne R du fichier source
    ]
    
    PLAN_ADRESSAGE_COLUMNS_WITH_U = PLAN_ADRESSAGE_COLUMNS + ['Adresse BAN']  # Colonne U

# Application metadata
class AppInfo:
    """Application information"""

    VERSION = "2.5"
    AUTHOR = "Equipe Plan Adressage - BLI"
    COPYRIGHT = "© 2025 Sofrecom Tunisie"
    DESCRIPTION = "Pladria - Activité Plan Adressae"
    FULL_DESCRIPTION = "Pladria : Une Initiative pour automatiser la génération des suivis pour l'activité CMS Adresse & Plan Adressage"

# Logging configuration
class LoggingConfig:
    """Logging configuration constants"""

    DEFAULT_LEVEL = "INFO"
    FILE_LOGGING = True
    LOG_FORMAT_CONSOLE = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FORMAT_FILE = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5



# Teams Channel configuration
class TeamsConfig:
    """Microsoft Teams channel configuration"""

    @staticmethod
    def get_teams_base_path():
        """
        Get the Teams base path dynamically based on current user.

        Returns:
            str: Teams base path for current user
        """
        import getpass

        # Get current username
        username = getpass.getuser()

        # Use AccessControl to get the correct Teams path
        teams_base = AccessControl.get_teams_path_for_user(username)
        teams_path = rf"{teams_base}\Suivis CMS Adresse_Plan Adressage\Actes des Traitements"

        return teams_path

    @staticmethod
    def get_global_teams_path():
        """
        Get the Teams global path for Suivi Global module.

        Returns:
            str: Teams global path for current user
        """
        import getpass

        # Get current username
        username = getpass.getuser()

        # Use AccessControl to get the correct Teams path
        teams_base = AccessControl.get_teams_path_for_user(username)
        global_path = rf"{teams_base}\Suivis CMS Adresse_Plan Adressage\Suivis Global Tickets CMS Adresse_Plan Adressage"

        return global_path

    @staticmethod
    def get_quality_control_teams_path():
        """
        Get the Teams path for Quality Control module.

        Returns:
            str: Teams quality control path for current user
        """
        import getpass

        # Get current username
        username = getpass.getuser()

        # Use AccessControl to get the correct Teams path
        teams_base = AccessControl.get_teams_path_for_user(username)
        quality_control_path = rf"{teams_base}\Suivis CMS Adresse_Plan Adressage\Contrôle Qualité"

        return quality_control_path

    # Legacy property for backward compatibility
    @property
    def TEAMS_BASE_PATH(self):
        return self.get_teams_base_path()

    # Folder naming pattern: NomCommune_IdTache
    FOLDER_NAME_PATTERN = "{nom_commune}_{id_tache}"

    # Enable automatic Teams saving (can be disabled for testing)
    ENABLE_TEAMS_SAVING = True

    # Fallback to file dialog if Teams path is not accessible
    FALLBACK_TO_DIALOG = True

class AccessControl:
    """
    Access control configuration for restricted modules.

    NOTE: Password protection added for Statistics Team module.
    All other modules remain accessible to all users.
    """

    # Password protection for Statistics Team module
    STATS_MODULE_PASSWORD = "G7v#9Lp@2Zm!XqRt"

    # Legacy authorized users list (no longer used for restrictions, kept for reference)
    AUTHORIZED_USERS = {
        'mbenali',      # User: mbenali
        'm.benali',     # User: m.benali (same person as mbenali, special Teams path)
        'welj',         # User: welj
        'wzaouga',      # User: wzaouga
        'awardi'        # User: awardi
    }

    # User aliases for Teams path mapping
    USER_ALIASES = {
        'm.benali': 'mbenali',  # m.benali is the same as mbenali (special Teams path handling)
    }

    @staticmethod
    def is_user_authorized(username=None):
        """
        Check if the current user is authorized to access restricted modules.

        NOTE: All restrictions have been removed - all users are now authorized.

        Args:
            username (str, optional): Username to check. If None, uses current user.

        Returns:
            bool: Always returns True (restrictions removed)
        """
        # All users are now authorized - restrictions removed
        return True

    @staticmethod
    def verify_stats_password(password):
        """
        Verify password for Statistics Team module access.

        Args:
            password (str): Password to verify

        Returns:
            bool: True if password is correct, False otherwise
        """
        return password == AccessControl.STATS_MODULE_PASSWORD

    @staticmethod
    def get_teams_path_for_user(username=None):
        """
        Get Teams path for user. Handles special case for m.benali user.

        Args:
            username (str, optional): Username to use for path construction

        Returns:
            str: Teams base path for the user
        """
        import getpass

        if username is None:
            username = getpass.getuser()

        # Special case: m.benali accesses Teams via a different path
        if username in ['m.benali', 'mbenali']:
         teams_path = r"C:\Users\m.benali\orange.com\BOT G2R - CM Adresses et Plan Adressage - CM Adresses et Plan Adressage"
         return teams_path

        # Use standard Teams path structure for all other users
        teams_path = rf"C:\Users\{username}\orange.com\BOT G2R - CM Adresses et Plan Adressage - CM Adresses et Plan Adressage"
        return teams_path

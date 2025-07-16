"""
File handling utilities for the Suivi Generator application.
"""

import os
import sys
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    
    Args:
        relative_path: Relative path to the resource
        
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        logger.debug(f"Running in PyInstaller mode, base path: {base_path}")
    except AttributeError:
        # Development mode
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logger.debug(f"Running in development mode, base path: {base_path}")
    
    full_path = os.path.join(base_path, relative_path)
    logger.debug(f"Resource path for '{relative_path}': {full_path}")
    return full_path


def get_logo_path() -> str:
    """
    Get the path to the application logo.

    Returns:
        Path to logo file
    """
    return get_resource_path("logo_Sofrecom.png")


def get_icon_path() -> str:
    """
    Get the path to the application icon.

    Returns:
        Path to icon file (prefers .ico over .png, validates .ico files)
    """
    # Try sharp .ico first, but validate it
    sharp_ico = get_resource_path("Icone_App_Sharp.ico")
    original_icon = get_resource_path("Icone_App.png")

    if os.path.exists(sharp_ico):
        # Validate that the .ico file is actually a valid ICO file
        try:
            with open(sharp_ico, 'rb') as f:
                # Read first few bytes to check ICO signature
                header = f.read(4)
                if header[:2] == b'\x00\x00' and header[2:4] == b'\x01\x00':
                    logger.debug(f"Using valid sharp icon: {sharp_ico}")
                    return sharp_ico
                else:
                    logger.warning(f"Invalid ICO file format: {sharp_ico}, falling back to PNG")
        except Exception as e:
            logger.warning(f"Error validating ICO file {sharp_ico}: {e}, falling back to PNG")

    logger.debug(f"Using original icon: {original_icon}")
    return original_icon


def create_ico_from_png(png_path: str, ico_path: str) -> bool:
    """
    Create a proper ICO file from a PNG file.

    Args:
        png_path: Path to the source PNG file
        ico_path: Path where to save the ICO file

    Returns:
        True if successful, False otherwise
    """
    try:
        from utils.lazy_imports import get_PIL
        Image, _ = get_PIL()

        if not os.path.exists(png_path):
            logger.error(f"Source PNG file not found: {png_path}")
            return False

        # Open the PNG image
        with Image.open(png_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Create multiple sizes for the ICO file (standard Windows icon sizes)
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

            # Create resized versions
            images = []
            for size in sizes:
                resized = img.resize(size, Image.Resampling.LANCZOS)
                images.append(resized)

            # Save as ICO with multiple sizes
            img.save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images])

            logger.info(f"Successfully created ICO file: {ico_path}")
            return True

    except Exception as e:
        logger.error(f"Failed to create ICO from PNG: {e}")
        return False


def ensure_valid_icon() -> str:
    """
    Ensure we have a valid icon file, creating one if necessary.

    Returns:
        Path to a valid icon file
    """
    sharp_ico = get_resource_path("Icone_App_Sharp.ico")
    original_png = get_resource_path("Icone_App.png")

    # Check if we have a valid ICO file
    if os.path.exists(sharp_ico):
        try:
            with open(sharp_ico, 'rb') as f:
                header = f.read(4)
                if header[:2] == b'\x00\x00' and header[2:4] == b'\x01\x00':
                    return sharp_ico
        except:
            pass

    # If ICO is invalid or missing, try to create it from PNG
    if os.path.exists(original_png):
        logger.info("Creating valid ICO file from PNG...")
        if create_ico_from_png(original_png, sharp_ico):
            return sharp_ico
        else:
            logger.warning("Failed to create ICO, using PNG fallback")
            return original_png

    logger.error("No valid icon files found")
    return original_png  # Return PNG path as fallback even if it doesn't exist


def validate_file_path(file_path: str) -> Dict[str, Any]:
    """
    Validate a file path and return status information.
    
    Args:
        file_path: Path to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'exists': False,
        'readable': False,
        'size': 0,
        'error': None
    }
    
    try:
        if not file_path:
            result['error'] = "File path is empty"
            return result
        
        path = Path(file_path)
        
        if not path.exists():
            result['error'] = f"File does not exist: {file_path}"
            return result
        
        result['exists'] = True
        
        if not os.access(file_path, os.R_OK):
            result['error'] = f"File is not readable: {file_path}"
            return result
        
        result['readable'] = True
        result['size'] = path.stat().st_size
        result['valid'] = True
        
    except Exception as e:
        result['error'] = f"Error validating file: {str(e)}"
        logger.error(f"File validation error for '{file_path}': {e}")
    
    return result


def get_safe_filename(filename: str) -> str:
    """
    Create a safe filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    safe_name = filename
    
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Remove multiple consecutive underscores
    while '__' in safe_name:
        safe_name = safe_name.replace('__', '_')
    
    # Remove leading/trailing underscores and spaces
    safe_name = safe_name.strip('_ ')
    
    return safe_name


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory '{directory_path}': {e}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension (including the dot)
    """
    return Path(file_path).suffix.lower()


def is_excel_file(file_path: str) -> bool:
    """
    Check if a file is an Excel file based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if it's an Excel file
    """
    excel_extensions = {'.xlsx', '.xls', '.xlsm', '.xlsb'}
    return get_file_extension(file_path) in excel_extensions


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)

    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1

    return f"{size:.1f} {size_names[i]}"


def check_file_access(file_path: str, mode: str = 'r') -> dict:
    """
    Check if a file can be accessed for reading or writing.

    Args:
        file_path: Path to the file to check
        mode: Access mode ('r' for read, 'w' for write, 'rw' for both)

    Returns:
        Dict with access status and user-friendly error messages
    """
    result = {
        'accessible': False,
        'exists': False,
        'readable': False,
        'writable': False,
        'error_type': None,
        'error_message': None,
        'user_message': None,
        'suggestions': []
    }

    try:
        # Check if file exists
        if os.path.exists(file_path):
            result['exists'] = True
            filename = os.path.basename(file_path)

            # Check read access
            if 'r' in mode:
                try:
                    with open(file_path, 'r', encoding='utf-8'):
                        pass
                    result['readable'] = True
                except PermissionError:
                    result['error_type'] = 'permission_denied'
                    result['error_message'] = f"Permission denied reading {filename}"
                    result['user_message'] = f"🔒 Le fichier '{filename}' est actuellement utilisé par Excel ou un autre programme."
                    result['suggestions'] = [
                        "Fermez Excel si le fichier y est ouvert",
                        "Vérifiez qu'aucun autre utilisateur n'utilise le fichier",
                        "Attendez quelques secondes et réessayez"
                    ]
                    return result
                except Exception as e:
                    result['error_type'] = 'read_error'
                    result['error_message'] = str(e)
                    result['user_message'] = f"❌ Impossible de lire le fichier '{filename}'"
                    result['suggestions'] = ["Vérifiez que le fichier n'est pas corrompu"]
                    return result

            # Check write access
            if 'w' in mode:
                try:
                    # Try to open in append mode to test write access without truncating
                    with open(file_path, 'a', encoding='utf-8'):
                        pass
                    result['writable'] = True
                except PermissionError:
                    result['error_type'] = 'file_locked'
                    result['error_message'] = f"File locked: {filename}"
                    result['user_message'] = f"🔒 Le fichier '{filename}' est ouvert dans Excel ou verrouillé par un autre processus."
                    result['suggestions'] = [
                        "Fermez Excel complètement",
                        "Vérifiez qu'aucun autre utilisateur ne modifie le fichier",
                        "Redémarrez Excel si nécessaire",
                        "Attendez quelques instants et réessayez"
                    ]
                    return result
                except Exception as e:
                    result['error_type'] = 'write_error'
                    result['error_message'] = str(e)
                    result['user_message'] = f"❌ Impossible d'écrire dans le fichier '{filename}'"
                    result['suggestions'] = ["Vérifiez les permissions du dossier"]
                    return result

            result['accessible'] = True

        else:
            result['error_type'] = 'not_found'
            result['error_message'] = f"File not found: {file_path}"
            result['user_message'] = f"📁 Le fichier '{os.path.basename(file_path)}' n'existe pas encore."
            result['suggestions'] = ["Le fichier sera créé automatiquement"]

    except Exception as e:
        result['error_type'] = 'unexpected'
        result['error_message'] = str(e)
        result['user_message'] = f"❌ Erreur inattendue lors de la vérification du fichier"
        result['suggestions'] = ["Contactez le support technique"]

    return result


def is_excel_file_open(file_path: str) -> bool:
    """
    Check if an Excel file is currently open by trying to access it.

    Args:
        file_path: Path to the Excel file

    Returns:
        True if file appears to be open/locked, False otherwise
    """
    if not os.path.exists(file_path):
        return False

    try:
        # Try to open the file in write mode
        with open(file_path, 'r+b'):
            pass
        return False  # File is not locked
    except (PermissionError, OSError):
        return True  # File is likely open in Excel
    except Exception:
        return False  # Other errors, assume not locked


def truncate_filename(filename: str, max_length: int = 50) -> str:
    """
    Truncate a filename for display purposes.

    Args:
        filename: Original filename
        max_length: Maximum length for display

    Returns:
        Truncated filename with ellipsis if needed
    """
    if len(filename) <= max_length:
        return filename

    return filename[:max_length-3] + "..."


def generate_teams_folder_path(nom_commune: str, id_tache: str) -> str:
    """
    Generate the Teams channel folder path for a specific commune and task.

    Args:
        nom_commune: Name of the commune
        id_tache: Task ID

    Returns:
        Full path to the Teams folder
    """
    from config.constants import TeamsConfig

    # Create safe folder name
    folder_name = TeamsConfig.FOLDER_NAME_PATTERN.format(
        nom_commune=get_safe_filename(nom_commune),
        id_tache=get_safe_filename(id_tache)
    )

    # Combine with base Teams path (dynamic)
    teams_folder_path = os.path.join(TeamsConfig.get_teams_base_path(), folder_name)

    logger.info(f"Generated Teams folder path: {teams_folder_path}")
    return teams_folder_path


def validate_teams_path() -> Dict[str, Any]:
    """
    Validate that the Teams channel base path is accessible.

    Returns:
        Dictionary with validation results
    """
    from config.constants import TeamsConfig

    result = {
        'valid': False,
        'exists': False,
        'writable': False,
        'path': TeamsConfig.TEAMS_BASE_PATH,
        'error': None
    }

    try:
        teams_base_path = TeamsConfig.get_teams_base_path()
        base_path = Path(teams_base_path)
        result['path'] = teams_base_path

        if not base_path.exists():
            result['error'] = f"Teams channel path does not exist: {teams_base_path}"
            return result

        result['exists'] = True

        # Test write access by trying to create a temporary directory
        test_dir = base_path / "test_write_access"
        try:
            test_dir.mkdir(exist_ok=True)
            test_dir.rmdir()
            result['writable'] = True
            result['valid'] = True
        except PermissionError:
            result['error'] = f"No write permission to Teams channel path: {teams_base_path}"
        except Exception as e:
            result['error'] = f"Cannot write to Teams channel path: {str(e)}"

    except Exception as e:
        result['error'] = f"Error validating Teams path: {str(e)}"
        logger.error(f"Teams path validation error: {e}")

    return result


def create_teams_folder(nom_commune: str, id_tache: str) -> Dict[str, Any]:
    """
    Create the Teams folder for a specific commune and task.

    Args:
        nom_commune: Name of the commune
        id_tache: Task ID

    Returns:
        Dictionary with creation results
    """
    result = {
        'success': False,
        'path': None,
        'created': False,
        'error': None
    }

    try:
        # Generate folder path
        folder_path = generate_teams_folder_path(nom_commune, id_tache)
        result['path'] = folder_path

        # Check if folder already exists
        if os.path.exists(folder_path):
            result['success'] = True
            result['created'] = False
            logger.info(f"Teams folder already exists: {folder_path}")
            return result

        # Create the folder
        if ensure_directory_exists(folder_path):
            result['success'] = True
            result['created'] = True
            logger.info(f"Teams folder created successfully: {folder_path}")
        else:
            result['error'] = f"Failed to create Teams folder: {folder_path}"

    except Exception as e:
        result['error'] = f"Error creating Teams folder: {str(e)}"
        logger.error(f"Teams folder creation error: {e}")

    return result


def get_teams_file_path(nom_commune: str, id_tache: str, filename: str) -> str:
    """
    Generate the complete file path for saving to Teams channel.

    Args:
        nom_commune: Name of the commune
        id_tache: Task ID
        filename: Name of the file to save

    Returns:
        Complete file path in Teams channel
    """
    folder_path = generate_teams_folder_path(nom_commune, id_tache)
    file_path = os.path.join(folder_path, filename)

    logger.info(f"Generated Teams file path: {file_path}")
    return file_path

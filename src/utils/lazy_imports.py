"""
Lazy import utilities for optimizing application startup time.
Heavy dependencies are loaded only when needed.
"""

import logging

# Global variables to store imported modules
_pandas = None
_PIL_Image = None
_PIL_ImageTk = None

# Cache for import status
_import_cache = {}

logger = logging.getLogger(__name__)


def get_pandas():
    """
    Lazy loading of pandas for optimizing startup time.

    Returns:
        pandas module
    """
    global _pandas
    if _pandas is None:
        try:
            # Use cache to avoid repeated import attempts
            if 'pandas' in _import_cache:
                _pandas = _import_cache['pandas']
            else:
                import pandas as pd
                _pandas = pd
                _import_cache['pandas'] = pd
                logger.debug("Pandas loaded successfully")
        except ImportError as e:
            logger.error(f"Failed to import pandas: {e}")
            raise ImportError("pandas is required but not installed. Please install it with: pip install pandas")
    return _pandas


def get_PIL():
    """
    Lazy loading of PIL for optimizing startup time.

    Returns:
        Tuple of (Image, ImageTk) modules
    """
    global _PIL_Image, _PIL_ImageTk
    if _PIL_Image is None or _PIL_ImageTk is None:
        try:
            # Use cache to avoid repeated import attempts
            if 'PIL_Image' in _import_cache and 'PIL_ImageTk' in _import_cache:
                _PIL_Image = _import_cache['PIL_Image']
                _PIL_ImageTk = _import_cache['PIL_ImageTk']
            else:
                from PIL import Image, ImageTk
                _PIL_Image = Image
                _PIL_ImageTk = ImageTk
                _import_cache['PIL_Image'] = Image
                _import_cache['PIL_ImageTk'] = ImageTk
                logger.info("PIL loaded successfully")
        except ImportError as e:
            logger.error(f"Failed to import PIL: {e}")
            raise ImportError("Pillow is required but not installed. Please install it with: pip install Pillow")
    return _PIL_Image, _PIL_ImageTk



def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        Dict with dependency status
    """
    dependencies = {
        'pandas': False,
        'PIL': False,
        'openpyxl': False
    }
    
    # Check pandas
    try:
        import pandas
        dependencies['pandas'] = True
    except ImportError:
        pass
    
    # Check PIL
    try:
        from PIL import Image, ImageTk
        dependencies['PIL'] = True
    except ImportError:
        pass
    
    # Check openpyxl
    try:
        import openpyxl
        dependencies['openpyxl'] = True
    except ImportError:
        pass
    
    return dependencies


def get_missing_dependencies():
    """
    Get list of missing dependencies.
    
    Returns:
        List of missing dependency names
    """
    deps = check_dependencies()
    return [name for name, available in deps.items() if not available]


def install_instructions():
    """
    Get installation instructions for missing dependencies.
    
    Returns:
        String with installation instructions
    """
    missing = get_missing_dependencies()
    if not missing:
        return "All dependencies are installed."
    
    instructions = "Missing dependencies found. Please install them:\n\n"
    
    if 'pandas' in missing:
        instructions += "pip install pandas\n"
    if 'PIL' in missing:
        instructions += "pip install Pillow\n"
    if 'openpyxl' in missing:
        instructions += "pip install openpyxl\n"
    
    instructions += "\nOr install all at once:\n"
    instructions += "pip install pandas Pillow openpyxl"
    
    return instructions

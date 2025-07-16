"""
Responsive UI utilities for dynamic scaling and layout adaptation.
Handles DPI awareness, font scaling, and responsive breakpoints.
"""

import tkinter as tk
import logging
from typing import Tuple, Dict, Any
import platform


class ResponsiveManager:
    """Manages responsive UI behavior including DPI scaling and layout adaptation."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the responsive manager.
        
        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.logger = logging.getLogger(__name__)
        
        # DPI and scaling factors
        self.dpi_scale = 1.0
        self.font_scale = 1.0
        self.ui_scale = 1.0
        
        # Screen dimensions
        self.screen_width = 0
        self.screen_height = 0
        
        # Responsive breakpoints (in pixels)
        self.breakpoints = {
            'xs': 480,   # Extra small screens
            'sm': 768,   # Small screens  
            'md': 1024,  # Medium screens
            'lg': 1366,  # Large screens
            'xl': 1920   # Extra large screens
        }
        
        # Initialize scaling
        self._detect_dpi_scaling()
        self._update_screen_dimensions()
        
    def _detect_dpi_scaling(self):
        """Detect system DPI scaling and calculate appropriate scale factors."""
        try:
            # Get DPI information
            dpi_x = self.root.winfo_fpixels('1i')  # Pixels per inch
            dpi_y = self.root.winfo_fpixels('1i')
            
            # Standard DPI is 96 on Windows, 72 on Mac
            standard_dpi = 96 if platform.system() == 'Windows' else 72
            
            # Calculate DPI scale factor
            self.dpi_scale = dpi_x / standard_dpi
            
            # Font scaling - ultra-conservative for corporate environments - maximum compactness
            if self.dpi_scale <= 1.0:
                self.font_scale = 0.8  # Smaller fonts for compact view
            elif self.dpi_scale <= 1.25:
                # For 125% scaling, make fonts much smaller to fit everything
                self.font_scale = 0.7  # 30% smaller fonts at 125%
            elif self.dpi_scale <= 1.5:
                self.font_scale = 0.75  # Still very compact at 150%
            elif self.dpi_scale <= 2.0:
                self.font_scale = 0.8  # Compact size at 200%
            else:
                self.font_scale = 0.9  # Still compact for very high DPI

            # UI scaling for padding, margins, etc. - ultra minimal for maximum compactness
            if self.dpi_scale <= 1.25:
                self.ui_scale = 0.3  # Ultra minimal UI elements at 125% to fit everything
            elif self.dpi_scale <= 1.5:
                self.ui_scale = 0.4  # Ultra minimal at 150%
            else:
                self.ui_scale = min(self.dpi_scale * 0.3, 0.6)  # Ultra minimal scaling
            
            self.logger.info(f"DPI scaling detected - DPI: {dpi_x:.1f}, Scale: {self.dpi_scale:.2f}, Font: {self.font_scale:.2f}, UI: {self.ui_scale:.2f}")
            
        except Exception as e:
            self.logger.warning(f"Could not detect DPI scaling: {e}")
            self.dpi_scale = 1.0
            self.font_scale = 1.0
            self.ui_scale = 1.0
    
    def _update_screen_dimensions(self):
        """Update current screen dimensions."""
        try:
            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()
            self.logger.debug(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
        except Exception as e:
            self.logger.warning(f"Could not get screen dimensions: {e}")
            self.screen_width = 1920
            self.screen_height = 1080
    
    def get_screen_category(self) -> str:
        """
        Get the current screen size category based on width.
        
        Returns:
            Screen category: 'xs', 'sm', 'md', 'lg', or 'xl'
        """
        width = self.screen_width
        
        if width < self.breakpoints['xs']:
            return 'xs'
        elif width < self.breakpoints['sm']:
            return 'sm'
        elif width < self.breakpoints['md']:
            return 'md'
        elif width < self.breakpoints['lg']:
            return 'lg'
        else:
            return 'xl'
    
    def scale_font_size(self, base_size: int) -> int:
        """
        Scale font size based on DPI and screen size.
        
        Args:
            base_size: Base font size in points
            
        Returns:
            Scaled font size
        """
        scaled_size = int(base_size * self.font_scale)
        
        # Ensure minimum readable size
        min_size = 8
        max_size = 24
        
        return max(min_size, min(scaled_size, max_size))
    
    def scale_dimension(self, dimension: int) -> int:
        """
        Scale UI dimension (padding, margins, etc.) based on DPI.
        
        Args:
            dimension: Base dimension in pixels
            
        Returns:
            Scaled dimension
        """
        return int(dimension * self.ui_scale)
    
    def get_responsive_font(self, base_family: str, base_size: int, weight: str = "normal") -> Tuple[str, int, str]:
        """
        Get a responsive font tuple.
        
        Args:
            base_family: Font family name
            base_size: Base font size
            weight: Font weight
            
        Returns:
            Font tuple (family, size, weight)
        """
        scaled_size = self.scale_font_size(base_size)
        return (base_family, scaled_size, weight)
    
    def get_responsive_padding(self, base_padding: int) -> int:
        """Get responsive padding value - maximum compact for corporate environments."""
        # For corporate environments, use minimal padding to maximize content space
        scaled = self.scale_dimension(base_padding)

        # Apply ultra minimal reduction for all elements to fit on screen
        if self.dpi_scale <= 1.25:
            # At 125% scaling, use 15% of base padding for ultra minimal layout
            return max(int(base_padding * 0.15), 1)  # Minimum 1px padding
        else:
            return max(int(scaled * 0.2), 1)  # Ultra minimal for higher scaling

    def get_responsive_margins(self, base_margin: int) -> int:
        """Get responsive margin value - maximum compact for corporate environments."""
        # Similar approach for margins - maximum compact
        scaled = self.scale_dimension(base_margin)

        if self.dpi_scale <= 1.25:
            # At 125% scaling, use 10% of base margins for ultra minimal layout
            return max(int(base_margin * 0.1), 1)  # Minimum 1px margin
        else:
            return max(int(scaled * 0.15), 1)  # Ultra minimal for higher scaling
    
    def get_minimum_window_size(self) -> Tuple[int, int]:
        """
        Get appropriate minimum window size based on screen - ultra compact for maximum compatibility.

        Returns:
            Tuple of (min_width, min_height)
        """
        screen_cat = self.get_screen_category()

        if screen_cat == 'xs':
            return (320, 250)  # Ultra minimal for very small screens
        elif screen_cat == 'sm':
            return (450, 350)  # Ultra minimal for small screens
        elif screen_cat == 'md':
            return (550, 400)  # Ultra minimal for medium screens
        else:
            return (600, 450)  # Ultra minimal for large screens
    
    def get_responsive_column_config(self) -> Dict[str, Any]:
        """
        Get responsive column configuration based on screen size.
        
        Returns:
            Dictionary with column configuration
        """
        screen_cat = self.get_screen_category()
        
        if screen_cat in ['xs', 'sm']:
            # Single column layout for small screens
            return {
                'columns': 1,
                'left_weight': 1,
                'middle_weight': 0,
                'right_weight': 0,
                'left_minsize': 250,  # Reduced for compactness
                'middle_minsize': 0,
                'right_minsize': 0
            }
        elif screen_cat == 'md':
            # Two column layout for medium screens
            return {
                'columns': 2,
                'left_weight': 1,
                'middle_weight': 1,
                'right_weight': 0,
                'left_minsize': 280,  # Reduced for compactness
                'middle_minsize': 280,  # Reduced for compactness
                'right_minsize': 0
            }
        else:
            # Three column layout for large screens - more compact
            return {
                'columns': 3,
                'left_weight': 0,
                'middle_weight': 1,
                'right_weight': 0,
                'left_minsize': self.scale_dimension(150),  # Reduced from 200
                'middle_minsize': self.scale_dimension(300),  # Reduced from 400
                'right_minsize': self.scale_dimension(200)   # Reduced from 250
            }
    
    def should_use_compact_layout(self) -> bool:
        """Determine if compact layout should be used."""
        return self.get_screen_category() in ['xs', 'sm']
    
    def get_adaptive_card_padding(self) -> Tuple[int, int]:
        """
        Get adaptive padding for cards based on screen size - maximum compact for corporate environments.

        Returns:
            Tuple of (horizontal_padding, vertical_padding)
        """
        screen_cat = self.get_screen_category()

        # Ultra minimal padding for corporate environments
        if screen_cat == 'xs':
            return (2, 1)  # Ultra minimal for small screens
        elif screen_cat == 'sm':
            return (3, 1)  # Ultra minimal for small screens
        else:
            # For larger screens, use ultra minimal padding
            if self.dpi_scale <= 1.25:
                # At 125% scaling, use ultra minimal padding
                return (3, 1)  # Ultra minimal
            else:
                return (self.scale_dimension(4), self.scale_dimension(2))

    def get_corporate_spacing(self) -> Dict[str, int]:
        """
        Get maximum compact corporate-optimized spacing values.

        Returns:
            Dictionary with maximum compact spacing values for corporate environments
        """
        return {
            'card_padding_x': 3 if self.dpi_scale <= 1.25 else self.scale_dimension(4),
            'card_padding_y': 1 if self.dpi_scale <= 1.25 else self.scale_dimension(2),
            'section_margin': 1 if self.dpi_scale <= 1.25 else self.scale_dimension(2),
            'element_spacing': 1 if self.dpi_scale <= 1.25 else self.scale_dimension(2),
            'button_padding_x': 3 if self.dpi_scale <= 1.25 else self.scale_dimension(4),
            'button_padding_y': 1 if self.dpi_scale <= 1.25 else self.scale_dimension(1),
            'card_margin': 1 if self.dpi_scale <= 1.25 else self.scale_dimension(1),
            'header_padding': 1 if self.dpi_scale <= 1.25 else self.scale_dimension(2)
        }


# Global responsive manager instance
_responsive_manager = None


def get_responsive_manager(root: tk.Tk = None) -> ResponsiveManager:
    """
    Get the global responsive manager instance.
    
    Args:
        root: Root window (required for first call)
        
    Returns:
        ResponsiveManager instance
    """
    global _responsive_manager
    
    if _responsive_manager is None:
        if root is None:
            raise ValueError("Root window required for first call to get_responsive_manager")
        _responsive_manager = ResponsiveManager(root)
    
    return _responsive_manager


def create_responsive_frame(parent: tk.Widget, **kwargs) -> tk.Frame:
    """
    Create a frame with responsive padding and margins.
    
    Args:
        parent: Parent widget
        **kwargs: Additional frame options
        
    Returns:
        Responsive frame widget
    """
    rm = get_responsive_manager()
    
    # Apply responsive padding if not specified - ultra minimal
    if 'padx' not in kwargs:
        kwargs['padx'] = rm.get_responsive_padding(3)  # Ultra minimal padding
    if 'pady' not in kwargs:
        kwargs['pady'] = rm.get_responsive_padding(3)  # Ultra minimal padding
    
    return tk.Frame(parent, **kwargs)

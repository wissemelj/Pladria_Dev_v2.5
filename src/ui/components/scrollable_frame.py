"""
Scrollable frame component with horizontal and vertical scrolling support.
Provides responsive scrolling behavior for content that might overflow.
"""

import tkinter as tk
from tkinter import ttk
import logging
from typing import Optional, Callable


class ScrollableFrame(tk.Frame):
    """A frame that provides both horizontal and vertical scrolling capabilities."""
    
    def __init__(self, parent, **kwargs):
        """
        Initialize the scrollable frame.
        
        Args:
            parent: Parent widget
            **kwargs: Additional frame options
        """
        super().__init__(parent, **kwargs)
        
        self.logger = logging.getLogger(__name__)
        
        # Create canvas and scrollbars
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        # Create the scrollable frame with no padding
        self.scrollable_frame = tk.Frame(self.canvas, bd=0, highlightthickness=0)
        
        # Configure canvas
        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )
        
        # Create window in canvas - ensure it starts at top-left with no offset
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        
        # Bind events
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mouse wheel support
        self._bind_mousewheel()
        
        # Layout scrollbars and canvas
        self._layout_components()
        
        # Track if scrollbars are visible
        self.v_scrollbar_visible = False
        self.h_scrollbar_visible = False
    
    def _layout_components(self):
        """Layout the canvas and scrollbars."""
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Place canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Initially hide scrollbars - they'll be shown when needed
        self.v_scrollbar.grid_remove()
        self.h_scrollbar.grid_remove()
    
    def _on_frame_configure(self, event=None):
        """Handle frame resize to update scroll region."""
        try:
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Check if scrollbars are needed
            self._update_scrollbar_visibility()
            
        except Exception as e:
            self.logger.debug(f"Error in frame configure: {e}")
    
    def _on_canvas_configure(self, event=None):
        """Handle canvas resize to update frame width."""
        try:
            # Update the scrollable frame width to match canvas width if content is smaller
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Get the required size of the content
                self.scrollable_frame.update_idletasks()
                required_width = self.scrollable_frame.winfo_reqwidth()
                required_height = self.scrollable_frame.winfo_reqheight()
                
                # Set frame size to at least canvas size
                frame_width = max(canvas_width, required_width)
                frame_height = max(canvas_height, required_height)
                
                self.canvas.itemconfig(
                    self.canvas_window, 
                    width=frame_width,
                    height=frame_height
                )
                
        except Exception as e:
            self.logger.debug(f"Error in canvas configure: {e}")
    
    def _update_scrollbar_visibility(self):
        """Show or hide scrollbars based on content size."""
        try:
            # Get canvas and content dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Get scroll region
            scroll_region = self.canvas.cget("scrollregion")
            if not scroll_region:
                return
                
            # Parse scroll region (x1, y1, x2, y2)
            x1, y1, x2, y2 = map(float, scroll_region.split())
            content_width = x2 - x1
            content_height = y2 - y1
            
            # Determine if scrollbars are needed
            need_v_scrollbar = content_height > canvas_height
            need_h_scrollbar = content_width > canvas_width
            
            # Show/hide vertical scrollbar
            if need_v_scrollbar and not self.v_scrollbar_visible:
                self.v_scrollbar.grid(row=0, column=1, sticky="ns")
                self.v_scrollbar_visible = True
            elif not need_v_scrollbar and self.v_scrollbar_visible:
                self.v_scrollbar.grid_remove()
                self.v_scrollbar_visible = False
            
            # Show/hide horizontal scrollbar
            if need_h_scrollbar and not self.h_scrollbar_visible:
                self.h_scrollbar.grid(row=1, column=0, sticky="ew")
                self.h_scrollbar_visible = True
            elif not need_h_scrollbar and self.h_scrollbar_visible:
                self.h_scrollbar.grid_remove()
                self.h_scrollbar_visible = False
                
        except Exception as e:
            self.logger.debug(f"Error updating scrollbar visibility: {e}")
    
    def _bind_mousewheel(self):
        """Bind mouse wheel events for scrolling."""
        def _on_mousewheel_vertical(event):
            """Handle vertical mouse wheel scrolling."""
            if self.v_scrollbar_visible:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _on_mousewheel_horizontal(event):
            """Handle horizontal mouse wheel scrolling (with Shift)."""
            if self.h_scrollbar_visible:
                self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_events(event):
            """Bind mouse wheel events when mouse enters."""
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel_vertical)
            self.canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel_horizontal)
        
        def _unbind_events(event):
            """Unbind mouse wheel events when mouse leaves."""
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Shift-MouseWheel>")
        
        # Bind enter/leave events
        self.canvas.bind('<Enter>', _bind_events)
        self.canvas.bind('<Leave>', _unbind_events)
    
    def scroll_to_top(self):
        """Scroll to the top of the content."""
        self.canvas.yview_moveto(0)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the content."""
        self.canvas.yview_moveto(1)
    
    def scroll_to_left(self):
        """Scroll to the left of the content."""
        self.canvas.xview_moveto(0)
    
    def scroll_to_right(self):
        """Scroll to the right of the content."""
        self.canvas.xview_moveto(1)
    
    def get_scrollable_frame(self) -> tk.Frame:
        """
        Get the frame that should contain the scrollable content.

        Returns:
            The scrollable frame widget
        """
        return self.scrollable_frame

    def update_scroll_region(self):
        """Force update of the scroll region to ensure all content is accessible."""
        try:
            # Force update of all widgets multiple times
            for _ in range(3):
                self.scrollable_frame.update_idletasks()
                self.canvas.update_idletasks()
                self.update_idletasks()

            # Get the actual required size of the content
            req_width = self.scrollable_frame.winfo_reqwidth()
            req_height = self.scrollable_frame.winfo_reqheight()

            # Ensure minimum height for all content visibility - Ultra compact
            min_height = req_height  # Use actual required height, no artificial minimum

            # Set scroll region to encompass all content with minimal padding
            self.canvas.configure(scrollregion=(0, 0, req_width, min_height + 10))  # Reduced padding

            # Force scrollbar visibility update
            self._update_scrollbar_visibility()

            self.logger.debug(f"Scroll region updated: {req_width}x{min_height + 50} (required: {req_height})")

        except Exception as e:
            self.logger.error(f"Error updating scroll region: {e}")


class ResponsiveScrollableFrame(ScrollableFrame):
    """A scrollable frame that adapts to responsive design patterns."""
    
    def __init__(self, parent, responsive_manager=None, **kwargs):
        """
        Initialize the responsive scrollable frame.
        
        Args:
            parent: Parent widget
            responsive_manager: ResponsiveManager instance
            **kwargs: Additional frame options
        """
        self.responsive_manager = responsive_manager
        super().__init__(parent, **kwargs)
        
        # Apply responsive styling if manager is available
        if self.responsive_manager:
            self._apply_responsive_styling()
    
    def _apply_responsive_styling(self):
        """Apply responsive styling to the scrollable frame."""
        try:
            # Get responsive padding - Ultra minimal
            padding = self.responsive_manager.get_responsive_padding(2)  # Ultra minimal padding
            
            # Configure canvas with responsive padding
            self.canvas.configure(bd=0, highlightthickness=0)
            
            # Apply responsive minimum sizes if screen is small - Ultra compact
            if self.responsive_manager.should_use_compact_layout():
                # For small screens, ensure minimum scrollable area - Ultra compact
                self.canvas.configure(width=250, height=150)  # Reduced for ultra compactness
            
        except Exception as e:
            self.logger.warning(f"Failed to apply responsive styling: {e}")


def create_scrollable_container(parent, responsive_manager=None, **kwargs) -> ResponsiveScrollableFrame:
    """
    Create a responsive scrollable container.
    
    Args:
        parent: Parent widget
        responsive_manager: ResponsiveManager instance
        **kwargs: Additional frame options
        
    Returns:
        ResponsiveScrollableFrame instance
    """
    return ResponsiveScrollableFrame(parent, responsive_manager, **kwargs)

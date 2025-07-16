"""
Utility modules for the Suivi Generator application.

This package contains utility functions and helpers:
- lazy_imports: Lazy loading of heavy dependencies
- file_utils: File handling utilities
- logging_config: Logging configuration
- performance: Performance monitoring and optimization
"""

from .lazy_imports import get_pandas, get_PIL
from .logging_config import setup_logging
from .performance import performance_monitor, async_task_manager, timed_operation

__all__ = [
    'get_pandas', 'get_PIL', 'setup_logging',
    'performance_monitor', 'async_task_manager', 'timed_operation'
]

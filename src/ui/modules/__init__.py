"""
Feature modules for the Suivi Generator platform.

This package contains individual feature modules that can be accessed
from the main navigation system.
"""

from .suivi_generator_module import SuiviGeneratorModule
from .suivi_global_module import SuiviGlobalModule
from .team_stats_module import TeamStatsModule
from .data_viewer_module import DataViewerModule
from .quality_control_module import QualityControlModule

__all__ = ['SuiviGeneratorModule', 'SuiviGlobalModule', 'TeamStatsModule', 'DataViewerModule', 'QualityControlModule']

# ============================================
# Sales Data Analysis System Package
# ============================================

__version__ = "1.0.0"
__author__ = "Data Analytics Team"
__description__ = "Config-Driven Sales Data Analysis System with MySQL and Python"

from .db import DatabaseManager, get_db_manager
from .query_loader import QueryLoader, get_query_loader
from .query_executor import QueryExecutor
from .analysis import AnalysisEngine
from .visualization import Visualizer

__all__ = [
    'DatabaseManager',
    'get_db_manager',
    'QueryLoader',
    'get_query_loader',
    'QueryExecutor',
    'AnalysisEngine',
    'Visualizer',
]
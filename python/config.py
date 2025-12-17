# ============================================
# Configuration Module
# Database credentials and environment setup
# ============================================

import os
from pathlib import Path

# ============================================
# Database Configuration
# ============================================
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'  # CHANGE THIS TO YOUR MYSQL PASSWORD
DB_NAME = 'sales_analytics'
DB_PORT = 3306

# ============================================
# Project Paths
# ============================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
QUERIES_DIR = PROJECT_ROOT / 'queries'
OUTPUT_DIR = PROJECT_ROOT / 'output'
INSIGHTS_DIR = PROJECT_ROOT / 'insights'
CHARTS_DIR = INSIGHTS_DIR / 'charts'

# Create directories if they don't exist
for directory in [DATA_DIR, QUERIES_DIR, OUTPUT_DIR, INSIGHTS_DIR, CHARTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================
# File Paths
# ============================================
QUERIES_FILE = QUERIES_DIR / 'queries.json'
SAMPLE_DATA_FILE = DATA_DIR / 'raw_sales_data.csv'
INSIGHTS_FILE = INSIGHTS_DIR / 'insights.md'

# ============================================
# Application Settings
# ============================================
DEBUG = True
LOG_LEVEL = 'INFO'
CHART_FORMAT = 'png'  # 'png' or 'svg'
CHART_DPI = 300

# ============================================
# Analysis Settings
# ============================================
DEFAULT_LIMIT = 10  # For top-N queries
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# ============================================
# Logging Configuration
# ============================================
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============================================
# Validation
# ============================================
def validate_config():
    """Validate that all required configuration is set."""
    if not DB_PASSWORD or DB_PASSWORD == 'root':
        print("⚠️  WARNING: Default MySQL password detected. Update DB_PASSWORD in config.py")
    return True

if __name__ == '__main__':
    print("✓ Configuration loaded successfully")
    print(f"  Database: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    print(f"  Project Root: {PROJECT_ROOT}")
    print(f"  Output Directory: {OUTPUT_DIR}")
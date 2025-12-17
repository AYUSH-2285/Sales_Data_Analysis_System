# ============================================
# Query Loader Module
# Loads and validates SQL queries from JSON
# ============================================

import json
import logging
from config import QUERIES_FILE

logger = logging.getLogger(__name__)

class QueryLoader:
    """Loads SQL queries from queries.json configuration file."""
    
    def __init__(self, queries_file=None):
        self.queries_file = queries_file or QUERIES_FILE
        self.queries = {}
        self.load_queries()
    
    def load_queries(self):
        """Load all queries from JSON file."""
        try:
            with open(self.queries_file, 'r') as f:
                self.queries = json.load(f)
            logger.info(f"✓ Loaded {len(self.queries)} queries from {self.queries_file.name}")
            return self.queries
        except FileNotFoundError:
            logger.error(f"✗ Queries file not found: {self.queries_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"✗ Invalid JSON in queries file: {e}")
            raise
    
    def get_query(self, query_name):
        """
        Get a specific query by name.
        
        Args:
            query_name (str): Name of the query
        
        Returns:
            dict: Query metadata including 'sql', 'description', 'params'
        """
        if query_name not in self.queries:
            available = ', '.join(self.queries.keys())
            logger.error(f"✗ Query '{query_name}' not found. Available: {available}")
            raise KeyError(f"Query '{query_name}' not found")
        
        return self.queries[query_name]
    
    def get_all_queries(self):
        """Get all loaded queries."""
        return self.queries
    
    def get_query_names(self):
        """Get list of all available query names."""
        return list(self.queries.keys())
    
    def get_query_description(self, query_name):
        """Get description of a query."""
        query = self.get_query(query_name)
        return query.get('description', 'No description available')
    
    def get_query_sql(self, query_name):
        """Get SQL statement of a query."""
        query = self.get_query(query_name)
        return query.get('sql', '')
    
    def get_query_params(self, query_name):
        """Get parameter list for a query."""
        query = self.get_query(query_name)
        return query.get('params', [])
    
    def reload(self):
        """Reload queries from file."""
        self.load_queries()
        logger.info("✓ Queries reloaded")
    
    def validate_query(self, query_name):
        """
        Validate query structure.
        
        Args:
            query_name (str): Name of the query
        
        Returns:
            bool: True if valid, raises exception otherwise
        """
        query = self.get_query(query_name)
        
        required_fields = ['sql', 'description', 'params']
        for field in required_fields:
            if field not in query:
                raise ValueError(f"Query '{query_name}' missing required field: {field}")
        
        if not isinstance(query['params'], list):
            raise ValueError(f"Query '{query_name}' params must be a list")
        
        logger.info(f"✓ Query '{query_name}' is valid")
        return True


# Global query loader instance
_query_loader = None

def get_query_loader():
    """Get or create global query loader."""
    global _query_loader
    if _query_loader is None:
        _query_loader = QueryLoader()
    return _query_loader

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    loader = QueryLoader()
    
    print("\n📋 Available Queries:")
    for query_name in loader.get_query_names():
        description = loader.get_query_description(query_name)
        params = loader.get_query_params(query_name)
        print(f"  • {query_name}")
        print(f"    Description: {description}")
        print(f"    Parameters: {params if params else 'None'}")
        print()
# ============================================
# Query Executor Module
# Safe parameterized query execution engine
# ============================================

import pandas as pd
import logging
from db import get_db_manager
from query_loader import get_query_loader

logger = logging.getLogger(__name__)

class QueryExecutor:
    """Executes SQL queries safely with parameter injection."""
    
    def __init__(self):
        self.db_manager = get_db_manager()
        self.query_loader = get_query_loader()
    
    def execute(self, query_name, params=None, as_dataframe=True):
        """
        Execute a query by name with optional parameters.
        
        Args:
            query_name (str): Name of the query in queries.json
            params (dict): Parameters for the query (e.g., {'limit': 10})
            as_dataframe (bool): Return pandas DataFrame (True) or raw results (False)
        
        Returns:
            DataFrame or list: Query results
        """
        # Get query metadata
        query_info = self.query_loader.get_query(query_name)
        sql = query_info['sql']
        required_params = query_info.get('params', [])
        
        # Validate parameters
        if required_params and not params:
            params = {}
        
        if params:
            self._validate_params(query_name, params, required_params)
        
        # Execute query
        logger.info(f"🔄 Executing query: {query_name}")
        
        try:
            results = self.db_manager.execute_query(sql, params)
            
            if as_dataframe:
                df = pd.DataFrame(results) if results else pd.DataFrame()
                logger.info(f"✓ Query executed. Rows: {len(df)}")
                return df
            else:
                logger.info(f"✓ Query executed. Rows: {len(results)}")
                return results
        
        except Exception as e:
            logger.error(f"✗ Query execution failed: {e}")
            raise
    
    def execute_raw(self, sql, params=None, as_dataframe=True):
        """
        Execute a raw SQL query (use with caution).
        
        Args:
            sql (str): Raw SQL query
            params (dict): Parameters for the query
            as_dataframe (bool): Return pandas DataFrame or raw results
        
        Returns:
            DataFrame or list: Query results
        """
        logger.warning("⚠️  Executing raw SQL query (not from queries.json)")
        
        try:
            results = self.db_manager.execute_query(sql, params)
            
            if as_dataframe:
                df = pd.DataFrame(results) if results else pd.DataFrame()
                logger.info(f"✓ Raw query executed. Rows: {len(df)}")
                return df
            else:
                logger.info(f"✓ Raw query executed. Rows: {len(results)}")
                return results
        
        except Exception as e:
            logger.error(f"✗ Raw query execution failed: {e}")
            raise
    
    def _validate_params(self, query_name, provided_params, required_params):
        """
        Validate that provided parameters match required parameters.
        
        Args:
            query_name (str): Name of query (for logging)
            provided_params (dict): Parameters provided by user
            required_params (list): Required parameter names
        
        Raises:
            ValueError: If parameters don't match
        """
        provided_keys = set(provided_params.keys())
        required_keys = set(required_params)
        
        missing = required_keys - provided_keys
        extra = provided_keys - required_keys
        
        if missing:
            logger.warning(f"⚠️  Query '{query_name}' missing parameters: {missing}")
        
        if extra:
            logger.warning(f"⚠️  Query '{query_name}' has extra parameters: {extra}")
        
        return True
    
    def list_available_queries(self):
        """List all available queries."""
        queries = self.query_loader.get_query_names()
        logger.info(f"📋 Available queries: {queries}")
        return queries
    
    def get_query_info(self, query_name):
        """Get detailed information about a query."""
        query = self.query_loader.get_query(query_name)
        return {
            'name': query_name,
            'description': query.get('description', ''),
            'sql': query.get('sql', ''),
            'parameters': query.get('params', [])
        }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    executor = QueryExecutor()
    
    # List available queries
    print("\n📋 Available Queries:")
    for query_name in executor.list_available_queries():
        print(f"  • {query_name}")
    
    # Execute sample query
    print("\n🔄 Executing sample query: monthly_sales")
    try:
        df = executor.execute('monthly_sales')
        print(df.head())
    except Exception as e:
        print(f"Note: Database must be populated first. Error: {e}")
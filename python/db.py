# ============================================
# Database Connection Manager
# Handles MySQL connections and operations
# ============================================

import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages MySQL database connections."""
    
    def __init__(self):
        self.connection = None
        self.host = DB_HOST
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_NAME
        self.port = DB_PORT
    
    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=True
            )
            logger.info(f"✓ Connected to MySQL database: {self.database}")
            return self.connection
        except Error as e:
            logger.error(f"✗ Database connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("✓ Disconnected from database")
    
    def is_connected(self):
        """Check if connection is active."""
        return self.connection and self.connection.is_connected()
    
    def execute_query(self, sql, params=None):
        """
        Execute a SELECT query and return results.
        
        Args:
            sql (str): SQL query string
            params (dict): Parameters for parameterized query
        
        Returns:
            list: List of result rows (tuples)
        """
        if not self.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            results = cursor.fetchall()
            cursor.close()
            logger.info(f"✓ Query executed successfully. Rows: {len(results)}")
            return results
        
        except Error as e:
            logger.error(f"✗ Query execution failed: {e}")
            raise
    
    def execute_insert_bulk(self, table, records):
        """
        Insert multiple records into a table.
        
        Args:
            table (str): Table name
            records (list): List of dictionaries containing record data
        """
        if not records:
            return
        
        if not self.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            
            # Get column names from first record
            columns = list(records[0].keys())
            placeholders = ', '.join(['%s'] * len(columns))
            col_str = ', '.join(columns)
            
            sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
            
            # Prepare data tuples
            data = [tuple(record.get(col) for col in columns) for record in records]
            
            cursor.executemany(sql, data)
            self.connection.commit()
            
            logger.info(f"✓ Inserted {cursor.rowcount} rows into {table}")
            cursor.close()
        
        except Error as e:
            logger.error(f"✗ Bulk insert failed: {e}")
            raise
    
    def get_connection(self):
        """Get the active connection object."""
        if not self.is_connected():
            self.connect()
        return self.connection
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False


# Global database manager instance
_db_manager = None

def get_db_manager():
    """Get or create global database manager."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    db = DatabaseManager()
    db.connect()
    
    # Test query
    results = db.execute_query("SELECT COUNT(*) as count FROM customers")
    print(f"✓ Test query successful: {results}")
    
    db.disconnect()
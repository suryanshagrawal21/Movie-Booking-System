import mysql.connector
from mysql.connector import Error
from ..utils.config_manager import ConfigManager
from ..utils.logger import logger

class BaseModel:
    """Base class for all models, handling database connectivity."""
    
    def __init__(self):
        config = ConfigManager.load_config()
        self.config = {
            "host": config["db_host"],
            "user": config["db_user"],
            "password": config["db_password"],
            "database": config["db_name"]
        }

    def _get_connection(self, database=None):
        """Internal method to get a connection."""
        cfg = self.config.copy()
        if database:
            cfg["database"] = database
        
        try:
            conn = mysql.connector.connect(**cfg)
            if conn.is_connected():
                return conn
        except Error as e:
            logger.error(f"Connection Error: {e}")
            return None

    def execute_query(self, query, params=None):
        conn = self._get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            logger.info(f"Executed Query: {query[:100]}...")
            return True
        except Error as e:
            logger.error(f"Query Execution Error: {e} | Query: {query}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def fetch_one(self, query, params=None):
        conn = self._get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except Error as e:
            logger.error(f"Fetch One Error: {e} | Query: {query}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def fetch_all(self, query, params=None):
        conn = self._get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            logger.error(f"Fetch All Error: {e} | Query: {query}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

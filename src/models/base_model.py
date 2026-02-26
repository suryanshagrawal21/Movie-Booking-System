import mysql.connector
from mysql.connector import Error
from ..utils.config_manager import ConfigManager

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
        """Internal method to get a connection. Parameter 'database' can override default."""
        cfg = self.config.copy()
        if database:
            cfg["database"] = database
        
        try:
            conn = mysql.connector.connect(**cfg)
            if conn.is_connected():
                return conn
        except Error as e:
            # Note: Caller should handle if None returned
            return None

    def test_connection(self, host, user, password, database=""):
        """Static method to test credentials before saving."""
        try:
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
            if conn.is_connected():
                conn.close()
                return True
        except Error:
            return False
        return False

    def execute_query(self, query, params=None):
        conn = self._get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return True
        except Error as e:
            print(f"Query Execution Error: {e}")
            return False
        finally:
            cursor.close()
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
            print(f"Fetch One Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query, params=None):
        conn = self._get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Fetch All Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

import unittest
from src.models.base_model import BaseModel

class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = BaseModel()

    def test_connection_handling(self):
        # This will test if the connection method returns None gracefully on failure
        # or a connection object on success.
        conn = self.db._get_connection()
        # We don't assert it must be connected because setup depends on user environment,
        # but we check it doesn't crash.
        if conn:
            self.assertTrue(conn.is_connected())
            conn.close()
        else:
            print("Warning: Database not connected. Test handles connection failure gracefully.")

    def test_fetch_all_on_empty_or_error(self):
        # Testing fetch_all behavior on a likely non-existent table or error
        result = self.db.fetch_all("SELECT * FROM non_existent_table")
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()

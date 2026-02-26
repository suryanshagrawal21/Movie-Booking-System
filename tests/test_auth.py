import unittest
from src.utils.helpers import SecurityUtils

class TestAuth(unittest.TestCase):
    def test_password_hashing(self):
        password = "test_password_123"
        hashed = SecurityUtils.hash_password(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(SecurityUtils.check_password(password, hashed))
        
    def test_wrong_password(self):
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = SecurityUtils.hash_password(password)
        
        self.assertFalse(SecurityUtils.check_password(wrong_password, hashed))

if __name__ == "__main__":
    unittest.main()

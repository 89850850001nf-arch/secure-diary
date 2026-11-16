import unittest

# Имитация безопасной проверки пароля
def safe_login(username, password):
    if username == "admin" and password == "secret":
        return True
    return False

class TestSecurity(unittest.TestCase):
    def test_sql_injection_attempt(self):
        hacker_input = "admin' OR '1'='1"
        result = safe_login(hacker_input, "any_password")
        self.assertFalse(result)
        
    def test_normal_login(self):
        result = safe_login("admin", "secret")
        self.assertTrue(result)

# ВОТ ЭТА СТРОЧКА ЗАПУСКАЕТ ТЕСТЫ
if __name__ == '__main__':
    unittest.main()

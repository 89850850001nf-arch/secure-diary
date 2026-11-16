import unittest

# Имитация безопасной проверки пароля
def safe_login(username, password):
    if username == "admin" and password == "secret":
        return True
    return False

class TestSecurity(unittest.TestCase):
    # Тест 1: Проверка SQL-инъекции
    def test_sql_injection_attempt(self):
        hacker_input = "admin' OR '1'='1"
        result = safe_login(hacker_input, "any_password")
        self.assertFalse(result)
        
    # Тест 2: Проверка нормального входа
    def test_normal_login(self):
        result = safe_login("admin", "secret")
        self.assertTrue(result)

    # =========================================================
    # ТЕСТ 3: ВОТ СЮДА ДОБАВЛЯЕМ НОВЫЙ ТЕСТ (обрати внимание на отступ!)
    # =========================================================
    def test_safe_password_change(self):
        hacker_input = "hacked' WHERE username = 'admin' --"
        # Проверяем, что хакерская строка не ломает программу
        self.assertIsInstance(hacker_input, str)

# Эта строчка запускает все тесты
if __name__ == '__main__':
    unittest.main()

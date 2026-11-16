import unittest
from calculator import add, divide, is_even  # <--- Импортируем всё нужное

class TestCalculator(unittest.TestCase):
    # Тест 1
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    # Тест 2
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5.0)

    # Тест 3
    def test_divide_by_zero(self):
        self.assertEqual(divide(10, 0), "Ошибка: деление на ноль")

    # Тест 4 (Хакерский - на склейку строк)
    def test_add_strings(self):
        self.assertEqual(add("2", "3"), "23")

    # Тест 5 (Проверка на четность)
    def test_is_even(self):
        self.assertTrue(is_even(4))    # 4 - четное
        self.assertFalse(is_even(5))   # 5 - нечетное

if __name__ == '__main__':
    unittest.main()

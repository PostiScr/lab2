import unittest
from unittest.mock import patch, mock_open
from src.regex_engine import RomanRegexEngine

class TestRomanRegexEngine(unittest.TestCase):
     # Тест для проверки класса

    def setUp(self):
        self.engine = RomanRegexEngine()

    def test_valid_roman_numbers(self):
        # Проверка корректных римских чисел
        valid_numbers = ["I", "V", "X", "L", "C", "D", "M", "MMXXIII", "MCMXCIV"]
        for num in valid_numbers:
            with self.subTest(num=num):
                self.assertTrue(self.engine.is_valid_roman(num), f"Число {num} должно быть валидным")

    def test_invalid_roman_numbers(self):
        # Проверка некорректных римских чисел
        invalid_numbers = ["IIII", "VV", "IC", "ABC", "M M", ""]
        for num in invalid_numbers:
            with self.subTest(num=num):
                self.assertFalse(self.engine.is_valid_roman(num), f"Число {num} должно быть невалидным")

    def test_find_in_text(self):
        # Проверка поиска чисел в тексте
        text = "В году MMXXIII мы прочитали XIV параграф. А римляне писали IIII."
        expected = ["MMXXIII", "XIV"]
        self.assertEqual(self.engine.find_in_text(text), expected)

    @patch("builtins.open", new_callable=mock_open, read_data="Здесь есть число X и еще MMXX.")
    def test_find_in_file(self, mock_file):
        # Проверка поиска в файле (файл имитируется, реального чтения нет)
        result = self.engine.find_in_file("dummy.txt")
        self.assertEqual(result, ["X", "MMXX"])
        
        mock_file.assert_called_once_with("dummy.txt", "r", encoding="utf-8")

    def test_find_in_file_not_found(self):
        # Проверка ошибки, если файла не существует
        with self.assertRaises(FileNotFoundError):
            self.engine.find_in_file("non_existent_file_12345.txt")

    @patch("src.regex_engine.requests.get")
    def test_find_on_web_success(self, mock_get):
        # Проверка поиска на сайте (интернет имитируется)
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Here is the year MMXXIV."
        
        result = self.engine.find_on_web("http://example.com")
        self.assertEqual(result, ["MMXXIV"])

    @patch("src.regex_engine.requests.get")
    def test_find_on_web_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Сетевая ошибка")
        
        with self.assertRaises(ConnectionError):
            self.engine.find_on_web("http://example.com")

if __name__ == "__main__":
    unittest.main()
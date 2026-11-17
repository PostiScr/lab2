import re
import requests
from pathlib import Path

class RomanRegexEngine:
    # Поиск и валидация римских чисел
    def __init__(self):
        # Паттерн для полного соответствия строки
        self.valid_pattern = re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")

        # Паттерн для поиска внутри текста
        self.search_pattern = re.compile( r"\b(?=[MDCLXVI])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b")

    def is_valid_roman(self, text: str) -> bool:
        # Проверка является ли строка римским числом
        if not text:
            return False
        clean_text = text.strip().upper()
        return bool(self.valid_pattern.match(clean_text))

    def find_in_text(self, text: str) -> list[str]:
        # Находит все корректные римские числа в переданном тексте
        return [match.group(0) for match in self.search_pattern.finditer(text.upper()) if match.group(0)]

    def find_in_file(self, filepath: str) -> list[str]:
        # Находит все корректные римские числа в файле
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Файл по пути {filepath} не найден")
        
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
        return self.find_in_text(content)

    def find_on_web(self, url: str) -> list[str]:
        # Находит все корректные римские числа на стринице по URL
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            
            return self.find_in_text(response.text)

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при подключении к {url}: {e}")
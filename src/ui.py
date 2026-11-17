from src.regex_engine import RomanRegexEngine

class ConsoleUI:
    # Консольный интерфейс для взаимодействия с пользователем

    def __init__(self):
        self.engine = RomanRegexEngine()

    def run(self) -> None:
        while True:
            print("\nПОИСК РИМСКИХ ЧИСЕЛ")
            print("1. Проверить корректность числа")
            print("2. Найти числа в локальном файле")
            print("3. Найти числа на веб-странице (по URL)")
            print("0. Выход")

            choice = input("Выберите действие: ").strip()

            try:
                match choice:
                    case "1":
                        self._check_user_input()
                    case "2":
                        self._search_in_file()
                    case "3":
                        self._search_on_web()
                    case "0":
                        print("До свидания")
                        break
                    case _:
                        print("Неизвестная команда. Попробуйте снова.")

            except FileNotFoundError as e:
                print(f"Ошибка файла: {e}")
            except ConnectionError as e:
                print(f"Сетевая ошибка: {e}")

            except (KeyboardInterrupt, EOFError):
                print("\nПрограмма была прервана пользователем.")
                break

    def _check_user_input(self) -> None:
        # Проверка введённой строки
        text = input("Введите римское число для проверки: ").strip()
        if self.engine.is_valid_roman(text):
            print(f"'{text.upper()}' — это КОРРЕКТНОЕ римское число.")
        else:
            print(f"'{text}' — это НЕКОРРЕКТНОЕ римское число.")

    def _search_in_file(self) -> None:
        # Поиск чисел в файле
        filepath = input("Введите путь к файлу: ").strip()
        results = self.engine.find_in_file(filepath)

        if results:
            print(f"Найдено {len(results)} римских чисел: {results}")
        else:
            print("В этом файле не найдено корректных римских чисел")

    def _search_on_web(self) -> None:
        # Запрашивает URL и ищет числа на странице
        url = input("Введите URL: ").strip()
        print("Загрузка страницы... Пожалуйста, подождите.")
        
        results = self.engine.find_on_web(url)
        
        if results:
            print(f"Найдено {len(results)} римских чисел: {results}")
        else:
            print("На этой странице не найдено корректных римских чисел.")
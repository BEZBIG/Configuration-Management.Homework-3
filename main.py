import json
import sys
import re

# Хранилище для констант
constants = {}  # Словарь для хранения объявленных констант
value_to_constant = {}  # Словарь для сопоставления значений с их константами
constant_counter = 0  # Счётчик для генерации уникальных имён констант


def get_or_create_constant(value):
    """
    Возвращает существующую константу для значения или создаёт новую.
    """
    global constant_counter  # Используем глобальный счётчик для уникальных имён констант
    if value in value_to_constant:  # Если значение уже связано с константой
        return f"^{value_to_constant[value]}"  # Возвращаем ссылку на эту константу
    else:
        constant_name = f"CONST_{constant_counter}"  # Генерируем новое имя константы
        constant_counter += 1  # Увеличиваем счётчик на 1
        declare_constant(constant_name, value)  # Сохраняем новое значение как константу
        value_to_constant[value] = constant_name  # Связываем значение с новой константой
        return f"^{constant_name}"  # Возвращаем ссылку на новую константу


def resolve_constant_reference(ref):
    """
    Разрешает ссылку на константу и возвращает её значение.
    """
    if ref.startswith("^") and ref[1:] in constants:
        return constants[ref[1:]]  # Возвращаем значение константы
    return ref  # Если ссылка не найдена, возвращаем исходное значение

def to_custom_lang(obj, indent=0):
    """
    Преобразует JSON-объект в учебный конфигурационный язык, заменяя константы на их значения.
    """
    spaces = ' ' * indent  # Создаём отступы

    if isinstance(obj, dict):  # Если объект является словарём
        lines = ["$["]  # Открываем блок словаря
        for key, value in obj.items():
            transformed_key = key.upper()  # Ключ в верхнем регистре
            lines.append(f"{spaces}  {transformed_key} : {to_custom_lang(value, indent + 2)},")
        lines.append(f"{spaces}]")
        return '\n'.join(lines)

    elif isinstance(obj, str) and obj.startswith("^"):
        # Если объект является ссылкой на константу, заменяем на её значение
        const_name = obj[1:]  # Извлекаем имя константы без "^"
        if const_name in constants:
            return to_custom_lang(constants[const_name], indent)  # Разрешаем константу до значения
        else:
            raise ValueError(f"Неизвестная константа: {const_name}")

    elif isinstance(obj, (str, int, float)):
        return f"\"{obj}\"" if isinstance(obj, str) else str(obj)

    else:
        raise ValueError(f"Недопустимый тип данных: {type(obj)}")


def declare_constant(name, value):
    """
    Объявляет новую константу.
    """
    constants[name.upper()] = value  # Сохраняем константу с именем в верхнем регистре


def parse_constants(data):
    """
    Обрабатывает раздел CONSTANTS и удаляет его из JSON.
    """
    if "CONSTANTS" in data:  # Проверяем наличие раздела CONSTANTS
        for name, value in data["CONSTANTS"].items():  # Перебираем константы
            declare_constant(name, value)  # Объявляем каждую константу
            value_to_constant[value] = name.upper()  # Сохраняем значение и его константу
        del data["CONSTANTS"]  # Удаляем раздел CONSTANTS из JSON
    return data  # Возвращаем JSON без констант

def main():
    """
    Основная функция программы для обработки JSON-файла.
    """
    if len(sys.argv) < 2:  # Проверяем, указан ли файл в аргументах командной строки
        print("Ошибка: укажите имя JSON-файла.", file=sys.stderr)  # Сообщаем об ошибке
        sys.exit(1)  # Завершаем программу с кодом ошибки 1

    filename = sys.argv[1]  # Получаем имя файла из аргументов

    try:
        with open(filename, 'r', encoding='utf-8') as file:  # Открываем файл для чтения
            data = json.load(file)  # Читаем и парсим JSON
            data = parse_constants(data)  # Обрабатываем и удаляем константы
            result = to_custom_lang(data)  # Преобразуем JSON в учебный язык
            print(result)  # Выводим результат
    except FileNotFoundError:  # Если файл не найден
        print(f"Ошибка: файл '{filename}' не найден.", file=sys.stderr)  # Сообщаем об ошибке
    except ValueError as ve:  # Если произошла ошибка в данных
        print(f"Ошибка: {ve}", file=sys.stderr)  # Сообщаем об ошибке
    except json.JSONDecodeError:  # Если произошла ошибка при разборе JSON
        print("Ошибка парсинга JSON", file=sys.stderr)  # Сообщаем об ошибке


if __name__ == "__main__":
    main()  # Запуск основной функции
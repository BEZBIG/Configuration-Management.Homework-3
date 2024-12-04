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
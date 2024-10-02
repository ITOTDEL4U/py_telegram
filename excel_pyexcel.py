import pyexcel as pe
from pyexcel import save_book_as
import shutil
import pandas as pd
import json
from datetime import datetime, timedelta
import os
from typing import Optional
import re


class File():
    def __init__(self, name, path, size, data, data_last_modification):
        self.name = name
        self.path = path
        self.size = round(size / 1024, 2)   # Размер в килобайтах
        self.data = self.format_datetime(data)
        self.data_last_modification = self.format_datetime(
            data_last_modification)

    @staticmethod
    def format_datetime(timestamp):
        """Форматирование даты и времени в формате День/Месяц/Год часы:Минуты"""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%d/%m/%Y %H:%M')


class Settings:
    def __init__(self):
        # Чтение конфигурации из config.json
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            self.directory_path = config['directory_path']
            self.directory_path_temp = config['directory_path_temp']
            self.file_extension = config['file_extension']
            self.prefix_number = config['prefix_number']
            self.name_pattern_contract = config['name_pattern_contract']
            self.name_pattern_act = config['name_pattern_act']

        if not os.path.exists(self.directory_path_temp):
            os.makedirs(self.directory_path_temp)
        else:
            clear_directory(self.directory_path_temp)


def clear_directory(path):
    if not os.path.isdir(path):
        return

    # Удаляем все содержимое папки
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


def search_files(directory, file_extension, name_pattern) -> Optional[File]:

    # Регулярное выражение для фильтрации имени файла
    regex = re.compile(name_pattern, re.IGNORECASE)

    files_info = []

    # Обход всех файлов в указанной директории
    for filename in os.listdir(directory):
        if filename.lower().endswith(file_extension) and regex.search(filename):

            filepath = os.path.join(directory, filename)
            # filepath = Path(filepath)

            file = File(filename, filepath, os.path.getsize(
                filepath), os.path.getctime(filepath), os.path.getmtime(filepath))

            files_info.append(file)

    # Сортировка файлов по дате модификации (от нового к старому)
    files_info.sort(key=lambda x: x.data_last_modification, reverse=True)

    if files_info:
        return files_info[0]
    else:
        return None


def modify_excel():

    settings = Settings()
    file = search_files(settings.directory_path,
                        settings.file_extension, settings.name_pattern_contract)

    if file is None:
        return

     # Получаем текущую дату и добавляем 1 день
    current_date = datetime.now()
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0)

    next_day = current_date + timedelta(days=1)
    next_day_formatted = next_day.strftime(
        '%d.%m')  # Форматируем дату в 'дд.мм'

    try:

        # Загрузка существующего файла
        book = pe.get_book(file_name=file.path)

        # Изменение данных в ячейке
        # Получение списка имен листов
        sheet_names = book.sheet_names()

        # Получение имени первого листа по индексу 0
        first_sheet_name = sheet_names[0]
        sheet = book[first_sheet_name]
        sheet[3][23] = 'New Value'  # 4-я строка, 24-й столбец (индексация с 0)

        # Создание стиля (стили ограничены в `pyexcel`)
        # В данном случае, если вам нужны сложные стили, `pyexcel` не поддерживает их напрямую.

        # Сохранение изменений в новый файл
        output_path = settings.directory_path_temp + file.name
        pe.save_book_as(book, dest_file_name=output_path)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        a = 0

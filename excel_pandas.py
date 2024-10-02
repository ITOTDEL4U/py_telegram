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
        # Шаг 1: Открываем существующий файл .xls для чтения
        # Чтение файла с помощью pandas и xlrd
        # readbook = xlrd.open_workbook(file.path, formatting_info=True)
        df = pd.read_excel(file.path, engine='xlrd')

        # Шаг 2: Вносим изменения в ячейку (1 строка, 1 столбец)
        # Индексация в pandas начинается с 0, поэтому ячейка (1, 1) соответствует df.iloc[0, 0]
        df.iloc[4, 24] = next_day_formatted

        # Шаг 3: Сохраняем изменения в новый файл
        # Запись изменений с помощью pandas и xlwt
        output_path = settings.directory_path_temp + file.name
        df.to_excel(output_path, index=False, engine='xlwt')

        print(f"Файл успешно обновлён и сохранён как '{output_path}'")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

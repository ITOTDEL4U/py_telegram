from typing import Optional
import os
import re
from datetime import datetime, timedelta
import xlwt
import xlrd
from xlutils.copy import copy
import os
import shutil
import json
import locale
from pathlib import Path


# exapmle use
# mymumber = "123456"
# excel.change_contract(mymumber)
# excel.change_act(mymumber)


def parse_ukraninan_date_to_datetime(date_str):

    # Словарь для преобразования украинских месяцев в английские
    months = {
        'січня': 'January', 'лютого': 'February', 'березня': 'March',
        'квітня': 'April', 'травня': 'May', 'червня': 'June',
        'липня': 'July', 'серпня': 'August', 'вересня': 'September',
        'жовтня': 'October', 'листопада': 'November', 'грудня': 'December'
    }

    # Заменяем украинские месяцы на английские
    for uk_month, en_month in months.items():
        if uk_month in date_str:
            date_str = date_str.replace(uk_month, en_month)
            break
    # Удаляем лишние слова и пробелы
    date_str = date_str.replace('року', '').strip()
    # Преобразуем строку в объект datetime
    return datetime.strptime(date_str, '%d %B %Y')


def parse_datetime_to_ukrainian_date(date):
    day = date.day
    month_ukrainian = [
        'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
        'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
    ][date.month - 1]
    year = date.year
    return f'{day} {month_ukrainian} {year}'


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


def change_contract(pNumber):
    settings = Settings()
    file = search_files(settings.directory_path,
                        settings.file_extension, settings.name_pattern_contract)

    if file is None:
        return

    # Открываем существующий файл .xls для чтения
    readbook = xlrd.open_workbook(file.path, formatting_info=True)
    writebook = copy(readbook)  # Копируем рабочую книгу для записи
    sheet = writebook.get_sheet(0)     # Выбираем первый лист

    # Чтение данных из первых 6 строк
    # read_sheet = readbook.sheet_by_index(0)
    # num_cols = read_sheet.ncols
    # num_rows = min(6, read_sheet.nrows)

    # # Чтение данных из первых 6 строк
    # for row_idx in range(num_rows):
    #     # Получаем значения в текущей строке
    #     row_values = []
    #     for col_idx in range(num_cols):
    #         cell_value = read_sheet.cell_value(row_idx, col_idx)
    #         row_values.append(cell_value)
    #         if cell_value != '':
    #             print(f"Строка {row_idx}, Колонка {col_idx},  имеют значение - {cell_value}")

    # Получаем значение из ячейки (строка 4, колонка 24) ДАТА
    cell_value_date = readbook.sheet_by_index(0).cell_value(4, 24)

    # Преобразуем значение в формат даты (предполагаем, что это строка в формате 'дд.мм')
    cell_date = datetime.strptime(cell_value_date, '%d.%m')

    # Получаем текущую дату и добавляем 1 день
    current_date = datetime.now()
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0)

    next_day = current_date + timedelta(days=1)
    next_day_formatted = next_day.strftime(
        '%d.%m')  # Форматируем дату в 'дд.мм'

    # Сравниваем даты и записываем значение, если они совпадают
    if cell_date.strftime('%d.%m') <= current_date.strftime('%d.%m'):
        # Создаем стиль для ячейки
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'Arial Narrow'
        font.height = 11 * 20  # размер шрифта в 1/20 пункта
        style.font = font

        # Создаем и настраиваем выравнивание
        alignment = xlwt.Alignment()
        # выравнивание по центру горизонтально
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        # выравнивание по нижнему краю вертикально
        alignment.vert = xlwt.Alignment.VERT_BOTTOM
        style.alignment = alignment

        # Устанавливаем формат данных как текст
        data_format = xlwt.XFStyle()
        data_format.num_format_str = '@'  # Формат текст
        style.num_format_str = '@'  # Применяем формат текст к основному стилю
        # Записываем новое значение в ячейку (строка 0, колонка 22)  НОВУЮ ДАТА
        sheet.write(4, 24, next_day_formatted, style)

        # Записываем значение в ячейку (строка 0, колонка 22)
        cell_value = settings.prefix_number + pNumber
        sheet.write(0, 22, cell_value, style)

        # Сохраняем изменения в временный файл
        new_temp_file = settings.directory_path_temp + file.name

        writebook.save(new_temp_file)

        # Перезаписываем существующий файл новым содержимым
        os.replace(new_temp_file, file.path)
        clear_directory(settings.directory_path_temp)


def change_act(pNumber):
    settings = Settings()
    file = search_files(settings.directory_path,
                        settings.file_extension, settings.name_pattern_act)

    if file is None:
        return

    # Открываем существующий файл .xls для чтения
    readbook = xlrd.open_workbook(file.path, formatting_info=True)
    writebook = copy(readbook)  # Копируем рабочую книгу для записи
    sheet = writebook.get_sheet(0)     # Выбираем первый лист

   # Определяем стиль для даты
    date_style = xlwt.XFStyle()

    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    font.height = 220  # Размер шрифта 11 пунктов

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER

    date_style.font = font
    date_style.alignment = alignment

    date_style.num_format_str = 'DD MMMM YYYY'  # Формат "01 January 2024"

    # Чтение данных из первых 6 строк
    # read_sheet = readbook.sheet_by_index(0)
    # num_cols = read_sheet.ncols
    # num_rows = read_sheet.nrows
    # Строка 1, Колонка 1,  имеют значение - 8632/24/009039
    # Строка 1, Колонка 6,  имеют значение - 29 серпня 2024 року
    # Строка 4, Колонка 1,  имеют значение - 8632/24/009039
    # Строка 4, Колонка 6,  имеют значение - 29 серпня 2024 року
    # Строка 55, Колонка 9,  имеют значение - 45533.0
    # Чтение данных из первых 6 строк
    # for row_idx in range(num_rows):
    #     # Получаем значения в текущей строке
    #     row_values = []
    #     for col_idx in range(num_cols):
    #         cell_value = read_sheet.cell_value(row_idx, col_idx)
    #         row_values.append(cell_value)
    #         if cell_value != '':
    #             print(f"Строка {row_idx}, Колонка {col_idx},  имеют значение - {cell_value}")

    # Получаем значение из ячейки (строка 4, колонка 24) ДАТА
    cell_1_6_value_date = readbook.sheet_by_index(0).cell_value(1, 6)

    # Преобразуем строку в объект datetime
    cell_1_6_value_date = parse_ukraninan_date_to_datetime(cell_1_6_value_date)
    # Получаем текущую дату и добавляем 1 день
    current_date = datetime.now()
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0)

    next_day = current_date + timedelta(days=1)

    # Сравниваем даты и записываем значение, если они совпадают
    if cell_1_6_value_date.date() <= current_date.date():
        # Форматируем дату в формате "1 вересня 2024"
        formatted_next_day_ukrainian_date = parse_datetime_to_ukrainian_date(
            next_day)

        sheet.write(1, 6, formatted_next_day_ukrainian_date, date_style)
        sheet.write(4, 6, formatted_next_day_ukrainian_date, date_style)
        # Форматируем дату в формате дд.мм.гггг  01.09.2024

        formatted_next_day_ddmmyyyy = next_day.strftime('%d.%m.%Y')
        sheet.write(55, 9, formatted_next_day_ddmmyyyy)

        cell_number = settings.prefix_number + pNumber
        sheet.write(1, 1, cell_number, date_style)
        sheet.write(4, 1, cell_number, date_style)

        # Сохраняем изменения в временный файл
        new_temp_file = settings.directory_path_temp + file.name
        writebook.save(new_temp_file)

        # Перезаписываем существующий файл новым содержимым
        os.replace(new_temp_file, file.path)

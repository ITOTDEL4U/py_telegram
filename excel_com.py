import shutil
import pandas as pd
import json
from datetime import datetime, timedelta
import os
from typing import Optional
import re
import win32com.client
from win32com.client import constants
import config
import xlrd
# Проверка доступных констант
# print(dir(win32com.client.constants))


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


def change_contract(pNumber):
    settings = config.get_config()
    file = search_files(settings.directory_path,
                        settings.file_extension, settings.name_pattern_contract)

    if file is None:
        return

    num_contract = settings.prefix_number + pNumber
    current_date = datetime.now()
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0)

    next_day = current_date + timedelta(days=1)
    next_day_formatted = next_day.strftime('%d.%m')

    # Настройка шрифта и форматирование ячеек
    font_name = 'Arial Narrow'
    font_size = 11

    try:
        # Открытие Excel и файла
        excel = win32com.client.Dispatch("Excel.Application")
        # Укажите полный путь к вашему файлу
        workbook = excel.Workbooks.Open(file.path)
        sheet = workbook.Sheets(1)
    except Exception as e:
        print(f"Произошла инициализации: {e}")

        # Изменение данных в ячейке
    cell_5_25 = sheet.Cells(5, 25)
    cell_1_23 = sheet.Cells(1, 23)

    cell_1_23.Font.Name = font_name
    cell_1_23.Font.Size = font_size

    cell_1_23.NumberFormat = '@'  # Формат текст

    cell_5_25.Font.Name = font_name
    cell_5_25.Font.Size = font_size

    cell_5_25.NumberFormat = '@'  # Формат текст

    if cell_1_23.Value is None:

        cell_5_25.Value = next_day_formatted
        cell_1_23.Value = num_contract

        output_path = os.path.join(settings.directory_path_temp, file.name)
        windows_path = str(output_path).replace('/', '\\')
        try:
            # Укажите полный путь к новому файлу
            workbook.SaveAs(windows_path)
        except Exception as e:
            print(f"Произошла ошибка Сохранения: {e}")

    try:
        workbook.Close()
        excel.Application.Quit()
    except Exception as e:
        print(f"Произошла ошибка закрытия: {e}")

    return windows_path


def change_act(pNumber):
    settings = config.get_config()
    file = search_files(settings.directory_path,
                        settings.file_extension, settings.name_pattern_act)

    if file is None:
        return

    num_contract = settings.prefix_number + pNumber
    current_date = datetime.now()
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0)

    next_day = current_date + timedelta(days=1)
    formatted_next_day_ukrainian_date = parse_datetime_to_ukrainian_date(
        next_day)

    formatted_next_day_ddmmyyyy = next_day.strftime('%d.%m.%Y')

    excel = None
    workbook = None

    try:
        # Открытие Excel и файла
        excel = win32com.client.Dispatch("Excel.Application")
        # Укажите полный путь к вашему файлу
        workbook = excel.Workbooks.Open(file.path)
        sheet = workbook.Sheets(1)
    except Exception as e:
        print(f"Произошла инициализации Excel.Application : {e}")
        return

    # Изменение данных в ячейке  НОМЕРА
    number_2_2 = sheet.Cells(2, 2)
    number_5_2 = sheet.Cells(5, 2)
    # дата прописью
    data_2_7 = sheet.Cells(2, 7)
    data_5_7 = sheet.Cells(5, 7)

    # Дата числом
    data_56_10 = sheet.Cells(56, 10)

    if number_2_2.Value is None:

        number_2_2.Value = num_contract
        number_5_2.Value = num_contract

        data_2_7.Value = formatted_next_day_ukrainian_date
        data_5_7.Value = formatted_next_day_ukrainian_date

        data_56_10.Value = formatted_next_day_ddmmyyyy

        output_path = os.path.join(settings.directory_path_temp, file.name)
        windows_path = str(output_path).replace('/', '\\')

        try:
            # Укажите полный путь к новому файлу
            workbook.SaveAs(windows_path)
        except Exception as e:
            print(f"Произошла ошибка Сохранения: {e}")

    try:
        workbook.Close()
        excel.Application.Quit()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return windows_path


def print_non_empty_cells(name_doc):

    settings = config.get_config()
    if name_doc == 'act':

        file = search_files(settings.directory_path,
                            settings.file_extension, settings.name_pattern_act)
    elif name_doc == 'contract':
        file = search_files(settings.directory_path,
                            settings.file_extension, settings.name_pattern_contract)
    else:
        file = None

    if file is None:
        return

    # Создание экземпляра Excel
    excel = win32com.client.Dispatch("Excel.Application")

    try:
        # Открытие файла
        workbook = excel.Workbooks.Open(file.path)
        sheet = workbook.Sheets(1)  # Открытие первого листа

        max_row = sheet.Cells(sheet.Rows.Count, 1).End(-4162).Row

        max_col = sheet.Cells(1, sheet.Columns.Count).End(-4159).Column
        max_col_alternate = 50
        max_col = max_col_alternate

        print(f"Максимальное количество строк: {max_row}")
        print(f"Максимальное количество столбцов: {max_col}")

        # Проход по всем строкам и столбцам
        for row in range(1, max_row + 1):
            for col in range(1, max_col + 1):
                cell_value = sheet.Cells(row, col).Value
                if cell_value not in (None, ''):
                    print(f"Ячейка ({row}, {col}) содержит значение: {
                          cell_value}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрытие книги и выход из Excel
        workbook.Close(SaveChanges=False)
        excel.Application.Quit()


def get_soname_and_auto():
    settings = config.get_config()
    file_contract = search_files(settings.directory_path,
                                 settings.file_extension, settings.name_pattern_contract)

    file_act = search_files(settings.directory_path,
                            settings.file_extension, settings.name_pattern_act)

    if file_act is None:
        return

    answer = ""
    soname = ""
    auto = ""
    try:
        # Открытие Excel и файла
        excel = win32com.client.Dispatch("Excel.Application")
        # Укажите полный путь к вашему файлу
        workbook = excel.Workbooks.Open(file_act.path)
        sheet = workbook.Sheets(1)
        soname = sheet.Cells(13, 10).Value
        auto = sheet.Cells(23, 10).Value
    except Exception as e:
        print(f"Произошла инициализации Excel.Application : {e}")
        return
     
    finally:
        # Закрытие книги и выход из Excel
        workbook.Close(SaveChanges=False)
        excel.Application.Quit()
  
        
        
    answer = f"{soname} {auto}"

    substring = "НЗ_залишаються"

    # Проверка, содержит ли строка подстроку
    if substring in file_contract.name:
        answer = f"{answer} {substring}"
    return answer



import re
from collections import Counter

import pandas as pd
import xlwings as xw

from src.autocad import AutocadWorker
from src.excel import ExcelWorker
from src.parsing import Templates, Parser, Splitter
from src.validation import SearchAmbiguity


@xw.sub
def insert_word_taxation_list():
    """Вставка Word ведомости таксации"""
    taxation_list = ExcelWorker.get_taxation_list()

    sheet = xw.sheets['Ведомость']
    sheet['A1'].value = ['Индекс', 'Номер точки', 'Наименование', 'Количество', 'Высота', 'Толщина', 'Состояние',
                         'Кустарник', 'Валидация']
    for l in ['A', 'B', 'D', 'E', 'F']:
        sheet[f'{l}:{l}'].number_format = '@'
    sheet.range('A2').value = taxation_list
    sheet["A1"].value = ['Индекс']


@xw.sub
def get_count_tree():
    """Подсчёт количества деревьев"""
    app = xw.apps.active

    selected_cells = xw.apps.active.selection
    df = pd.DataFrame(data=selected_cells.value, columns=['Количество'], dtype=str)

    def get_count(text: str) -> int:
        if re.match(Templates.DIGIT, text) or re.match(Templates.FLOAT_DIGIT, text):
            return int(float(text.strip()))
        elif re.match(Templates.TRUNKS, text):
            return 1
        else:
            return 0

    df_count = df['Количество'].apply(get_count)

    app.alert(f"Найдено деревьев: {df_count.sum()}", "Подсчёт количества деревьев")


@xw.func
def get_is_shrub(name: str) -> int:
    """Определить кустарник"""
    is_shrub = Parser.get_specie(name).is_shrub
    return int(is_shrub)


@xw.sub
def get_is_shrub_sub():
    """Вставка формулы: Определить кустарник"""
    xw.apps.active.selection.formula = "=get_is_shrub([@Наименование])"


@xw.func
def check_ambiguity(number, quantity, height, diameter, is_shrub) -> int:
    """Поиск неоднозначностей в количественных характеристиках"""
    number, quantity, height, diameter = str(number), str(quantity), str(height), str(diameter)
    result = SearchAmbiguity.check_in_row_from_taxation_list(number, quantity, height, diameter, is_shrub)
    return int(not result)


@xw.sub
def check_ambiguity_sub():
    """Вставка формулы: Поиск неоднозначностей в количественных характеристиках"""
    xw.apps.active.selection.formula = ("=check_ambiguity([@Номер точки],[@Количество],[@Высота],[@Толщина],"
                                        "[@Кустарник])")


@xw.sub
def replace_comma_to_dot():
    """Замена запятой на точку"""
    selected_cells = xw.apps.active.selection
    for cell in selected_cells:
        if not xw.sheets.active.api.Rows(cell.row).Hidden and ',' in str(cell.value):
            cell.value = str(cell.value).replace(',', '.')


@xw.sub
def replace_dot_comma_to_comma():
    """Замена точки с запятой на запятую"""
    selected_cells = xw.apps.active.selection
    for cell in selected_cells:
        if not xw.sheets.active.api.Rows(cell.row).Hidden and ';' in str(cell.value):
            cell.value = str(cell.value).replace(';', ',')


@xw.sub
def compare_numbers():
    """Сравнить наличие номеров в Excel и Autocad"""
    numbers_from_excel = ExcelWorker.get_numbers(xw.sheets['Ведомость'], 'Номер точки')
    numbers_from_acad = AutocadWorker.get_numbers('номера')
    split_numbers_from_excel = []
    for number_excel in numbers_from_excel:
        split_numbers_from_excel.extend(Splitter.number(str(number_excel)))
    split_numbers_from_acad = []
    for number_acad in numbers_from_acad:
        split_numbers_from_acad.extend(Splitter.number(str(number_acad)))
    counter_split_numbers_from_excel = Counter(split_numbers_from_excel)
    duplicates_split_numbers_from_excel = [key for key, value in counter_split_numbers_from_excel.items() if value > 1]
    counter_split_numbers_from_acad = Counter(split_numbers_from_acad)
    duplicates_split_numbers_from_acad = [key for key, value in counter_split_numbers_from_acad.items() if value > 1]
    unique_in_excel = list(set(split_numbers_from_excel) - set(split_numbers_from_acad))
    unique_in_acad = list(set(split_numbers_from_acad) - set(split_numbers_from_excel))
    new_doc = xw.books.add()
    new_doc.sheets[0]['A1'].value = ["Дубликаты Excel", "Дубликаты Autocad", "Только в Excel", "Только в Autocad"]
    i = 1
    for value in duplicates_split_numbers_from_excel:
        i += 1
        new_doc.sheets[0][f'A{i}'].value = value
    i = 1
    for value in duplicates_split_numbers_from_acad:
        i += 1
        new_doc.sheets[0][f'B{i}'].value = value
    i = 1
    for value in unique_in_excel:
        i += 1
        new_doc.sheets[0][f'C{i}'].value = value
    i = 1
    for value in unique_in_acad:
        i += 1
        new_doc.sheets[0][f'D{i}'].value = value


@xw.sub
def insert_taxation_data_from_autocad():
    """Вставка таксационных данных из топографического плана Autocad в лист"""
    topographic_plan = AutocadWorker.get_df_topographic_plan(["номера"], ["полосы"], ["контуры"], wkt_convert=True)
    sheet = xw.sheets['Автокад']
    for l in ['A', 'B', 'C']:
        sheet[f'{l}:{l}'].number_format = '@'
    sheet.range('A1').value = topographic_plan
    sheet["A1"].value = ['Индекс']


@xw.sub
def insert_taxation_list_orm():
    """Вставка ведомости ОРМ"""
    taxation_list_orm = ExcelWorker.get_taxation_list_orm(wkt_convert=True)
    sheet = xw.sheets['Ведомость ОРМ']
    for l in ['A', 'B', 'D', 'E', 'F']:
        sheet[f'{l}:{l}'].number_format = '@'
    sheet.range('A1').value = taxation_list_orm
    sheet["A1"].value = ['Индекс']


@xw.sub
def insert_zones_from_autocad():
    """Вставить зоны из топографического плана в таблицу"""
    zones = AutocadWorker.get_df_zones(['зоны'], wkt_convert=True)
    sheet = xw.sheets['Зоны']
    sheet[f'A:A'].number_format = '@'
    sheet.range('A1').value = zones
    sheet["A1"].value = ['Индекс']


@xw.sub
def insert_protected_zones_from_autocad():
    """Вставить охранные зоны из топографического плана в таблицу"""
    zones = AutocadWorker.get_df_protection_zones(['охранные зоны'], wkt_convert=True)
    sheet = xw.sheets['Охранные зоны']
    sheet[f'A:A'].number_format = '@'
    sheet.range('A1').value = zones
    sheet["A1"].value = ['Индекс']


@xw.sub
def insert_zone_objects():
    """Вставить объекты для зоны"""
    sheet = xw.sheets.active
    objects_in_zone = ExcelWorker.get_objects_from_zone(sheet.name, wkt_convert=True)
    for l in ['A', 'B', 'C', 'E', 'F', 'G']:
        sheet[f'{l}:{l}'].number_format = '@'
    sheet.range('A1').value = objects_in_zone
    sheet["A1"].value = ['Индекс']

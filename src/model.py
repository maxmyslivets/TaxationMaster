import re
from collections import Counter
from pathlib import Path

import pandas as pd
import xlwings as xw

from src.autocad import AutocadWorker
from src.excel import ExcelWorker
from src.parsing import Templates, Parser, Splitter
from src.validation import Validate
from src.ui.additional import Progress


class Model:

    @staticmethod
    def open_excel_template(progress: Progress) -> None:
        """Открытие шаблона"""
        progress.total = 1
        progress.status = "Открытие шаблона ..."
        app = xw.App(visible=True, add_book=False)
        app.books.open(Path(__file__).parent.parent/"data"/"template_excel.xlsx")
        progress.next()

    @staticmethod
    def insert_word_taxation_list(progress: Progress) -> None:
        """Вставка Word ведомости таксации"""
        progress.status = "Вставка Word ведомости таксации ..."
        taxation_list = ExcelWorker.get_taxation_list(progress)
        progress.total = 1
        sheet = xw.sheets['Ведомость']
        sheet['A1'].value = ['Индекс', 'Номер точки', 'Наименование', 'Количество', 'Высота', 'Толщина', 'Состояние',
                             'Кустарник', 'Валидация']
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A2').value = taxation_list
        sheet["A1"].value = ['Индекс']
        progress.next()

    @staticmethod
    def get_count_tree(progress: Progress) -> None:
        """Подсчёт количества деревьев"""
        progress.status = "Подсчёт количества деревьев ..."
        progress.total = 1
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

        print(f"Найдено деревьев: {df_count.sum()}.")
        progress.next()

    @staticmethod
    def identification_shrub(progress: Progress) -> None:
        """Определить кустарник"""
        sheet = xw.sheets['Ведомость']
        col = ExcelWorker.column_from_title(sheet)
        selected_cells = ExcelWorker.selected_cells(progress)
        progress.status = "Определение кустарников ..."
        progress.total = len(selected_cells)
        for cell in selected_cells:
            name = sheet.range(f"{col['Наименование']}{cell.row}").value
            try:
                is_shrub = Parser.get_specie(name).is_shrub
                sheet.range(f"{col['Кустарник']}{cell.row}").value = int(is_shrub)
            except ValueError as e:
                sheet.range(f"{col['Кустарник']}{cell.row}").value = str(e)
            progress.next()

    @staticmethod
    def validation(progress: Progress) -> None:
        """Поиск неоднозначностей в количественных характеристиках"""
        sheet = xw.sheets['Ведомость']
        col = ExcelWorker.column_from_title(sheet)
        selected_cells = ExcelWorker.selected_cells(progress)
        progress.status = "Валидация количественных и качественных характеристик ..."
        progress.total = len(selected_cells)
        for cell in selected_cells:
            number = sheet.range(f"{col['Номер точки']}{cell.row}").value
            quantity = sheet.range(f"{col['Количество']}{cell.row}").value
            height = sheet.range(f"{col['Высота']}{cell.row}").value
            diameter = sheet.range(f"{col['Толщина']}{cell.row}").value
            is_shrub = bool(sheet.range(f"{col['Кустарник']}{cell.row}").value)
            quality = sheet.range(f"{col['Состояние']}{cell.row}").value
            problem = Validate.check_taxation_list_row(number, quantity, height, diameter, quality, is_shrub)
            sheet.range(f"{col['Валидация']}{cell.row}").value = int(not problem)
            progress.next()

    @staticmethod
    def replace_comma_to_dot(progress: Progress) -> None:
        """Замена запятой на точку"""
        selected_cells = ExcelWorker.selected_cells(progress)
        progress.status = "Замена запятой на точку ..."
        progress.total = len(selected_cells)
        print(f"Замена пунктуации в {len(selected_cells)} ячейках ...")
        for cell in selected_cells:
            if ',' in str(cell.value):
                cell.value = str(cell.value).replace(',', '.')
            progress.next()

    @staticmethod
    def replace_dot_comma_to_comma(progress: Progress) -> None:
        """Замена точки с запятой на запятую"""
        selected_cells = ExcelWorker.selected_cells(progress)
        progress.status = "Замена точки с запятой на запятую ..."
        progress.total = len(selected_cells)
        for cell in selected_cells:
            if ';' in str(cell.value):
                cell.value = str(cell.value).replace(';', ',')
            progress.next()

    @staticmethod
    def compare_numbers(progress: Progress):
        """Сравнить наличие номеров в Excel и Autocad"""
        progress.status = "Сравнение номеров в Excel и Autocad ..."
        progress.total = 100
        numbers_from_excel = ExcelWorker.get_numbers(xw.sheets['Ведомость'], 'Номер точки')
        numbers_from_acad = AutocadWorker.get_numbers('номера')
        progress.update(5)

        split_numbers_from_excel = []
        for number_excel in numbers_from_excel:
            split_numbers_from_excel.extend(Splitter.number(str(number_excel)))
        split_numbers_from_acad = []
        for number_acad in numbers_from_acad:
            split_numbers_from_acad.extend(Splitter.number(str(number_acad)))
        progress.update(20)

        counter_split_numbers_from_excel = Counter(split_numbers_from_excel)
        duplicates_split_numbers_from_excel = [key for key, value in counter_split_numbers_from_excel.items() if value > 1]
        print(f"Дубликаты Excel: {duplicates_split_numbers_from_excel}")
        progress.update(40)

        counter_split_numbers_from_acad = Counter(split_numbers_from_acad)
        duplicates_split_numbers_from_acad = [key for key, value in counter_split_numbers_from_acad.items() if value > 1]
        print(f"Дубликаты Autocad: {duplicates_split_numbers_from_acad}")
        progress.update(60)

        unique_in_excel = list(set(split_numbers_from_excel) - set(split_numbers_from_acad))
        print(f"Только в Excel: {unique_in_excel}")
        progress.update(80)

        unique_in_acad = list(set(split_numbers_from_acad) - set(split_numbers_from_excel))
        print(f"Только в Autocad: {unique_in_acad}")
        progress.update(100)


    @staticmethod
    def insert_taxation_data_from_autocad(progress: Progress):
        """Вставка таксационных данных из топографического плана Autocad в лист"""
        progress.status = "Вставка таксационных данных из топографического плана Autocad в лист ..."
        topographic_plan = AutocadWorker.get_df_topographic_plan(["номера"], ["полосы"], ["контуры"],
                                                                 wkt_convert=True, progress=progress)
        sheet = xw.sheets['Автокад']
        ExcelWorker.set_text_format(sheet, [1, 2, 3])
        sheet.range('A1').value = topographic_plan
        sheet["A1"].value = ['Индекс']
        progress.update(100)

    @staticmethod
    def insert_taxation_list_orm(progress: Progress):
        """Вставка ведомости ОРМ"""
        progress.status = "Создание ведомости ОРМ ..."
        taxation_list_orm = ExcelWorker.get_taxation_list_orm(wkt_convert=True, progress=progress)
        sheet = xw.sheets['Ведомость ОРМ']
        ExcelWorker.set_text_format(sheet, [1, 2, 3])
        sheet.range('A1').value = taxation_list_orm
        sheet["A1"].value = ['Индекс']
        progress.update(100)

    @staticmethod
    def insert_zones_from_autocad(progress: Progress):
        """Вставить зоны из топографического плана в таблицу"""
        progress.status = "Создание ведомости ОРМ ..."
        zones = AutocadWorker.get_df_zones(['зоны'], wkt_convert=True, progress=progress)
        sheet = xw.sheets['Зоны']
        ExcelWorker.set_text_format(sheet, [1])
        sheet.range('A1').value = zones
        sheet["A1"].value = ['Индекс']
        progress.update(100)

    @staticmethod
    def insert_protected_zones_from_autocad(progress: Progress):
        """Вставить охранные зоны из топографического плана в таблицу"""
        progress.total = 100
        progress.status = "Вставка охранных зон из топографического плана в таблицу ..."
        zones = AutocadWorker.get_df_protection_zones(['охранные зоны'], wkt_convert=True, progress=progress)
        sheet = xw.sheets['Охранные зоны']
        ExcelWorker.set_text_format(sheet, [1])
        sheet.range('A1').value = zones
        sheet["A1"].value = ['Индекс']
        progress.update(100)

    @staticmethod
    def insert_zone_objects(progress: Progress):
        """Вставить объекты для зоны"""
        progress.total = 100
        progress.status = "Вставка ОРМ в лист зоны ..."
        sheet = xw.sheets.active
        objects_in_zone = ExcelWorker.get_objects_from_zone(sheet.name, wkt_convert=True, progress=progress)
        ExcelWorker.set_text_format(sheet, [1, 2, 3, 5, 6, 7])
        sheet.range('A1').value = objects_in_zone
        sheet["A1"].value = ['Индекс']
        progress.update(100)

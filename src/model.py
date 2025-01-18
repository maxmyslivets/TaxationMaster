import re
import subprocess
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd
import xlwings as xw

from src.autocad import AutocadWorker
from src.excel import ExcelWorker
from src.parsing import Templates, Parser, Splitter
from src.validation import Validate


class Model:

    @staticmethod
    def open_excel_template(app) -> None:
        """Открытие шаблона"""
        progress = app.progress_manager.new("Открытие шаблона", 1)
        app = xw.App(visible=True, add_book=False)
        app.books.open(Path(__file__).parent.parent/"data"/"template_excel.xlsx")
        progress.next()

    @staticmethod
    def insert_word_taxation_list(app) -> None:
        """Вставка Word ведомости таксации"""
        progress = app.progress_manager.new("Вставка ведомости таксации", 1)
        taxation_list = ExcelWorker.get_taxation_list(app)
        sheet = xw.sheets['Ведомость']
        sheet['A1'].value = ['Индекс', 'Номер точки', 'Наименование', 'Количество', 'Высота', 'Толщина', 'Состояние',
                             'Кустарник', 'Валидация']
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A2').value = taxation_list
        sheet["A1"].value = ['Индекс']
        progress.next()

    @staticmethod
    def get_count_tree(app) -> None:
        """Подсчёт количества деревьев"""
        progress = app.progress_manager.new("Подсчёт количества деревьев", 1)
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
    def identification_shrub(app) -> None:
        """Определить кустарник"""
        progress = app.progress_manager.new("Определение кустарников", 1)
        sheet = xw.sheets['Ведомость']
        col = ExcelWorker.column_from_title(sheet)
        selected_cells = ExcelWorker.selected_cells(app)
        progress.progress.setMaximum(len(selected_cells))
        for cell in selected_cells:
            name = sheet.range(f"{col['Наименование']}{cell.row}").value
            try:
                is_shrub = Parser.get_specie(name).is_shrub
                sheet.range(f"{col['Кустарник']}{cell.row}").value = int(is_shrub)
            except ValueError as e:
                sheet.range(f"{col['Кустарник']}{cell.row}").value = str(e)
                print(e)
            progress.next()

    @staticmethod
    def validation(app) -> None:
        """Поиск неоднозначностей в количественных характеристиках"""
        progress = app.progress_manager.new("Валидация", 1)
        sheet = xw.sheets['Ведомость']
        col = ExcelWorker.column_from_title(sheet)
        selected_cells = ExcelWorker.selected_cells(app)
        progress.progress.setMaximum(len(selected_cells))
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
    def replace_comma_to_dot(app) -> None:
        """Замена запятой на точку"""
        selected_cells = ExcelWorker.selected_cells(app)
        progress = app.progress_manager.new("Замена запятой на точку", len(selected_cells))
        print(f"Замена пунктуации в {len(selected_cells)} ячейках ...")
        for cell in selected_cells:
            if ',' in str(cell.value):
                cell.value = str(cell.value).replace(',', '.')
            progress.next()

    @staticmethod
    def replace_dot_comma_to_comma(app) -> None:
        """Замена точки с запятой на запятую"""
        selected_cells = ExcelWorker.selected_cells(app)
        progress = app.progress_manager.new("Замена точки с запятой на запятую", len(selected_cells))
        for cell in selected_cells:
            if ';' in str(cell.value):
                cell.value = str(cell.value).replace(';', ',')
            progress.next()

    @staticmethod
    def compare_numbers(app):
        """Сравнить наличие номеров в Excel и Autocad"""
        progress = app.progress_manager.new("Сравнение номеров в Excel и Autocad", 6)
        numbers_from_excel = ExcelWorker.get_numbers(xw.sheets['Ведомость'], 'Номер точки')
        numbers_from_acad = AutocadWorker.get_numbers('номера')
        progress.set_value(1)

        split_numbers_from_excel = []
        for number_excel in numbers_from_excel:
            split_numbers_from_excel.extend(Splitter.number(str(number_excel)))
        split_numbers_from_acad = []
        for number_acad in numbers_from_acad:
            split_numbers_from_acad.extend(Splitter.number(str(number_acad)))
        progress.set_value(2)

        counter_split_numbers_from_excel = Counter(split_numbers_from_excel)
        duplicates_split_numbers_from_excel = [key for key, value in counter_split_numbers_from_excel.items() if value > 1]
        print(f"Дубликаты Excel: {duplicates_split_numbers_from_excel}")
        progress.set_value(3)

        counter_split_numbers_from_acad = Counter(split_numbers_from_acad)
        duplicates_split_numbers_from_acad = [key for key, value in counter_split_numbers_from_acad.items() if value > 1]
        print(f"Дубликаты Autocad: {duplicates_split_numbers_from_acad}")
        progress.set_value(4)

        unique_in_excel = list(set(split_numbers_from_excel) - set(split_numbers_from_acad))
        print(f"Только в Excel: {unique_in_excel}")
        progress.set_value(5)

        unique_in_acad = list(set(split_numbers_from_acad) - set(split_numbers_from_excel))
        print(f"Только в Autocad: {unique_in_acad}")
        progress.set_value(6)

    @staticmethod
    def insert_taxation_data_from_autocad(app):
        """Вставка таксационных данных из топографического плана Autocad в лист"""
        progress = app.progress_manager.new("Вставка таксации из Autocad в лист", 100)
        topographic_plan = AutocadWorker.get_df_topographic_plan(["номера"], ["полосы"], ["контуры"],
                                                                 wkt_convert=True, app=app)
        sheet = xw.sheets['Автокад']
        ExcelWorker.set_text_format(sheet, [1, 2, 3])
        sheet.range('A1').value = topographic_plan
        sheet["A1"].value = ['Индекс']
        progress.set_value(100)

    @staticmethod
    def insert_taxation_list_orm(app):
        """Вставка ведомости ОРМ"""
        progress = app.progress_manager.new("Создание ведомости ОРМ", 100)
        taxation_list_orm = ExcelWorker.get_taxation_list_orm(wkt_convert=True, app=app)
        sheet = xw.sheets['Ведомость ОРМ']
        ExcelWorker.set_text_format(sheet, [1, 2, 3])
        sheet.range('A1').value = taxation_list_orm
        sheet["A1"].value = ['Индекс']
        progress.set_value(100)

    @staticmethod
    def insert_zones_from_autocad(app):
        """Вставить зоны из топографического плана в таблицу"""
        progress = app.progress_manager.new("Вставка зон из Autocad", 100)
        zones = AutocadWorker.get_df_zones(['зоны'], wkt_convert=True, app=app)
        sheet = xw.sheets['Зоны']
        ExcelWorker.set_text_format(sheet, [1])
        sheet.range('A1').value = zones
        sheet["A1"].value = ['Индекс']
        progress.set_value(100)

    @staticmethod
    def insert_protected_zones_from_autocad(app):
        """Вставить охранные зоны из топографического плана в таблицу"""
        progress = app.progress_manager.new("Вставка охранных зон из Autocad", 100)
        zones = AutocadWorker.get_df_protection_zones(['охранные зоны'], wkt_convert=True, app=app)
        sheet = xw.sheets['Охранные зоны']
        ExcelWorker.set_text_format(sheet, [1])
        sheet.range('A1').value = zones
        sheet["A1"].value = ['Индекс']
        progress.set_value(100)

    @staticmethod
    def insert_zone_objects(app):
        """Вставить объекты для зоны"""
        progress = app.progress_manager.new("Вставка ОРМ в лист зоны", 100)
        sheet = xw.sheets.active
        objects_in_zone = ExcelWorker.get_objects_from_zone(sheet.name, wkt_convert=True, app=app)
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A1').value = objects_in_zone
        sheet["A1"].value = ['Индекс']
        progress.set_value(100)

    @staticmethod
    def generate_numeration(app):
        """Нумерация по ближайшим"""
        sheet = xw.sheets.active
        objects_in_zone = ExcelWorker.generate_numeration_from_zone(wkt_convert=True, app=app)
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A1').value = objects_in_zone
        sheet["A1"].value = ['Индекс']

    @staticmethod
    def removable_or_transplantable(app):
        """Определение действия над деревьями и кустарниками. Удалять или пересаживать"""
        sheet = xw.sheets.active
        taxation_list_orm_df = ExcelWorker.removable_or_transplantable(wkt_convert=True, app=app)
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A1').value = taxation_list_orm_df
        sheet["A1"].value = ['Индекс']

    @staticmethod
    def insert_calculation_landings(app):
        """Расчет компенсационных посадок"""
        sheet = xw.sheets.active
        taxation_list_orm_df = ExcelWorker.calculation_landings_or_payments(landings=True, app=app)
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A1').value = taxation_list_orm_df
        sheet["A1"].value = ['Индекс']

    @staticmethod
    def insert_calculation_payments(app):
        """Расчет компенсационных выплат"""
        sheet = xw.sheets.active
        taxation_list_orm_df = ExcelWorker.calculation_landings_or_payments(payments=True, app=app)
        ExcelWorker.set_text_format(sheet, [1, 2, 4, 5, 6])
        sheet.range('A1').value = taxation_list_orm_df
        sheet["A1"].value = ['Индекс']

    @staticmethod
    def insert_numbers_to_autocad(app):
        """Вставка номеров в Autocad"""
        numbers_in_zone = ExcelWorker.get_zip_numbers(app=app)
        dxf_template = str(Path(__file__).parent.parent/"data"/"template.dxf")
        dt = datetime.now().strftime('%Y%m%d%H%M%S')
        dxf_output = str(Path(tempfile.gettempdir()) / f"taxation_tool_{dt}.dxf")
        AutocadWorker.insert_numbers_to_dxf(numbers_in_zone, dxf_template, dxf_output, app=app)
        subprocess.Popen(f'explorer /select,"{dxf_output}"')

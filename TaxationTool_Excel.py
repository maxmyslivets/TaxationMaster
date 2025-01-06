import re
from tkinter.filedialog import askopenfilename

import pandas as pd
import xlwings as xw
from docx import Document as DocxDocument

from src.parsing import Templates, Parser
from src.validation import SearchAmbiguity


@xw.sub
def insert_word_taxation_list():
    """Вставка Word ведомости таксации"""
    app = xw.apps.active

    file_path = askopenfilename(filetypes=[("Word files", "*.docx *.doc"), ("All files", "*.*")])
    if not file_path:
        return

    app.status_bar = 'Чтение ведомости таксации... 0%'

    doc = DocxDocument(file_path)
    data = []

    count_row = 0
    for table in doc.tables:
        count_row += len(table.rows)
    i_row = 0

    for table in doc.tables:
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            data.append(row_data)

            progress = int(((i_row + 1) / count_row) * 100)
            app.status_bar = f"Чтение ведомости таксации... {progress}%"
            i_row += 1

    df = pd.DataFrame(data)

    sheet = xw.sheets.active
    sheet['A1'].value = "Порядок колонок:"
    sheet['A1'].font.bold = True
    sheet['A2'].value = ['Индекс', 'Номер', 'Наименование', 'Количество', 'Высота', 'Диаметр', 'Состояние', 'Кустарник',
                         'Неоднозначность', 'Пень']
    sheet['A3'].options(index=True, header=False).value = df
    sheet.tables.add(source=sheet['A3'].expand(), name='ВедомостьТаксации')

    app.status_bar = 'Готово'


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
        elif re.match(Templates.CONTOUR, text):
            return 0
        elif re.match(Templates.LINE, text):
            return 0
        else:
            return 0

    df_count = df['Количество'].apply(get_count)

    app.alert(f"Найдено деревьев: {df_count.sum()}", "Подсчёт количества деревьев")


@xw.sub
def replace_comma_to_dot():
    """Замена запятой на точку"""
    app = xw.apps.active
    with app.properties(status_bar='Замена знака пунктуации...'):
        selected_cells = xw.apps.active.selection
        for cell in selected_cells:
            cell.value = str(cell.value).replace(',', '.')


@xw.sub
def replace_dot_comma_to_comma():
    """Замена точки с запятой на запятую"""
    selected_cells = xw.apps.active.selection
    for cell in selected_cells:
        cell.value = str(cell.value).replace(';', ',')


@xw.func
def get_is_shrub(name: str) -> int:
    """Определить кустарник"""
    is_shrub = Parser.get_specie(name).is_shrub
    return int(is_shrub)


@xw.sub
def get_is_shrub_sub():
    """Вставка формулы: Определить кустарник"""
    selected_cells = xw.apps.active.selection
    for cell in selected_cells:
        cell.value = "=get_is_shrub()"


@xw.func
def check_ambiguity(number, quantity, height, diameter, is_shrub) -> int:
    """Поиск неоднозначностей в количественных характеристиках"""
    number, quantity, height, diameter = str(number), str(quantity), str(height), str(diameter)
    result = SearchAmbiguity.check_in_row_from_taxation_list(number, quantity, height, diameter, is_shrub)
    return int(not result)


@xw.sub
def check_ambiguity_sub():
    """Вставка формулы: Поиск неоднозначностей в количественных характеристиках"""
    selected_cells = xw.apps.active.selection
    for cell in selected_cells:
        cell.value = "=check_ambiguity()"


@xw.func
def identification_stump(height, diameter, is_shrub) -> int:
    """Определить пень"""
    is_stump = Parser.identification_stump(height, diameter, is_shrub)
    return int(is_stump)


@xw.sub
def identification_stump_sub():
    """Вставка формулы: Определить пень"""
    selected_cells = xw.apps.active.selection
    for cell in selected_cells:
        cell.value = "=identification_stump()"


# def main():
#     wb = xw.Book.caller()
#
#
# if __name__ == "__main__":
#     xw.Book("proj1.xlsm").set_mock_caller()
#     main()

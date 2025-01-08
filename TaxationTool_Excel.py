import re
from collections import Counter
from tkinter.filedialog import askopenfilename

import pandas as pd
import xlwings as xw
from docx import Document as DocxDocument
from pyautocad import Autocad
from pyautocad.utils import mtext_to_string
from shapely import Point, LineString, Polygon

from src.parsing import Templates, Parser, Splitter
from src.validation import SearchAmbiguity


@xw.sub
def insert_word_taxation_list():
    """Вставка Word ведомости таксации"""
    file_path = askopenfilename(filetypes=[("Word files", "*.docx *.doc"), ("All files", "*.*")])
    if not file_path:
        return

    doc = DocxDocument(file_path)
    data = []

    for table in doc.tables:
        for row in table.rows:
            row_data = ["'"+cell.text.strip() for cell in row.cells]
            data.append(row_data)

    df = pd.DataFrame(data)
    df.index = df.index - 1

    sheet = xw.sheets.active
    sheet['A1'].value = ['Индекс', 'Номер точки', 'Наименование', 'Количество', 'Высота', 'Толщина', 'Состояние',
                         'Кустарник', 'Неоднозначность', 'Пень', 'Наименование (пень)']
    sheet['A2'].options(index=True, header=False).value = df


@xw.sub
def create_table():
    """Преобразовать ведомость таксации в таблицу"""
    selected_cells = xw.apps.active.selection
    xw.sheets.active.tables.add(source=selected_cells, name='ВедомостьТаксации', table_style_name='TableStyleMedium9')


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


@xw.func
def identification_stump(height, diameter, is_shrub) -> int:
    """Определить пень"""
    is_stump = Parser.identification_stump(height, diameter, is_shrub)
    return int(is_stump)


@xw.sub
def identification_stump_sub():
    """Вставка формулы: Определить пень"""
    xw.apps.active.selection.formula = "=identification_stump([@Высота],[@Толщина],[@Кустарник])"


@xw.func
def insert_stump(name, is_stump) -> str:
    """Вставить пень"""
    assert "пень" not in name.lower()
    if is_stump:
        return name + " (пень)"
    else:
        return name


@xw.sub
def insert_stump_sub():
    """Вставка формулы: Вставить пень"""
    xw.apps.active.selection.formula = "=insert_stump([@Наименование],[@Пень])"


@xw.sub
def compare_numbers():
    """Сравнить наличие номеров в Excel и Autocad"""
    sheet = xw.sheets.active
    table_range = sheet['A1'].expand('table')
    data = table_range.value
    headers = data[0]
    col_index = headers.index("Номер точки")
    numbers_from_excel = [row[col_index] for row in data[1:]]
    acad = Autocad()
    numbers_from_acad = []
    for obj in acad.iter_objects(['AcDbText', 'AcDbMText']):
        if obj.Layer == "номера":
            numbers_from_acad.append(obj.TextString)
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
def read_autocad():
    """Чтение таксационных данных из топографического плана Autocad в буфер обмена"""
    numbers_layers = ["номера"]
    lines_layers = ["полосы"]
    contours_layers = ["контуры"]
    min_distance = 0.01

    acad = Autocad()
    numbers_data = []

    for obj in acad.iter_objects(['AcDbText', 'AcDbMText']):
        if obj.ObjectName == 'AcDbText' and obj.Layer in numbers_layers:
            x, y, _ = obj.InsertionPoint
            numbers_data.append({
                'number': obj.TextString,
                'position': Point(x, y)
            })
        elif obj.ObjectName == 'AcDbMText' and obj.Layer in numbers_layers:
            x, y, _ = obj.InsertionPoint
            numbers_data.append({
                'number': mtext_to_string(obj.TextString).replace('\n', ' '),
                'position': Point(x, y)
            })

    numbers_df = pd.DataFrame(numbers_data)

    shapes_data = []
    for obj in acad.iter_objects(['AcDbLine', 'AcDbPolyline', 'AcDbPolygon']):
        if obj.ObjectName == 'AcDbLine' and obj.Layer in lines_layers:
            shape = LineString([(obj.StartPoint[0], obj.StartPoint[1]),
                                (obj.EndPoint[0], obj.EndPoint[1])])
            shapes_data.append({
                'geometry': shape,
                'type': 'LineString'
            })
        elif obj.ObjectName == 'AcDbPolyline' and obj.Layer in lines_layers:
            acad_polygon_vertexes = [vertex for vertex in obj.Coordinates]
            shape = LineString(
                [(acad_polygon_vertexes[i], acad_polygon_vertexes[i + 1])
                 for i in range(0, len(acad_polygon_vertexes), 2)])
            shapes_data.append({
                'geometry': shape,
                'type': 'LineString'
            })
        elif obj.ObjectName == 'AcDbPolyline' and obj.Layer in contours_layers:
            acad_polygon_vertexes = [vertex for vertex in obj.Coordinates]
            shape = Polygon(
                [(acad_polygon_vertexes[i], acad_polygon_vertexes[i + 1])
                 for i in range(0, len(acad_polygon_vertexes), 2)])
            shapes_data.append({
                'geometry': shape,
                'type': 'Polygon'
            })

    shapes_df = pd.DataFrame(shapes_data)

    # Связывание номеров и фигур
    numbers_shapes_data = []
    if not numbers_df.empty and not shapes_df.empty:
        # Создаем геометрические точки для всех номеров
        number_points = numbers_df.apply(lambda row: row['position'], axis=1)

        # Для каждой фигуры проверяем все номера
        for shape_id, shape_row in shapes_df.iterrows():
            shape_type = shape_row['type']
            shape_geom = shape_row['geometry']

            # Вычисляем расстояния до всех точек
            if shape_type == 'LineString':
                distances = number_points.apply(lambda p: shape_geom.distance(p))
            else:
                distances = number_points.apply(lambda p: p.distance(shape_geom.exterior))

            # Находим номера, которые находятся достаточно близко
            close_numbers = distances[distances < min_distance]

            for number_id in close_numbers.index:
                numbers_shapes_data.append({
                    'number_id': number_id,
                    'shape_id': shape_id
                })

    numbers_shapes_df = pd.DataFrame(numbers_shapes_data)

    # Сбор деревьев (точечных объектов)
    unassigned_numbers = numbers_df.index.difference(numbers_shapes_df['number_id'])

    trees_data = []
    for number_id in unassigned_numbers:
        trees_data.append({
            'number_id': number_id
        })

    trees_df = pd.DataFrame(trees_data)

    topographic_plan_data = []

    for number_id in trees_df['number_id']:
        for _split_number in Splitter.number(numbers_df.iloc[number_id]['number']):
            topographic_plan_data.append(
                {
                    'origin_number': numbers_df.iloc[number_id]['number'],
                    'number_position': numbers_df.iloc[number_id]['position'],
                    'split_number': _split_number,
                    'type': 'Point',
                    'geometry': numbers_df.iloc[number_id]['position'],
                    'size': None
                }
            )

    for numbers_shapes_id in numbers_shapes_df.index:

        number_id = numbers_shapes_df.iloc[numbers_shapes_id]['number_id']
        shape_id = numbers_shapes_df.iloc[numbers_shapes_id]['shape_id']
        shape: LineString | Polygon = shapes_df.iloc[shape_id]['geometry']
        shape_type = shapes_df.iloc[shape_id]['type']

        for _split_number in Splitter.number(numbers_df.iloc[number_id]['number']):
            topographic_plan_data.append(
                {
                    'origin_number': numbers_df.iloc[number_id]['number'],
                    'number_position': numbers_df.iloc[number_id]['position'],
                    'split_number': _split_number,
                    'type': shape_type,
                    'geometry': shape,
                    'size': shape.length if isinstance(shape, LineString) else shape.area
                }
            )

    topographic_plan = pd.DataFrame(topographic_plan_data)

    sheet = xw.sheets['Автокад']
    sheet["A1"].value = ['index']
    sheet["B1"].value = topographic_plan.columns.to_list()
    row = 1
    for _, series in topographic_plan.iterrows():
        row += 1
        data = [str(v) for v in series.to_list()]
        data[0], data[2] = f"'{data[0]}", f"'{data[2]}"
        data.insert(0, row - 2)
        sheet[f'A{row}'].value = data
    sheet_range = sheet["A1"].expand()
    xw.sheets.active.tables.add(source=sheet_range, name='ТаксацияАвтокад',
                                table_style_name='TableStyleMedium9')


# def main():
#     wb = xw.Book.caller()
#
#
# if __name__ == "__main__":
#     xw.Book("proj1.xlsm").set_mock_caller()
#     main()

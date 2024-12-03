from pathlib import Path

import ezdxf
import pandas as pd
from ezdxf.entities import MText
from shapely import LineString, Polygon, Point

from src.processing.splitting import split_number


def create_topographic_plan(dxf_path: Path, numbers_layers: list[str],
                            lines_layers: list[str], contours_layers: list[str],
                            max_distance: float) -> pd.DataFrame:
    """
    Создание DataFrame объектов топографического плана.

    Series
    ----
    * origin_number - оригинальный номер.
    * number_position - координаты номера.
    * split_number - разделенный номер.
    * type - тип геометрии объекта.
    * geometry - геометрия объекта.
    * size - размер геометрии объекта (длина | площадь | None).

    :param dxf_path: Путь до dxf файла.
    :param numbers_layers: Список слоев с номерами.
    :param lines_layers: Список слоев с полосами растительности.
    :param contours_layers: Список слоев с контурами растительности.
    :param max_distance: Максимальное расстояние между номером и фигурой для их соединения.
    :return: DataFrame | None
    """

    doc = ezdxf.readfile(dxf_path)

    # Сбор номеров и их позиций
    numbers_data = []

    # Собираем отдельно TEXT и MTEXT
    for layer in numbers_layers:
        text_entities = doc.modelspace().query(f'TEXT[layer=="{layer}"]')
        mtext_entities = doc.modelspace().query(f'MTEXT[layer=="{layer}"]')

        for text in list(text_entities) + list(mtext_entities):
            number = text.plain_text().replace('\n', ' ') if isinstance(text, MText) else text.plain_text()
            numbers_data.append({
                'number': number,
                'position': Point(text.dxf.insert[0], text.dxf.insert[1])
            })

    numbers_df = pd.DataFrame(numbers_data)

    # Сбор геометрических фигур
    shapes_data = []

    # Сбор линий
    for layer in lines_layers:
        lines = doc.modelspace().query(f'LINE[layer=="{layer}"]')
        polylines = doc.modelspace().query(f'LWPOLYLINE[layer=="{layer}"]')

        for line in lines:
            shape = LineString([(line.dxf.start.x, line.dxf.start.y),
                                (line.dxf.end.x, line.dxf.end.y)])
            shapes_data.append({
                'geometry': shape,
                'type': 'LineString'
            })

        for pline in polylines:
            shape = LineString([(float(x), float(y)) for x, y in list(pline.vertices())])
            shapes_data.append({
                'geometry': shape,
                'type': 'LineString'
            })

    # Сбор контуров
    for layer in contours_layers:
        contours = doc.modelspace().query(f'LWPOLYLINE[layer=="{layer}"]')
        for contour in contours:
            shape = Polygon([(float(x), float(y)) for x, y in list(contour.vertices())])
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
            close_numbers = distances[distances < max_distance]

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

    # Сбор итоговой таблицы с разделенными номерами
    topographic_plan_data = []

    for number_id in trees_df['number_id']:
        for _split_number in split_number(numbers_df.iloc[number_id]['number']):
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

        for _split_number in split_number(numbers_df.iloc[number_id]['number']):
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

    return topographic_plan

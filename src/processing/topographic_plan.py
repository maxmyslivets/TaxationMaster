from pathlib import Path

import ezdxf
import pandas as pd
from ezdxf.entities import MText
from shapely import LineString, Polygon, Point

from src.objects import TopographicPlan
from src.processing.splitting_numbers import split_number


def create_topographic_plan(dxf_path: Path, numbers_layers: list[str],
                            lines_layers: list[str], contours_layers: list[str],
                            min_distance: float) -> TopographicPlan | None:
    valid = True
    doc = ezdxf.readfile(dxf_path)
    topographical_plan = TopographicPlan()

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

    topographical_plan._numbers_df = pd.DataFrame(numbers_data)
    if not topographical_plan._numbers_df.empty:
        topographical_plan._numbers_df.index.name = 'id'

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

    topographical_plan._shapes_df = pd.DataFrame(shapes_data)
    if not topographical_plan._shapes_df.empty:
        topographical_plan._shapes_df.index.name = 'id'

    # Связывание номеров и фигур
    numbers_shapes_data = []
    if not topographical_plan._numbers_df.empty and not topographical_plan._shapes_df.empty:
        # Создаем геометрические точки для всех номеров
        number_points = topographical_plan._numbers_df.apply(lambda row: row['position'], axis=1)

        # Для каждой фигуры проверяем все номера
        for shape_id, shape_row in topographical_plan._shapes_df.iterrows():
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

    topographical_plan._numbers_shapes_df = pd.DataFrame(numbers_shapes_data)

    # # Валидация
    # if not topographical_plan.numbers_shapes_df.empty:
    #     duplicates = (topographical_plan.numbers_shapes_df.groupby('number_id')
    #                   .size()
    #                   .reset_index(name='count')
    #                   .query('count > 1'))
    #
    #     if not duplicates.empty:
    #         valid = False
    #         for _, row in duplicates.iterrows():
    #             number = topographical_plan.numbers_df.loc[row['number_id'], 'number']
    #             print(f"[ERROR]\tНомер `{number}` встречается в чертеже на {row['count']} фигурах.")

    # Сбор деревьев (точечных объектов)
    if not topographical_plan._numbers_df.empty and not topographical_plan._numbers_shapes_df.empty:
        unassigned_numbers = topographical_plan._numbers_df.index.difference(
            topographical_plan._numbers_shapes_df['number_id'])

        trees_data = []
        for number_id in unassigned_numbers:
            trees_data.append({
                'number_id': number_id
            })

        topographical_plan._trees_df = pd.DataFrame(trees_data)

    # # Разделение номеров
    # splitted_numbers = []
    # for _, row in topographical_plan.numbers_df.iterrows():
    #     items = [item.strip() for item in row['number'].split(",")]
    #     for number in items:
    #         splitted_numbers_list = split_number(number)
    #         if splitted_numbers_list:
    #             for splitted_number in splitted_numbers_list:
    #                 splitted_numbers.append({
    #                     'splitted_number': splitted_number,
    #                     'original_number': row['number'],
    #                     'is_bug': False
    #                 })
    #         else:
    #             splitted_numbers.append({
    #                 'splitted_number': number,
    #                 'original_number': row['number'],
    #                 'is_bug': True
    #             })
    #
    # topographical_plan.splitted_numbers_df = pd.DataFrame(splitted_numbers)
    #
    # if not valid:
    #     print("[ERROR]\tЧертеж таксации содержит ошибки и не будет обработан.")
    #     return None
    #
    # # Формирование итоговой таблицы
    # table_data = []
    # processed_numbers = set()  # Для отслеживания уже обработанных номеров
    #
    # for _, row in topographical_plan.splitted_numbers_df.iterrows():
    #     splitted_number = row['splitted_number']
    #
    #     # Пропускаем, если номер уже обработан
    #     if splitted_number in processed_numbers:
    #         continue
    #
    #     base_data = {
    #         'splitted_number': splitted_number,
    #         'number': row['original_number']
    #     }
    #
    #     # Находим связанные фигуры для данного номера
    #     if not topographical_plan.numbers_shapes_df.empty:
    #         number_shapes = topographical_plan.numbers_shapes_df.merge(
    #             topographical_plan.shapes_df,
    #             on='shape_id'
    #         )
    #         shape_data = number_shapes[
    #             number_shapes['number_id'].astype(str) == str(row['original_number'])
    #             ]
    #
    #         if not shape_data.empty:
    #             # Берем первую найденную фигуру
    #             shape = shape_data.iloc[0]
    #             if shape['type'] == 'LineString':
    #                 table_data.append({
    #                     **base_data,
    #                     'type_shape': 'Полоса',
    #                     'value': str(round(shape['geometry'].length, 1)),
    #                     'unit': 'м.п.'
    #                 })
    #             else:
    #                 table_data.append({
    #                     **base_data,
    #                     'type_shape': 'Контур',
    #                     'value': str(round(shape['geometry'].area, 1)),
    #                     'unit': 'м2'
    #                 })
    #             processed_numbers.add(split_number)
    #             continue
    #
    #     # Если нет связанных фигур, значит это дерево
    #     if split_number not in processed_numbers:
    #         table_data.append({
    #             **base_data,
    #             'type_shape': 'Дерево',
    #             'value': '-',
    #             'unit': 'шт.'
    #         })
    #         processed_numbers.add(split_number)
    #
    # # Создаем DataFrame без использования drop_duplicates
    # topographical_plan.table_data = pd.DataFrame(table_data)

    return topographical_plan

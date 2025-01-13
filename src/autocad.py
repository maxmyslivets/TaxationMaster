import pandas as pd
from pyautocad import Autocad
from pyautocad.utils import mtext_to_string
from shapely import Point, LineString, Polygon
from shapely.geometry.multipolygon import MultiPolygon


from src.parsing import Splitter


class AutocadWorker:
    """Набор методов для работы с Autocad"""

    @staticmethod
    def get_numbers(layer: str) -> list[str]:
        """
        Получить список номеров из текстовых объектов указанного слоя Autocad

        Args:
            layer (str): Имя слоя Autocad

        Returns:
            list[str]: Список номеров
        """
        acad = Autocad()
        numbers = []
        for obj in acad.iter_objects(['AcDbText', 'AcDbMText']):
            if obj.Layer == layer:
                numbers.append(obj.TextString)
        return numbers

    @staticmethod
    def get_df_topographic_plan(numbers_layers, lines_layers: list[str], contours_layers: list[str],
                                min_distance: float = 0.01, wkt_convert: bool = False) -> pd.DataFrame:
        """
        Получить датафрейм таксационных данных из чертежа Autocad

        Args:
            numbers_layers (list[str]): Имена слоёв, содержащих объекты номеров
            lines_layers (list[str]): Имена слоёв, содержащих объекты полос растительности
            contours_layers (list[str]): Имена слоёв, содержащих объекты контуров растительности
            min_distance (float): буфер для привязки номеров к линейным объектам
            wkt_convert (bool): Преобразование геометрии в wkt

        Returns:
            pd.DataFrame: Датафрейм таксационных данных
        """
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
                        'Номер точки': numbers_df.iloc[number_id]['number'],
                        'Разделенный номер': _split_number,
                        'Позиция номера': numbers_df.iloc[number_id]['position'],
                        'Геометрия': numbers_df.iloc[number_id]['position'],
                        'Размер': None
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
                        'Номер точки': numbers_df.iloc[number_id]['number'],
                        'Разделенный номер': _split_number,
                        'Позиция номера': numbers_df.iloc[number_id]['position'],
                        'Геометрия': shape,
                        'Размер': shape.length if isinstance(shape, LineString) else shape.area
                    }
                )

        topographic_plan = pd.DataFrame(topographic_plan_data)
        topographic_plan.drop_duplicates(subset=['Разделенный номер', 'Геометрия'], keep='last',
                                         inplace=True, ignore_index=True)

        if not wkt_convert:
            return topographic_plan
        else:
            topographic_plan['Позиция номера'] = topographic_plan['Позиция номера'].apply(
                lambda geom: geom.wkt if geom else None)
            topographic_plan['Геометрия'] = topographic_plan['Геометрия'].apply(lambda geom: geom.wkt if geom else None)
            return topographic_plan

    @staticmethod
    def get_df_zones(zones_layers: list[str], min_distance: float = 0.01, wkt_convert: bool = False) -> pd.DataFrame:
        """
        Получить датафрейм зон из чертежа Autocad

        Args:
            zones_layers (list[str]): Имена слоёв, содержащих границы зон
            min_distance (float): буфер для привязки названия к полигону
            wkt_convert (bool): Преобразование геометрии в wkt

        Returns:
            pd.DataFrame: Датафрейм названий и геометрии зон
        """
        acad = Autocad()

        names_data = []
        for obj in acad.iter_objects(['AcDbText', 'AcDbMText']):
            if obj.ObjectName == 'AcDbText' and obj.Layer in zones_layers:
                x, y, _ = obj.InsertionPoint
                names_data.append((obj.TextString, Point(x, y)))
            elif obj.ObjectName == 'AcDbMText' and obj.Layer in zones_layers:
                x, y, _ = obj.InsertionPoint
                names_data.append((mtext_to_string(obj.TextString).replace('\n', ' '), Point(x, y)))

        zones_shapes_data = []
        for obj in acad.iter_objects('AcDbPolyline'):
            if obj.Layer in zones_layers:
                acad_polygon_vertexes = [vertex for vertex in obj.Coordinates]
                shape = Polygon(
                    [(acad_polygon_vertexes[i], acad_polygon_vertexes[i + 1])
                     for i in range(0, len(acad_polygon_vertexes), 2)])
                zones_shapes_data.append(shape)

        zones_data = {name: [] for name, shape in names_data}
        for shape in zones_shapes_data:
            for name, point in names_data:
                if point.distance(shape.exterior) < min_distance:
                    zones_data[name].append(shape)

        zones = {}

        for name, shapes in zones_data.items():
            zones[name] = MultiPolygon(shapes) if len(shapes) > 1 else shapes[0]

        zones_for_df = []

        for name, geometry in zones.items():
            if name + '_' in list(zones.keys()):
                zones[name] = geometry.difference(zones[name + '_'])
            if not name.endswith('_'):
                zones_for_df.append({'Наименование': name, 'Геометрия': zones[name]})

        zones_df = pd.DataFrame(zones_for_df)

        if not wkt_convert:
            return zones_df
        else:
            zones_df['Геометрия'] = zones_df['Геометрия'].apply(lambda geom: geom.wkt if geom else None)
            return zones_df

    @staticmethod
    def get_df_protection_zones(zones_layers: list[str], wkt_convert: bool = False) -> (
            pd.DataFrame):
        """
        Получить датафрейм охранных зон из чертежа Autocad

        Args:
            zones_layers (list[str]): Имена слоёв, содержащих границы зон
            wkt_convert (bool): Преобразование геометрии в wkt

        Returns:
            pd.DataFrame: Датафрейм геометрии зон
        """
        acad = Autocad()

        zones_shapes_data = []
        for obj in acad.iter_objects('AcDbPolyline'):
            if obj.Layer in zones_layers:
                acad_polygon_vertexes = [vertex for vertex in obj.Coordinates]
                shape = Polygon(
                    [(acad_polygon_vertexes[i], acad_polygon_vertexes[i + 1])
                     for i in range(0, len(acad_polygon_vertexes), 2)])
                zones_shapes_data.append({"Геометрия": shape})

        zones_df = pd.DataFrame(zones_shapes_data)

        if not wkt_convert:
            return zones_df
        else:
            zones_df['Геометрия'] = zones_df['Геометрия'].apply(lambda geom: geom.wkt if geom else None)
            return zones_df

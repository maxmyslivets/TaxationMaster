import ezdxf
import pandas as pd
from ezdxf.addons import Importer
from ezdxf.math import Vec2
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
                                min_distance: float = 0.01, wkt_convert: bool = False, app=None) -> pd.DataFrame:
        """
        Получить датафрейм таксационных данных из чертежа Autocad

        Args:
            numbers_layers (list[str]): Имена слоёв, содержащих объекты номеров
            lines_layers (list[str]): Имена слоёв, содержащих объекты полос растительности
            contours_layers (list[str]): Имена слоёв, содержащих объекты контуров растительности
            min_distance (float): буфер для привязки номеров к линейным объектам
            wkt_convert (bool): Преобразование геометрии в wkt
            app: Прогресс бар

        Returns:
            pd.DataFrame: Датафрейм таксационных данных
        """
        acad = Autocad()
        numbers_data = []

        progress_1 = app.progress_manager.new("Получение датафрейма", 100)
        progress_2 = app.progress_manager.new("Чтение текстовых объектов Autocad", len(list(acad.iter_objects(['AcDbText', 'AcDbMText']))))

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
            progress_2.next()

        numbers_df = pd.DataFrame(numbers_data)

        progress_1.set_value(15)
        progress_2 = app.progress_manager.new("Чтение линейных объектов Autocad", len(list(acad.iter_objects(['AcDbLine', 'AcDbPolyline', 'AcDbPolygon']))))
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
            progress_2.next()

        shapes_df = pd.DataFrame(shapes_data)
        progress_1.set_value(30)

        # Связывание номеров и фигур
        numbers_shapes_data = []
        if not numbers_df.empty and not shapes_df.empty:
            # Создаем геометрические точки для всех номеров
            number_points = numbers_df.apply(lambda row: row['position'], axis=1)

            progress_2 = app.progress_manager.new("Связывание номеров и фигур", len(shapes_df))
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
                progress_2.next()

        numbers_shapes_df = pd.DataFrame(numbers_shapes_data)
        progress_1.set_value(45)

        # Сбор деревьев (точечных объектов)
        unassigned_numbers = numbers_df.index.difference(numbers_shapes_df['number_id'])

        trees_data = []
        for number_id in unassigned_numbers:
            trees_data.append({
                'number_id': number_id
            })

        trees_df = pd.DataFrame(trees_data)
        progress_1.set_value(60)

        topographic_plan_data = []
        progress_2 = app.progress_manager.new("Фильтрация точечных объектов", len(trees_df['number_id']))
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
            progress_2.next()

        progress_1.set_value(75)

        progress_2 = app.progress_manager.new("Сбор итогового датафрейма", len(numbers_shapes_df.index))
        for numbers_shapes_id in numbers_shapes_df.index:

            number_id = numbers_shapes_df.iloc[numbers_shapes_id]['number_id']
            shape_id = numbers_shapes_df.iloc[numbers_shapes_id]['shape_id']
            shape: LineString | Polygon = shapes_df.iloc[shape_id]['geometry']
            # shape_type = shapes_df.iloc[shape_id]['type']

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
            progress_2.next()

        topographic_plan = pd.DataFrame(topographic_plan_data)
        topographic_plan.drop_duplicates(subset=['Разделенный номер', 'Геометрия'], keep='last',
                                         inplace=True, ignore_index=True)
        progress_1.set_value(100)

        if not wkt_convert:
            return topographic_plan
        else:
            topographic_plan['Позиция номера'] = topographic_plan['Позиция номера'].apply(
                lambda geom: geom.wkt if geom else None)
            topographic_plan['Геометрия'] = topographic_plan['Геометрия'].apply(lambda geom: geom.wkt if geom else None)
            return topographic_plan

    @staticmethod
    def get_df_zones(zones_layers: list[str], min_distance: float = 0.01, wkt_convert: bool = False,
                     app=None) -> pd.DataFrame:
        """
        Получить датафрейм зон из чертежа Autocad

        Args:
            zones_layers (list[str]): Имена слоёв, содержащих границы зон
            min_distance (float): буфер для привязки названия к полигону
            wkt_convert (bool): Преобразование геометрии в wkt
            progress (Progress): Прогресс бар

        Returns:
            pd.DataFrame: Датафрейм названий и геометрии зон
        """
        acad = Autocad()
        progress_1 = app.progress_manager.new("Получение датафрейма", 100)
        progress_2 = app.progress_manager.new("Чтение текстовых объектов Autocad", len(list(acad.iter_objects(['AcDbText', 'AcDbMText']))))

        names_data = []
        for obj in acad.iter_objects(['AcDbText', 'AcDbMText']):
            if obj.ObjectName == 'AcDbText' and obj.Layer in zones_layers:
                x, y, _ = obj.InsertionPoint
                names_data.append((obj.TextString, Point(x, y)))
            elif obj.ObjectName == 'AcDbMText' and obj.Layer in zones_layers:
                x, y, _ = obj.InsertionPoint
                names_data.append((mtext_to_string(obj.TextString).replace('\n', ' '), Point(x, y)))
            progress_2.next()

        progress_1.set_value(20)
        progress_2 = app.progress_manager.new("Чтение линейных объектов Autocad", len(list(acad.iter_objects('AcDbPolyline'))))

        zones_shapes_data = []
        for obj in acad.iter_objects('AcDbPolyline'):
            if obj.Layer in zones_layers:
                acad_polygon_vertexes = [vertex for vertex in obj.Coordinates]
                shape = Polygon(
                    [(acad_polygon_vertexes[i], acad_polygon_vertexes[i + 1])
                     for i in range(0, len(acad_polygon_vertexes), 2)])
                zones_shapes_data.append(shape)
            progress_2.next()

        progress_1.set_value(40)
        progress_2 = app.progress_manager.new("Определение названий зон", len(zones_shapes_data))

        zones_data = {name: [] for name, shape in names_data}
        for shape in zones_shapes_data:
            for name, point in names_data:
                if point.distance(shape.exterior) < min_distance:
                    zones_data[name].append(shape)
            progress_2.next()

        progress_1.set_value(60)
        progress_2 = app.progress_manager.new("Объединение одноименных зон", len(zones_data))

        zones = {}
        for name, shapes in zones_data.items():
            zones[name] = MultiPolygon(shapes) if len(shapes) > 1 else shapes[0]
            progress_2.next()

        progress_1.set_value(80)
        progress_2 = app.progress_manager.new("Вычитание внутренних полигонов", len(zones))

        zones_for_df = []
        for name, geometry in zones.items():
            if name + '_' in list(zones.keys()):
                zones[name] = geometry.difference(zones[name + '_'])
            if not name.endswith('_'):
                zones_for_df.append({'Наименование': name, 'Геометрия': zones[name]})
            progress_2.next()

        zones_df = pd.DataFrame(zones_for_df)
        progress_1.set_value(100)

        if not wkt_convert:
            return zones_df
        else:
            zones_df['Геометрия'] = zones_df['Геометрия'].apply(lambda geom: geom.wkt if geom else None)
            return zones_df

    @staticmethod
    def get_df_protection_zones(zones_layers: list[str], wkt_convert: bool = False, app=None) -> pd.DataFrame:
        """
        Получить датафрейм охранных зон из чертежа Autocad

        Args:
            zones_layers (list[str]): Имена слоёв, содержащих границы зон
            wkt_convert (bool): Преобразование геометрии в wkt
            app: Прогресс бар

        Returns:
            pd.DataFrame: Датафрейм геометрии зон
        """
        acad = Autocad()
        progress = app.progress_manager.new("Получение линейных объектов Autocad", len(list(acad.iter_objects('AcDbPolyline'))))

        zones_shapes_data = []
        for obj in acad.iter_objects('AcDbPolyline'):
            if obj.Layer in zones_layers:
                acad_polygon_vertexes = [vertex for vertex in obj.Coordinates]
                shape = Polygon(
                    [(acad_polygon_vertexes[i], acad_polygon_vertexes[i + 1])
                     for i in range(0, len(acad_polygon_vertexes), 2)])
                zones_shapes_data.append({"Геометрия": shape})
            progress.next()

        zones_df = pd.DataFrame(zones_shapes_data)

        if not wkt_convert:
            return zones_df
        else:
            zones_df['Геометрия'] = zones_df['Геометрия'].apply(lambda geom: geom.wkt if geom else None)
            return zones_df

    @staticmethod
    def insert_numbers_to_dxf(data: pd.DataFrame, dxf_template_path: str, dxf_output_path: str, app=None) -> None:
        """
        Вставить номера в чертеж DXF
        Args:
            data:
            dxf_template_path:
            dxf_output_path:
            app:

        Returns:

        """
        # TODO: Для полос и ?контуров? штриховка
        layer_name_taxation_removable = 'Таксация_деревья(удаляемые)'
        layer_name_taxation_transplantable = 'Таксация_деревья(пересаживаемые)'
        layer_name_leader_removable = 'Таксация_номера(удаляемые)'
        layer_name_leader_transplantable = 'Таксация_номера(пересаживаемые)'
        block_scale = 0.004
        dxfattribs_block = {'xscale': block_scale,
                            'yscale': block_scale}
        mtext_segment = Vec2.from_deg_angle(45, 3)
        block_name_removable = 'taxation_removable'
        block_name_transplantable = 'taxation_transplantable'

        dxf_source = ezdxf.readfile(dxf_template_path)
        dxf_new = ezdxf.new(dxfversion='R2013', setup=True, units=6)
        msp = dxf_new.modelspace()

        importer = Importer(dxf_source, dxf_new)
        importer.import_block(block_name_removable)
        importer.import_block(block_name_transplantable)
        importer.finalize()

        progress = app.progress_manager.new("Вставка номеров в DXF", len(data))

        for _, series in data.iterrows():
            insert_point = Vec2(series['Позиция номера'].x, series['Позиция номера'].y)
            text_number = series['Номер']

            action = series['Действие']
            if action == 'Удаление':
                dxfattribs_block['layer'] = layer_name_taxation_removable
                layer = layer_name_leader_removable
                block_name = block_name_removable
            elif action == 'Пересадка':
                dxfattribs_block['layer'] = layer_name_taxation_transplantable
                layer = layer_name_leader_transplantable
                block_name = block_name_transplantable
            else:
                raise ValueError(f"Номер {text_number} - неизвестное действие '{action}'")

            msp.add_blockref(block_name, insert_point, dxfattribs=dxfattribs_block)
            ml_builder = msp.add_multileader_mtext(style='Standard', dxfattribs={'layer': layer})
            ml_builder.quick_leader(text_number, insert_point, mtext_segment)

            progress.next()

        dxf_new.saveas(dxf_output_path)

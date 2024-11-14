import re
import traceback
from collections import Counter
from itertools import combinations

import ezdxf
from PySide6 import QtCore
from ezdxf.entities import Text, MText, Line, LWPolyline
from shapely import MultiPolygon
from shapely.geometry import Point, LineString, Polygon

from source.model.project import Project


class Processing(QtCore.QObject):

    def __init__(self, project: Project, log):
        super(Processing, self).__init__()

        self.log = log
        self.project = project

        self.valid = True

    def read_data_from_taxation_plan(self, numbers_layers: list[str], lines_layers: list[str],
                                     contours_layers: list[str], zones_layers: list[str], min_distance: float,
                                     min_area: float) -> None:
        """
        Чтение файла dxf чертежа таксации и структурирование данных.
        """

        self.clear_data_for_autocad_data_structuring()
        self.valid = True

        try:
            entity_numbers, entity_lines, entity_contours, entity_zones = [], [], [], []

            doc = ezdxf.readfile(self.project.path_dxf)

            for entity in doc.modelspace():

                if isinstance(entity, Text) and entity.dxf.layer in numbers_layers:
                    entity_numbers.append(entity)
                elif isinstance(entity, MText) and entity.dxf.layer in numbers_layers:
                    entity_numbers.append(entity)

                elif isinstance(entity, LWPolyline) and entity.dxf.layer in lines_layers:
                    entity_lines.append(entity)
                elif isinstance(entity, Line) and entity.dxf.layer in lines_layers:
                    entity_lines.append(entity)

                elif isinstance(entity, LWPolyline) and entity.dxf.layer in contours_layers:
                    entity_contours.append(entity)

                elif isinstance(entity, LWPolyline) and entity.dxf.layer in zones_layers:
                    entity_zones.append(entity)
                elif isinstance(entity, MText) and entity.dxf.layer in zones_layers:
                    entity_zones.append(entity)
                elif isinstance(entity, Text) and entity.dxf.layer in zones_layers:
                    entity_zones.append(entity)

        except Exception:
            self.log(f"Ошибка чтения данных из чертежа."
                     f"\n{traceback.format_exc()}")
            return

        # Собираем self.numbers и self.number_positions

        for k_number, text in enumerate(entity_numbers):
            number = text.plain_text().replace('\n', ' ') if isinstance(text, MText) else text.plain_text()
            self.project.numbers[k_number] = number
            position = Point(text.dxf.insert[0], text.dxf.insert[1])
            self.project.numbers_position[k_number] = position

        # Собираем self.shapes

        k_shape = 0
        for line in entity_lines:
            if isinstance(line, LWPolyline):
                shape = LineString([(float(x), float(y)) for x, y in list(line.vertices())])
                self.project.shapes[k_shape] = shape
                k_shape += 1
            if isinstance(line, Line):
                shape = LineString([(line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y)])
                self.project.shapes[k_shape] = shape
                k_shape += 1
        for contour in entity_contours:
            shape = Polygon([(float(x), float(y)) for x, y in list(contour.vertices())])
            self.project.shapes[k_shape] = shape
            k_shape += 1

        # Собираем self.numbers_from_shape

        for k_number, k_position in self.project.numbers_position.items():
            for k_shape, shape in self.project.shapes.items():
                if isinstance(shape, LineString):
                    distance = shape.distance(k_position)
                elif isinstance(shape, Polygon):
                    distance = k_position.distance(shape.exterior)
                else:
                    self.log(f"[WARNING]\tТип фигуры {type(shape)} не является LineString или Polygon.")
                    continue
                if distance < min_distance:
                    if k_shape not in self.project.numbers_from_shape:
                        self.project.numbers_from_shape[k_shape] = list()
                    self.project.numbers_from_shape[k_shape].append(k_number)

        # Валидация на наличие одинаковых номеров на разных фигурах
        shapes_validation_dict = dict()
        for k_shape, k_number_list in self.project.numbers_from_shape.items():
            for k_number in k_number_list:
                if self.project.numbers[k_number] not in shapes_validation_dict:
                    shapes_validation_dict[self.project.numbers[k_number]] = list()
                shapes_validation_dict[self.project.numbers[k_number]].append(k_shape)
        for number, k_shape_list in shapes_validation_dict.items():
            if len(set(k_shape_list)) > 1:
                self.valid = False
                self.log(f"[ERROR]\tНомер `{number}` встречается в чертеже на {len(k_shape_list)} фигурах.")

        # Собираем self.zone_shapes

        k_zone = 0
        for entity in entity_zones:
            if isinstance(entity, LWPolyline):
                self.project.zone_shapes[k_zone] = Polygon([(float(x), float(y)) for x, y in list(entity.vertices())])
                k_zone += 1
            elif isinstance(entity, Text) or isinstance(entity, MText):
                continue
            else:
                self.log(f"[WARNING]\tТип фигуры {type(entity)} не является LWPolyline, Text или MText.")

        # Собираем self.zone_names и self.zones_from_zone_names

        k_zone_name = 0
        zone_names_temp_list = []
        for entity in entity_zones:
            if isinstance(entity, Text) or isinstance(entity, MText):
                zone_name = entity.plain_text()
                if zone_name not in zone_names_temp_list:
                    self.project.zone_names[k_zone_name] = zone_name
                    zone_names_temp_list.append(zone_name)
                    k_zone_name += 1
                zone_name_position = Point(entity.dxf.insert[0], entity.dxf.insert[1])
                for k_zone, shape in self.project.zone_shapes.items():
                    if zone_name_position.distance(shape.exterior) < min_distance:
                        _k_zone_name = next(k for k, v in self.project.zone_names.items() if v == zone_name)
                        if _k_zone_name not in self.project.zones_from_zone_names:
                            self.project.zones_from_zone_names[_k_zone_name] = list()
                        self.project.zones_from_zone_names[_k_zone_name].append(k_zone)
            elif isinstance(entity, LWPolyline):
                continue
            else:
                self.log(f"[WARNING]\tТип фигуры {type(entity)} не является LWPolyline, Text или MText.")

        # Валидация перекрытия зон
        pairs_k_zone_names_validation = list(combinations(self.project.zone_names.keys(), 2))
        for k_zone_name_1, k_zone_name_2 in pairs_k_zone_names_validation:
            k_zone_shape_list_1 = self.project.zones_from_zone_names[k_zone_name_1]
            k_zone_shape_list_2 = self.project.zones_from_zone_names[k_zone_name_2]
            zone_shapes_1_list = [self.project.zone_shapes[k] for k in [k for k in k_zone_shape_list_1]]
            zone_shapes_2_list = [self.project.zone_shapes[k] for k in [k for k in k_zone_shape_list_2]]
            zone_1 = MultiPolygon([polygon for polygon in zone_shapes_1_list])
            zone_2 = MultiPolygon([polygon for polygon in zone_shapes_2_list])

            if zone_1.intersection(zone_2).area > min_area:
                self.valid = False
                self.log(f"[ERROR]\tЗоны `{self.project.zone_names[k_zone_name_1]}` и "
                         f"`{self.project.zone_names[k_zone_name_2]}` перекрываются на "
                         f"{round(zone_1.intersection(zone_2).area, 2)} м2.")

        # Собираем self.tree и self.numbers_from_tree

        shape_numbers_temp_list = []
        for k_shape, k_number_list in self.project.numbers_from_shape.items():
            shape_numbers_temp_list.extend(k_number_list)

        numbers_from_tree_validation = []  # список номеров для валидации
        k_tree = 0
        for k_number, number_position in self.project.numbers_position.items():
            if k_number not in shape_numbers_temp_list:
                self.project.tree[k_tree] = number_position
                self.project.numbers_from_tree[k_tree] = k_number
                numbers_from_tree_validation.append(self.project.numbers[k_number])
                k_tree += 1

        # Валидация на наличие одинаковых номеров для точечных объектов растительности
        counter_number_of_tree = Counter(numbers_from_tree_validation)
        for number, count in counter_number_of_tree.items():
            if count > 1:
                self.valid = False
                self.log(f"[ERROR]\tНомер точечного объекта растительности `{number}` встречается в чертеже "
                         f"{count} раз(а).")

        # Валидация на наличие одинаковых номеров у объектов растительности относительно фигур
        for number in list(set(shapes_validation_dict.keys()) & set(numbers_from_tree_validation)):
            self.valid = False
            self.log(f"[ERROR]\tНомер `{number}` встречается в чертеже и на точечном объекте растительности "
                     f"и на фигуре")

        if not self.valid:
            self.log(f"[ERROR]\tЧертеж таксации содержит ошибки и не будет обработан. "
                     f"Исправьте файл чертежа таксации и импортируйте его заново.")
            self.clear_data_for_autocad_data_structuring()

    def clear_data_for_autocad_data_structuring(self) -> None:
        """Очистка данных при повторном вызове метода autocad_data_structuring"""

        del self.project.numbers
        del self.project.numbers_position
        del self.project.shapes
        del self.project.numbers_from_shape
        del self.project.zone_shapes
        del self.project.zone_names
        del self.project.zones_from_zone_names
        del self.project.tree
        del self.project.numbers_from_tree
        del self.project.split_numbers
        del self.project.number_from_split_number
        del self.project.intersects_shapes_in_zones

    def splitting_numbers(self) -> None:
        """
        Разделение составных номеров.
        """

        del self.project.split_numbers
        del self.project.number_from_split_number
        del self.project.intersects_shapes_in_zones

        if not self.valid:
            return

        k_split_number = -1
        split_numbers_temp_list = []
        for k_number, source_number in self.project.numbers.items():
            items = [item.strip() for item in source_number.split(",")]
            for number in items:

                if number in split_numbers_temp_list:
                    exist_k_split_number = next(k for k, v in self.project.split_numbers.items() if v == number)
                    self.project.number_from_split_number[exist_k_split_number].append(k_number)
                    continue

                # Извлечение простых чисел
                if re.match(r'^\d+$', number):
                    k_split_number += 1
                    self.project.split_numbers[k_split_number] = number
                    self.project.number_from_split_number[k_split_number] = [k_number]
                    split_numbers_temp_list.append(number)

                # Обработка отдельных элементов с буквенным окончанием (например, "8г")
                elif re.match(r'^\d+[а-я]$', number):
                    k_split_number += 1
                    self.project.split_numbers[k_split_number] = number
                    self.project.number_from_split_number[k_split_number] = [k_number]

                # Извлечение диапазона чисел с разделителем "-"
                elif re.match(r'^\d+-\d+$', number):
                    start, end = map(int, number.split('-'))
                    result = [str(i) for i in range(start, end + 1)]
                    for new_number in result:
                        k_split_number += 1
                        self.project.split_numbers[k_split_number] = new_number
                        if k_split_number not in self.project.number_from_split_number:
                            self.project.number_from_split_number[k_split_number] = []
                        self.project.number_from_split_number[k_split_number].append(k_number)
                    split_numbers_temp_list.append(number)

                # Извлечение диапазона чисел с буквенным окончанием
                elif re.match(r'^\d+[а-я]-[а-я]$', number):
                    num = re.match(r'\d+', number).group()
                    start_letter, end_letter = re.findall(r'[а-я]', number)
                    result = [f"{num}{chr(i)}" for i in range(ord(start_letter), ord(end_letter) + 1)]
                    for new_number in result:
                        k_split_number += 1
                        self.project.split_numbers[k_split_number] = new_number
                        if k_split_number not in self.project.number_from_split_number:
                            self.project.number_from_split_number[k_split_number] = []
                        self.project.number_from_split_number[k_split_number].append(k_number)
                    split_numbers_temp_list.append(number)

                # Все остальные непредусмотренные случаи
                else:
                    # TODO: Предусмотреть изменение через графический интерфейс
                    self.log(f"[WARNING]\tНе удалось подобрать регулярное выражения для номера `{number}`."
                             f"Предлагается ввести значения вручную через табличную форму.")

    def calculate_intersects_shapes_in_zones(self) -> None:
        """
        Вычисление вхождений фигур и точечных объектов растительности в зоны
        """
        # TODO: Добавить вычисление площадей и длин линий для объектов на каждой зоне отдельно
        for k_zone, zone_shape in self.project.zone_shapes.items():
            for k_split_number, _ in self.project.split_numbers.items():
                k_number_list = self.project.number_from_split_number[k_split_number]
                for k_number in k_number_list:
                    try:
                        k_tree = next(k for k, v in self.project.numbers_from_tree.items() if v == k_number)
                    except StopIteration:
                        k_tree = None
                    if k_tree is not None and zone_shape.contains(self.project.tree[k_tree]):
                        # Не добавление в список, а замена, т.к. точечный объект должен находиться только в одной зоне
                        self.project.intersects_shapes_in_zones[k_split_number] = [k_zone]
                    try:
                        k_shape = next(k for k, v in self.project.numbers_from_shape.items() if k_number in v)
                    except StopIteration:
                        k_shape = None
                    if k_shape is not None and zone_shape.intersects(self.project.shapes[k_shape]):
                        if k_split_number not in self.project.intersects_shapes_in_zones:
                            self.project.intersects_shapes_in_zones[k_split_number] = []
                        self.project.intersects_shapes_in_zones[k_split_number].append(k_zone)

        for k in self.project.intersects_shapes_in_zones.keys():
            self.project.intersects_shapes_in_zones[k] = list(set(self.project.intersects_shapes_in_zones[k]))

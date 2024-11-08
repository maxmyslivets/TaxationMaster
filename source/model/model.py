import re
from pathlib import Path

from PySide6 import QtCore
from ezdxf.entities import Text, MText, Line, LWPolyline
from shapely.geometry import Point, LineString, Polygon

from processing.autocad import extract_data_from_taxation_plan


class Model(QtCore.QObject):

    def __init__(self, log):
        super(Model, self).__init__()

        self.log = log

        self.taxation_plan_entity_objects = {
            "номера": list(),
            "полосы": list(),
            "контуры": list(),
            "зоны": list()
        }

        self.MIN_DISTANCE = 0.01    # TODO: вынести в настройки

        self.numbers = dict()                   # key: k_number     value: number
        self.numbers_position = dict()          # key: k_number     value: position
        self.shapes = dict()                    # key: k_shape      value: shape
        self.numbers_from_shape = dict()        # key: k_shape      value: list[k_number]
        self.zone_shapes = dict()               # key: k_zone       value: shape
        self.zone_names = dict()                # key: k_zone_name  value: zone_name
        self.zones_from_zone_names = dict()     # key: k_zone_name  value: list[k_zone]
        self.tree = dict()                      # key: k_tree       value: position
        self.numbers_from_tree = dict()         # key: k_tree       value: k_number

        self.split_numbers = dict()             # key: k_split_number     value: split_number
        self.number_from_split_number = dict()  # key: k_split_number     value: list[k_number]

    def read_taxation_plan(self, taxation_plan_path: Path) -> None:
        """
        Чтение данных из dxf чертежа таксации.
        :param taxation_plan_path: Путь до dxf чертежа
        :return:
        """
        try:
            numbers, lines, contours, zones = extract_data_from_taxation_plan(taxation_plan_path)
        except Exception as e:
            self.log(f"Ошибка чтения данных из чертежа: {e}")
            return
        self.taxation_plan_entity_objects["номера"] = numbers
        self.taxation_plan_entity_objects["полосы"] = lines
        self.taxation_plan_entity_objects["контуры"] = contours
        self.taxation_plan_entity_objects["зоны"] = zones

    def autocad_data_structuring(self) -> None:
        """
        Структурирование данных из объектов autocad в словари.
        """

        # Собираем self.numbers и self.number_positions

        for k_number, text in enumerate(self.taxation_plan_entity_objects["номера"]):
            number = text.plain_text().replace('\n', ' ') if isinstance(text, MText) else text.plain_text()
            self.numbers[k_number] = number
            position = Point(text.dxf.insert[0], text.dxf.insert[1])
            self.numbers_position[k_number] = position

        # Собираем self.shapes

        k_shape = 0
        for line in self.taxation_plan_entity_objects["полосы"]:
            if isinstance(line, LWPolyline):
                shape = LineString([(float(x), float(y)) for x, y in list(line.vertices())])
                self.shapes[k_shape] = shape
                k_shape += 1
            if isinstance(line, Line):
                shape = LineString([(line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y)])
                self.shapes[k_shape] = shape
                k_shape += 1
        for contour in self.taxation_plan_entity_objects["контуры"]:
            shape = Polygon([(float(x), float(y)) for x, y in list(contour.vertices())])
            self.shapes[k_shape] = shape
            k_shape += 1

        # Собираем self.numbers_from_shape

        for k_number, k_position in self.numbers_position.items():
            for k_shape, shape in self.shapes.items():
                if isinstance(shape, LineString):
                    distance = shape.distance(k_position)
                elif isinstance(shape, Polygon):
                    distance = k_position.distance(shape.exterior)
                else:
                    self.log(f"[WARNING]\tТип фигуры {type(shape)} не является LineString или Polygon.")
                    continue
                if distance < self.MIN_DISTANCE:
                    if k_shape not in self.numbers_from_shape:
                        self.numbers_from_shape[k_shape] = list()
                    self.numbers_from_shape[k_shape].append(k_number)

        # Собираем self.zone_shapes

        k_zone = 0
        for entity in self.taxation_plan_entity_objects["зоны"]:
            if isinstance(entity, LWPolyline):
                self.zone_shapes[k_zone] = Polygon([(float(x), float(y)) for x, y in list(entity.vertices())])
                k_zone += 1
            elif isinstance(entity, Text) or isinstance(entity, MText):
                continue
            else:
                self.log(f"[WARNING]\tТип фигуры {type(entity)} не является LWPolyline, Text или MText.")

        # Собираем self.zone_names и self.zones_from_zone_names

        k_zone_name = 0
        zone_names_temp_list = []
        for entity in self.taxation_plan_entity_objects["зоны"]:
            if isinstance(entity, Text) or isinstance(entity, MText):
                zone_name = entity.plain_text()
                if zone_name not in zone_names_temp_list:
                    self.zone_names[k_zone_name] = zone_name
                    zone_names_temp_list.append(zone_name)
                    k_zone_name += 1
                zone_name_position = Point(entity.dxf.insert[0], entity.dxf.insert[1])
                for k_zone, shape in self.zone_shapes.items():
                    if zone_name_position.distance(shape.exterior) < self.MIN_DISTANCE:
                        if k_zone_name not in self.zones_from_zone_names:
                            self.zones_from_zone_names[k_zone_name] = list()
                        self.zones_from_zone_names[k_zone_name].append(k_zone)
            elif isinstance(entity, LWPolyline):
                continue
            else:
                self.log(f"[WARNING]\tТип фигуры {type(entity)} не является LWPolyline, Text или MText.")

        # Собираем self.tree и self.numbers_from_tree

        shape_numbers_temp_list = []
        for k_shape, k_number_list in self.numbers_from_shape.items():
            shape_numbers_temp_list.extend(k_number_list)

        k_tree = 0
        for k_number, number_position in self.numbers_position.items():
            if k_number not in shape_numbers_temp_list:
                self.tree[k_tree] = number_position
                k_tree += 1
                self.numbers_from_tree[k_tree] = k_number

    def splitting_numbers(self) -> None:
        """
        Разделение составных номеров.
        """

        k_split_number = -1
        split_numbers_temp_list = []
        for k_number, number in self.numbers.items():
            if number in split_numbers_temp_list:
                exist_k_split_number = next(k for k, v in self.split_numbers.items() if v == number)
                self.number_from_split_number[exist_k_split_number].append(k_number)
                continue
            # Извлечение простых чисел
            if re.match('^[0-9]*$', number) is not None:
                k_split_number += 1
                self.split_numbers[k_split_number] = number
                self.number_from_split_number[k_split_number] = [k_number]
                split_numbers_temp_list.append(number)
            # Извлечение диапазона чисел с разделителем "-"
            elif re.match(r'\d+-\d+', number):
                start, end = map(int, number.split('-'))
                result = [str(i) for i in range(start, end + 1)]
                for new_number in result:
                    k_split_number += 1
                    self.split_numbers[k_split_number] = new_number
                    if k_split_number not in self.number_from_split_number:
                        self.number_from_split_number[k_split_number] = list()
                    self.number_from_split_number[k_split_number].append(k_number)
                split_numbers_temp_list.append(number)
            # Извлечение диапазона чисел с буквенным окончанием
            elif re.match(r'\d+[а-я]', number):
                num = re.match(r'\d+', number).group()
                start_letter, end_letter = re.findall(r'[а-я]', number)
                result = [f"{num}{chr(i)}" for i in range(ord(start_letter), ord(end_letter) + 1)]
                for new_number in result:
                    k_split_number += 1
                    self.split_numbers[k_split_number] = new_number
                    if k_split_number not in self.number_from_split_number:
                        self.number_from_split_number[k_split_number] = list()
                    self.number_from_split_number[k_split_number].append(k_number)
                split_numbers_temp_list.append(number)

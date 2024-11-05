from itertools import chain
from typing import Union
import ezdxf
from ezdxf.entities import Text, MText, Line, LWPolyline
from shapely.geometry import Point, LineString, Polygon
from pathlib import Path

from shapely.ops import unary_union


class TaxationObject:
    def __init__(self, number: str, shape: Union[Point, LineString, Polygon]):
        self.number = number
        self.shape = shape

    def __repr__(self) -> str:
        return f"TaxationObject({self.number}, {self.shape})"


class TaxationCollection:
    trees: list[TaxationObject]
    lines: list[TaxationObject]
    contours: list[TaxationObject]
    zones: list[TaxationObject]

    def __init__(self) -> None:
        self.trees = list()
        self.lines = list()
        self.contours = list()
        self.zones = list()

    def __repr__(self) -> str:
        return (f"TaxationCollection(Trees:{len(self.trees)}, Lines:{len(self.lines)}, Contours:{len(self.contours)}, "
                f"Zones:{len(self.zones)})")


def extract_data_from_taxation_plan(file_path: Path,
                                    numbers_layers: list[str] = ["номера"],
                                    lines_layers: list[str] = ["полосы"],
                                    contours_layers: list[str] = ["контуры"],
                                    zones_layers: list[str] = ["зоны"]) -> tuple[list, list, list, list]:
    """
    Извлечение данных из чертежа таксации
    :param file_path: путь к файлу
    :param numbers_layers: слои с номерами
    :param lines_layers: слои с линиями
    :param contours_layers: слои с контурами
    :param zones_layers: слои с зонами
    :return: список объектов
    """

    doc = ezdxf.readfile(file_path)

    numbers, lines, contours, zones = [], [], [], []

    for entity in doc.modelspace():

        if isinstance(entity, Text) and entity.dxf.layer in numbers_layers:
            numbers.append(entity)
        elif isinstance(entity, MText) and entity.dxf.layer in numbers_layers:
            numbers.append(entity)

        elif isinstance(entity, LWPolyline) and entity.dxf.layer in lines_layers:
            lines.append(entity)
        elif isinstance(entity, Line) and entity.dxf.layer in lines_layers:
            lines.append(entity)

        elif isinstance(entity, LWPolyline) and entity.dxf.layer in contours_layers:
            contours.append(entity)

        elif isinstance(entity, LWPolyline) and entity.dxf.layer in zones_layers:
            zones.append(entity)
        elif isinstance(entity, MText) and entity.dxf.layer in zones_layers:
            zones.append(entity)
        elif isinstance(entity, Text) and entity.dxf.layer in zones_layers:
            zones.append(entity)

    return numbers, lines, contours, zones


def correcting_data_from_taxation_plan(numbers: list, lines: list, contours: list, zones: list):
    """Метод для коррекции номеров"""

    taxation_collection_temp = TaxationCollection()
    taxation_collection = TaxationCollection()

    zone_names = []
    zones_temp = []
    for zone in zones:
        if isinstance(zone, LWPolyline):
            zones_temp.append(Polygon([(float(x), float(y)) for x, y in list(zone.vertices())]))
        if isinstance(zone, Text) or isinstance(zone, MText):
            number = zone.plain_text()
            x, y = zone.dxf.insert[0], zone.dxf.insert[1]
            zone_names.append(TaxationObject(number, Point(x, y)))
    zone_chunks = {}
    for zone_name in zone_names:
        if zone_name.number not in zone_chunks.keys():
            zone_chunks[zone_name.number] = []
        for polygon in zones_temp:
            if zone_name.shape.distance(polygon.exterior) < 0.01:
                zone_chunks[zone_name.number].append(polygon)
    for name, polygons in zone_chunks.items():
        taxation_collection.zones.append(TaxationObject(name, unary_union(polygons)))

    for text in numbers:
        number = text.plain_text().replace('\n', ' ') if isinstance(text, MText) else text.plain_text()
        x, y = text.dxf.insert[0], text.dxf.insert[1]
        taxation_collection_temp.trees.append(TaxationObject(number, Point(x, y)))

    for line in lines:
        if isinstance(line, LWPolyline):
            coordinates = [(float(x), float(y)) for x, y in list(line.vertices())]
            taxation_collection_temp.lines.append(TaxationObject(None, LineString(coordinates)))
        if isinstance(line, Line):
            coordinates = [(line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y)]
            taxation_collection_temp.lines.append(TaxationObject(None, LineString(coordinates)))

    for contour in contours:
        taxation_collection_temp.contours.append(
            TaxationObject(None, Polygon([(float(x), float(y)) for x, y in list(contour.vertices())]))
        )

    for number in taxation_collection_temp.trees:
        for line in taxation_collection_temp.lines:
            if line.shape.distance(number.shape) < 0.01:
                line_ = TaxationObject(number.number, line.shape)
                taxation_collection.lines.append(line_)
                break
        for polygon in taxation_collection_temp.contours:
            if number.shape.distance(polygon.shape.exterior) < 0.01:
                polygon_ = TaxationObject(number.number, polygon.shape)
                taxation_collection.contours.append(polygon_)
                break

    all_numbers = set([_.number for _ in taxation_collection_temp.trees])
    shapes_numbers = set([_.number for _ in chain(taxation_collection.lines, taxation_collection.contours)])
    numbers_of_trees = all_numbers - shapes_numbers

    for number in taxation_collection_temp.trees:
        if number.number in numbers_of_trees:
            taxation_collection.trees.append(number)

    # TODO: разделить номера типа 24-25 и 19а-в на 24,25 и 19а,19б,19в

    return taxation_collection

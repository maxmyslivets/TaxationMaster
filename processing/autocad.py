from typing import Union
import ezdxf
from ezdxf.entities import Text, MText, Line, LWPolyline
from shapely.geometry import Point, LineString, Polygon
from pathlib import Path


class TaxationObject:
    def __init__(self, number: str, shape: Union[Point, LineString, Polygon]):
        self.number = number
        self.shape = shape

    def __repr__(self) -> str:
        return f"TaxationObject({self.number}, {self.shape})"


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

    return numbers, lines, contours, zones


def correcting_data_from_taxation_plan(numbers: list, lines: list, contours: list, zones: list):
    """Метод для коррекции номеров"""

    data = {
        "numbers": [],
        "lines": [],
        "contours": [],
        "zones": []
    }

    for text in numbers:
        number = text.plain_text().replace('\n', ' ') if isinstance(text, MText) else text.plain_text()
        x, y = text.dxf.insert[1], text.dxf.insert[0]
        data["numbers"].append(TaxationObject(number, Point(x, y)))

    for line in lines:
        if isinstance(line, LWPolyline):
            coordinates = [(float(x), float(y)) for x, y in list(line.vertices())]
            data["lines"].append(TaxationObject(None, LineString(coordinates)))
        if isinstance(line, Line):
            coordinates = [(line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y)]
            data["lines"].append(TaxationObject(None, LineString(coordinates)))

    for contour in contours:
        data["contours"].append(
            TaxationObject(None, Polygon([(float(x), float(y)) for x, y in list(contour.vertices())]))
        )

    for zone in zones:
        data["zones"].append(TaxationObject(None, Polygon([(float(x), float(y)) for x, y in list(zone.vertices())])))

    return data

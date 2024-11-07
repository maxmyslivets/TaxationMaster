from typing import Union

import ezdxf
from ezdxf.entities import Text, MText, Line, LWPolyline
from pathlib import Path


def extract_data_from_taxation_plan(file_path: Path,
                                    numbers_layers: list[str] = ["номера"],
                                    lines_layers: list[str] = ["полосы"],
                                    contours_layers: list[str] = ["контуры"],
                                    zones_layers: list[str] = ["зоны"]) -> tuple[list[Union[Text, MText]], list[Union[Line, LWPolyline]], list[Union[Line, LWPolyline]], list[Union[Text, MText, LWPolyline]]]:
    """
    Извлечение данных из чертежа таксации
    :param file_path: путь к файлу
    :param numbers_layers: слои с номерами
    :param lines_layers: слои с линиями
    :param contours_layers: слои с контурами
    :param zones_layers: слои с зонами
    :return: кортеж из списков номеров, линий, контуров и зон
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

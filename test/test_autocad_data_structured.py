from pathlib import Path

import pytest
from shapely.geometry import LineString, Polygon

from source.model.model import Model


def log_function(s: str):

    PRINT_LOG = True

    if PRINT_LOG:
        print("\n\033[33m" + s + "\033[0m")
    else:
        pass


@pytest.fixture(scope='module')
def init_model():
    model = Model(log=log_function)
    model.read_taxation_plan(Path("test.dxf"))
    model.autocad_data_structuring()
    return model


def test_numbers(init_model):

    # Количество номеров в чертеже
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10а", "11", "12", "13", "14", "15", "16", "16", "17",
               "18", "19а-г", "20", "21", "22", "23", "24, 25а", "26-27", "28", "28", "28"]
    NUMBERS.sort()

    model = init_model

    numbers = [number for _, number in model.numbers.items()]
    numbers.sort()

    assert numbers == NUMBERS, "Номера не совпадают с чертежом"


def test_len_numbers_position(init_model):

    # Количество номеров в чертеже
    COUNT_NUMBER = 29

    model = init_model

    assert len(model.numbers_position) == COUNT_NUMBER, "Количество позиций номеров не совпадает с чертежом"


def test_len_shapes(init_model):

    # Количество фигур в чертеже
    COUNT_SHAPES = 6

    model = init_model

    assert len(model.shapes) == COUNT_SHAPES, "Количество фигур не совпадает с чертежом"


def test_len_zone_shapes(init_model):

    # Количество зон в чертеже
    COUNT_ZONES = 3

    model = init_model

    assert len(model.zone_shapes) == COUNT_ZONES, "Количество зон не совпадает с чертежом"


def test_len_zone_names(init_model):

    # Количество названий зон в чертеже (несколько одинаковых названий считаются за одно)
    COUNT_NAMES = 2

    model = init_model

    assert len(model.zone_names) == COUNT_NAMES, "Количество имен зон не совпадает с чертежом"


def test_len_tree_from_numbers(init_model):

    # Количество точечных объектов в чертеже
    COUNT_TREES = 18

    model = init_model

    assert len(model.tree) == COUNT_TREES, "Количество точечных объектов не совпадает с чертежом"


def test_zones_from_zone_names(init_model):
    """Проверка совпадения названий зон с названиями из чертежа"""

    # Названия зон в чертеже
    ZONE_NAMES = ["Зона 1", "Зона 2"]
    ZONE_NAMES.sort()

    model = init_model

    zone_names_from_model = []
    for _, zone_name in model.zone_names.items():
        zone_names_from_model.append(zone_name)
    zone_names_from_model.sort()

    assert zone_names_from_model == ZONE_NAMES, "Названия зон не совпадают с чертежом"


def test_numbers_from_tree(init_model):
    """Проверка совпадения номеров точечных объектов с названиями из чертежа"""

    # Список номеров точечных объектов чертеже
    TREE_NUMBERS = ["3", "4", "5", "6", "7", "10а", "11", "12", "13", "14", "18", "19а-г", "20", "21", "22", "23",
                    "24, 25а", "26-27"]
    TREE_NUMBERS.sort()

    model = init_model

    tree_numbers_from_model = []
    for _, k_number in model.numbers_from_tree.items():
        tree_numbers_from_model.append(model.numbers[k_number])
    tree_numbers_from_model.sort()

    assert tree_numbers_from_model == TREE_NUMBERS, "Номера деревьев не совпадают с чертежом"


def test_numbers_from_shape(init_model):
    """Проверка совпадения номеров фигур с названиями из чертежа"""

    # Список номеров контуров в чертеже
    NUMBERS_FROM_SHAPE = ["1", "2", "8", "9", "15", "16", "16", "17", "28", "28", "28"]
    NUMBERS_FROM_SHAPE.sort()

    model = init_model

    numbers_from_shape_from_model = []
    idx_numbers_from_shape_from_model = []
    for _, k_numbers_list in model.numbers_from_shape.items():
        idx_numbers_from_shape_from_model.extend(k_numbers_list)
    for k_number in idx_numbers_from_shape_from_model:
        numbers_from_shape_from_model.append(model.numbers[k_number])
    numbers_from_shape_from_model.sort()

    assert numbers_from_shape_from_model == NUMBERS_FROM_SHAPE, "Номера фигур не совпадают с чертежом"


def test_count_shape_is_line(init_model):
    """Проверка количества полученных линий с количеством из чертежа"""

    # Количество полос в чертеже
    COUNT_LINE = 2

    model = init_model

    line_count = 0
    for _, shape in model.shapes.items():
        if isinstance(shape, LineString):
            line_count += 1

    assert line_count == COUNT_LINE, "Количество полученных линий не совпадает с чертежом"


def test_count_shape_is_contour(init_model):
    """Проверка количества полученных контуров с количеством из чертежа"""

    # Количество контуров в чертеже
    COUNT_CONTOUR = 4

    model = init_model

    contour_count = 0
    for _, shape in model.shapes.items():
        if isinstance(shape, Polygon):
            contour_count += 1

    assert contour_count == COUNT_CONTOUR, "Количество полученных контуров не совпадает с чертежом"

import pytest
from shapely.geometry import LineString, Polygon

from source.model import Model
from test import log


@pytest.fixture(scope='module')
def init_project():
    model = Model(log=log)
    model.project.dir_dxf = "test_model/data"
    model.project.dxf_name = "test.dxf"
    model.processing.autocad_data_structuring()
    return model.project


@pytest.fixture(scope='module')
def init_autocad_data_structuring():
    model = Model(log=log)
    model.project.dir_dxf = "test_model/data"
    model.project.dxf_name = "test.dxf"
    model.processing.autocad_data_structuring()
    return model.project


def test_numbers(init_autocad_data_structuring):

    # Количество номеров в чертеже
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10а", "11", "12", "13", "14", "15", "16", "16", "17",
               "18", "19а-г", "20", "21", "22", "23", "24, 25а", "26-27", "28", "28", "28"]
    NUMBERS.sort()

    project = init_autocad_data_structuring

    numbers = [number for _, number in project.numbers.items()]
    numbers.sort()

    assert numbers == NUMBERS, "Номера не совпадают с чертежом"


def test_len_numbers_position(init_autocad_data_structuring):

    # Количество номеров в чертеже
    COUNT_NUMBER = 29

    project = init_autocad_data_structuring

    assert len(project.numbers_position) == COUNT_NUMBER, "Количество позиций номеров не совпадает с чертежом"


def test_len_shapes(init_autocad_data_structuring):

    # Количество фигур в чертеже
    COUNT_SHAPES = 6

    project = init_autocad_data_structuring

    assert len(project.shapes) == COUNT_SHAPES, "Количество фигур не совпадает с чертежом"


def test_len_zone_shapes(init_autocad_data_structuring):

    # Количество зон в чертеже
    COUNT_ZONES = 3

    project = init_autocad_data_structuring

    assert len(project.zone_shapes) == COUNT_ZONES, "Количество зон не совпадает с чертежом"


def test_len_zone_names(init_autocad_data_structuring):

    # Количество названий зон в чертеже (несколько одинаковых названий считаются за одно)
    COUNT_NAMES = 2

    project = init_autocad_data_structuring

    assert len(project.zone_names) == COUNT_NAMES, "Количество имен зон не совпадает с чертежом"


def test_len_tree_from_numbers(init_autocad_data_structuring):

    # Количество точечных объектов в чертеже
    COUNT_TREES = 18

    project = init_autocad_data_structuring

    assert len(project.tree) == COUNT_TREES, "Количество точечных объектов не совпадает с чертежом"


def test_zones_from_zone_names(init_autocad_data_structuring):
    """Проверка совпадения названий зон с названиями из чертежа"""

    # Названия зон в чертеже
    ZONE_NAMES = ["Зона 1", "Зона 2"]
    ZONE_NAMES.sort()

    project = init_autocad_data_structuring

    zone_names_from_model = []
    for _, zone_name in project.zone_names.items():
        zone_names_from_model.append(zone_name)
    zone_names_from_model.sort()

    assert zone_names_from_model == ZONE_NAMES, "Названия зон не совпадают с чертежом"


def test_numbers_from_tree(init_autocad_data_structuring):
    """Проверка совпадения номеров точечных объектов с названиями из чертежа"""

    # Список номеров точечных объектов чертеже
    TREE_NUMBERS = ["3", "4", "5", "6", "7", "10а", "11", "12", "13", "14", "18", "19а-г", "20", "21", "22", "23",
                    "24, 25а", "26-27"]
    TREE_NUMBERS.sort()

    project = init_autocad_data_structuring

    tree_numbers_from_model = []
    for _, k_number in project.numbers_from_tree.items():
        tree_numbers_from_model.append(project.numbers[k_number])
    tree_numbers_from_model.sort()

    assert tree_numbers_from_model == TREE_NUMBERS, "Номера деревьев не совпадают с чертежом"


def test_numbers_from_shape(init_autocad_data_structuring):
    """Проверка совпадения номеров фигур с названиями из чертежа"""

    # Список номеров контуров в чертеже
    NUMBERS_FROM_SHAPE = ["1", "2", "8", "9", "15", "16", "16", "17", "28", "28", "28"]
    NUMBERS_FROM_SHAPE.sort()

    project = init_autocad_data_structuring

    numbers_from_shape_from_model = []
    idx_numbers_from_shape_from_model = []
    for _, k_numbers_list in project.numbers_from_shape.items():
        idx_numbers_from_shape_from_model.extend(k_numbers_list)
    for k_number in idx_numbers_from_shape_from_model:
        numbers_from_shape_from_model.append(project.numbers[k_number])
    numbers_from_shape_from_model.sort()

    assert numbers_from_shape_from_model == NUMBERS_FROM_SHAPE, "Номера фигур не совпадают с чертежом"


def test_count_shape_is_line(init_autocad_data_structuring):
    """Проверка количества полученных линий с количеством из чертежа"""

    # Количество полос в чертеже
    COUNT_LINE = 2

    project = init_autocad_data_structuring

    line_count = 0
    for _, shape in project.shapes.items():
        if isinstance(shape, LineString):
            line_count += 1

    assert line_count == COUNT_LINE, "Количество полученных линий не совпадает с чертежом"


def test_count_shape_is_contour(init_autocad_data_structuring):
    """Проверка количества полученных контуров с количеством из чертежа"""

    # Количество контуров в чертеже
    COUNT_CONTOUR = 4

    project = init_autocad_data_structuring

    contour_count = 0
    for _, shape in project.shapes.items():
        if isinstance(shape, Polygon):
            contour_count += 1

    assert contour_count == COUNT_CONTOUR, "Количество полученных контуров не совпадает с чертежом"

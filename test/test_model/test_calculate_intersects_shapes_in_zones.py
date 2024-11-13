from pathlib import Path

import pytest

from source.model import Model
from test.test_model.fake_view import FakeView


@pytest.fixture(scope='module')
def init_project():
    view = FakeView()
    model = Model(view)
    model.project._dir_dxf = Path("test_model/data")
    model.project._dxf_name = Path("test.dxf")
    model.processing.read_data_from_taxation_plan()
    model.processing.splitting_numbers()
    model.processing.calculate_intersects_shapes_in_zones()
    return model.project


def test_intersects_shapes_in_zones(init_project):
    """Проверка вхождений фигур и точечных объектов растительности в зоны"""

    # Названия зон в чертеже
    SPLIT_NUMBERS_IN_ZONES = {
        "Зона 1": ["3", "4", "5", "6", "7", "8", "9", "15", "16", "19а", "19б", "19в", "19г", "24", "25а", "26", "27"],
        "Зона 2": ["1", "2", "8", "9", "10а", "11", "12", "13", "14", "15", "17", "18", "20", "21", "22", "28"]
    }
    for k in SPLIT_NUMBERS_IN_ZONES.keys():
        SPLIT_NUMBERS_IN_ZONES[k].sort()
    split_numbers_in_zones = dict(sorted(SPLIT_NUMBERS_IN_ZONES.items()))

    project = init_project

    split_numbers_in_zones_from_model = {zone_name: [] for _, zone_name in project.zone_names.items()}
    for zone_name in split_numbers_in_zones_from_model.keys():
        k_zone_name = next(k for k, v in project.zone_names.items() if v == zone_name)
        k_zone_list = project.zones_from_zone_names[k_zone_name]
        for k_zone in k_zone_list:
            for k_split_number, _k_zone_list in project.intersects_shapes_in_zones.items():
                for _k_zone in _k_zone_list:
                    if _k_zone == k_zone:
                        split_numbers_in_zones_from_model[zone_name].append(project.split_numbers[k_split_number])

    for k in split_numbers_in_zones_from_model.keys():
        split_numbers_in_zones_from_model[k].sort()
    _split_numbers_in_zones_from_model = dict(sorted(split_numbers_in_zones_from_model.items()))

    assert _split_numbers_in_zones_from_model == split_numbers_in_zones, "Вхождение объектов в зоны определено не верно"


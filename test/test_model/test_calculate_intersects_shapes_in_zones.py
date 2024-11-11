from pathlib import Path

import pytest

from source.model.model import Model
from test import log


@pytest.fixture()
def init_model():
    model = Model(log=log)
    model.read_taxation_plan(Path("test_model/data/test.dxf"))
    model.autocad_data_structuring()
    model.splitting_numbers()
    model.calculate_intersects_shapes_in_zones()
    return model


def test_intersects_shapes_in_zones(init_model):
    """Проверка вхождений фигур и точечных объектов растительности в зоны"""

    # Названия зон в чертеже
    SPLIT_NUMBERS_IN_ZONES = {
        "Зона 1": ["3", "4", "5", "6", "7", "8", "9", "15", "16", "19а", "19б", "19в", "19г", "24", "25а", "26", "27"],
        "Зона 2": ["1", "2", "8", "9", "10а", "11", "12", "13", "14", "15", "17", "18", "20", "21", "22", "28"]
    }
    for k in SPLIT_NUMBERS_IN_ZONES.keys():
        SPLIT_NUMBERS_IN_ZONES[k].sort()
    split_numbers_in_zones = dict(sorted(SPLIT_NUMBERS_IN_ZONES.items()))

    model = init_model

    split_numbers_in_zones_from_model = {zone_name: [] for _, zone_name in model.zone_names.items()}
    for zone_name in split_numbers_in_zones_from_model.keys():
        k_zone_name = next(k for k, v in model.zone_names.items() if v == zone_name)
        k_zone_list = model.zones_from_zone_names[k_zone_name]
        for k_zone in k_zone_list:
            for k_split_number, _k_zone_list in model.intersects_shapes_in_zones.items():
                for _k_zone in _k_zone_list:
                    if _k_zone == k_zone:
                        split_numbers_in_zones_from_model[zone_name].append(model.split_numbers[k_split_number])

    for k in split_numbers_in_zones_from_model.keys():
        split_numbers_in_zones_from_model[k].sort()
    _split_numbers_in_zones_from_model = dict(sorted(split_numbers_in_zones_from_model.items()))

    assert _split_numbers_in_zones_from_model == split_numbers_in_zones, "Вхождение объектов в зоны определено не верно"


from pathlib import Path

import pytest

from source.model.model import Model


def log_function(s: str):

    PRINT_LOG = True

    if PRINT_LOG:
        print("\n\033[33m" + s + "\033[0m")
    else:
        pass


def init_model_fail_duplicate_numbers_of_tree() -> Model:
    model = Model(log=log_function)
    model.read_taxation_plan(Path("test_fail_duplicate_numbers_of_tree.dxf"))
    model.autocad_data_structuring()
    return model


def init_model_fail_duplicate_numbers_of_shapes() -> Model:
    model = Model(log=log_function)
    model.read_taxation_plan(Path("test_fail_duplicate_numbers_of_shapes.dxf"))
    model.autocad_data_structuring()
    return model


def init_model_fail_duplicate_numbers_tree_shapes() -> Model:
    model = Model(log=log_function)
    model.read_taxation_plan(Path("test_fail_duplicate_numbers_tree-shapes.dxf"))
    model.autocad_data_structuring()
    return model


def init_model_fail_intersection_zone() -> Model:
    model = Model(log=log_function)
    model.read_taxation_plan(Path("test_fail_intersection_zone.dxf"))
    model.autocad_data_structuring()
    return model


init_models = [
    init_model_fail_duplicate_numbers_of_tree,
    init_model_fail_duplicate_numbers_of_shapes,
    init_model_fail_duplicate_numbers_tree_shapes,
    init_model_fail_intersection_zone,
]


@pytest.mark.parametrize('init_model', init_models)
def test_valid(init_model):

    model = init_model()

    assert not model.valid


@pytest.mark.parametrize('init_model', init_models)
def test_exist_data(init_model):

    model = init_model()

    assert len(model.taxation_plan_entity_objects["номера"]) == 0
    assert len(model.taxation_plan_entity_objects["полосы"]) == 0
    assert len(model.taxation_plan_entity_objects["контуры"]) == 0
    assert len(model.taxation_plan_entity_objects["зоны"]) == 0
    assert len(model.numbers) == 0
    assert len(model.numbers_position) == 0
    assert len(model.shapes) == 0
    assert len(model.numbers_from_shape) == 0
    assert len(model.zone_shapes) == 0
    assert len(model.zone_names) == 0
    assert len(model.zones_from_zone_names) == 0
    assert len(model.tree) == 0
    assert len(model.numbers_from_tree) == 0
    assert len(model.split_numbers) == 0
    assert len(model.number_from_split_number) == 0

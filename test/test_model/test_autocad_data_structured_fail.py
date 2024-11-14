from pathlib import Path

import pytest

from source.model import Model
from test.test_model.fake_view import FakeView


def init_model_fail_duplicate_numbers_of_tree() -> Model:
    view = FakeView()
    model = Model(view)
    model.project._dir_dxf = Path("test_model/data")
    model.project._dxf_name = Path("test_fail_duplicate_numbers_of_tree.dxf")
    model.processing.read_data_from_taxation_plan(model.config.numbers_layers, model.config.lines_layers,
                                                  model.config.contours_layers, model.config.zones_layers,
                                                  model.config.min_distance, model.config.min_area)
    return model


def init_model_fail_duplicate_numbers_of_shapes() -> Model:
    view = FakeView()
    model = Model(view)
    model.project._dir_dxf = Path("test_model/data")
    model.project._dxf_name = Path("test_fail_duplicate_numbers_of_shapes.dxf")
    model.processing.read_data_from_taxation_plan(model.config.numbers_layers, model.config.lines_layers,
                                                  model.config.contours_layers, model.config.zones_layers,
                                                  model.config.min_distance, model.config.min_area)
    return model


def init_model_fail_duplicate_numbers_tree_shapes() -> Model:
    view = FakeView()
    model = Model(view)
    model.project._dir_dxf = Path("test_model/data")
    model.project._dxf_name = Path("test_fail_duplicate_numbers_tree-shapes.dxf")
    model.processing.read_data_from_taxation_plan(model.config.numbers_layers, model.config.lines_layers,
                                                  model.config.contours_layers, model.config.zones_layers,
                                                  model.config.min_distance, model.config.min_area)
    return model


def init_model_fail_intersection_zone() -> Model:
    view = FakeView()
    model = Model(view)
    model.project._dir_dxf = Path("test_model/data")
    model.project._dxf_name = Path("test_fail_intersection_zone.dxf")
    model.processing.read_data_from_taxation_plan(model.config.numbers_layers, model.config.lines_layers,
                                                  model.config.contours_layers, model.config.zones_layers,
                                                  model.config.min_distance, model.config.min_area)
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
    model.processing.read_data_from_taxation_plan(model.config.numbers_layers, model.config.lines_layers,
                                                  model.config.contours_layers, model.config.zones_layers,
                                                  model.config.min_distance, model.config.min_area)

    assert model.processing.valid == False


@pytest.mark.parametrize('init_model', init_models)
def test_exist_data(init_model):

    model = init_model()

    assert len(model.project.numbers) == 0
    assert len(model.project.numbers_position) == 0
    assert len(model.project.shapes) == 0
    assert len(model.project.numbers_from_shape) == 0
    assert len(model.project.zone_shapes) == 0
    assert len(model.project.zone_names) == 0
    assert len(model.project.zones_from_zone_names) == 0
    assert len(model.project.tree) == 0
    assert len(model.project.numbers_from_tree) == 0
    assert len(model.project.split_numbers) == 0
    assert len(model.project.number_from_split_number) == 0

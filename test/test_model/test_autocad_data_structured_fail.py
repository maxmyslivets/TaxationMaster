import pytest

from source.model.model import Model
from source.model.project import Project
from test import log


def init_model_fail_duplicate_numbers_of_tree() -> Model:
    model = Model(log=log)
    model.project = Project()
    model.project.dir_dxf = "test_model/data"
    model.project.dxf_name = "test_fail_duplicate_numbers_of_tree.dxf"
    model.autocad_data_structuring()
    return model


def init_model_fail_duplicate_numbers_of_shapes() -> Model:
    model = Model(log=log)
    model.project = Project()
    model.project.dir_dxf = "test_model/data"
    model.project.dxf_name = "test_fail_duplicate_numbers_of_shapes.dxf"
    model.autocad_data_structuring()
    return model


def init_model_fail_duplicate_numbers_tree_shapes() -> Model:
    model = Model(log=log)
    model.project = Project()
    model.project.dir_dxf = "test_model/data"
    model.project.dxf_name = "test_fail_duplicate_numbers_tree-shapes.dxf"
    model.autocad_data_structuring()
    return model


def init_model_fail_intersection_zone() -> Model:
    model = Model(log=log)
    model.project = Project()
    model.project.dir_dxf = "test_model/data"
    model.project.dxf_name = "test_fail_intersection_zone.dxf"
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
    model.autocad_data_structuring()

    assert model.valid == False


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

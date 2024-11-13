import inspect

import pytest

from source.model.model import Model
from source.model.project import Project
from test import log


@pytest.fixture
def init_project():
    model = Model(log=log)
    model.project = Project()
    return model.project


def test_after_(init_project):

    project = init_project

    STR_PROJECT_SETTERS = ["name", "path", "dir_dwg", "dir_dxf", "dwg_name", "dxf_name", "path_dwg", "path_dxf"]
    DICT_PROJECT_SETTERS = ["numbers", "numbers_position", "shapes", "numbers_from_shape", "zone_shapes", "zone_names",
                            "zones_from_zone_names", "tree", "numbers_from_tree", "split_numbers",
                            "number_from_split_number", "intersects_shapes_in_zones"]

    assert project.is_saved == True

    project.dir_dxf = "_"
    project.dxf_name = "_"
    project.dir_dwg = "_"
    project.dwg_name = "_"

    project.is_saved = True

    for name, attr in inspect.getmembers(project, lambda x: isinstance(x, property)):
        if attr.fset:
            if name in STR_PROJECT_SETTERS:
                project.__dict__[name] = str()
                assert project.is_saved == False
            if name in DICT_PROJECT_SETTERS:
                project.__dict__[name] = dict()
                assert project.is_saved == False
            project.is_saved = True

    assert project.is_saved == False

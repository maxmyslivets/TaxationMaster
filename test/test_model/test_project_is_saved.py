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
    taxation_plan = project.taxation_plan

    STR_PROJECT_SETTERS = ["name", "path"]
    DICT_PROJECT_SETTERS = ["numbers", "numbers_position", "shapes", "numbers_from_shape", "zone_shapes", "zone_names",
                            "zones_from_zone_names", "tree", "numbers_from_tree", "split_numbers",
                            "number_from_split_number", "intersects_shapes_in_zones"]
    STR_TAXATION_PLAN_SETTERS = ["dir_dwg", "dir_dxf", "path_dwg", "path_dxf", "entity_path"]

    assert project.is_saved == True

    for name, attr in inspect.getmembers(project, lambda x: isinstance(x, property)):
        if attr.fset:
            if name in STR_PROJECT_SETTERS:
                project.__dict__[name] = str()
                assert project.is_saved == False
            if name in DICT_PROJECT_SETTERS:
                project.__dict__[name] = dict()
                assert project.is_saved == False
            project.is_saved = True

    project.taxation_plan = taxation_plan
    assert project.is_saved == False

    project.is_saved = True

    for name, attr in inspect.getmembers(project, lambda x: isinstance(x, property)):
        if attr.fset:
            if name in STR_TAXATION_PLAN_SETTERS:
                project.__dict__[name] = str()
                assert project.is_saved == False

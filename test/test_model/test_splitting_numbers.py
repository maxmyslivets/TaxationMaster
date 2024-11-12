import pytest

from source.model.model import Model
from source.model.project import Project
from test import log


@pytest.fixture(scope='module')
def init_project():
    model = Model(log=log)
    model.project = Project()
    model.project.taxation_plan.path_dxf = "test_model/data/test.dxf"
    model.read_taxation_plan()
    model.autocad_data_structuring()
    model.splitting_numbers()
    return model.project


def test_split_numbers(init_project):
    """Проверка списка разделенных номеров"""

    # Список разделенных номеров
    SPLIT_NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10а", "11", "12", "13", "14", "15", "16", "17",
                     "18", "19а", "19б", "19в", "19г", "20", "21", "22", "23", "24", "25а", "26", "27", "28"]
    SPLIT_NUMBERS.sort()

    project = init_project

    split_numbers_from_model = [split_number for _, split_number in project.split_numbers.items()]
    split_numbers_from_model.sort()

    assert split_numbers_from_model == SPLIT_NUMBERS, "Список разделенных номеров не совпадает с чертежом"


def test_number_from_split_number(init_project):
    """Проверка связей разделенных номеров"""

    project = init_project

    # Список разделенных номеров
    SPLIT_NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10а", "11", "12", "13", "14", "15", "16", "17",
                     "18", "19а", "19б", "19в", "19г", "20", "21", "22", "23", "24", "25а", "26", "27", "28"]
    NUMBER_FROM_GET_KEY_FOR_SPLIT_NUMBER = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10а", "11", "12", "13", "14",
                                            "15", "16", "17", "18", "19а-г", "19а-г", "19а-г", "19а-г",
                                            "20", "21", "22", "23", "24, 25а", "24, 25а", "26-27", "26-27", "28"]

    assert len(NUMBER_FROM_GET_KEY_FOR_SPLIT_NUMBER) == len(SPLIT_NUMBERS), "Неверно введены проверочные данные"

    def get_k_split_number(number: str) -> int:
        return next(k for k, v in project.split_numbers.items() if v == number)

    def get_k_number(number: str) -> list[int]:
        return sorted([k for k, v in project.numbers.items() if v == number])

    k_number_list = [get_k_number(number) for number in NUMBER_FROM_GET_KEY_FOR_SPLIT_NUMBER]
    k_split_number_list = [get_k_split_number(number) for number in SPLIT_NUMBERS]

    # Словарь связи разделенных номеров с номерами
    NUMBER_FROM_SPLIT_NUMBER = {}

    for k_split_number, list_k_number in zip(k_split_number_list, k_number_list):
        NUMBER_FROM_SPLIT_NUMBER[k_split_number] = list_k_number

    sorted_dict_from_model = dict(sorted(project.number_from_split_number.items()))
    sorted_dict = dict(sorted(NUMBER_FROM_SPLIT_NUMBER.items()))

    assert sorted_dict_from_model == sorted_dict, "Список разделенных номеров не совпадает с чертежом"

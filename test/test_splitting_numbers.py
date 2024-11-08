from pathlib import Path

import pytest
from shapely.geometry import LineString, Polygon

from source.model.model import Model


@pytest.fixture(scope='module')
def init_model():
    model = Model(log=print)
    model.read_taxation_plan(Path("test.dxf"))
    model.autocad_data_structuring()
    model.splitting_numbers()
    return model


def test_split_numbers(init_model):
    """Проверка списка разделенных номеров"""

    # Список разделенных номеров
    SPLIT_NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                     "18", "19а", "19б", "19в", "19г", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
    SPLIT_NUMBERS.sort()

    model = init_model

    split_numbers_from_model = [split_number for _, split_number in model.split_numbers.items()]
    split_numbers_from_model.sort()

    assert split_numbers_from_model == SPLIT_NUMBERS, "Список разделенных номеров не совпадает с чертежом"


def test_number_from_split_number(init_model):
    """Проверка связей разделенных номеров"""

    model = init_model

    # Список разделенных номеров
    SPLIT_NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                     "18", "19а", "19б", "19в", "19г", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
    NUMBER_FROM_GET_KEY_FOR_SPLIT_NUMBER = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
                                            "15", "16", "17", "18", "19а-г", "19а-г", "19а-г", "19а-г", "20", "21",
                                            "22", "23", "24-25", "24-25", "26-27", "26-27", "28"]

    assert len(NUMBER_FROM_GET_KEY_FOR_SPLIT_NUMBER) == len(SPLIT_NUMBERS), "Неверно введены проверочные данные"

    def get_k_split_number(number: str) -> int:
        return next(k for k, v in model.split_numbers.items() if v == number)

    def get_k_number(number: str) -> list[int]:
        return sorted([k for k, v in model.numbers.items() if v == number])

    k_number_list = [get_k_number(number) for number in NUMBER_FROM_GET_KEY_FOR_SPLIT_NUMBER]
    k_split_number_list = [get_k_split_number(number) for number in SPLIT_NUMBERS]

    # Словарь связи разделенных номеров с номерами
    NUMBER_FROM_SPLIT_NUMBER = {}

    for k_split_number, list_k_number in zip(k_split_number_list, k_number_list):
        NUMBER_FROM_SPLIT_NUMBER[k_split_number] = list_k_number

    sorted_dict_from_model = dict(sorted(model.number_from_split_number.items()))
    sorted_dict = dict(sorted(NUMBER_FROM_SPLIT_NUMBER.items()))

    assert sorted_dict_from_model == sorted_dict, "Список разделенных номеров не совпадает с чертежом"

import re

from src.parsing import Splitter, Templates


class SearchAmbiguity:
    """
    Поиск неоднозначности данных
    """

    @staticmethod
    def check_in_row_from_taxation_list(number: str, quantity: str, height: str, diameter: str, is_shrub: bool) -> bool:
        """
        Поиск неоднозначности в количестве численных характеристик объекта растительности
        Args:
            number (str): Исходный номер объекта растительности
            quantity (str): Количество объектов растительности
            height (str): Высоты объекта растительности
            diameter (str): Диаметры объекта растительности
            is_shrub (bool): Тип объекта растительности (дерево/куст)

        Returns:
            bool: False, если неоднозначность найдена
        """

        if None in Splitter.number(number):
            return False
        if None in Splitter.size(height):
            return False
        if None in Splitter.size(diameter):
            return False

        count_numbers = len(Splitter.number(number))
        count_height = len(Splitter.size(height))
        count_diameter = len(Splitter.size(diameter))

        match_trunk = re.search(Templates.TRUNKS, quantity)
        match_contour = re.search(Templates.CONTOUR, quantity)
        match_line = re.search(Templates.LINE, quantity)

        if match_trunk:
            count_quantity = int(match_trunk.group(1))
        elif match_contour:
            count_quantity = 1
        elif match_line:
            count_quantity = 1
        else:
            count_quantity = int(float(quantity))

        max_count = max([count_numbers, count_height, count_diameter, count_quantity])
        # FIXME: Переписать все условия
        if not is_shrub and diameter == '-':
            return False
        if match_trunk and count_numbers == 1:
            if count_quantity == count_height == count_diameter:
                return True
            elif 1 == count_height == count_diameter:
                return True
        elif match_contour and count_numbers == 1:
            if count_quantity == count_height == count_diameter == 1:
                return True
            elif (count_quantity == count_height == 1) and (diameter == '-'):
                return True
        elif match_line and count_numbers == 1:
            if count_quantity == count_height == count_diameter == 1:
                return True
            elif (count_quantity == count_height == 1) and (diameter == '-'):
                return True
        elif not match_contour and not match_line and not match_trunk:
            if count_numbers == count_quantity == count_height == count_diameter:
                return True
            elif (count_height == 1 or count_height == max_count) and (count_diameter == 1 or count_diameter == max_count):
                if (count_numbers == 1 or count_numbers == max_count) and (count_quantity == max_count):
                    return True

        return False

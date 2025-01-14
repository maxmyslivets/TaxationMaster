import re

from src.parsing import Splitter, Templates


class Validate:
    """
    Поиск неоднозначности данных
    """

    @staticmethod
    def check_taxation_list_row(number: str, quantity: str, height: str, diameter: str, quality: str, is_shrub: bool) -> bool:
        """
        Поиск неоднозначности в количестве численных характеристик объекта растительности
        Args:
            number (str): Исходный номер объекта растительности
            quantity (str): Количество объектов растительности
            height (str): Высоты объекта растительности
            diameter (str): Диаметры объекта растительности
            quality (str): Состояния объекта растительности
            is_shrub (bool): Тип объекта растительности - True, если кустарник.

        Returns:
            bool: False, если неоднозначность найдена
        """
        split_numbers = Splitter.number(number)
        split_height = Splitter.size(height)
        split_diameter = Splitter.size(diameter)
        split_quality = Splitter.quality(quality)

        if (None in split_numbers) or (None in split_height) or (None in split_diameter):
            return False
        if (0 in split_height) or (0 in split_diameter):
            return False

        count_numbers = len(split_numbers)
        count_height = len(split_height)
        count_diameter = len(split_diameter)

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

        if (not is_shrub and diameter == '-') or (is_shrub and diameter != '-'):
            return False
        if len(split_quality) != 1 and len(split_quality) != max_count:
            return False

        if not match_contour and not match_line and not match_trunk:
            if (count_numbers == 1 or count_numbers == max_count) and count_quantity == max_count:
                if (count_diameter == 1 or count_diameter == max_count) and (count_height == 1 or count_height == max_count):
                    return True
                else:
                    return False
            else:
                return False
        elif match_trunk:
            if count_numbers == 1 and count_quantity == max_count:
                if (count_diameter == 1 or count_diameter == max_count) and (count_height == 1 or count_height == max_count):
                    return True
                else:
                    return False
            else:
                return False
        elif match_contour:
            if count_numbers == 1 and count_quantity == 1 and count_height == 1 and count_diameter == 1:
                return True
            else:
                return False
        elif match_line:
            if count_numbers == 1 and count_quantity == 1 and count_height == 1 and count_diameter == 1:
                return True
            else:
                return False
        else:
            return False

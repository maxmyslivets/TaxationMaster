import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.database import Database
from src.objects import Specie, Tree, TreeContour, TreeLine


@dataclass
class Templates:
    """
    Шаблоны регулярных выражений для поиска отдельных элементов характеристик древесной растительности.

    Attributes:
        DIGIT: шаблон '19'
        FLOAT_DIGIT: шаблон '2.1'
        DIGIT_LETTER: шаблон '8д'
        DIGIT_RANGE: шаблон '21-23'
        FLOAT_RANGE: шаблон '13.1-13.4'
        DIGIT_LETTER_RANGE: шаблон '11а-в'
        DIGIT_X_DIGIT: шаблон '11x2'
        FLOAT_X_DIGIT: шаблон '1.5x3'
        TRUNKS: шаблон '11 стволов'
        CONTOUR: шаблон '23 м2'
        LINE: шаблон '18 м.п.'

    DIGIT: шаблон для поиска целого числа

    FLOAT_DIGIT: шаблон  для поиска числа с плавающей точкой

    DIGIT_LETTER: шаблон для поиска целого числа с буквой

    DIGIT_RANGE: шаблон для поиска диапазонов целых чисел

    FLOAT_RANGE: шаблон для поиска диапазонов чисел с плавающей точкой

    DIGIT_LETTER_RANGE: шаблон для поиска диапазонов, представляющих целое число с буквой

    DIGIT_X_DIGIT: шаблон для поиска чисел, помноженных на количество

    FLOAT_X_DIGIT: шаблон для поиска чисел с плавающей точкой, помноженных на количество

    TRUNKS: шаблон для поиска количества стволов

    CONTOUR: шаблон для поиска значения площади в метрах квадратных

    LINE: шаблон для поиска значения длины в метрах погонных
    """

    DIGIT = re.compile(r'\d+$')
    FLOAT_DIGIT = re.compile(r'\d+\.\d+$')
    DIGIT_LETTER = re.compile(r'^\d+[а-я]$')
    DIGIT_RANGE = re.compile(r'^\d+-\d+$')
    FLOAT_RANGE = re.compile(r'^\d+\.\d+-\d+\.\d+$')
    DIGIT_LETTER_RANGE = re.compile(r'^\d+[а-я]-[а-я]$')
    DIGIT_X_DIGIT = re.compile(r'^\d+x\d+$')
    FLOAT_X_DIGIT = re.compile(r'^\d+\.\d+x\d+$')
    TRUNKS = re.compile(r'(\d+)\s*ствол', re.IGNORECASE)
    CONTOUR = re.compile(r'^\d+\.?\d+\s*м\s*(2|кв\.?)$', re.IGNORECASE)
    LINE = re.compile(r'^\d+\s*м\.?\s*п\.?$', re.IGNORECASE)


class Splitter:
    """
    Класс для разделения текста характеристик на отдельные строки.
    """

    @staticmethod
    def number(text: str) -> list[str | None]:
        """
        Разделяет объединенные номера на отдельные элементы.

        Args:
            text (str): Строка, содержащая объединенные номера.

        Returns:
            list[str | None]: Список разделенных номеров. Если номер не определился, возвращается None.
        """

        split_numbers = []

        text = text.strip().replace(' ', '')

        for part in text.split(','):

            if re.match(Templates.DIGIT, part):
                split_numbers.append(part)

            elif re.match(Templates.FLOAT_DIGIT, part):
                split_numbers.append(part)

            elif re.match(Templates.DIGIT_LETTER, part):
                split_numbers.append(part)

            elif re.match(Templates.DIGIT_RANGE, part):
                start, end = map(int, part.split('-'))
                split_numbers.extend([str(i) for i in range(start, end + 1)])

            elif re.match(Templates.FLOAT_RANGE, part):
                start, end = part.split('-')
                start_main, start_sub = map(int, start.split('.'))
                end_main, end_sub = map(int, end.split('.'))
                if start_main != end_main:
                    split_numbers.append(None)
                else:
                    split_numbers.extend([f"{start_main}.{i}" for i in range(start_sub, end_sub + 1)])

            elif re.match(Templates.DIGIT_LETTER_RANGE, part):
                num = re.match(r'\d+', part).group()
                start_letter, end_letter = re.findall(r'[а-я]', part)
                split_numbers.extend([f"{num}{chr(i)}" for i in range(ord(start_letter), ord(end_letter) + 1)])

        return split_numbers if len(split_numbers) > 0 else [None]

    @staticmethod
    def size(text: str) -> list[int | float | None]:
        """
        Разделяет объединенные размеры на отдельные элементы.

        Args:
            text (str): Строка, содержащая объединенные размеры.

        Returns:
            list[str | None]: Список разделенных размеров. Если размер не определился, возвращается None.
        """

        split_values = []

        text = text.strip().replace(' ', '')

        for part in text.split(','):
            part = part.replace('х', 'x').replace('Х', 'x').replace('X', 'x')

            if re.match(Templates.DIGIT, part):
                split_values.append(int(part))

            elif re.match(Templates.FLOAT_DIGIT, part):
                split_values.append(float(part))

            elif re.match(Templates.DIGIT_X_DIGIT, part):
                size, quantity = part.split('x')
                for _ in range(int(quantity)):
                    split_values.append(int(size))

            elif re.match(Templates.FLOAT_X_DIGIT, part):
                size, quantity = part.split('x')
                for _ in range(int(quantity)):
                    split_values.append(float(size))

            elif part == '-':
                split_values.append(part)

            else:
                split_values.append(None)

        return split_values

    @staticmethod
    def quality(quality: str) -> list[str]:
        values = quality.lower().replace(' ', '').replace(';', ',').split(',')
        patterns = {
            r'хор': 'Хорошее',
            r'плох': 'Плохое',
            r'неуд': 'Неудовлетворительное'
        }
        result = []
        for value in values:
            numbers = [int(num) for num in re.findall(r'\d+', value)]
            assert len(numbers) <= 1, \
                f"В строке Состояние {quality} содержится более одного численного значения. {numbers}"
            count = 1 if len(numbers) == 0 else numbers[0]
            is_found = False
            for pattern, word in patterns.items():
                if re.search(pattern, value):
                    result.extend([word] * count)
                    is_found = True
                    break
            if not is_found:
                result.extend([value] * count)
        return result


class Parser:
    """
    Класс для анализа информации о древесной растительности.
    """

    @staticmethod
    def get_specie(text: str) -> Specie:
        """
        Определение рода, вида и типа из наименования дерева.

        Args:
            text (str): наименование дерева

        Returns:
            tuple[str, str, str]: Кортеж с родом и видом породы дерева
        """

        text = text.strip().replace('ё', 'е').lower()
        breeds = text.split(' ')

        if len(breeds) == 1:
            breed_genus = breeds[0]
            breed_specie = ''     # TODO: Брать из БД основной вид породы

        elif len(breeds) == 2:
            breed_genus = breeds[0]
            breed_specie = breeds[1]

        else:
            raise ValueError(f'Некорректное название породы: {text}. Ожидается 1 или 2 значения, принято {len(breeds)}.')

        # TODO: Исправить после создания БД
        shrub_species, wood_species = Database(Path(__file__).parent.parent/"data"/"species.json").get_species()

        if breed_genus in shrub_species:
            is_shrub = True
        elif breed_genus in wood_species:
            is_shrub = False
        else:
            raise ValueError(f'Неизвестная порода: {breed_genus}.')

        return Specie(breed_genus, breed_specie, is_shrub)

    @staticmethod
    def get_type_tree_object(text: str) -> type[Tree | TreeContour | TreeLine]:
        """
        Определение типа объекта из строки количества.

        Args:
            text (str): строка количества

        Returns:
            Tree | TreeContour | TreeLine: объект дерева, контура или полосы
        """

        text = text.strip().replace(' ', '')

        if re.match(Templates.DIGIT, text) or re.match(Templates.TRUNKS, text):
            return Tree

        elif re.match(Templates.CONTOUR, text):
            return TreeContour

        elif re.match(Templates.LINE, text):
            return TreeLine

        else:
            raise ValueError(f'Некорректное значение количества: {text}.')

    @staticmethod
    def identification_stump(height: str | float, diameter: str | float, is_shrub: bool) -> bool:
        """
        Определение пня.
        Args:
            height (str | float): Высота
            diameter (str | float): Диаметр
            is_shrub (bool): Кустарник

        Returns:
            (bool): True, если пень
        """
        is_stump = False
        if is_shrub:
            return is_stump
        split_height = Splitter.size(str(height))
        split_diameter = Splitter.size(str(diameter))
        for h, d in zip(split_height, split_diameter):
            if float(h) < 0.7 and float(d) / float(h) > 0.1:
                is_stump = True
                break
        return is_stump


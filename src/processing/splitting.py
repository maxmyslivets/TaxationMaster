import re


def split_number(number: str) -> list[str | None]:
    """
    Разделение номеров
    :param number: Строка объединенных номеров
    :return: Список разделенных номеров
    """

    if re.match(r'^\d+$', number):
        return [number]

    elif re.match(r'^\d+[а-я]$', number):
        return [number]

    elif re.match(r'^\d+-\d+$', number):
        start, end = map(int, number.split('-'))
        return [str(i) for i in range(start, end + 1)]

    elif re.match(r'^\d+[а-я]-[а-я]$', number):
        num = re.match(r'\d+', number).group()
        start_letter, end_letter = re.findall(r'[а-я]', number)
        return [f"{num}{chr(i)}" for i in range(ord(start_letter), ord(end_letter) + 1)]

    return [None]


def split_tree_size(tree_size: str) -> list[str]:
    """
    Разделение высот или диаметров деревьев/стволов
    :param tree_size: Строка объединенных размеров деревьев/стволов
    :return: Список разделенных размеров деревьев/стволов
    """

    pass    # TODO

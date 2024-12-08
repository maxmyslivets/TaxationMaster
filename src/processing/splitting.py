import re


def split_number(number: str) -> list[str | None]:
    """
    Разделение номеров
    :param number: Строка объединенных номеров
    :return: Список разделенных номеров
    """

    numbers = []

    for part in number.split(','):
        part = part.strip()

        if re.match(r'^\d+$', part):
            numbers.append(part)

        elif re.match(r'^\d+\.\d+$', part):
            numbers.append(part)

        elif re.match(r'^\d+[а-я]$', part):
            numbers.append(part)

        elif re.match(r'^\d+-\d+$', part):
            start, end = map(int, part.split('-'))
            numbers.extend([str(i) for i in range(start, end + 1)])

        elif re.match(r'^\d+\.\d+-\d+\.\d+$', part):
            start, end = part.split('-')
            start_main, start_sub = map(int, start.split('.'))
            end_main, end_sub = map(int, end.split('.'))
            if start_main != end_main:
                numbers.append(None)
            else:
                numbers.extend([f"{start_main}.{i}" for i in range(start_sub, end_sub + 1)])

        elif re.match(r'^\d+[а-я]-[а-я]$', part):
            num = re.match(r'\d+', part).group()
            start_letter, end_letter = re.findall(r'[а-я]', part)
            numbers.extend([f"{num}{chr(i)}" for i in range(ord(start_letter), ord(end_letter) + 1)])

    return numbers if len(numbers) > 0 else [None]


def split_tree_size(tree_size: str) -> list[str]:
    """
    Разделение высот или диаметров деревьев/стволов
    :param tree_size: Строка объединенных размеров деревьев/стволов
    :return: Список разделенных размеров деревьев/стволов
    """

    pass    # TODO

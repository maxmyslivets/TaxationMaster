# FIXME: После сборки в exe изменения в файле rules.py не влияют на результат.
#  Решение: ...

def transplant(x, y) -> str:
    """
    Определяет действие с деревом или кустарником (удаление или пересадка)
    Args:
        ...
    Returns:
        str: Удаление/Пересадка
    """
    # TODO: Добавить фильтр
    # return 'Удаление\nСм.Прим.#'
    return 'Пересадка\nСм.Прим.#'


def calc_landings(x, y) -> str:
    """
    Определяет количество посадок
    Args:
        x:
        y:

    Returns:
        str: Строка расчета посадок
    """
    # TODO: Добавить фильтр
    # TODO: Что делать если у стволов одного дерева разные состояния
    return '...= N посадок'


def calc_payments(x, y) -> str:
    """
    Определяет сумму выплат
    Args:
        x:
        y:

    Returns:
        str: Строка расчета выплат
    """
    # TODO: Добавить фильтр
    # TODO: Что делать если у стволов одного дерева разные состояния
    return '...= N выплат'


class _TableStyle:
    class TextTitle:
        style = 'NF_VGP_5.0'
        height = 400.268

    class TextColumnName:
        style = 'NF_VGP_3.0'
        height = 300

    class TextZone:
        style = 'NF_VGP_5.0'
        height = 300

    class TextORM:
        style = 'NF_VGP_3.0'
        height = 300
        h_margin = 100


class TableStyleExists(_TableStyle):
    class TableSize:
        class Column:
            spacings = (
                ('Поз.', 1005.4436),
                ('Наименование\nпороды', 6000.1037),
                ('Кол-во,\nшт.', 1427.5616),
                ('Высота,\nм', 1500.0259),
                ('Диаметр\nствола,\nсм', 1572.4902),
                ('Качественное\nсостояние', 4000.0691),
                ('Примечание', 3000.0058)
            )
            full_width = sum([width for name, width in spacings])

        class Row:
            column_name = 1500.0259
            zone = 800.0138
            orm = 800.0138


class TableStyleRemovable(_TableStyle):
    # TODO
    column_titles = [...]

    class TableSize:
        class Column:
            pass

        class Row:
            pass

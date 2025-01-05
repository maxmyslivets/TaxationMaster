from dataclasses import dataclass

from shapely import Point, Polygon, LineString


@dataclass
class Number:
    """
    Номер объекта.

    Attributes:
        origin (str): исходный номер
        split (str): номер, разделенный номер
        position (Point | Polygon | LineString | None): географическая привязка
    """
    origin: str
    split: str
    position: Point | Polygon | LineString | None


@dataclass
class Specie:
    """
    Порода дерева.

    Attributes:
        breed_genus (str): Род породы
        breed_specie (str): Вид породы
        is_shrub (bool): True если кустарник, False если дерево
    """
    breed_genus: str
    breed_specie: str
    is_shrub: bool


@dataclass
class Trunk:
    """
    Объект ствола дерева.

    Attributes:
        diameter (float | int): диаметр ствола
        height (float | int): высота ствола
        quality (str): состояние ствола
    """
    diameter: float | int
    height: float | int
    quality: str


@dataclass
class Tree:
    """
    Объект дерева.

    Attributes:
        number (Number): номер объекта
        specie (Specie): порода дерева
        trunks (list[Trunk]): список стволов
    """
    number: Number
    specie: Specie
    trunks: list[Trunk]


@dataclass
class TreeContour(Tree):
    """
    Объект контура древесной растительности.

    Attributes:
        trunks (Trunk): объект ствола
        area (float | int): площадь контура
    """
    trunks: Trunk
    area: float | int


@dataclass
class TreeLine(Tree):
    """
    Объект полосы древесной растительности.

    Attributes:
        trunks (Trunk): объект ствола
        length (float | int): длина полосы
    """
    trunks: Trunk
    length: float | int

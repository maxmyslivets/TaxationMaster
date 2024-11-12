import shutil
from pathlib import Path

from ezdxf.entities import Text, MText, Line, LWPolyline


class Entity:
    _numbers: list[Text | MText] = None
    _lines: list[Line | LWPolyline] = None
    _contours: list[LWPolyline] = None
    _zones: list[Text | MText | LWPolyline] = None

    @property
    def numbers(self) -> list[Text | MText]:
        return self._numbers

    @numbers.setter
    def numbers(self, numbers: list[Text | MText]) -> None:
        self._numbers = numbers

    @property
    def lines(self) -> list[Line | LWPolyline]:
        return self._lines

    @lines.setter
    def lines(self, lines: list[Line | LWPolyline]) -> None:
        self._lines = lines

    @property
    def contours(self) -> list[LWPolyline]:
        return self._contours

    @contours.setter
    def contours(self, contours: list[LWPolyline]) -> None:
        self._contours = contours

    @property
    def zones(self) -> list[Text | MText | LWPolyline]:
        return self._zones

    @zones.setter
    def zones(self, zones: list[Text | MText | LWPolyline]) -> None:
        self._zones = zones

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)


class TaxationPlan:

    _dir_dwg: Path = None
    _dir_dxf: Path = None
    _path_dwg: Path = None
    _path_dxf: Path = None

    _entity_path: Path = None
    entity = Entity()

    @property
    def dir_dwg(self) -> Path:
        return self._dir_dwg

    @dir_dwg.setter
    def dir_dwg(self, path: str | Path) -> None:
        self._dir_dwg = path if isinstance(path, Path) else Path(path)

    @property
    def dir_dxf(self) -> Path:
        return self._dir_dxf

    @dir_dxf.setter
    def dir_dxf(self, path: str | Path) -> None:
        self._dir_dxf = path if isinstance(path, Path) else Path(path)

    @property
    def path_dwg(self) -> Path:
        return self._path_dwg

    @path_dwg.setter
    def path_dwg(self, path: str | Path):
        self._path_dwg = path if isinstance(path, Path) else Path(path)
        if self._path_dxf is not None and self._path_dxf.exists():
            shutil.rmtree(self._path_dxf, ignore_errors=True)

    @property
    def path_dxf(self) -> Path:
        return self._path_dxf

    @path_dxf.setter
    def path_dxf(self, path: str | Path):
        self._path_dxf = path if isinstance(path, Path) else Path(path)

    @property
    def entity_path(self) -> Path:
        return self._entity_path

    @entity_path.setter
    def entity_path(self, path: str | Path):
        self._entity_path = path if isinstance(path, Path) else Path(path)

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)


class Project:

    _name: str = None
    _path: Path = None
    _dir: Path = None

    _taxation_plan_path: Path = None
    taxation_plan = TaxationPlan()

    is_saved: bool = True

    _numbers = dict()                           # key: k_number         value: number
    _numbers_position = dict()                  # key: k_number         value: position
    _shapes = dict()                            # key: k_shape          value: shape
    _numbers_from_shape = dict()                # key: k_shape          value: list[k_number]
    _zone_shapes = dict()                       # key: k_zone           value: shape
    _zone_names = dict()                        # key: k_zone_name      value: zone_name
    _zones_from_zone_names = dict()             # key: k_zone_name      value: list[k_zone]
    _tree = dict()                              # key: k_tree           value: position
    _numbers_from_tree = dict()                 # key: k_tree           value: k_number
    _split_numbers = dict()                     # key: k_split_number   value: split_number
    _number_from_split_number = dict()          # key: k_split_number   value: list[k_number]
    _intersects_shapes_in_zones = dict()        # key: k_split_number   value: list[k_zone]

    # TODO: добавить декоратор, который изменяет self.is_saved при срабатывании setter методов

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def suffix(self) -> str:
        return ".ttpr"

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: str | Path) -> None:
        self._path = path if isinstance(path, Path) else Path(path)
        self._name = self._path.stem
        self._dir = self._path.parent / self._name
        self._taxation_plan_path = self._dir / "taxation_plan" / "taxation_plan.pkl"
        self.taxation_plan.dir_dwg = self._dir / "taxation_plan" / "dwg"
        self.taxation_plan.dir_dxf = self._dir / "taxation_plan" / "dxf"
        self.taxation_plan.entity_path = self._dir / "taxation_plan" / "entity.pkl"

    @property
    def dir(self) -> Path:
        return self._dir

    @property
    def taxation_plan_path(self) -> Path:
        return self._taxation_plan_path

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)

    @property
    def numbers(self) -> dict:
        return self._numbers

    @numbers.setter
    def numbers(self, numbers: dict) -> None:
        self._numbers = numbers

    @numbers.deleter
    def numbers(self) -> None:
        self._numbers = dict()

    @property
    def numbers_position(self) -> dict:
        return self._numbers_position

    @numbers_position.setter
    def numbers_position(self, numbers_position: dict) -> None:
        self._numbers = numbers_position

    @numbers_position.deleter
    def numbers_position(self) -> None:
        self._numbers_position = dict()

    @property
    def shapes(self) -> dict:
        return self._shapes

    @shapes.setter
    def shapes(self, shapes: dict) -> None:
        self._shapes = shapes

    @shapes.deleter
    def shapes(self) -> None:
        self._shapes = dict()

    @property
    def numbers_from_shape(self) -> dict:
        return self._numbers_from_shape

    @numbers_from_shape.setter
    def numbers_from_shape(self, numbers_from_shape: dict) -> None:
        self._numbers_from_shape = numbers_from_shape

    @numbers_from_shape.deleter
    def numbers_from_shape(self) -> None:
        self._numbers_from_shape = dict()

    @property
    def zone_shapes(self) -> dict:
        return self._zone_shapes

    @zone_shapes.setter
    def zone_shapes(self, zone_shapes: dict) -> None:
        self._zone_shapes = zone_shapes

    @zone_shapes.deleter
    def zone_shapes(self) -> None:
        self._zone_shapes = dict()

    @property
    def zone_names(self) -> dict:
        return self._zone_names

    @zone_names.setter
    def zone_names(self, zone_names: dict) -> None:
        self._zone_names = zone_names

    @zone_names.deleter
    def zone_names(self) -> None:
        self._zone_names = dict()

    @property
    def zones_from_zone_names(self) -> dict:
        return self._zones_from_zone_names

    @zones_from_zone_names.setter
    def zones_from_zone_names(self, zones_from_zone_names: dict) -> None:
        self._zones_from_zone_names = zones_from_zone_names

    @zones_from_zone_names.deleter
    def zones_from_zone_names(self) -> None:
        self._zones_from_zone_names = dict()

    @property
    def tree(self) -> dict:
        return self._tree

    @tree.setter
    def tree(self, tree: dict) -> None:
        self._tree = tree

    @tree.deleter
    def tree(self) -> None:
        self._tree = dict()

    @property
    def numbers_from_tree(self) -> dict:
        return self._numbers_from_tree

    @numbers_from_tree.setter
    def numbers_from_tree(self, numbers_from_tree: dict) -> None:
        self._numbers_from_tree = numbers_from_tree

    @numbers_from_tree.deleter
    def numbers_from_tree(self) -> None:
        self._numbers_from_tree = dict()

    @property
    def split_numbers(self) -> dict:
        return self._split_numbers

    @split_numbers.setter
    def split_numbers(self, split_numbers: dict) -> None:
        self._split_numbers = split_numbers

    @split_numbers.deleter
    def split_numbers(self) -> None:
        self._split_numbers = dict()

    @property
    def number_from_split_number(self) -> dict:
        return self._number_from_split_number

    @number_from_split_number.setter
    def number_from_split_number(self, number_from_split_number: dict) -> None:
        self._number_from_split_number = number_from_split_number

    @number_from_split_number.deleter
    def number_from_split_number(self) -> None:
        self._number_from_split_number = dict()

    @property
    def intersects_shapes_in_zones(self) -> dict:
        return self._intersects_shapes_in_zones

    @intersects_shapes_in_zones.setter
    def intersects_shapes_in_zones(self, intersects_shapes_in_zones: dict) -> None:
        self._intersects_shapes_in_zones = intersects_shapes_in_zones

    @intersects_shapes_in_zones.deleter
    def intersects_shapes_in_zones(self) -> None:
        self._intersects_shapes_in_zones = dict()

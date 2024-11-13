import shutil
from pathlib import Path


def mark_as_unsaved(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.is_saved = False
        return result
    return wrapper


class Project:

    def __init__(self):
        self._dir_dwg: Path = None
        self._dir_dxf: Path = None
        self._dwg_name: str = None
        self._dxf_name: str = None
        self._name: str = None
        self._path: Path = None
        self._dir: Path = None

        self.is_saved: bool = True

        self._numbers = dict()                           # key: k_number         value: number
        self._numbers_position = dict()                  # key: k_number         value: position
        self._shapes = dict()                            # key: k_shape          value: shape
        self._numbers_from_shape = dict()                # key: k_shape          value: list[k_number]
        self._zone_shapes = dict()                       # key: k_zone           value: shape
        self._zone_names = dict()                        # key: k_zone_name      value: zone_name
        self._zones_from_zone_names = dict()             # key: k_zone_name      value: list[k_zone]
        self._tree = dict()                              # key: k_tree           value: position
        self._numbers_from_tree = dict()                 # key: k_tree           value: k_number
        self._split_numbers = dict()                     # key: k_split_number   value: split_number
        self._number_from_split_number = dict()          # key: k_split_number   value: list[k_number]
        self._intersects_shapes_in_zones = dict()        # key: k_split_number   value: list[k_zone]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @mark_as_unsaved
    def name(self, name: str) -> None:
        self._name = name

    @property
    def suffix(self) -> str:
        return ".ttpr"

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    @mark_as_unsaved
    def path(self, path: str | Path) -> None:
        self._path = path if isinstance(path, Path) else Path(path)
        self._name = self._path.stem
        self._dir = self._path.parent / self._name
        self.dir_dwg = self._dir / "taxation_plan" / "dwg"
        self.dir_dxf = self._dir / "taxation_plan" / "dxf"

    @property
    def dir(self) -> Path:
        return self._dir

    @property
    def dir_dwg(self) -> Path:
        return self._dir_dwg

    @dir_dwg.setter
    @mark_as_unsaved
    def dir_dwg(self, path: str | Path) -> None:
        self._dir_dwg = path if isinstance(path, Path) else Path(path)

    @property
    def dir_dxf(self) -> Path:
        return self._dir_dxf

    @dir_dxf.setter
    @mark_as_unsaved
    def dir_dxf(self, path: str | Path) -> None:
        self._dir_dxf = path if isinstance(path, Path) else Path(path)

    @property
    def dwg_name(self) -> str:
        return self._dwg_name

    @dwg_name.setter
    @mark_as_unsaved
    def dwg_name(self, dwg_name: str):
        self._dwg_name = dwg_name
        if self._dxf_name is not None and (self._dir_dwg / self._dxf_name).exists():
            shutil.rmtree(self._dir_dwg / self._dxf_name, ignore_errors=True)

    @property
    def dxf_name(self) -> str:
        return self._dxf_name

    @dxf_name.setter
    @mark_as_unsaved
    def dxf_name(self, dxf_name: str):
        self._dxf_name = dxf_name

    @property
    def path_dwg(self) -> Path:
        return self._dir_dwg / self._dwg_name

    @property
    def path_dxf(self) -> Path:
        return self._dir_dxf / self._dxf_name

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)

    @property
    def numbers(self) -> dict:
        return self._numbers

    @numbers.setter
    @mark_as_unsaved
    def numbers(self, numbers: dict) -> None:
        self._numbers = numbers

    @numbers.deleter
    @mark_as_unsaved
    def numbers(self) -> None:
        self._numbers = dict()

    @property
    def numbers_position(self) -> dict:
        return self._numbers_position

    @numbers_position.setter
    @mark_as_unsaved
    def numbers_position(self, numbers_position: dict) -> None:
        self._numbers = numbers_position

    @numbers_position.deleter
    @mark_as_unsaved
    def numbers_position(self) -> None:
        self._numbers_position = dict()

    @property
    def shapes(self) -> dict:
        return self._shapes

    @shapes.setter
    @mark_as_unsaved
    def shapes(self, shapes: dict) -> None:
        self._shapes = shapes

    @shapes.deleter
    @mark_as_unsaved
    def shapes(self) -> None:
        self._shapes = dict()

    @property
    @mark_as_unsaved
    def numbers_from_shape(self) -> dict:
        return self._numbers_from_shape

    @numbers_from_shape.setter
    @mark_as_unsaved
    def numbers_from_shape(self, numbers_from_shape: dict) -> None:
        self._numbers_from_shape = numbers_from_shape

    @numbers_from_shape.deleter
    @mark_as_unsaved
    def numbers_from_shape(self) -> None:
        self._numbers_from_shape = dict()

    @property
    def zone_shapes(self) -> dict:
        return self._zone_shapes

    @zone_shapes.setter
    @mark_as_unsaved
    def zone_shapes(self, zone_shapes: dict) -> None:
        self._zone_shapes = zone_shapes

    @zone_shapes.deleter
    @mark_as_unsaved
    def zone_shapes(self) -> None:
        self._zone_shapes = dict()

    @property
    def zone_names(self) -> dict:
        return self._zone_names

    @zone_names.setter
    @mark_as_unsaved
    def zone_names(self, zone_names: dict) -> None:
        self._zone_names = zone_names

    @zone_names.deleter
    @mark_as_unsaved
    def zone_names(self) -> None:
        self._zone_names = dict()

    @property
    def zones_from_zone_names(self) -> dict:
        return self._zones_from_zone_names

    @zones_from_zone_names.setter
    @mark_as_unsaved
    def zones_from_zone_names(self, zones_from_zone_names: dict) -> None:
        self._zones_from_zone_names = zones_from_zone_names

    @zones_from_zone_names.deleter
    @mark_as_unsaved
    def zones_from_zone_names(self) -> None:
        self._zones_from_zone_names = dict()

    @property
    def tree(self) -> dict:
        return self._tree

    @tree.setter
    @mark_as_unsaved
    def tree(self, tree: dict) -> None:
        self._tree = tree

    @tree.deleter
    @mark_as_unsaved
    def tree(self) -> None:
        self._tree = dict()

    @property
    def numbers_from_tree(self) -> dict:
        return self._numbers_from_tree

    @numbers_from_tree.setter
    @mark_as_unsaved
    def numbers_from_tree(self, numbers_from_tree: dict) -> None:
        self._numbers_from_tree = numbers_from_tree

    @numbers_from_tree.deleter
    @mark_as_unsaved
    def numbers_from_tree(self) -> None:
        self._numbers_from_tree = dict()

    @property
    def split_numbers(self) -> dict:
        return self._split_numbers

    @split_numbers.setter
    @mark_as_unsaved
    def split_numbers(self, split_numbers: dict) -> None:
        self._split_numbers = split_numbers

    @split_numbers.deleter
    @mark_as_unsaved
    def split_numbers(self) -> None:
        self._split_numbers = dict()

    @property
    def number_from_split_number(self) -> dict:
        return self._number_from_split_number

    @number_from_split_number.setter
    @mark_as_unsaved
    def number_from_split_number(self, number_from_split_number: dict) -> None:
        self._number_from_split_number = number_from_split_number

    @number_from_split_number.deleter
    @mark_as_unsaved
    def number_from_split_number(self) -> None:
        self._number_from_split_number = dict()

    @property
    def intersects_shapes_in_zones(self) -> dict:
        return self._intersects_shapes_in_zones

    @intersects_shapes_in_zones.setter
    @mark_as_unsaved
    def intersects_shapes_in_zones(self, intersects_shapes_in_zones: dict) -> None:
        self._intersects_shapes_in_zones = intersects_shapes_in_zones

    @intersects_shapes_in_zones.deleter
    @mark_as_unsaved
    def intersects_shapes_in_zones(self) -> None:
        self._intersects_shapes_in_zones = dict()

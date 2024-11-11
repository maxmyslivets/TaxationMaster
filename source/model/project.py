import os
import pickle
import shutil
from pathlib import Path

from ezdxf.entities import Text, MText, Line, LWPolyline


class Entity:
    numbers: list[Text | MText] = None
    lines: list[Line | LWPolyline] = None
    contours: list[LWPolyline] = None
    zones: list[Text | MText | LWPolyline] = None

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)


class TaxationPlan:

    _dir_dwg: Path = None
    _dir_dxf: Path = None
    _path_dwg: Path = None
    _path_dxf: Path = None

    entity: Entity = None

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

import os
import tempfile
from pathlib import Path
import platform

import configobj


def _get_system32() -> Path:
    is_wow64 = (platform.architecture()[0] == '32bit' and 'ProgramFiles(x86)' in os.environ)
    return Path(os.path.join(os.environ['SystemRoot'], 'SysNative' if is_wow64 else 'System32'))


class Config:

    def __init__(self, path: Path = Path("config.ini")) -> None:
        self.path = path
        if not self.path.exists():
            self.default_setup()
        self.config = configobj.ConfigObj(str(self.path), list_values=True, encoding='utf-8')

    def save(self) -> None:
        self.config.filename = str(self.path)
        self.config.write()

    def reload(self) -> None:
        self.config = configobj.ConfigObj(str(self.path), list_values=True, encoding='utf-8')

    def default_setup(self) -> None:
        self.config = configobj.ConfigObj(list_values=True, encoding='utf-8')
        self.config["system"] = {}
        self.config["user"] = {}
        # temp_path
        self.config["system"]["temp_path"] = str(Path(tempfile.gettempdir()) / "TaxationTool")
        # converter
        self.config["system"]["temp_path_convert_input"] = str(Path(self.config["system"]["temp_path"]) / "convert" / "input")
        self.config["system"]["temp_path_convert_output"] = str(Path(self.config["system"]["temp_path"]) / "convert" / "output")
        self.config["system"]["oda_converter_path"] = str(_get_system32() / "ODAFileConverter.exe")
        self.config["system"]["timeout"] = 10
        # taxation_plan
        self.config["user"]["numbers_layers"] = ["номера"]
        self.config["user"]["lines_layers"] = ["полосы"]
        self.config["user"]["contours_layers"] = ["контуры"]
        self.config["user"]["zones_layers"] = ["зоны"]
        self.config["user"]["min_distance"] = 0.01
        self.config["user"]["min_area"] = 0.01
        self.save()

    @property
    def temp_path(self) -> Path:
        return Path(self.config["system"]["temp_path"])

    @temp_path.setter
    def temp_path(self, path: str | Path) -> None:
        self.config["system"]["temp_path"] = path if isinstance(path, str) else str(path)

    @property
    def temp_path_convert_input(self) -> Path:
        return Path(self.config["system"]["temp_path_convert_input"])

    @temp_path_convert_input.setter
    def temp_path_convert_input(self, path: str | Path) -> None:
        self.config["system"]["temp_path_convert_input"] = path if isinstance(path, str) else str(path)

    @property
    def temp_path_convert_output(self) -> Path:
        return Path(self.config["system"]["temp_path_convert_output"])

    @temp_path_convert_output.setter
    def temp_path_convert_output(self, path: str | Path) -> None:
        self.config["system"]["temp_path_convert_output"] = path if isinstance(path, str) else str(path)

    @property
    def oda_converter_path(self) -> Path:
        return Path(self.config["system"]["oda_converter_path"])

    @oda_converter_path.setter
    def oda_converter_path(self, path: str | Path) -> None:
        self.config["system"]["oda_converter_path"] = path if isinstance(path, str) else str(path)

    @property
    def timeout(self) -> int:
        return int(self.config["system"]["timeout"])

    @timeout.setter
    def timeout(self, seconds: int) -> None:
        self.config["system"]["timeout"] = seconds

    @property
    def numbers_layers(self) -> list[str]:
        return self.config["user"]["numbers_layers"]

    @numbers_layers.setter
    def numbers_layers(self, numbers_layers: list[str]) -> None:
        self.config["user"]["numbers_layers"] = numbers_layers

    @property
    def lines_layers(self) -> list[str]:
        return self.config["user"]["lines_layers"]

    @lines_layers.setter
    def lines_layers(self, lines_layers: list[str]) -> None:
        self.config["user"]["lines_layers"] = lines_layers

    @property
    def contours_layers(self) -> list[str]:
        return self.config["user"]["contours_layers"]

    @contours_layers.setter
    def contours_layers(self, contours_layers: list[str]) -> None:
        self.config["user"]["contours_layers"] = contours_layers

    @property
    def zones_layers(self) -> list[str]:
        return self.config["user"]["zones_layers"]

    @zones_layers.setter
    def zones_layers(self, zones_layers: list[str]) -> None:
        self.config["user"]["zones_layers"] = zones_layers

    @property
    def min_distance(self) -> float:
        return float(self.config["user"]["min_distance"])

    @min_distance.setter
    def min_distance(self, min_distance: float) -> None:
        self.config["user"]["min_distance"] = min_distance

    @property
    def min_area(self) -> float:
        return float(self.config["user"]["min_area"])

    @min_area.setter
    def min_area(self, min_area: float) -> None:
        self.config["user"]["min_area"] = min_area

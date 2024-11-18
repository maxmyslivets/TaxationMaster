import shutil
from pathlib import Path

from shapely import Point, LineString


class ProjectData:
    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    def suffix(self) -> str:
        return ".ttpr"

    @property
    def name(self) -> str:
        return self.path.stem

    # @property
    # def dir(self) -> Path:
    #     return self.path.parent / self.name


# class _Dict(dict):
#     """Кастомный словарь, уведомляющий об изменениях"""
#     def __init__(self, *args, on_change=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._on_change = on_change
#
#     def _notify_change(self):
#         """Вызывает уведомление об изменении"""
#         if self._on_change:
#             self._on_change()
#
#     # Переопределение методов изменения данных
#     def __setitem__(self, key, value):
#         super().__setitem__(key, value)
#         self._notify_change()
#
#     def __delitem__(self, key):
#         super().__delitem__(key)
#         self._notify_change()
#
#     def pop(self, key, *args):
#         result = super().pop(key, *args)
#         self._notify_change()
#         return result
#
#     def popitem(self):
#         result = super().popitem()
#         self._notify_change()
#         return result
#
#     def clear(self):
#         super().clear()
#         self._notify_change()
#
#     def update(self, *args, **kwargs):
#         super().update(*args, **kwargs)
#         self._notify_change()
#
#     def setdefault(self, key, default=None):
#         result = super().setdefault(key, default)
#         self._notify_change()
#         return result
#
#
# class _List(list):
#     """Кастомный список, уведомляющий об изменениях"""
#     def __init__(self, *args, on_change=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._on_change = on_change
#
#     def _notify_change(self):
#         """Вызов уведомления, если передан обработчик"""
#         if self._on_change:
#             self._on_change()
#
#     # Переопределение методов изменения данных
#     def __setitem__(self, index, value):
#         super().__setitem__(index, value)
#         self._notify_change()
#
#     def __delitem__(self, index):
#         super().__delitem__(index)
#         self._notify_change()
#
#     def append(self, value):
#         super().append(value)
#         self._notify_change()
#
#     def extend(self, iterable):
#         super().extend(iterable)
#         self._notify_change()
#
#     def insert(self, index, value):
#         super().insert(index, value)
#         self._notify_change()
#
#     def pop(self, index=-1):
#         result = super().pop(index)
#         self._notify_change()
#         return result
#
#     def remove(self, value):
#         super().remove(value)
#         self._notify_change()
#
#     def clear(self):
#         super().clear()
#         self._notify_change()
#
#     def sort(self, *args, **kwargs):
#         super().sort(*args, **kwargs)
#         self._notify_change()
#
#     def reverse(self):
#         super().reverse()
#         self._notify_change()
#
#     def __iadd__(self, other):
#         result = super().__iadd__(other)
#         self._notify_change()
#         return result
#
#     def __imul__(self, other):
#         result = super().__imul__(other)
#         self._notify_change()
#         return result


class Project:

    class TaxationPlan:
        """Данные чертежа таксации"""
        def __init__(self):
            self.numbers = dict()                           # key: k_number         value: number
            self.numbers_position = dict()                  # key: k_number         value: position
            self.shapes = dict()                            # key: k_shape          value: shape
            self.numbers_from_shape = dict()                # key: k_shape          value: list[k_number]
            self.tree = dict()                              # key: k_tree           value: position
            self.numbers_from_tree = dict()                 # key: k_tree           value: k_number
            self.split_numbers = dict()                     # key: k_split_number   value: split_number
            self.number_from_split_number = dict()          # key: k_split_number   value: list[k_number]
            self.table_data = list()                        # [[number, type_shape, value, unit],...]

    class TaxationList:
        """Данные ведомости таксации"""
        def __init__(self):
            pass

    taxation_plan: TaxationPlan
    taxation_list: TaxationList

    def __init__(self):

        self.is_saved: bool = True

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)

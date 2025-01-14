import traceback
from typing import Callable, Optional

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QStatusBar, QTextEdit


class ConsoleOutputRedirector:
    """
    Перенаправляет вывод stdout и stderr в текстовый виджет.
    append_callback: QTextEdit.append
    """
    def __init__(self, console: QTextEdit, type_text) -> None:
        self.console = console
        self.type_text = type_text

    def write(self, text: str) -> None:
        if text.strip():
            self.console.append(text)

    def flush(self):
        pass


class Progress:
    """
    Класс для управления прогрессом.
    Принимает общее количество шагов и рассчитывает прогресс в процентах.
    """

    def __init__(self, callback: Callable, callback2: Optional[Callable] = None,
                 status_bar: Optional[QStatusBar] = None) -> None:
        self.callback = callback
        self._total = 0
        self._current = 0
        self._status_bar = status_bar
        self.progress = None
        if callback2 is not None:
            self.progress = Progress(callback2)

    @property
    def total(self) -> int:
        return self._total

    @total.setter
    def total(self, value: int) -> None:
        self._total = value
        self._current = 0

    @property
    def status(self) -> None:
        return

    @status.setter
    def status(self, text: str) -> None:
        print(text)
        self._status_bar.showMessage(text)

    def next(self) -> None:
        """
        Обновляет текущий шаг на 1 и вычисляет прогресс.
        """
        self.update(self._current + 1)

    def update(self, value: int | float) -> None:
        """
        Обновляет текущий шаг и вычисляет прогресс.

        Args:
            value (int | float): Текущий значение (от 0 до total_steps).
        """
        assert 0 <= value <= self._total, (f"Ошибка ProgressBar, указанное значение {value}. Значение должно "
                                           f"находиться между 0 и {self._total}.")
        assert self._total != 0, f"Ошибка ProgressBar, указано максимальное значение: {self._total}."
        self._current = value
        self.callback((self._current / self._total) * 100)
        if (self._current / self._total) * 100 == 100 and self._status_bar is not None:
            self.status = 'Готово'

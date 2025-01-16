from PySide6.QtWidgets import QTextEdit, QHBoxLayout, QLabel, QProgressBar, QBoxLayout, QVBoxLayout, QWidget
from PySide6 import QtGui


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


class ProgressWidget(QWidget):
    """
    Виджет прогресса
    """

    def __init__(self, parent: QVBoxLayout, info: str, maximum: int = 100) -> None:
        """
        Args:
            parent (QBoxLayout): Родительский слой
            info (str): Текст прогресса
            maximum (int): Максимальное значение прогресса
        """
        super().__init__()
        self.parent_layout = parent
        self.maximum = maximum

        self.progress_layout = QHBoxLayout()
        self.progress_layout.setContentsMargins(0, 0, 0, 0)

        self.progress_layout.addWidget(QLabel(info))

        self.progress = QProgressBar()
        self.progress.setMaximum(self.maximum)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFormat(u"%v/%m")

        self.progress_layout.addWidget(self.progress)

        self.parent_layout.addLayout(self.progress_layout)

    def next(self) -> None:
        """
        Обновляет текущий шаг на 1.
        """
        self.set_value(self.progress.value() + 1)

    def set_value(self, value: int) -> None:
        """
        Обновляет текущий шаг.

        Args:
            value (int): Значение от 0 до maximum.
        """
        if not (0 <= value <= self.progress.maximum()):
            print(f"Ошибка ProgressBar, указанное значение {value}. Допустимый диапазон 0-{self.progress.maximum()}.")
        self.progress.setValue(value)
        if self.progress.value() == self.progress.maximum():
            self.delete()
        QtGui.QGuiApplication.processEvents()

    def delete(self) -> None:
        """
        Удаляет виджет прогресса.
        """
        for i in reversed(range(self.progress_layout.count())):
            widget = self.progress_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.progress_layout.setParent(None)
        self.setParent(None)


class ProgressManager:
    """
    Класс для управления прогрессом.
    Принимает общее количество шагов и рассчитывает прогресс в процентах.
    """

    def __init__(self, parent: QVBoxLayout) -> None:
        self.parent_layout = parent

    def new(self, info: str, maximum: int = 100) -> ProgressWidget:
        """
        Создать новый прогресс.
        Args:
            info (str): Текст прогресса
            maximum (int): Максимальное значение прогресса

        Returns:
            ProgressWidget: Виджет прогресса
        """
        return ProgressWidget(self.parent_layout, info, maximum)

import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QSplitter
from PySide6.QtCore import Qt

from .view.view import View
from .model.model import Model


class TaxationTool:
    def __init__(self, model, view, app):
        super(TaxationTool, self).__init__()

        self.model = model
        self.view = view
        self.app = app

        self.connect_signals()

        self.view.show()

        self.view.log("hello")

        splitter = QSplitter(Qt.Horizontal)


    def connect_signals(self) -> None:
        pass
        # self.view.pushButton_Calculate.clicked.connect(self.calculate)

    # def calculate(self):
    #     r = self.model.calculate()
    #     self.view.log(r)


def main():
    """
        Здесь мы создаем приложение и запускаем цикл событий Qt. Обратите внимание, что модель и представление
        создаются первыми, и что у них нет ссылок ни друг на друга, ни на ведущего. Это сделано специально.
        Если модель и представление хотят общаться с ведущим (или, в редких случаях, друг с другом),
        они должны использовать сигналы.
    """

    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    view = View()
    taxation_tool = TaxationTool(model, view, app)
    sys.exit(app.exec_())

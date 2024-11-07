import traceback

from PySide6.QtWidgets import QMainWindow
from .ui.ui_mainwindow import Ui_MainWindow


class View(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(View, self).__init__()

        self.setupUi(self)

    def log(self, text) -> None:
        try:
            self.console_log.append(str(text))
        except Exception:
            self.console_log.append(traceback.format_exc())

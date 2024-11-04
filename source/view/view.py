import traceback

from PySide6 import QtCore
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QMainWindow, QTreeWidgetItem
from .ui.ui_mainwindow import Ui_MainWindow


class View(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(View, self).__init__()

        self.setupUi(self)

        # item = QTreeWidgetItem(self.tree_manager)
        # print(self.tree_manager.findItems("Чертеж таксации (dxf)", QtCore.Qt.MatchContains)[0])

    def log(self, text) -> None:
        try:
            self.console_log.append(str(text))
        except Exception:
            self.console_log.append(traceback.format_exc())

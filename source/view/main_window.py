import traceback

from PySide6.QtWidgets import QMainWindow, QTreeWidget, QVBoxLayout, QSizePolicy, QFrame

from .custom_widgets import CustomTabWidget
from .ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.tab_widget = CustomTabWidget(self.centralwidget)
        # self.tab_widget.setStyleSheet(u"porder: none;\nbackground: transparent;\n")
        tab_widget_layout = QVBoxLayout(self.centralwidget)
        tab_widget_layout.setSpacing(0)
        tab_widget_layout.setContentsMargins(0, 0, 0, 0)
        tab_widget_layout.addWidget(self.tab_widget)

    def log(self, text: str) -> None:
        if text.startswith("[DEBUG]"):
            color = "green"
        elif text.startswith("[WARNING]"):
            color = "yellow"
        elif text.startswith("[ERROR]"):
            color = "red"
        else:
            color = None
        if color is not None:
            color_string = f"<p style='color:{color};'>{text}</p>"
        else:
            color_string = text
        try:
            self.console_log.append(color_string)
        except Exception:
            self.console_log.append(f"[ERROR]\n{traceback.format_exc()}")

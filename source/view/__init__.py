from source.view.dialog import ConfirmCloseUnsavedProject
from source.view.main_window import MainWindow
from source.view.settings import Settings


class View:
    def __init__(self):
        self.main_window = MainWindow()
        self.confirm_close_unsaved_project = ConfirmCloseUnsavedProject
        self.settings = Settings

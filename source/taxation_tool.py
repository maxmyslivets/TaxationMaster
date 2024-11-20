import sys

from PySide6 import QtWidgets, QtCore
from .view import View
from .model import Model
from .view.settings import Settings


class TaxationTool:
    def __init__(self, model, view, app):
        super(TaxationTool, self).__init__()
        # FIXME: Сделать вывод любых ошибок программы в console_log через декоратор

        self.model = model
        self.view = view
        self.app = app

        self.model.interface.create_new_project()

        self.connect_signals()

        self.view.main_window.show()

    def connect_signals(self) -> None:

        # Меню проекта
        self.view.main_window.menu_project_save_as.triggered.connect(self.model.interface.save_as_project)
        self.view.main_window.menu_project_save.triggered.connect(self.model.interface.save_project)
        self.view.main_window.menu_project_new.triggered.connect(self.model.interface.create_new_project)
        self.view.main_window.menu_project_open.triggered.connect(self.model.interface.open_project)
        self.view.main_window.menu_project_import_taxation_plan.triggered.connect(
            self.model.interface.import_taxation_plan)
        self.view.main_window.menu_project_import_taxation_list.triggered.connect(
            self.model.interface.import_taxation_list)

        # Меню обработки
        # self.view.main_window.menu_processing_preprocessing.triggered.connect(self.model.interface.preprocessing)

        # Меню настроек
        self.view.main_window.menu_settings_settings.triggered.connect(Settings)
        self.view.main_window.menu_settings_settings.triggered.connect(
            lambda config: Settings(self.model.config))

        # Менеджер проекта
        manager_project = self.view.main_window.tree_manager
        manager_project.itemDoubleClicked.connect(self.model.interface.project_manager_double_clicked)
        manager_project.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        manager_project.customContextMenuRequested.connect(self.model.interface.project_manager_context_menu)

        # Таблица
        # table = self.view.main_window.table
        # table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # table.customContextMenuRequested.connect(self.model.interface.table_context_menu)


def run():
    app = QtWidgets.QApplication(sys.argv)
    view = View()
    model = Model(view)
    TaxationTool(model, view, app)
    sys.exit(app.exec_())

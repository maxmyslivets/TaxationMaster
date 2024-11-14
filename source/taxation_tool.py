import sys

from PySide6 import QtWidgets
from .view import View
from .model import Model


class TaxationTool:
    def __init__(self, model, view, app):
        super(TaxationTool, self).__init__()

        self.model = model
        self.view = view
        self.app = app

        self.view.main_window.tree_manager.expandAll()

        self.model.interface.create_new_project()

        self.connect_signals()

        self.view.main_window.show()

    def connect_signals(self) -> None:
        self.view.main_window.menu_project_save_as.triggered.connect(self.model.interface.save_as_project)
        self.view.main_window.menu_project_save.triggered.connect(self.model.interface.save_project)
        self.view.main_window.menu_project_new.triggered.connect(self.model.interface.create_new_project)
        self.view.main_window.menu_project_open.triggered.connect(self.model.interface.open_project)

        self.view.main_window.menu_project_import_taxation_plan.triggered.connect(self.model.interface.import_dwg_taxation)

        self.view.main_window.menu_processing_preprocessing.triggered.connect(self.model.interface.preprocessing)


def run():
    app = QtWidgets.QApplication(sys.argv)
    view = View()
    model = Model(view)
    TaxationTool(model, view, app)
    sys.exit(app.exec_())

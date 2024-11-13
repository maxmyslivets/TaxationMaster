import sys

from PySide6 import QtWidgets
from .view.view import View
from .model import Model


class TaxationTool:
    def __init__(self, model, view, app):
        super(TaxationTool, self).__init__()

        self.model = model
        self.view = view
        self.app = app

        self.view.tree_manager.expandAll()

        self.model.interface.create_new_project()

        self.connect_signals()

        self.view.show()

    def connect_signals(self) -> None:
        self.view.menu_project_save_as.triggered.connect(self.model.interface.save_as_project)
        self.view.menu_project_save.triggered.connect(self.model.interface.save_project)
        self.view.menu_project_new.triggered.connect(self.model.interface.create_new_project)
        self.view.menu_project_open.triggered.connect(self.model.interface.open_project)

        self.view.menu_project_import.triggered.connect(self.model.interface.import_dwg_taxation)
        self.view.menu_processing_converting_to_dxf.triggered.connect(self.model.interface.convert_dwg_taxation_to_dxf)
        self.view.menu_processing_load_dxf.triggered.connect(self.model.interface.load_dxf_taxation)

        self.view.menu_processing_classification.triggered.connect(self.model.interface.process_classification)


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = View()
    model = Model(view)
    TaxationTool(model, view, app)
    sys.exit(app.exec_())

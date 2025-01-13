from PySide6.QtWidgets import QApplication, QMainWindow

from src.model import Model
from src.ui.ui_mainwindow import Ui_MainWindow

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup_toolbars()

    def setup_toolbars(self):
        self.ui.action_open_excel_template.triggered.connect(Model.open_excel_template)
        self.ui.action_import_taxation_list.triggered.connect(Model.insert_word_taxation_list)
        self.ui.action_import_topographic_plan.triggered.connect(Model.insert_taxation_data_from_autocad)
        self.ui.action_get_count_tree.triggered.connect(Model.get_count_tree)
        self.ui.action_identification_shrub.triggered.connect(Model.identification_shrub)
        self.ui.action_validation.triggered.connect(Model.validation)
        self.ui.action_replace_comma_to_dot.triggered.connect(Model.replace_comma_to_dot)
        self.ui.action_replace_dot_comma_to_comma.triggered.connect(Model.replace_dot_comma_to_comma)
        self.ui.action_compare_numbers.triggered.connect(Model.compare_numbers)
        self.ui.action_insert_taxation_list_orm.triggered.connect(Model.insert_taxation_list_orm)
        self.ui.action_insert_zones.triggered.connect(Model.insert_zones_from_autocad)
        self.ui.action_insert_protected_zones.triggered.connect(Model.insert_protected_zones_from_autocad)
        self.ui.action_insert_zone_objects.triggered.connect(Model.insert_zone_objects)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

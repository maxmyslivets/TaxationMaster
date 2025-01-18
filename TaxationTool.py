import sys
import traceback

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QMainWindow
from win32api import ExitWindows

from src.model import Model
from src.ui.additional import ConsoleOutputRedirector, ProgressManager
from src.ui.ui_mainwindow import Ui_TaxationTool


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_TaxationTool()
        self.ui.setupUi(self)

        self.setup_console()
        self.setup_toolbars()
        self.setup_input_validators()

        self.progress_manager = ProgressManager(self.ui.progress_layout)


    def setup_toolbars(self) -> None:
        self.ui.action_open_excel_template.triggered.connect(lambda x: Model.open_excel_template(self))
        self.ui.action_import_taxation_list.triggered.connect(lambda x: Model.insert_word_taxation_list(self))
        self.ui.action_import_topographic_plan.triggered.connect(lambda x: Model.insert_taxation_data_from_autocad(self))
        self.ui.action_get_count_tree.triggered.connect(lambda x: Model.get_count_tree(self))
        self.ui.action_identification_shrub.triggered.connect(lambda x: Model.identification_shrub(self))
        self.ui.action_validation.triggered.connect(lambda x: Model.validation(self))
        self.ui.action_replace_comma_to_dot.triggered.connect(lambda x: Model.replace_comma_to_dot(self))
        self.ui.action_replace_dot_comma_to_comma.triggered.connect(lambda x: Model.replace_dot_comma_to_comma(self))
        self.ui.action_compare_numbers.triggered.connect(lambda x: Model.compare_numbers(self))
        self.ui.action_insert_taxation_list_orm.triggered.connect(lambda x: Model.insert_taxation_list_orm(self))
        self.ui.action_insert_zones.triggered.connect(lambda x: Model.insert_zones_from_autocad(self))
        self.ui.action_insert_protected_zones.triggered.connect(lambda x: Model.insert_protected_zones_from_autocad(self))
        self.ui.action_insert_zone_objects.triggered.connect(lambda x: Model.insert_zone_objects(self))
        self.ui.action_kmean_numeration.triggered.connect(lambda x: Model.generate_numeration(self))
        self.ui.action_removable_or_transplantable.triggered.connect(lambda x: Model.removable_or_transplantable(self))
        self.ui.action_calc_compensatory_landings.triggered.connect(lambda x: Model.insert_calculation_landings(self))
        self.ui.action_calc_compensatory_payments.triggered.connect(lambda x: Model.insert_calculation_payments(self))
        self.ui.action_insert_numbers_to_dxf.triggered.connect(lambda x: Model.insert_numbers_to_autocad(self))

    def closeEvent(self, event) -> None:
        """
        Восстанавливает стандартный вывод при закрытии приложения.
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        super().closeEvent(event)
        raise KeyboardInterrupt("Закрыто пользователем")

    def setup_console(self):
        """
        Перенаправляет вывод консоли
        """
        sys.stdout = ConsoleOutputRedirector(self.ui.textEdit, 'info')
        sys.excepthook = self.global_exception_handler

    def global_exception_handler(self, exctype, value, tb):
        """
        Глобальный обработчик необработанных исключений.
        Выводит traceback в QTextEdit.
        """
        # Форматируем traceback
        error_text = "".join(traceback.format_exception(exctype, value, tb))
        # Добавляем текст в QTextEdit
        self.ui.textEdit.setTextColor("red")
        self.ui.textEdit.append(error_text)
        self.ui.textEdit.setTextColor("white")
        # Также отправляем исключение в стандартный вывод ошибок
        sys.__excepthook__(exctype, value, tb)

    def setup_input_validators(self) -> None:
        """
        Задает правило ввода только цифр
        """
        rx = QRegularExpression("\d+")
        self.ui.lineEdit_start_numeration.setValidator(QRegularExpressionValidator(rx))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QSpinBox
from .ui.ui_configuration_import import Ui_Dialog


class ConfigurationImport(QDialog, Ui_Dialog):
    def __init__(self, taxation_list_data: list[list[str]]) -> None:
        super().__init__()

        self.setupUi(self)

        self._taxation_list_data = taxation_list_data

        self._connect_signals()
        self._set_data_in_table()

        self.exec_()

    def _connect_signals(self) -> None:
        self.checkBox_import_first_row.stateChanged.connect(self._set_data_in_table)
        self.spinBox_number.valueChanged.connect(
            lambda x: self._reorder_columns(self.spinBox_number, "Номер точки"))
        self.spinBox_name.valueChanged.connect(
            lambda x: self._reorder_columns(self.spinBox_name, "Наименование"))
        self.spinBox_quantity.valueChanged.connect(
            lambda x: self._reorder_columns(self.spinBox_quantity, "Количество"))
        self.spinBox_height.valueChanged.connect(
            lambda x: self._reorder_columns(self.spinBox_height, "Высота"))
        self.spinBox_diameter.valueChanged.connect(
            lambda x: self._reorder_columns(self.spinBox_diameter, "Диаметр"))
        self.spinBox_quality.valueChanged.connect(
            lambda x: self._reorder_columns(self.spinBox_quality, "Состояние"))

    def _set_data_in_table(self) -> None:
        taxation_list_data = self._taxation_list_data.copy()

        if not self.checkBox_import_first_row.isChecked():
            taxation_list_data.pop(0)

        for idx, data in enumerate(taxation_list_data[:20]):
            number, name, quantity, height, diameter, quality = data
            items = [
                QTableWidgetItem(str(number)),
                QTableWidgetItem(str(name)),
                QTableWidgetItem(str(quantity)),
                QTableWidgetItem(str(height)),
                QTableWidgetItem(str(diameter)),
                QTableWidgetItem(str(quality)),
            ]

            for col, item in enumerate(items):
                self.table_preshow.setItem(idx, col, item)

        self.table_preshow.setEditTriggers(QTableWidget.NoEditTriggers)

    def _reorder_columns(self, spinbox: QSpinBox, header: str) -> None:

        column_order = {
            self.spinBox_number.value() - 1: "Номер точки",
            self.spinBox_name.value() - 1: "Наименование",
            self.spinBox_quantity.value() - 1: "Количество",
            self.spinBox_height.value() - 1: "Высота",
            self.spinBox_diameter.value() - 1: "Диаметр",
            self.spinBox_quality.value() - 1: "Состояние",
        }

        for col_idx in range(self.table_preshow.columnCount()):
            try:
                self.table_preshow.setHorizontalHeaderItem(col_idx, QTableWidgetItem(column_order[col_idx]))
            except KeyError:
                self.table_preshow.setHorizontalHeaderItem(col_idx, QTableWidgetItem(""))
        self.table_preshow.setHorizontalHeaderItem(spinbox.value() - 1, QTableWidgetItem(header))

    @property
    def parameters(self) -> dict | None:

        parameters = {
            "number": self.spinBox_number.value() - 1,
            "name": self.spinBox_name.value() - 1,
            "quantity": self.spinBox_quantity.value() - 1,
            "height": self.spinBox_height.value() - 1,
            "diameter": self.spinBox_diameter.value() - 1,
            "quality": self.spinBox_quality.value() - 1
        }

        # Проверяем на наличие дубликатов
        if len(set(parameters.values())) != len(parameters.values()):
            QMessageBox.warning(self, "Ошибка", "Колонки не могут находиться на одинаковых позициях.")
            return None
        else:
            parameters["is_import_first_row"] = self.checkBox_import_first_row.isChecked()

        return parameters if self.result() else None

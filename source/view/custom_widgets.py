from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QComboBox, QTabWidget, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMenu


class EditableComboBox(QComboBox):
    def __init__(self, items: list[str], value: str, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.addItems(items)
        self.lineEdit().setText(value)
        self.lineEdit().textChanged.connect(self.validate_text)

    def wheelEvent(self, event):
        # Игнорируем событие прокрутки
        event.ignore()

    def validate_text(self, text):
        # Проверяем, есть ли элементы, начинающиеся с введенного текста
        matching_items = [item for item in [self.itemText(i) for i in range(self.count())] if item.startswith(text)]

        # Если совпадений нет, обрезаем последний символ
        if not matching_items:
            self.lineEdit().setText(text[:-1])


# class _TableCustomItem(QTableWidgetItem):
#     dict_name: str
#     dict_key: str|int
#
#     def set_dict_data(self, dict_name: str, dict_key: str|int) -> None:
#         self.dict_name = dict_name
#         self.dict_key = dict_key


# class Custom


class CustomTabWidget(QTabWidget):
    """
    Возможности класса:
    - При нажатии на кнопку закрытия вкладки, вкладка скрывается
    - При вызове вкладки, на таблице отображаются данные, которые были на ней перед закрытием
    - При новом импорте данных, таблица на вкладке обновляется
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)  # Добавить кнопку закрытия на табы
        self.tabCloseRequested.connect(self.hide_tab)

        # Словарь для скрытых табов
        self.hidden_tabs = {}

        self.tab_taxation_plan = QTabWidget()
        self.tab_taxation_list = QTabWidget()

        self.table_taxation_plan = QTableWidget(0, 5)
        self.table_taxation_plan.setHorizontalHeaderLabels(
            ["Номер", "Исх.Номер", "Тип", "Значение", "Ед.изм."])
        self.table_taxation_list = QTableWidget(0, 7)
        self.table_taxation_list.setHorizontalHeaderLabels(
            ["Номер", "Исх.Номер", "Наименование", "Количество", "Диаметр", "Высота", "Состояние"])

        for tab, title, table in ((self.tab_taxation_plan, "Чертеж таксации", self.table_taxation_plan),
                                  (self.tab_taxation_list, "Ведомость таксации", self.table_taxation_list)):
            layout = QVBoxLayout(tab)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            self.addTab(tab, title)
            layout.addWidget(table)
            table.setContextMenuPolicy(Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(self.table_context_menu)

        for index in range(self.count()):
            self.hide_tab(0)

        self.all_numbers_taxation_plan = []
        self.all_numbers_taxation_list = []

    def open_tab(self, title: str) -> None:
        """Создает таб с указанным названием или открывает его, если он уже существует."""
        # Если таб уже существует, отображаем его
        for index in range(self.count()):
            if self.tabText(index) == title:
                self.setCurrentIndex(index)
                return

        # Если таб скрыт, восстанавливаем его
        if title in self.hidden_tabs:
            widget = self.hidden_tabs.pop(title)
            index = self.addTab(widget, title)
            self.setCurrentIndex(index)
            return

        # Создаем новый таб
        new_tab = QTabWidget()
        layout = QVBoxLayout(new_tab)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addTab(new_tab, title)
        self.setCurrentWidget(new_tab)

    def hide_tab(self, index: int) -> None:
        """Скрывает таб, но не удаляет его."""
        title = self.tabText(index)
        widget = self.widget(index)
        self.hidden_tabs[title] = widget
        self.removeTab(index)

    def update_data_to_table(self, data: list, tab_name: str) -> None:

        tab: QTabWidget | QWidget | None = None
        for i in range(self.count()):
            if self.tabText(i) == tab_name:
                tab = self.widget(i)
        if tab is None:
            return

        if tab is self.tab_taxation_plan:
            self.all_numbers_taxation_plan = [number for _, number, _, _, _ in data]
            self.table_taxation_plan.setRowCount(0)
            for split_number, number, type_shape, value, unit in data:
                item_split_number = QTableWidgetItem(split_number)
                cell_widget_number = EditableComboBox(self.all_numbers_taxation_plan, number)
                item_type_shape = QTableWidgetItem(type_shape)
                item_value = QTableWidgetItem(value)
                item_unit = QTableWidgetItem(unit)

                row_position = self.table_taxation_plan.rowCount()
                self.table_taxation_plan.insertRow(row_position)

                self.table_taxation_plan.setItem(row_position, 0, item_split_number)
                self.table_taxation_plan.setCellWidget(row_position, 1, cell_widget_number)
                self.table_taxation_plan.setItem(row_position, 2, item_type_shape)
                self.table_taxation_plan.setItem(row_position, 3, item_value)
                self.table_taxation_plan.setItem(row_position, 4, item_unit)

                item_type_shape.setFlags(item_type_shape.flags() & ~Qt.ItemIsEditable)
                item_value.setFlags(item_value.flags() & ~Qt.ItemIsEditable)
                item_unit.setFlags(item_unit.flags() & ~Qt.ItemIsEditable)

        elif tab is self.tab_taxation_list:
            self.all_numbers_taxation_list = [number for _, number, _, _, _, _, _ in data]
            for split_number, number, name, quantity, height, diameter, quality in data:
                item_split_number = QTableWidgetItem(split_number)
                cell_widget_number = EditableComboBox(self.all_numbers_taxation_list, number)
                item_name = QTableWidgetItem(name)
                item_quantity = QTableWidgetItem(quantity)
                item_height = QTableWidgetItem(height)
                item_diameter = QTableWidgetItem(diameter)
                item_quality = QTableWidgetItem(quality)

                row_position = self.table_taxation_list.rowCount()
                self.table_taxation_list.insertRow(row_position)

                self.table_taxation_list.setItem(row_position, 0, item_split_number)
                self.table_taxation_list.setCellWidget(row_position, 1, cell_widget_number)
                self.table_taxation_list.setItem(row_position, 2, item_name)
                self.table_taxation_list.setItem(row_position, 3, item_quantity)
                self.table_taxation_list.setItem(row_position, 4, item_height)
                self.table_taxation_list.setItem(row_position, 5, item_diameter)
                self.table_taxation_list.setItem(row_position, 6, item_quality)

                item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
                item_quantity.setFlags(item_quantity.flags() & ~Qt.ItemIsEditable)
                item_height.setFlags(item_height.flags() & ~Qt.ItemIsEditable)
                item_diameter.setFlags(item_diameter.flags() & ~Qt.ItemIsEditable)
                item_quality.setFlags(item_quality.flags() & ~Qt.ItemIsEditable)

    def current_table(self) -> QTableWidget | None:
        if self.currentWidget() is self.tab_taxation_plan:
            return self.table_taxation_plan
        elif self.currentWidget() is self.tab_taxation_list:
            return self.table_taxation_list
        else:
            return

    def table_context_menu(self, pos) -> None:
        table = self.current_table()
        if table is None:
            return
        # Определяем строку, где было вызвано меню
        index = table.indexAt(pos)
        if not index.isValid():
            return  # Игнорируем, если клик был вне таблицы

        row = index.row()

        # Создаем контекстное меню
        menu = QMenu(table)
        split_row_action = menu.addAction("Разделить строку")
        delete_row_action = menu.addAction("Удалить строку")
        apply_action = menu.addAction("Подтвердить")

        # Обработка нажатия на пункт меню
        split_row_action.triggered.connect(lambda: self.split_table_row(row))
        delete_row_action.triggered.connect(lambda: self.delete_table_row(row))
        apply_action.triggered.connect(lambda: self.apply_table_row(row))

        # Показываем меню
        menu.exec_(table.viewport().mapToGlobal(pos))

    def split_table_row(self, row):
        table = self.current_table()
        if table is None:
            return
        # Копируем данные из текущей строки
        copied_data = [table.item(row, col).text() if table.item(row, col) else "" for col in range(table.columnCount())]
        # Вставляем новую строку ниже текущей
        table.insertRow(row + 1)

        # Заполняем новую строку скопированными данными
        for col, data in enumerate(copied_data):
            new_item = QTableWidgetItem(data)
            new_item.setForeground(QBrush(QColor(255, 255, 0)))  # Устанавливаем желтый цвет текста
            table.setItem(row + 1, col, new_item)

        if self.currentWidget() is self.tab_taxation_plan:
            combobox_number = EditableComboBox(
                self.all_numbers_taxation_plan, table.cellWidget(row, 1).currentText())
            table.setCellWidget(row + 1, 1, combobox_number)

        elif self.currentWidget() is self.tab_taxation_list:
            combobox_number = EditableComboBox(
                self.all_numbers_taxation_list, table.cellWidget(row, 1).currentText())
            table.setCellWidget(row + 1, 1, combobox_number)

    def delete_table_row(self, row):
        pass

    def apply_table_row(self, row):
        pass

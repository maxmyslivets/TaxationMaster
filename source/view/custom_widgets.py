from PySide6.QtWidgets import QComboBox, QTabWidget, QWidget, QVBoxLayout, QLabel, QTableWidget


class EditableComboBox(QComboBox):
    def __init__(self, items: list[str], value: str, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.addItems(items)
        self.lineEdit().setText(value)
        self.lineEdit().textChanged.connect(self.validate_text)

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)  # Добавить кнопку закрытия на табы
        self.tabCloseRequested.connect(self.hide_tab)

        # Словарь для скрытых табов
        self.hidden_tabs = {}

    def create_or_open_tab(self, title: str) -> bool:
        """Создает таб с указанным названием или открывает его, если он уже существует."""
        # Если таб уже существует, отображаем его
        for index in range(self.count()):
            if self.tabText(index) == title:
                self.setCurrentIndex(index)
                return True

        # Если таб скрыт, восстанавливаем его
        if title in self.hidden_tabs:
            widget = self.hidden_tabs.pop(title)
            index = self.addTab(widget, title)
            self.setCurrentIndex(index)
            return False

        # Создаем новый таб
        new_tab = QTabWidget()
        layout = QVBoxLayout(new_tab)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(QLabel(f"Content of {title}"))
        self.addTab(new_tab, title)
        self.setCurrentWidget(new_tab)

    def get_open_tab_title(self) -> str:
        """Возвращает название открытого таба."""
        return self.tabText(self.currentIndex())

    def add_table_to_tab(self, table_widget: QTableWidget):
        """Добавляет указанный QTableWidget в текущий таб."""
        current_tab = self.currentWidget()
        if current_tab:
            layout = current_tab.layout()
            layout.addWidget(table_widget)

    def hide_tab(self, index: int):
        """Скрывает таб, но не удаляет его."""
        title = self.tabText(index)
        widget = self.widget(index)
        self.hidden_tabs[title] = widget
        self.removeTab(index)

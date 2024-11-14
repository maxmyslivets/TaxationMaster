from PySide6.QtWidgets import QDialog, QLineEdit, QFormLayout, QLabel, QDoubleSpinBox, QSpinBox
from .ui.ui_settings import Ui_Dialog
from ..model import Config


class Settings(QDialog, Ui_Dialog):
    # TODO: добавить фильтры на ввод настроек
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)

        self.buttonBox.accepted.connect(self.save_settings)

        self.buttonBox.buttons()[0].setText("Сохранить")
        self.buttonBox.buttons()[1].setText("Отмена")

        self.config = Config()

        # Вкладка пользовательских настройки

        tab_user_settings = QFormLayout(self.tab_user_settings)

        self.numbers_layers = QLineEdit(str(self.config.numbers_layers))
        tab_user_settings.addRow(QLabel("Слои с номерами таксации"), self.numbers_layers)
        self.lines_layers = QLineEdit(str(self.config.lines_layers))
        tab_user_settings.addRow(QLabel("Слои с полосами деревьев"), self.lines_layers)
        self.contours_layers = QLineEdit(str(self.config.contours_layers))
        tab_user_settings.addRow(QLabel("Слои с контурами растительности"), self.contours_layers)
        self.zones_layers = QLineEdit(str(self.config.zones_layers))
        tab_user_settings.addRow(QLabel("Слои с именами и полигонами зон"), self.zones_layers)
        self.min_distance = QDoubleSpinBox()
        self.min_distance.setValue(self.config.min_distance)
        self.min_distance.setSingleStep(0.01)
        tab_user_settings.addRow(QLabel("Максимальная длина линии присвоения номера, м"), self.min_distance)
        self.min_area = QDoubleSpinBox()
        self.min_area.setValue(self.config.min_area)
        self.min_area.setSingleStep(0.01)
        tab_user_settings.addRow(QLabel("Допуск максимальной площади перекрытия зон, м2"), self.min_area)

        # Вкладка системных настройки

        tab_system_settings = QFormLayout(self.tab_system_settings)

        self.temp_path = QLineEdit(str(self.config.temp_path))
        tab_system_settings.addRow(QLabel("Временная директория"), self.temp_path)
        self.temp_path_convert_input = QLineEdit(str(self.config.temp_path_convert_input))
        tab_system_settings.addRow(QLabel("Директория для выходного файла конвертера"), self.temp_path_convert_input)
        self.temp_path_convert_output = QLineEdit(str(self.config.temp_path_convert_output))
        tab_system_settings.addRow(QLabel("Директория для входного файла конвертера"), self.temp_path_convert_output)
        self.oda_converter_path = QLineEdit(str(self.config.oda_converter_path))
        tab_system_settings.addRow(QLabel("Расположение конвертера"), self.oda_converter_path)
        self.timeout = QSpinBox()
        self.timeout.setValue(self.config.timeout)
        tab_system_settings.addRow(QLabel("Лимит времени конвертирования, сек"), self.timeout)

        self.exec_()

    def save_settings(self) -> None:

        self.config.numbers_layers = eval(self.numbers_layers.text())
        self.config.lines_layers = eval(self.lines_layers.text())
        self.config.contours_layers = eval(self.contours_layers.text())
        self.config.zones_layers = eval(self.zones_layers.text())
        self.config.min_distance = float(self.min_distance.value())
        self.config.min_area = float(self.min_area.value())
        self.config.temp_path = self.temp_path.text()
        self.config.temp_path_convert_input = self.temp_path_convert_input.text()
        self.config.temp_path_convert_output = self.temp_path_convert_output.text()
        self.config.oda_converter_path = self.oda_converter_path.text()
        self.config.timeout = int(self.timeout.value())

        self.config.save()



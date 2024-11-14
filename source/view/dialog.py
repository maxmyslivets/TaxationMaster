from PySide6.QtWidgets import QMessageBox


class ConfirmCloseUnsavedProject(QMessageBox):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Подтвердите действие")
        self.setText("Проект не сохранен.\nПродолжить?")
        self.setIcon(QMessageBox.Icon.Warning)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.Yes)
        self.exec_()

    @property
    def result_yes(self) -> bool:
        return self.result() == QMessageBox.StandardButton.Yes

    @property
    def result_no(self) -> bool:
        return self.result() == QMessageBox.StandardButton.No

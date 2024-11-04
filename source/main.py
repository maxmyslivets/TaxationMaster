import os
import shutil
import sys
import tempfile
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from .view.view import View
from .model.model import Model


class TaxationTool:
    project: Path
    def __init__(self, model, view, app):
        super(TaxationTool, self).__init__()

        self.model = model
        self.view = view
        self.app = app

        self.temp_path = Path(tempfile.gettempdir()) / "TaxationTool"
        self.create_new_project()

        self.connect_signals()

        self.view.show()


    def connect_signals(self) -> None:
        self.view.menu_project_save_as.triggered.connect(self.save_project)
        self.view.menu_project_new.triggered.connect(self.create_new_project)
        self.view.menu_project_open.triggered.connect(self.open_project)

    def save_project(self) -> None:
        save_as = QFileDialog()
        save_as.setDefaultSuffix('.ttpr')
        project_path, _ = save_as.getSaveFileName(parent=self.view, caption="Сохранить как...", dir='/',
                                                  filter="Taxation tool project (*.ttpr)")
        if project_path:
            try:
                os.makedirs(Path(project_path).parent / f"TaxationTool_{Path(project_path).name[:-4]}")
            except Exception as e:
                self.view.log(f"[ERROR]\tОшибка создания временной директории ({self.temp_path}).\n{str(e)}")
                return
            with open(project_path, 'w', encoding='utf-8') as f:
                pass
            if Path(project_path).exists():
                self.project = Path(project_path)
                self.clear_temp_project()
                self.update_interface()
                self.view.log(f"[DEBUG]\tПроект ({self.project}) успешно сохранен.")
            else:
                self.view.log(f"[ERROR]\tНе удалось сохранить проект ({project_path}).")

    def create_new_project(self) -> None:

        # todo предупреждение и запрос на сохранение
        self.clear_temp_project()

        try:
            os.makedirs(self.temp_path)
            os.makedirs(self.temp_path / "TaxationTool_Новый проект")
        except Exception as e:
            self.view.log(f"[ERROR]\tОшибка создания временной директории ({self.temp_path}).\n{str(e)}")
            return

        project_path = self.temp_path / "Новый проект.ttpr"
        with open(project_path, 'w', encoding='utf-8') as f:
            pass

        if project_path.exists():
            self.project = Path(project_path)
            self.update_interface()
            self.view.log(f"[DEBUG]\tПроект ({self.project}) успешно создан.")
        else:
            self.view.log(f"[ERROR]\tОшибка создания проекта во временной директории ({project_path}).")
            return

    def open_project(self) -> None:
        open_dialog = QFileDialog()
        open_dialog.setDefaultSuffix('.ttpr')
        project_path, _ = open_dialog.getOpenFileName(parent=self.view, caption="Открыть проект...", dir='/',
                                                      filter="Taxation tool project (*.ttpr)")
        if project_path:
            if Path(project_path).exists():
                self.project = Path(project_path)
                self.clear_temp_project()
                self.update_interface()
                self.view.log(f"[DEBUG]\tПроект ({self.project}) успешно открыт.")
            else:
                self.view.log(f"[ERROR]\tНе удалось открыть проект ({project_path}).")


    def clear_temp_project(self) -> None:
        self.view.log("[DEBUG]\tУдаление временных файлов.")
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)

    def update_interface(self) -> None:
        # self.view.console_log.clear()
        self.view.setWindowTitle("Taxation Tool - " + self.project.name)
        self.view.log("[DEBUG]\tОбновление интерфейса.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    view = View()
    taxation_tool = TaxationTool(model, view, app)
    sys.exit(app.exec_())

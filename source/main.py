import os
import shutil
import sys
import tempfile
from pathlib import Path

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem

from utils.convert import oda_converter
from .view.view import View
from .model.model import Model


class TaxationTool:

    project: Path
    project_dir: Path
    taxation_plan: Path

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

        self.view.menu_project_import.triggered.connect(self.import_dxf_taxation)

        self.view.menu_processing_classification.triggered.connect(self.process_classification)

    def save_project(self) -> None:
        save_as = QFileDialog()
        save_as.setDefaultSuffix('.ttpr')
        project_path, _ = save_as.getSaveFileName(parent=self.view, caption="Сохранить как...", dir='/',
                                                  filter="Taxation tool project (*.ttpr)")
        if project_path:
            project_path = Path(project_path).parent / Path(project_path).name.replace(" ", "_")
            try:
                project_dir = Path(project_path).parent / f"TaxationTool_{Path(project_path).name[:-4]}"
                os.makedirs(project_dir)
                self.project_dir = project_dir
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
            project_dir = self.temp_path / "TaxationTool_Новый_проект"
            os.makedirs(project_dir)
            self.project_dir = project_dir
        except Exception as e:
            self.view.log(f"[ERROR]\tОшибка создания временной директории ({self.temp_path}).\n{str(e)}")
            return

        project_path = self.temp_path / "Новый_проект.ttpr"
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

    def import_dxf_taxation(self) -> None:

        input_dir = self.project_dir / "taxation_plan_dwg"
        if input_dir.exists():
            shutil.rmtree(input_dir)
        os.makedirs(input_dir, exist_ok=True)

        output_dir = self.project_dir / "taxation_plan_dxf"
        if output_dir.exists():
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        import_dialog = QFileDialog()
        import_dialog.setDefaultSuffix('.dwg')
        dwg_path, _ = import_dialog.getOpenFileName(parent=self.view, caption="Импорт чертежа...", dir='/',
                                                      filter="Чертежи (*.dwg)")
        if not dwg_path:
            return

        shutil.copyfile(dwg_path, input_dir / Path(dwg_path).name.replace(" ", "_"))

        converter_path = Path("utils/ODAFileConverter.exe").absolute()

        invalid_path = []
        for path in [input_dir, output_dir, converter_path]:
            if isinstance(path, Path) and ' ' in str(path):
                invalid_path.append(str(path))
        if invalid_path:
            self.view.log(
                f"[ERROR]\tПереместите папку с программой ({invalid_path}) в директорию без пробелов в именах папок.")
            return

        try:
            oda_converter(converter_path, input_dir, output_dir)
        except Exception as e:
            self.view.log(f"[ERROR]\tОшибка конвертации файлов из ({input_dir}) в ({output_dir}).")
            return
        self.view.log(f"[DEBUG]\tФайлы успешно конвертированы из ({input_dir}) в ({output_dir}).")

        self.taxation_plan = output_dir / Path(dwg_path).name.replace(" ", "_").replace(".dwg", ".dxf")

        item = self.view.tree_manager.findItems("Чертеж таксации", QtCore.Qt.MatchContains)[0]
        children_item = QTreeWidgetItem(item)
        children_item.setText(0, self.taxation_plan.name)

        self.view.log(f"Файл чертежа таксации ({dwg_path}) успешно импортирован.")

    def process_classification(self) -> None:
        data = self.model.process_classification(self.taxation_plan)
        self.view.log(str(data))


def main():
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    view = View()
    taxation_tool = TaxationTool(model, view, app)
    sys.exit(app.exec_())

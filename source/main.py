import os
import pickle
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMessageBox

from utils.convert import oda_converter
from .view.view import View
from .model.model import Model
from .model.project import Project


class TaxationTool:
    def __init__(self, model, view, app):
        super(TaxationTool, self).__init__()

        self.model = model
        self.view = view
        self.app = app

        self.temp_path = Path(tempfile.gettempdir()) / "TaxationTool"
        self.temp_path_convert_input = self.temp_path / "convert" / "input"
        self.temp_path_convert_output = self.temp_path / "convert" / "output"

        self.project = Project()
        self.model.project = self.project
        self.create_new_project()

        self.connect_signals()

        self.view.show()

    def connect_signals(self) -> None:
        self.view.menu_project_save_as.triggered.connect(self.save_as_project)
        self.view.menu_project_new.triggered.connect(self.create_new_project)
        self.view.menu_project_open.triggered.connect(self.open_project)

        self.view.menu_project_import.triggered.connect(self.import_dwg_taxation)
        self.view.menu_processing_converting_to_dxf.triggered.connect(self.convert_dwg_taxation_to_dxf)
        self.view.menu_processing_load_dxf.triggered.connect(self.load_dxf_taxation)

        self.view.menu_processing_classification.triggered.connect(self.process_classification)

    @staticmethod
    def _confirm_close_unsaved_project() -> bool:
        dialog = QMessageBox()
        dialog.setWindowTitle("Подтвердите действие")
        dialog.setText("Проект не сохранен.\nСоздать новый проект?")
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
        dialog.exec_()
        return True if dialog.result() == QMessageBox.StandardButton.Yes else False

    def save_as_project(self) -> None:
        save_as = QFileDialog()
        save_as.setDefaultSuffix(Project().suffix)
        _project_path, _ = save_as.getSaveFileName(parent=self.view, caption="Сохранить как...", dir='/',
                                                   filter=f"Taxation tool project (*{Project().suffix})")
        if _project_path:
            try:
                project_path = Path(_project_path)
                shutil.copytree(self.project.dir, project_path.parent / project_path.stem)
                self.project.path = project_path
                with open(self.project.path, 'wb') as file:
                    pickle.dump(self.project, file)
                with open(self.project.taxation_plan_path, 'wb') as file:
                    pickle.dump(self.project.taxation_plan, file)
                # FIXME: сохранение проекта в то же место, или перезапись другого проекта

                self.clear_temp_project()
                self.update_interface()

                self.view.log(f"[DEBUG]\tПроект `{self.project.path}` успешно сохранен.")
            except Exception:
                self.view.log(f"[ERROR]\tНе удалось сохранить проект в `{_project_path}`."
                              f"\n{traceback.format_exc()}")

    def create_new_project(self) -> None:

        # проверка на сохранение проекта перед созданием/открытием нового
        if not self.project.is_saved and not TaxationTool._confirm_close_unsaved_project():
            return

        try:
            self.clear_temp_project()

            # создание необходимых для работы директорий во временном каталоге
            try:
                os.makedirs(self.temp_path)
                os.makedirs(self.temp_path_convert_input)
                os.makedirs(self.temp_path_convert_output)
            except Exception as e:
                self.view.log(f"[ERROR]\tОшибка создания временной директории ({self.temp_path}).\n{str(e)}")
                shutil.rmtree(self.temp_path, ignore_errors=True)
                return

            # создание проекта во временном каталоге
            self.project.path = self.temp_path / ("New project" + self.project.suffix)
            os.makedirs(self.project.dir)
            os.makedirs(self.project.taxation_plan.dir_dwg)
            os.makedirs(self.project.taxation_plan.dir_dxf)

            self.update_interface()

            self.view.log(f"[DEBUG]\tПроект `{self.project.path}` успешно создан.")

        except Exception:
            self.view.log(f"[ERROR]\tОшибка создания проекта во временной директории."
                          f"\n{traceback.format_exc()}")

    def open_project(self) -> None:

        # проверка на сохранение проекта перед созданием/открытием нового
        if not self.project.is_saved and not TaxationTool._confirm_close_unsaved_project():
            return

        open_dialog = QFileDialog()
        open_dialog.setDefaultSuffix(self.project.suffix)
        _project_path, _ = open_dialog.getOpenFileName(parent=self.view, caption="Открыть проект...", dir='/',
                                                       filter=f"Taxation tool project (*{self.project.suffix})")
        if _project_path:
            try:
                project_path = Path(_project_path)
                if project_path.suffix != self.project.suffix:
                    raise ValueError(f"Неверное расширение файла: `{self.project.suffix}`. "
                                     f"Требуется `{self.project.suffix}`")
                with open(project_path, 'rb') as file:
                    self.project = pickle.load(file)
                with open(self.project.taxation_plan_path, 'rb') as file:
                    self.project.taxation_plan = pickle.load(file)

                self.clear_temp_project()
                self.update_interface()

                self.view.log(f"[DEBUG]\tПроект `{self.project.path}` успешно открыт.")
            except Exception:
                self.view.log(f"[ERROR]\tНе удалось открыть проект `{_project_path}`."
                              f"\n{traceback.format_exc()}")

    def clear_temp_project(self) -> None:
        self.view.log("[DEBUG]\tУдаление временных файлов.")
        if self.temp_path.exists():
            shutil.rmtree(self.temp_path)

    def update_interface(self) -> None:
        self.view.setWindowTitle("Taxation Tool - " + self.project.name)
        self.view.log("[DEBUG]\tОбновление интерфейса.")

    def import_dwg_taxation(self) -> None:
        import_dialog = QFileDialog()
        import_dialog.setDefaultSuffix('.dwg')
        dwg_path, _ = import_dialog.getOpenFileName(parent=self.view, caption="Импорт чертежа...", dir='/',
                                                    filter="Чертежи (*.dwg)")
        if dwg_path == "":
            return

        dwg_dir_dst = self.project.taxation_plan.dir_dwg
        if self.project.taxation_plan.dir_dwg.exists():
            shutil.rmtree(self.project.taxation_plan.dir_dwg)
        os.makedirs(self.project.taxation_plan.dir_dwg)

        dwg_path_dst = dwg_dir_dst / Path(dwg_path).name
        shutil.copyfile(dwg_path, dwg_path_dst)

        self.project.taxation_plan.path_dwg = dwg_path_dst

        # добавление имени dwg файла в позицию `Чертеж таксации` менеджера проекта
        root_item_taxation_plan = self.view.tree_manager.findItems("Чертеж таксации", QtCore.Qt.MatchContains)[0]
        root_item_taxation_plan.takeChild(0)
        children_item_taxation_plan = QTreeWidgetItem(root_item_taxation_plan)
        children_item_taxation_plan.setText(0, self.project.taxation_plan.path_dwg.name)

        self.view.log(f"[DEBUG]\tDWG файл чертежа таксации `{dwg_path}` успешно импортирован в "
                      f"`{self.project.taxation_plan.path_dwg}`.")

    def convert_dwg_taxation_to_dxf(self) -> None:

        dwg_path_without_space = self.project.taxation_plan.path_dwg.name.replace(" ", "_")

        if self.temp_path_convert_input.exists():
            shutil.rmtree(self.temp_path_convert_input)
        os.makedirs(self.temp_path_convert_input, exist_ok=True)

        shutil.copyfile(self.project.taxation_plan.path_dwg, self.temp_path_convert_input / dwg_path_without_space)

        if self.temp_path_convert_output.exists():
            shutil.rmtree(self.temp_path_convert_output)
        os.makedirs(self.temp_path_convert_output, exist_ok=True)

        converter_path = Path("utils/ODAFileConverter.exe").absolute()  # TODO: перенести в настройки

        try:
            oda_converter(converter_path, self.temp_path_convert_input, self.temp_path_convert_output)
        except Exception:
            self.view.log(f"[ERROR]\tОшибка конвертации файлов."
                          f"\n{traceback.format_exc()}")
            return

        self.view.log(f"[DEBUG]\tФайлы успешно конвертированы из `{self.temp_path_convert_input}` в "
                      f"`{self.temp_path_convert_output}`.")

    def load_dxf_taxation(self) -> None:
        try:
            dxf = self.temp_path_convert_output / next(file for file in os.listdir(self.temp_path_convert_output))
        except StopIteration:
            self.view.log(f"[ERROR]\tНе удалось найти файл dxf в `{self.temp_path_convert_output}`.")
            return
        path_dxf_dst = self.project.taxation_plan.dir_dxf / dxf.name
        shutil.copyfile(dxf, path_dxf_dst)

        self.project.taxation_plan.path_dxf = path_dxf_dst

        self.view.log(f"[DEBUG]\tDXF файл успешно загружен из `{dxf.parent}` в "
                      f"`{self.project.taxation_plan.dir_dxf}`.")

    def process_classification(self) -> None:
        self.model.read_taxation_plan()
        self.view.log(f"Количество объектов слоя номера: {len(self.project.taxation_plan.entity.numbers)}")
        self.view.log(f"Количество объектов слоя полосы: {len(self.project.taxation_plan.entity.lines)}")
        self.view.log(f"Количество объектов слоя контуры: {len(self.project.taxation_plan.entity.contours)}")
        self.view.log(f"Количество объектов слоя зоны: {len(self.project.taxation_plan.entity.zones)}")
        self.model.autocad_data_structuring()
        self.view.log("Файл чертежа таксации успешно обработан.")
        self.view.log(f"Количество точечных растений: {len(self.project.numbers)}")
        self.view.log(f"Количество полос и контуров растительности: {len(self.project.shapes)}")
        self.view.log(f"Зоны: {[name for _, name in self.project.zone_names.items()]}")
        self.model.splitting_numbers()
        self.model.calculate_intersects_shapes_in_zones()

        split_numbers_in_zones_from_model = {zone_name: [] for _, zone_name in self.project.zone_names.items()}
        for zone_name in split_numbers_in_zones_from_model.keys():
            k_zone_name = next(k for k, v in self.project.zone_names.items() if v == zone_name)
            k_zone_list = self.project.zones_from_zone_names[k_zone_name]
            for k_zone in k_zone_list:
                for k_split_number, _k_zone_list in self.project.intersects_shapes_in_zones.items():
                    for _k_zone in _k_zone_list:
                        if _k_zone == k_zone:
                            split_numbers_in_zones_from_model[zone_name].append(self.project.split_numbers[k_split_number])
        for zone_name in split_numbers_in_zones_from_model.keys():
            self.view.log(f"Вхождения объектов в зону `{zone_name}`: "
                          f"{split_numbers_in_zones_from_model[zone_name]}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    view = View()
    model = Model(view.log)
    taxation_tool = TaxationTool(model, view, app)
    sys.exit(app.exec_())

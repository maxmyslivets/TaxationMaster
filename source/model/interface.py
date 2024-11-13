import os
import pickle
import shutil
import tempfile
import time
import traceback
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox, QFileDialog, QTreeWidgetItem

from utils.convert import oda_converter


class Interface:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._temp_path = Path(tempfile.gettempdir()) / "TaxationTool"      # TODO: вынести в настройки
        self._temp_path_convert_input = self._temp_path / "convert" / "input"
        self._temp_path_convert_output = self._temp_path / "convert" / "output"

    @staticmethod
    def _confirm_close_unsaved_project() -> bool:
        dialog = QMessageBox()
        dialog.setWindowTitle("Подтвердите действие")
        dialog.setText("Проект не сохранен.\nПродолжить?")
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
        dialog.exec_()
        return True if dialog.result() == QMessageBox.StandardButton.Yes else False

    def save_as_project(self) -> None:
        save_as = QFileDialog()
        save_as.setDefaultSuffix(self.model.project.suffix)
        _project_path, _ = save_as.getSaveFileName(parent=self.view, caption="Сохранить как...", dir='/',
                                                   filter=f"Taxation tool project (*{self.model.project.suffix})")
        if _project_path:
            try:
                project_path = Path(_project_path)
                if project_path.exists():
                    os.remove(project_path)
                    shutil.rmtree(project_path.parent / project_path.stem)
                elif project_path == self.model.project.path:
                    self.save_project()
                shutil.copytree(self.model.project.dir, project_path.parent / project_path.stem)
                self.model.project.path = project_path
                self.model.project.is_saved = True
                with open(self.model.project.path, 'wb') as file:
                    pickle.dump(self.model.project, file)

                self.clear_temp_project()
                self.update_interface()

                self.view.log(f"[DEBUG]\tПроект `{self.model.project.path}` успешно сохранен.")
            except Exception:
                self.view.log(f"[ERROR]\tНе удалось сохранить проект в `{_project_path}`."
                              f"\n{traceback.format_exc()}")

    def save_project(self) -> None:
        self.model.project.is_saved = True
        try:
            with open(self.model.project.path, 'wb') as file:
                pickle.dump(self.model.project, file)
            self.view.log(f"[DEBUG]\tПроект `{self.model.project.path}` успешно сохранен.")
        except Exception:
            self.view.log(f"[ERROR]\tНе удалось сохранить проект `{self.model.project.path}`."
                          f"\n{traceback.format_exc()}")

    def create_new_project(self) -> None:

        # проверка на сохранение проекта перед созданием/открытием нового
        if not self.model.project.is_saved and not Interface._confirm_close_unsaved_project():
            return

        try:
            self.clear_temp_project()
            self.model.clear_project()

            # создание необходимых для работы директорий во временном каталоге
            try:
                os.makedirs(self._temp_path)
                os.makedirs(self._temp_path_convert_input)
                os.makedirs(self._temp_path_convert_output)
            except Exception as e:
                self.view.log(f"[ERROR]\tОшибка создания временной директории ({self._temp_path}).\n{str(e)}")
                shutil.rmtree(self._temp_path, ignore_errors=True)
                return

            # создание проекта во временном каталоге
            self.model.project.path = self._temp_path / ("New project" + self.model.project.suffix)
            self.model.project.is_saved = True
            os.makedirs(self.model.project.dir)
            os.makedirs(self.model.project.dir_dwg)
            os.makedirs(self.model.project.dir_dxf)

            self.update_interface()

            self.view.log(f"[DEBUG]\tПроект `{self.model.project.path}` успешно создан.")

        except Exception:
            self.view.log(f"[ERROR]\tОшибка создания проекта во временной директории."
                          f"\n{traceback.format_exc()}")

    def open_project(self) -> None:

        # проверка на сохранение проекта перед созданием/открытием нового
        if not self.model.project.is_saved and not Interface._confirm_close_unsaved_project():
            return

        open_dialog = QFileDialog()
        open_dialog.setDefaultSuffix(self.model.project.suffix)
        _project_path, _ = open_dialog.getOpenFileName(parent=self.view, caption="Открыть проект...", dir='/',
                                                       filter=f"Taxation tool project (*{self.model.project.suffix})")
        if _project_path:
            try:
                project_path = Path(_project_path)
                if project_path.suffix != self.model.project.suffix:
                    raise ValueError(f"Неверное расширение файла: `{self.model.project.suffix}`. "
                                     f"Требуется `{self.model.project.suffix}`")
                with open(project_path, 'rb') as file:
                    self.model.project = pickle.load(file)

                self.model.project.is_saved = True

                self.clear_temp_project()
                self.update_interface()

                self.view.log(f"[DEBUG]\tПроект `{self.model.project.path}` успешно открыт.")

                self.view.log(f"[DEBUG]\tПеременные экземпляра класса Project:")
                for var, value in self.model.project.__dict__.items():
                    self.view.log(f"[DEBUG]\t{var} = {value}")

            except Exception:
                self.view.log(f"[ERROR]\tНе удалось открыть проект `{_project_path}`."
                              f"\n{traceback.format_exc()}")

    def clear_temp_project(self) -> None:
        self.view.log("[DEBUG]\tУдаление временных файлов.")
        if self._temp_path.exists():
            shutil.rmtree(self._temp_path)

    def update_interface(self) -> None:
        self.view.setWindowTitle("Taxation Tool - " + self.model.project.name)
        self.view.log("[DEBUG]\tОбновление интерфейса.")

    def import_dwg_taxation(self) -> None:
        import_dialog = QFileDialog()
        import_dialog.setDefaultSuffix('.dwg')
        dwg_path, _ = import_dialog.getOpenFileName(parent=self.view, caption="Импорт чертежа...", dir='/',
                                                    filter="Чертежи (*.dwg)")
        if dwg_path == "":
            return

        if self.model.project.dir_dwg.exists():
            shutil.rmtree(self.model.project.dir_dwg)
        os.makedirs(self.model.project.dir_dwg)

        self.model.processing.clear_data_for_autocad_data_structuring()

        self.model.project.dwg_name = Path(dwg_path).name
        shutil.copyfile(dwg_path, self.model.project.path_dwg)

        # добавление имени dwg файла в позицию `Чертеж таксации` менеджера проекта
        root_item_taxation_plan = self.view.tree_manager.findItems("Чертеж таксации", QtCore.Qt.MatchContains)[0]
        root_item_taxation_plan.takeChild(0)
        children_item_taxation_plan = QTreeWidgetItem(root_item_taxation_plan)
        children_item_taxation_plan.setText(0, self.model.project.path_dwg.name)

        self.view.log(f"[DEBUG]\tDWG файл чертежа таксации `{dwg_path}` успешно импортирован в "
                      f"`{self.model.project.path_dwg}`.")

        # конвертация dwg в dxf
        dwg_path_without_space = self.model.project.path_dwg.name.replace(" ", "_")

        if self._temp_path_convert_input.exists():
            shutil.rmtree(self._temp_path_convert_input)
        os.makedirs(self._temp_path_convert_input, exist_ok=True)

        shutil.copyfile(self.model.project.path_dwg, self._temp_path_convert_input / dwg_path_without_space)

        if self._temp_path_convert_output.exists():
            shutil.rmtree(self._temp_path_convert_output)
        os.makedirs(self._temp_path_convert_output, exist_ok=True)

        converter_path = Path("utils/ODAFileConverter.exe").absolute()  # TODO: вынести в настройки

        try:
            oda_converter(converter_path, self._temp_path_convert_input, self._temp_path_convert_output)
        except Exception:
            self.view.log(f"[ERROR]\tОшибка конвертации файлов."
                          f"\n{traceback.format_exc()}")
            return

        dxf_file = None
        timeout = 10    # TODO: вынести в настройки
        while not dxf_file:
            try:
                dxf_file = self._temp_path_convert_output / next(
                    file for file in os.listdir(self._temp_path_convert_output))
            except StopIteration:
                time.sleep(1)
                timeout -= 1
            if timeout == 0:
                self.view.log(f"[ERROR]\tНе удалось импортировать файл dxf. Превышено время ожидания.")
                break
        if timeout == 0:
            return

        self.model.project.dxf_name = dxf_file.name
        shutil.copyfile(dxf_file, self.model.project.path_dxf)
        self.view.log(f"[DEBUG]\tФайл успешно конвертирован из `{self._temp_path_convert_input}` в "
                      f"`{self._temp_path_convert_output}`.")
        self.view.log(f"[DEBUG]\tDXF файл успешно загружен из `{dxf_file.parent}` в "
                      f"`{self.model.project.dir_dxf}`.")
        shutil.rmtree(self._temp_path_convert_output)

    def preprocessing(self) -> None:
        self.model.processing.read_data_from_taxation_plan()
        self.view.log("Файл чертежа таксации успешно обработан.")
        self.view.log(f"Количество точечных растений: {len(self.model.project.numbers)}")
        self.view.log(f"Количество полос и контуров растительности: {len(self.model.project.shapes)}")
        self.view.log(f"Зоны: {[name for _, name in self.model.project.zone_names.items()]}")
        self.model.processing.splitting_numbers()
        self.model.processing.calculate_intersects_shapes_in_zones()

        split_numbers_in_zones_from_model = {zone_name: [] for _, zone_name in self.model.project.zone_names.items()}
        for zone_name in split_numbers_in_zones_from_model.keys():
            k_zone_name = next(k for k, v in self.model.project.zone_names.items() if v == zone_name)
            k_zone_list = self.model.project.zones_from_zone_names[k_zone_name]
            for k_zone in k_zone_list:
                for k_split_number, _k_zone_list in self.model.project.intersects_shapes_in_zones.items():
                    for _k_zone in _k_zone_list:
                        if _k_zone == k_zone:
                            split_numbers_in_zones_from_model[zone_name].append(self.model.project.split_numbers[k_split_number])
        for zone_name in split_numbers_in_zones_from_model.keys():
            self.view.log(f"Вхождения объектов в зону `{zone_name}`: "
                          f"{split_numbers_in_zones_from_model[zone_name]}")

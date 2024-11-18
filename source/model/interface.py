import os
import pickle
import shutil
import time
import traceback
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QTreeWidget, QMenu, QTableView, QTableWidget, \
    QTableWidgetItem

from source.model.project import ProjectData, Project
from utils.convert import oda_converter


class Interface:
    project_data: ProjectData

    def __init__(self, model, view):
        self.model = model
        self.view = view

    ###################################################################################################################
    # Меню Проект
    ###################################################################################################################

    def save_as_project(self) -> None:
        save_as = QFileDialog()
        save_as.setDefaultSuffix(self.model.config.extension)
        _project_path, _ = save_as.getSaveFileName(parent=self.view.main_window, caption="Сохранить как...", dir='/',
                                                   filter=f"Taxation tool project (*{self.model.config.extension})")
        if _project_path:
            try:
                project_path = Path(_project_path)
                if project_path.exists():
                    os.remove(project_path)
                    shutil.rmtree(project_path.parent / project_path.stem)
                elif project_path == self.project_data.path:
                    self.save_project()
                # shutil.copytree(self.project_data.dir, project_path.parent / project_path.stem)
                self.project_data.path = project_path
                self.model.project.is_saved = True
                with open(self.project_data.path, 'wb') as file:
                    pickle.dump(self.model.project, file)

                self.clear_temp_project()
                self.update_interface()

                self.view.main_window.log(f"[DEBUG]\tПроект `{self.project_data.path}` успешно сохранен.")
            except Exception:
                self.view.main_window.log(f"[ERROR]\tНе удалось сохранить проект в `{_project_path}`."
                                          f"\n{traceback.format_exc()}")

    def save_project(self) -> None:
        try:
            with open(self.project_data.path, 'wb') as file:
                pickle.dump(self.model.project, file)
            self.model.project.is_saved = True
            self.view.main_window.log(f"[DEBUG]\tПроект `{self.project_data.path}` успешно сохранен.")
        except Exception:
            self.view.main_window.log(f"[ERROR]\tНе удалось сохранить проект `{self.project_data.path}`."
                                      f"\n{traceback.format_exc()}")

    def create_new_project(self) -> None:

        # проверка на сохранение проекта перед созданием/открытием нового
        if not self.model.project.is_saved and self.view.confirm_close_unsaved_project().result_no:
            return

        try:
            self.clear_temp_project()
            self.model.clear_project()

            # создание необходимых для работы директорий во временном каталоге
            try:
                os.makedirs(self.model.config.temp_path)
                os.makedirs(self.model.config.temp_path_convert_input)
                os.makedirs(self.model.config.temp_path_convert_output)
            except Exception as e:
                self.view.main_window.log(f"[ERROR]\tОшибка создания временной директории "
                                          f"`{self.model.config.temp_path}`.\n{str(e)}")
                shutil.rmtree(self.model.config.temp_path, ignore_errors=True)
                return

            # создание проекта во временном каталоге
            self.project_data = ProjectData(self.model.config.temp_path / ("New project" + self.model.config.extension))
            self.model.project.is_saved = True
            # os.makedirs(self.project_data.dir)

            self.update_interface()
            # self.show_table_from_taxation_plan()

            self.view.main_window.log(f"[DEBUG]\tПроект `{self.project_data.path}` успешно создан.")

        except Exception:
            self.view.main_window.log(f"[ERROR]\tОшибка создания проекта во временной директории."
                                      f"\n{traceback.format_exc()}")

    def open_project(self) -> None:

        # проверка на сохранение проекта перед созданием/открытием нового
        if not self.model.project.is_saved and self.view.confirm_close_unsaved_project().result_no:
            return

        open_dialog = QFileDialog()
        open_dialog.setDefaultSuffix(self.model.config.extension)
        _project_path, _ = open_dialog.getOpenFileName(parent=self.view.main_window, caption="Открыть проект...", dir='/',
                                                       filter=f"Taxation tool project (*{self.model.config.extension})")
        if _project_path:
            try:
                project_path = Path(_project_path)
                if project_path.suffix != self.model.config.extension:
                    raise ValueError(f"Неверное расширение файла: `{self.model.config.extension}`. "
                                     f"Требуется `{self.model.project.suffix}`")
                with open(project_path, 'rb') as file:
                    self.model.project = pickle.load(file)

                self.model.project.is_saved = True

                self.clear_temp_project()

                self.view.main_window.log(f"[DEBUG]\tПроект `{self.project_data.path}` успешно открыт.")

                self.view.main_window.log(f"[DEBUG]\tПеременные экземпляра класса Project:")
                for var, value in self.model.project.__dict__.items():
                    self.view.main_window.log(f"[DEBUG]\t{var} = {value}")

                self.update_interface()

                self.clear_project_manager()
                if "taxation_plan" in self.model.project.__dict__.keys():
                    self.set_taxation_plan_to_project_manager()

            except Exception:
                self.view.main_window.log(f"[ERROR]\tНе удалось открыть проект `{_project_path}`."
                                          f"\n{traceback.format_exc()}")

    def clear_temp_project(self) -> None:
        self.view.main_window.log("[DEBUG]\tУдаление временных файлов.")
        if self.model.config.temp_path.exists():
            shutil.rmtree(self.model.config.temp_path)
        if self.model.config.temp_path_convert_input.exists():
            shutil.rmtree(self.model.config.temp_path_convert_input)
        if self.model.config.temp_path_convert_output.exists():
            shutil.rmtree(self.model.config.temp_path_convert_output)

    def import_taxation_plan(self) -> None:
        import_dialog = QFileDialog()
        import_dialog.setDefaultSuffix('.dwg')
        dwg_path, _ = import_dialog.getOpenFileName(parent=self.view.main_window, caption="Импорт чертежа...", dir='/',
                                                    filter="Чертежи (*.dwg)")
        if dwg_path == "":
            return

        # self.model.processing.clear_data_for_autocad_data_structuring()

        # конвертация dwg в dxf
        dwg_path_without_space = Path(dwg_path).name.replace(" ", "_")

        if self.model.config.temp_path_convert_input.exists():
            shutil.rmtree(self.model.config.temp_path_convert_input)
        os.makedirs(self.model.config.temp_path_convert_input, exist_ok=True)

        shutil.copyfile(Path(dwg_path), self.model.config.temp_path_convert_input / dwg_path_without_space)

        if self.model.config.temp_path_convert_output.exists():
            shutil.rmtree(self.model.config.temp_path_convert_output)
        os.makedirs(self.model.config.temp_path_convert_output, exist_ok=True)

        try:
            oda_converter(self.model.config.oda_converter_path, self.model.config.temp_path_convert_input,
                          self.model.config.temp_path_convert_output)
        except Exception:
            self.view.main_window.log(f"[ERROR]\tОшибка конвертации файлов."
                                      f"\n{traceback.format_exc()}")
            return

        timeout = self.model.config.timeout
        dxf_file = None
        while not dxf_file:
            try:
                dxf_file = self.model.config.temp_path_convert_output / next(
                    file for file in os.listdir(self.model.config.temp_path_convert_output))
            except StopIteration:
                time.sleep(1)
                timeout -= 1
            if timeout == 0:
                self.view.main_window.log(f"[ERROR]\tНе удалось конвертировать файл dxf. Превышено время ожидания.")
                break
        if timeout == 0:
            return

        timeout = self.model.config.timeout
        permission = False
        while not permission:
            try:
                permission = True
            except PermissionError:
                time.sleep(1)
                timeout -= 1
                if timeout == 0:
                    self.view.main_window.log(f"[ERROR]\tНе удалось импортировать файл dxf. Превышено время ожидания.")
                    break
        if timeout == 0:
            return

        taxation_plan = self.model.processing.create_taxation_plan(dxf_file,
                                                                   self.model.config.numbers_layers,
                                                                   self.model.config.lines_layers,
                                                                   self.model.config.contours_layers,
                                                                   self.model.config.min_distance)
        if taxation_plan is not None:
            self.model.project.taxation_plan = taxation_plan

        self.set_taxation_plan_to_project_manager()

        self.view.main_window.log(f"[DEBUG]\tЧертеж таксации успешно импортирован.")
        shutil.rmtree(self.model.config.temp_path_convert_output)

    def update_interface(self) -> None:
        self.view.main_window.setWindowTitle("Taxation Tool - " + self.project_data.name)
        # self.update_project_manager()
        self.view.main_window.log("[DEBUG]\tОбновление интерфейса.")

    ###################################################################################################################
    # Меню Обработка
    ###################################################################################################################

    # def preprocessing(self) -> None:
    #     self.model.processing.read_data_from_taxation_plan(self.model.config.numbers_layers,
    #                                                        self.model.config.lines_layers,
    #                                                        self.model.config.contours_layers,
    #                                                        self.model.config.zones_layers,
    #                                                        self.model.config.min_distance,
    #                                                        self.model.config.min_area)
    #     self.view.main_window.log("Файл чертежа таксации успешно обработан.")
    #     self.view.main_window.log(f"Количество точечных растений: {len(self.model.project.numbers)}")
    #     self.view.main_window.log(f"Количество полос и контуров растительности: {len(self.model.project.shapes)}")
    #     self.view.main_window.log(f"Зоны: {[name for _, name in self.model.project.zone_names.items()]}")
    #     self.model.processing.splitting_numbers()
    #     self.model.processing.calculate_intersects_shapes_in_zones()
    #
    #     split_numbers_in_zones_from_model = {zone_name: [] for _, zone_name in self.model.project.zone_names.items()}
    #     for zone_name in split_numbers_in_zones_from_model.keys():
    #         k_zone_name = next(k for k, v in self.model.project.zone_names.items() if v == zone_name)
    #         k_zone_list = self.model.project.zones_from_zone_names[k_zone_name]
    #         for k_zone in k_zone_list:
    #             for k_split_number, _k_zone_list in self.model.project.intersects_shapes_in_zones.items():
    #                 for _k_zone in _k_zone_list:
    #                     if _k_zone == k_zone:
    #                         split_numbers_in_zones_from_model[zone_name].append(self.model.project.split_numbers[k_split_number])
    #     for zone_name in split_numbers_in_zones_from_model.keys():
    #         self.view.main_window.log(f"Вхождения объектов в зону `{zone_name}`: "
    #                       f"{split_numbers_in_zones_from_model[zone_name]}")
    #     self.model.processing.splitting_shapes_in_zones()
    #     self.update_interface()
    #     self.show_table_from_taxation_plan()

    ###################################################################################################################
    # Управление виджетом менеджера проекта
    ###################################################################################################################

    def clear_project_manager(self) -> None:
        manager_project: QTreeWidget = self.view.main_window.tree_manager
        manager_project.clear()

    def set_taxation_plan_to_project_manager(self) -> None:
        manager_project: QTreeWidget = self.view.main_window.tree_manager
        try:
            manager_project_taxation_plan: QTreeWidgetItem = manager_project.findItems(
                "Чертеж таксации",
                QtCore.Qt.MatchStartsWith | QtCore.Qt.MatchRecursive)[0]
            index = manager_project.indexOfTopLevelItem(manager_project_taxation_plan)
            manager_project.takeTopLevelItem(index)
        except IndexError:
            pass
        manager_project_taxation_plan = QTreeWidgetItem([f"Чертеж таксации"])
        manager_project.insertTopLevelItem(0, manager_project_taxation_plan)

    def project_manager_double_clicked(self) -> None:
        manager_project: QTreeWidget = self.view.main_window.tree_manager
        item: QTreeWidgetItem = manager_project.selectedItems()[0]
        if item and item.parent() is None and item.text(0).startswith("Чертеж таксации"):
            self.show_taxation_plan_in_table()

    def project_manager_context_menu(self, pos) -> None:
        manager_project: QTreeWidget = self.view.main_window.tree_manager
        item: QTreeWidgetItem = manager_project.itemAt(pos)
        if item and item.parent() is None and item.text(0).startswith("Чертеж таксации"):
            menu = QMenu()
            import_taxation_plan_action = QAction("Новый импорт")
            import_taxation_plan_action.triggered.connect(self.import_taxation_plan)
            menu.addAction(import_taxation_plan_action)
            menu.exec_(manager_project.viewport().mapToGlobal(pos))

    ###################################################################################################################
    # Управление виджетом таблицы
    ###################################################################################################################

    def show_taxation_plan_in_table(self) -> None:

        table: QTableWidget = self.view.main_window.table
        table.setRowCount(0)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Номер", "Тип", "Значение", "Ед.изм."])

        for number, type_shape, value, unit in self.model.project.taxation_plan.table_data:
            item_number = QTableWidgetItem(number)
            item_type_shape = QTableWidgetItem(type_shape)
            item_value = QTableWidgetItem(value)
            item_unit = QTableWidgetItem(unit)

            row_position = table.rowCount()
            table.insertRow(row_position)

            table.setItem(row_position, 0, item_number)
            table.setItem(row_position, 1, item_type_shape)
            table.setItem(row_position, 2, item_value)
            table.setItem(row_position, 3, item_unit)

        table.setEditTriggers(QTableWidget.NoEditTriggers)


# class _TableCustomItem(QTableWidgetItem):
#     dict_name: str
#     dict_key: str|int
#
#     def set_dict_data(self, dict_name: str, dict_key: str|int) -> None:
#         self.dict_name = dict_name
#         self.dict_key = dict_key

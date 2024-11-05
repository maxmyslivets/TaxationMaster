from pathlib import Path

from PySide6 import QtCore

from processing.autocad import extract_data_from_taxation_plan, correcting_data_from_taxation_plan


class Model(QtCore.QObject):

    def __init__(self):
        super(Model, self).__init__()

    @staticmethod
    def process_classification(taxation_plan_path: Path):

        dxf_data = extract_data_from_taxation_plan(taxation_plan_path)
        result = correcting_data_from_taxation_plan(*dxf_data)

        return result

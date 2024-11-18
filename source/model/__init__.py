from source.model.config import Config
from source.model.interface import Interface
from source.model.project import Project
from source.model.processing import Processing


class Model:
    def __init__(self, view):
        self.config = Config()
        self._project = Project()
        self.processing = Processing(view.main_window.log)
        self.interface = Interface(self, view)

    def clear_project(self) -> None:
        self._project = Project()
        self.processing.project = self._project

    @property
    def project(self) -> Project:
        return self._project

    @project.setter
    def project(self, new_project: Project) -> None:
        self.clear_project()
        self._project = new_project
        self.processing.project = self._project

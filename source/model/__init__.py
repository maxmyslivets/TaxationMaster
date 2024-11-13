from source.model.processing import Processing
from source.model.project import Project


class Model:
    def __init__(self, log):
        self.project = Project()
        self.processing = Processing(self.project, log)

    def clear_project(self) -> None:
        self.project = Project()
        self.processing.project = self.project

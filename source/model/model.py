from PySide6 import QtCore


class Model(QtCore.QObject):

    def __init__(self):
        super(Model, self).__init__()

    def calculate(self):
        return 'Hello World'


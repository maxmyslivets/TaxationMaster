import ezdxf
from pathlib import Path

from PySide6 import QtCore


class Model(QtCore.QObject):

    def __init__(self):
        super(Model, self).__init__()

    @staticmethod
    def extract_taxation_plan(file_path: Path):
        doc = ezdxf.readfile(file_path)

        numbers = []
        for t in doc.modelspace().query('TEXT'):
            if t.dxf.layer == 'номера':
                numbers.append((t.plain_text(), t.dxf.insert[1], t.dxf.insert[0]))
        for mt in doc.modelspace().query('MTEXT'):
            if mt.dxf.layer == 'номера':
                numbers.append((mt.plain_text().replace('\n', ' '), mt.dxf.insert[1], mt.dxf.insert[0]))

        lines = []
        for entity in doc.modelspace():
            if entity.dxf.layer == 'полосы':
                if isinstance(entity, ezdxf.entities.lwpolyline.LWPolyline):
                    lines.append([(float(x), float(y)) for x, y in list(entity.vertices())])
                elif isinstance(entity, ezdxf.entities.line.Line):
                    lines.append(((entity.dxf.start.x, entity.dxf.start.y), (entity.dxf.end.x, entity.dxf.end.y)))

        contours = []
        for entity in doc.modelspace():
            if entity.dxf.layer == 'контуры':
                if isinstance(entity, ezdxf.entities.lwpolyline.LWPolyline):
                    contours.append([(float(x), float(y)) for x, y in list(entity.vertices())])

        _zones = []
        for entity in doc.modelspace():
            if entity.dxf.layer == 'зоны':
                if isinstance(entity, ezdxf.entities.lwpolyline.LWPolyline):
                    _zones.append([(float(x), float(y)) for x, y in list(entity.vertices())])

        # zones = {}
        # for t in doc.modelspace().query('TEXT'):
        #     if t.dxf.layer == 'зоны':
        #         zones[t.plain_text()] = (t.dxf.insert[1], t.dxf.insert[0])
        # for mt in doc.modelspace().query('MTEXT'):
        #     if mt.dxf.layer == 'зоны':
        #         numbers.append(mt.plain_text().replace('\n', ' '), mt.dxf.insert[1], mt.dxf.insert[0])

        return numbers, lines, contours, _zones

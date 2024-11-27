import pandas as pd


class TopographicPlan:
    """Данные чертежа таксации"""

    def __init__(self):
        # DataFrame исходных номеров и их позиций
        self._numbers_df = pd.DataFrame(columns=['id', 'number', 'position'])

        # DataFrame исходных фигур
        self._shapes_df = pd.DataFrame(columns=['id', 'geometry', 'type'])

        # DataFrame связей исходных номеров и фигур
        self._numbers_shapes_df = pd.DataFrame(columns=['number_id', 'shape_id'])

        # DataFrame связей точечных объектов растительности и исходных номеров
        self._trees_df = pd.DataFrame(columns=['id', 'number_id'])

        # DataFrame разделенных номеров для обработки
        self.splitted_numbers_df = pd.DataFrame(columns=['splitted_number', 'original_number', 'valid'])

        # DataFrame контуров растительности
        self.contours_df = pd.DataFrame(columns=['id', 'splitted_number', 'geometry', 'number_id'])

        # DataFrame полос растительности
        self.lines_df = pd.DataFrame(columns=['id', 'splitted_number', 'geometry', 'number_id'])

        # DataFrame точечных объектов растительности
        self.trees_df = pd.DataFrame(columns=['id', 'splitted_number', 'point', 'number_id'])


class TaxationList:
    """Данные ведомости таксации"""

    def __init__(self):
        # Основной DataFrame для хранения всех данных
        self.numbers_df = pd.DataFrame(columns=[
            'number',
            'name',
            'quantity',
            'height',
            'diameter',
            'quality'
        ])

        # DataFrame для разделенных номеров
        self.splitted_numbers_df = pd.DataFrame(columns=['splitted_number', 'original_number', 'is_bug'])

        # Результирующая таблица
        self.table_data = pd.DataFrame(columns=[
            'splitted_number',
            'number',
            'name',
            'quantity',
            'height',
            'diameter',
            'quality'
        ])
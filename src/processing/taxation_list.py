from pathlib import Path

import pandas as pd
from docx import Document as DocxDocument

from src.processing.splitting_numbers import split_number


def _create_taxation_list(table_data: list[list[str]]) -> pd.DataFrame:
    """Создание ведомости таксации из табличных данных"""

    taxation_list = []

    # Создаем DataFrame из исходных данных
    table_data_df = pd.DataFrame(
        table_data,
        columns=['origin_number', 'name', 'quantity', 'height', 'diameter', 'quality']
    )

    # TODO

    return table_data_df


def create_taxation_list(file_path: Path,
                         is_import_first_row: bool = False,
                         column_mapping: dict = None) -> pd.DataFrame:
    """Создание ведомости таксации из файла docx/xlsx"""

    if column_mapping is None:
        column_mapping = {
            'number': 0,
            'name': 1,
            'quantity': 2,
            'height': 3,
            'diameter': 4,
            'quality': 5
        }

    # Чтение данных из файла
    data = []
    if file_path.suffix == '.docx':
        doc = DocxDocument(str(file_path))
        for table in doc.tables:
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                data.append(row_data)

    elif file_path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, header=None)
        data = df.values.tolist()

    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_path.suffix}")

    # Пропускаем первую строку если нужно
    if not is_import_first_row and data:
        data = data[1:]

    # Преобразование данных с учетом маппинга колонок
    processed_data = []
    for row in data:
        if len(row) > 0:  # Пропускаем пустые строки
            processed_row = []
            for col_name in ['number', 'name', 'quantity', 'height', 'diameter', 'quality']:
                col_idx = column_mapping[col_name]
                processed_row.append(row[col_idx] if col_idx < len(row) else '')
            processed_data.append(processed_row)

    return _create_taxation_list(processed_data)

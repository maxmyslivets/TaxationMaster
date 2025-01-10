import xlwings as xw


class ExcelWorker:

    @staticmethod
    def get_numbers(sheet: xw.Sheet, column_name: str) -> list[str]:
        table_range = sheet['A1'].expand('table')
        data = table_range.value
        headers = data[0]
        col_index = headers.index(column_name)
        return [row[col_index] for row in data[1:]]

    @staticmethod
    def get_tables_info():
        pass

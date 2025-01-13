import re
from tkinter.filedialog import askopenfilename
from docx import Document as DocxDocument

import xlwings as xw
import pandas as pd
from shapely.wkt import loads
from win32com.universal import com_error

from src.parsing import Splitter, Parser, Templates


class ExcelWorker:

    @staticmethod
    def get_taxation_list() -> pd.DataFrame:
        """
        Получение ведомости таксации из Word

        Returns:
            pd.DataFrame: ведомость таксации
        """
        file_path = askopenfilename(filetypes=[("Word files", "*.docx *.doc"), ("All files", "*.*")])

        assert file_path is not None

        doc = DocxDocument(file_path)
        data = []

        for table in doc.tables:
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                data.append(row_data)

        return pd.DataFrame(data)

    @staticmethod
    def get_numbers(sheet: xw.Sheet, column_name: str) -> list[str]:
        table_range = sheet['A1'].expand('table')
        data = table_range.value
        headers = data[0]
        col_index = headers.index(column_name)
        return [row[col_index] for row in data[1:]]

    @staticmethod
    def split_taxation_list_item(df: pd.DataFrame, series: pd.Series) -> list[dict]:
        """
        Получение строки ОРМ из строки таблицы Ведомости

        Args:
            df (pd.DataFrame): Датафрейм листа Автокад
            series (pd.Series): Строка таблицы

        Returns:
            list[dict]: Список словарей ОРМ для датафрейма
        """
        match_trunk = re.search(Templates.TRUNKS, series['Количество'])
        match_contour = re.search(Templates.CONTOUR, series['Количество'])
        match_line = re.search(Templates.LINE, series['Количество'])
        shapes = ExcelWorker.get_shapes_from_autocad_df(df, series['Номер точки'])
        numbers_positions, geometries = shapes['Список позиций номеров'], shapes['Список геометрии']
        if not match_contour and not match_line and not match_trunk:
            split_numbers = Splitter.number(series['Номер точки'])
            split_height = Splitter.size(series['Высота'])
            split_diameter = Splitter.size(series['Толщина'])
            split_quality = Splitter.quality(series['Состояние'])
            is_stump = Parser.identification_stump(series['Высота'], series['Толщина'], bool(series['Кустарник']))
            if len(split_numbers) == 1:
                if (not is_stump or "пень" in series['Наименование'].lower()) and len(split_quality) == 1 and len(
                        numbers_positions) == 1 and len(geometries) == 1:
                    series_dict = series.to_dict()
                    series_dict['Позиция номера'] = numbers_positions[0]
                    series_dict['Геометрия'] = geometries[0]
                    return [series_dict]
            else:
                if (not is_stump or "пень" in series['Наименование'].lower()) and len(split_quality) == 1 and len(
                        numbers_positions) == 1 and len(geometries) == 1:
                    series_dict = series.to_dict()
                    series_dict['Позиция номера'] = numbers_positions[0]
                    series_dict['Геометрия'] = geometries[0]
                    return [series_dict]
                if len(split_height) == 1:
                    split_height = split_height * int(series['Количество'])
                if len(split_diameter) == 1:
                    split_diameter = split_diameter * int(series['Количество'])
                if len(split_quality) == 1:
                    split_quality = split_quality * int(series['Количество'])
                series_data = []
                for idx in range(len(split_numbers)):
                    if "пень" not in series['Наименование'].lower():
                        is_stump = Parser.identification_stump(split_height[idx], split_diameter[idx],
                                                               bool(series['Кустарник']))
                        name = series['Наименование'] + " (пень)" if is_stump else series['Наименование']
                    else:
                        name = series['Наименование']
                    series_data.append({
                        'Номер точки': split_numbers[idx],
                        'Наименование': name,
                        'Количество': 1,
                        'Высота': split_height[idx],
                        'Толщина': split_diameter[idx],
                        'Состояние': split_quality[idx],
                        'Кустарник': series['Кустарник'],
                        'Позиция номера': numbers_positions[idx],
                        'Геометрия': geometries[idx]
                    })
                return series_data
        else:
            series_dict = series.to_dict()
            series_dict['Позиция номера'] = numbers_positions[0]
            series_dict['Геометрия'] = geometries[0]
            return [series_dict]

    @staticmethod
    def get_shapes_from_autocad_df(df: pd.DataFrame, number: str) -> dict:
        """
        Получение геометрии из датафрейма "Автокад" по номеру точки
        Args:
            df (pd.DataFrame): Датафрейм "Автокад"
            number (str): Номер точки

        Returns:
            dict: Словарь двух колонок для датафрейма со списками позиций номеров и геометрий
        """
        number_positions, geometries = [], []
        split_numbers = Splitter.number(number)
        df = df.set_index('Разделенный номер')
        for split_number in split_numbers:
            shapes = df.loc[split_number][['Позиция номера', 'Геометрия']].to_dict()
            number_positions.append(shapes['Позиция номера'])
            geometries.append(shapes['Геометрия'])
        return {'Список позиций номеров': number_positions, 'Список геометрии': geometries}

    @staticmethod
    def get_taxation_list_orm(wkt_convert: bool = False) -> pd.DataFrame:
        """
        Получение датафрейма "Ведомости ОРМ" из таблиц "Ведомость" и "Автокад"

        Args:
            wkt_convert (bool): Преобразование геометрии в wkt

        Returns:
            pd.DataFrame: Датафрейм ведомости ОРМ
        """
        sheet_taxation_list = xw.sheets['Ведомость']
        taxation_list_df = sheet_taxation_list.range('A1').expand().options(pd.DataFrame, header=1).value
        taxation_list_df = taxation_list_df[
            ['Номер точки', 'Наименование', 'Количество', 'Высота', 'Толщина', 'Состояние', 'Кустарник']]

        sheet_autocad = xw.sheets['Автокад']
        autocad_df = sheet_autocad.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
        autocad_df['Позиция номера'] = autocad_df['Позиция номера'].apply(lambda x: loads(x))
        autocad_df['Геометрия'] = autocad_df['Геометрия'].apply(lambda x: loads(x))

        assert autocad_df['Разделенный номер'].is_unique

        taxation_list_orm = []
        for _, series in taxation_list_df.iterrows():
            taxation_list_orm.extend(ExcelWorker.split_taxation_list_item(autocad_df, series))

        taxation_list_orm_df = pd.DataFrame(taxation_list_orm)

        if not wkt_convert:
            return taxation_list_orm_df
        else:
            taxation_list_orm_df['Позиция номера'] = taxation_list_orm_df['Позиция номера'].apply(lambda geom: geom.wkt)
            taxation_list_orm_df['Геометрия'] = taxation_list_orm_df['Геометрия'].apply(lambda geom: geom.wkt)
            return taxation_list_orm_df

    @staticmethod
    def get_objects_from_zone(zone_result: str, wkt_convert: bool = False) -> pd.DataFrame:
        """
        Получить датафрейм объектов, входящих в указанную зону

        Args:
            zone_result (str): Название зоны
            wkt_convert (bool): Преобразование геометрии в wkt

        Returns:
            pd.DataFrame: Датафрейм объектов, входящих в зону
        """
        sheet_autocad = xw.sheets['Автокад']
        autocad_df = sheet_autocad.range('A1').expand().options(pd.DataFrame, header=1, index=False).value
        autocad_df['number_position'] = autocad_df['number_position'].apply(lambda x: loads(x))
        autocad_df['geometry'] = autocad_df['geometry'].apply(lambda x: loads(x))

        sheet_zones = xw.sheets['Зоны']
        zones_df = sheet_zones.range('A1').expand().options(pd.DataFrame, header=1, index=False).value

        zone_names = zones_df.name.tolist()
        zone_names.remove(zone_result)

        used_split_numbers_df = pd.DataFrame(columns=['split_number', 'type'])
        for zone_name in zone_names:
            try:
                sheet_zone = xw.sheets[zone_name]
            except com_error:
                continue
            if sheet_zone.range('A1').value is None:
                continue
            _used_split_numbers_df = sheet_zone.range('A1').expand().options(pd.DataFrame, header=1, index=False).value[
                ['split_number', 'type']]
            used_split_numbers_df = pd.concat([used_split_numbers_df, _used_split_numbers_df])
        used_split_numbers = used_split_numbers_df[used_split_numbers_df['type'] == 'Point']['split_number'].tolist()

        autocad_df_not_used = autocad_df[~autocad_df['split_number'].isin(used_split_numbers)]

        zone_shape = loads(zones_df[zones_df['name'] == zone_result]['geometry'].tolist()[0])

        intersections_shapes = []
        for _, series in autocad_df_not_used.iterrows():
            geometry = series['geometry']
            geometry_type = series['type']
            intersection = zone_shape.intersection(geometry)
            if geometry_type == 'Polygon' or geometry_type == 'MultiPolygon':
                size = intersection.area
            elif geometry_type == 'LineString' or geometry_type == 'MultiLineString':
                size = intersection.length
            else:
                size = None
            if intersection:
                intersections_shapes.append({
                    'split_number': series['split_number'],
                    'number_position': series['number_position'],
                    'type': geometry_type,
                    'geometry': intersection,
                    'size': size
                })
        intersections_shapes_df = pd.DataFrame(intersections_shapes)
        intersections_shapes_df.index.name = 'index'

        if not wkt_convert:
            return intersections_shapes_df
        else:
            intersections_shapes_df.index = intersections_shapes_df.index.astype(str)
            intersections_shapes_df['number_position'] = intersections_shapes_df['number_position'].apply(
                lambda geom: geom.wkt if geom else None)
            intersections_shapes_df['geometry'] = intersections_shapes_df['geometry'].apply(
                lambda geom: geom.wkt if geom else None)
            return intersections_shapes_df
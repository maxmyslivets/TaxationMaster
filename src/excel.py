import xlwings as xw
import pandas as pd
from shapely.wkt import loads
from win32com.universal import com_error


class ExcelWorker:

    @staticmethod
    def get_numbers(sheet: xw.Sheet, column_name: str) -> list[str]:
        table_range = sheet['A1'].expand('table')
        data = table_range.value
        headers = data[0]
        col_index = headers.index(column_name)
        return [row[col_index] for row in data[1:]]

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
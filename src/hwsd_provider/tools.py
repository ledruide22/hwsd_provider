from os import environ
from pathlib import Path

import numpy as np
import rasterio
from rasterio.mask import mask

from .object.db_connection import DbConnection
from .object.hwsd_soil_dto import HwsdSoilDto, SoilComposition

RASTER_PATH = Path(environ['HWSD_DATA']) / 'HWSD_RASTER' / 'hwsd.bil'


def aggregate_soil_data(soil_composition):
    """
    Aggregate list of most representative soil by weight
    Args:
        soil_composition (HwsdSoilDto): soil composition object

    Returns:
        (HwsdSoilDto): soil composition object aggregate
    """
    hwsd_soil_dto = HwsdSoilDto(SoilComposition(), SoilComposition())
    soil_key_list = [key for key in hwsd_soil_dto.top_soil.__dict__.keys()]
    for soil in soil_composition:
        top_soil = soil.top_soil
        sub_soil = soil.sub_soil
        ratio_top = top_soil.share / 100.
        ratio_sub = sub_soil.share / 100.
        if ratio_top is not None:
            for atr in soil_key_list:
                if atr == "share":
                    value_top = 1.
                else:
                    value_top = getattr(soil.top_soil, atr)
                if value_top is not None:
                    prev_val = getattr(hwsd_soil_dto.top_soil, atr)
                    if prev_val is None:
                        prev_val = 0
                    hwsd_soil_dto.top_soil.__setattr__(atr, round(value_top * ratio_top + prev_val, 5))
        if ratio_sub is not None:
            for atr in soil_key_list:
                if atr == "share":
                    value_sub = 1.
                else:
                    value_sub = getattr(soil.sub_soil, atr)
                if value_sub is not None:
                    prev_val = getattr(hwsd_soil_dto.sub_soil, atr)
                    if prev_val is None:
                        prev_val = 0
                    hwsd_soil_dto.sub_soil.__setattr__(atr, round(value_sub * ratio_sub + prev_val, 5))
    hwsd_soil_dto.sub_soil.share = hwsd_soil_dto.sub_soil.share * 100
    hwsd_soil_dto.top_soil.share = hwsd_soil_dto.top_soil.share * 100
    return hwsd_soil_dto


def retrieve_soil_composition(coordinate, db_connection=None):
    """
        Retrieve soil id from HWSD raster at the coordinate
    Args:
        coordinate (list): (long, lat)
        db_connection (DbConnection): object containing connection to db

    Returns:
        (list): list of HwsdSoilDto, one for each coordinates
    """
    mu_global = retrieve_mu_global_from_raster(coordinate)
    return retrieve_soil_composition_from_mu_global(mu_global, db_connection)


def retrieve_mu_global_from_raster_by_zone(geojson):
    """
    This function retrieve all mu_global in the geojson
    Args:
        geojson (dict): geojson represent the area where mu_global should be find

    Returns:
        (list(dict)): list of mu_global inside the geojson area with their area percentage
    """

    if geojson['type'].lower() != "polygon":
        raise ValueError("Geojson should be of type polygon only")
    with rasterio.open(str(RASTER_PATH)) as src:
        out_image, _ = rasterio.mask.mask(src, [geojson], crop=True)
    mu_globals = list(np.delete(np.unique(out_image), np.where(np.unique(out_image) == 0), axis=0))
    soil_composition_temp = {}
    soil_composition_final = []
    sum_count = 0
    for mu_global in mu_globals:
        count = np.count_nonzero(out_image == mu_global)
        sum_count += count
        soil_composition_temp[str(mu_global)] = count
    for mu_global in mu_globals:
        soil_composition_final.append({'mu_global': int(mu_global),
                                       'area_perc': round(soil_composition_temp[str(mu_global)] / sum_count * 100, 2)})
    return soil_composition_final


def retrieve_mu_global_from_raster(coordinate):
    """
        Retrieve mu_global from HWSD raster at the coordinate
    Args:
        coordinate (tuple): (longitude, latitude)

    Returns:
        (int): soil id  corresponding to coordinate point
    """

    with rasterio.open(str(RASTER_PATH)) as src:
        return int([x[0] for x in src.sample([coordinate])][0])


def __execute_mbd_query(sql_query, db_connection, force_open=False):
    """
        Function to connect to msdb for linux and windows and execute querys
    Args:
        sql_query (str): sql query to retrieve data
        db_connection (DbConnection): object containing connection to db

    Returns:
        query_data (list(tuple)): the tuple contains requested values from ms db
    """

    cur = db_connection.connexion.cursor()
    cur.execute(sql_query)
    query_data = cur.fetchall()
    cur.close()
    if not db_connection.is_permanent and not force_open:
        db_connection.close_connection()

    return query_data


def retrieve_soil_composition_from_mu_global(mu_global, db_connection):
    """
        Retrieve soil composition with HWSD database for each soil_ids
    Args:
        mu_global (int): soil id list corresponding to coordinate point (see. retrieve_soil_id_from_raster)
        db_connection (DbConnection): object containing connection to db
    Returns:
         (list): list of HwsdSoilDto, one for each soil_ids
    """
    if db_connection is None:
        db_connection = DbConnection(is_permanent=False)
        db_connection.open_connection()

    # define query
    top_soil_sql_query = f'SELECT SHARE, T_GRAVEL, T_SAND, T_SILT, T_CLAY, T_REF_BULK_DENSITY, T_BULK_DENSITY, T_OC,' \
                         f' T_PH_H2O, T_CEC_CLAY, T_CEC_SOIL, T_BS, T_TEB, T_CACO3,T_CASO4,T_ESP,T_ECE ' \
                         f'FROM HWSD_DATA WHERE MU_GLOBAL = {str(mu_global)}'
    sub_soil_sql_query = f'SELECT SHARE, S_GRAVEL, S_SAND, S_SILT, S_CLAY, S_REF_BULK_DENSITY, S_BULK_DENSITY, S_OC, ' \
                         f'S_PH_H2O, S_CEC_CLAY, S_CEC_SOIL, S_BS, S_TEB, S_CACO3, S_CASO4, S_ESP, S_ECE' \
                         f' FROM HWSD_DATA WHERE MU_GLOBAL = {str(mu_global)}'

    top_soils_data = __execute_mbd_query(top_soil_sql_query, db_connection, force_open=True)
    sub_soils_data = __execute_mbd_query(sub_soil_sql_query, db_connection)
    soil_composition = []
    for top_soil_data, sub_soil_data in zip(top_soils_data, sub_soils_data):
        hwsd_soil_dto = HwsdSoilDto()
        hwsd_soil_dto.complete(top_soil_data, sub_soil_data)
        soil_composition.append(hwsd_soil_dto)

    return soil_composition

from os import environ
from pathlib import Path

import rasterio
from pyodbc import connect

from .object.hwsd_soil_dto import HwsdSoilDto


def retrieve_soil_composition(coordinates):
    """
        Retrieve soil id from HWSD raster at the coordinate
    Args:
        coordinates (list): list of (latitude, longitude)

    Returns:
        (list): list of HwsdSoilDto, one for each coordinates
    """
    soil_ids = retrieve_soil_id_from_raster(coordinates)
    return retrieve_soil_composition_from_soil_id(soil_ids)


def retrieve_soil_id_from_raster(coordinates):
    """
        Retrieve soil id from HWSD raster at the coordinate
    Args:
        coordinates (list): list of (latitude, longitude)

    Returns:
        (tuple): soil id list corresponding to coordinates point
    """
    raster_path = Path(environ['HWSD_DATA']) / 'HWSD_RASTER' / 'hwsd.bil'
    src = rasterio.open(str(raster_path))
    return tuple(x[0] for x in src.sample(coordinates))


def retrieve_soil_composition_from_soil_id(soil_ids):
    """
        Retrieve soil composition with HWSD database for each soil_ids
    Args:
        soil_ids (tuple): soil id list corresponding to coordinates point (see. retrieve_soil_id_from_raster)

    Returns:
         (list): list of HwsdSoilDto, one for each soil_ids
    """
    # set up some constants
    msdb = str(Path(environ['HWSD_DATA']) / 'HWSD' / 'HWSD.mdb')
    driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'

    # connect to db
    con = connect('DRIVER={};DBQ={};'.format(driver, msdb))
    cur = con.cursor()

    # run a query and get the results
    soil_ids_str = soil_ids.__str__()[0:-2] + ')' if len(soil_ids) == 1 else soil_ids.__str__()
    top_soil_sql_query = f'SELECT T_GRAVEL, T_SAND, T_SILT , T_REF_BULK_DENSITY, T_BULK_DENSITY, T_OC, T_PH_H2O, ' \
                         f'T_CEC_CLAY, T_CEC_SOIL, T_BS, T_TEB, T_CACO3, T_CASO4,T_ESP,T_ECE FROM HWSD_DATA' \
                         f' WHERE ID IN {soil_ids_str}'
    sub_soil_sql_query = f'SELECT  S_GRAVEL, S_SAND, S_SILT, S_REF_BULK_DENSITY, S_BULK_DENSITY, S_OC, S_PH_H2O, ' \
                         f'S_CEC_CLAY, S_CEC_SOIL, S_BS, S_TEB, S_CACO3, S_CASO4, S_ESP, S_ECE FROM HWSD_DATA' \
                         f' WHERE ID IN {soil_ids_str}'
    top_soils_data = cur.execute(top_soil_sql_query).fetchall()
    sub_soils_data = cur.execute(sub_soil_sql_query).fetchall()
    cur.close()
    con.close()
    soil_composition = []
    for top_soil_data, sub_soil_data in zip(top_soils_data, sub_soils_data):
        hwsd_soil_dto = HwsdSoilDto()
        hwsd_soil_dto.complete(top_soil_data, sub_soil_data)
        soil_composition.append(hwsd_soil_dto)

    return soil_composition

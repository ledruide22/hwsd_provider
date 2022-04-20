from os import environ
from pathlib import Path

import rasterio

from .object.db_connection import DbConnection
from .object.hwsd_soil_dto import HwsdSoilDto


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


def retrieve_mu_global_from_raster(coordinate):
    """
        Retrieve mu_global from HWSD raster at the coordinate
    Args:
        coordinate (tuple): (longitude, latitude)

    Returns:
        (int): soil id  corresponding to coordinate point
    """
    raster_path = Path(environ['HWSD_DATA']) / 'HWSD_RASTER' / 'hwsd.bil'
    src = rasterio.open(str(raster_path))
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

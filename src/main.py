from os import environ
from pathlib import Path

import pyodbc
import rasterio


def retrieve_soil_id_from_raster(coordinates):
    """
        Retrieve soil id from HWSD raster at the coordinate
    Args:
        coordinates (list): list of (latitude, longitude)

    Returns:
        (list): soil id list corresponding to coordinates point
    """
    raster_path = Path(environ['HWSD_DATA']) / 'HWSD_RASTER' / 'hwsd.bil'
    src = rasterio.open(str(raster_path))
    return [x[0] for x in src.sample(coordinates)]


def open_hwsd_db():
    # set up some constants
    MDB = str(Path().absolute().parent / 'resources' / 'HWSD' / 'HWSD.mdb')
    DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'

    # connect to db
    con = pyodbc.connect('DRIVER={};DBQ={};'.format(DRV, MDB))
    cur = con.cursor()

    # run a query and get the results
    SQL = 'SELECT * FROM mytable;'  # your query goes here
    rows = cur.execute(SQL).fetchall()
    cur.close()
    con.close()
    return True

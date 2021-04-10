from src.main import retrieve_soil_id_from_raster, open_hwsd_db

coordinates = [(-3.8530, 48.2268)]

soil_id_list = retrieve_soil_id_from_raster(coordinates)
soil_data_list = open_hwsd_db(soil_id_list)

from src.main import retrieve_soil_id_from_raster, retrieve_soil_composition_from_soil_id

coordinates = [(-3.8530, 48.2268)]#, (-3.8530, 48.2268)]

soil_ids = retrieve_soil_id_from_raster(coordinates)
soil_data_list = retrieve_soil_composition_from_soil_id(soil_ids)

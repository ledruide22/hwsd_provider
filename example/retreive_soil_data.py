from hwsd_provider.main import retrieve_soil_composition

coordinates = [(44.8530, -72.2268), (-3.8530, 48.2268)]

soil_data_list = retrieve_soil_composition(coordinates)
print(soil_data_list[0].top_soil.silt)

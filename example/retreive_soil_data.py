from hwsd_provider.tools import retrieve_soil_composition

coordinate = (-72.2268, 44.8530)

soil_data = retrieve_soil_composition(coordinate)
print(soil_data[0].top_soil.silt)

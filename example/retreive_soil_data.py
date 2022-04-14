import json

from hwsd_provider.tools import retrieve_soil_composition, aggregate_soil_data

coordinate = (-72.2268, 44.8530)

soil_data_list = retrieve_soil_composition(coordinate)
soil_data_mean = aggregate_soil_data(soil_data_list)
print(json.dumps(soil_data_mean.to_dict()))

import json

from hwsd_provider.tools import retrieve_soil_composition

coordinate = (-72.2268, 44.8530)

soil_data_list = retrieve_soil_composition(coordinate)
print(json.dumps([soil_data.to_dict() for soil_data in soil_data_list]))

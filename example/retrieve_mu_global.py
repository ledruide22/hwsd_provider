from src.hwsd_provider.tools import retrieve_mu_global_from_raster_by_zone

geojson = {'type': 'Polygon', 'coordinates': [
    [(-72.2268, 44.8530), (-72.2268, 44.9530), (-72.5268, 44.9530), (-72.5268, 44.8530), (-72.2268, 44.8530)]]}

mu_global_list = retrieve_mu_global_from_raster_by_zone(geojson)

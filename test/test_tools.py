from mock.mock import MagicMock

from src.hwsd_provider.object.hwsd_soil_dto import HwsdSoilDto
from src.hwsd_provider.tools import retrieve_soil_composition, retrieve_mu_global_from_raster, \
    retrieve_soil_composition_from_mu_global, aggregate_soil_data


def test_aggregate_soil_data():
    # Given
    top_soil_1 = (50, 37, 44, 1.41, 1.24, 2.13, 7.5, 80.0, 27.0, 100.0, 28.8, 6.0, 0.0, 2.0, 0.1)
    top_soil_2 = (50, 37, 44, 1.41, 1.24, 2.13, 7.5, 80.0, 27.0, 100.0, 28.8, 6.0, 0.0, 2.0, 0.1)
    hwsd_soil_dto_1 = HwsdSoilDto()
    hwsd_soil_dto_1.complete(top_soil_1, top_soil_1)
    hwsd_soil_dto_2 = HwsdSoilDto()
    hwsd_soil_dto_2.complete(top_soil_2, top_soil_2)
    # When
    response = aggregate_soil_data([hwsd_soil_dto_1, hwsd_soil_dto_2])
    # Then
    hwsd_soil_dto_1.top_soil.share = 100.
    hwsd_soil_dto_1.sub_soil.share = 100.
    assert response.__dict__['top_soil'].__dict__ == hwsd_soil_dto_1.__dict__['top_soil'].__dict__
    assert response.__dict__['sub_soil'].__dict__ == hwsd_soil_dto_1.__dict__['sub_soil'].__dict__


def test_retrieve_soil_composition(mocker):
    # Given
    coordinates = [(10.23, 12.22)]
    hwsd_soil_dto = HwsdSoilDto('top_soil', 'sub_soil')
    mocker.patch('src.hwsd_provider.tools.retrieve_mu_global_from_raster', return_value=1234)
    mocker.patch('src.hwsd_provider.tools.retrieve_soil_composition_from_mu_global', return_value=[hwsd_soil_dto])
    # When
    response = retrieve_soil_composition(coordinates)
    # Then
    assert response[0] == hwsd_soil_dto


def test_retrieve_mu_global_from_raster(mocker):
    # Given
    expected_response = [1]
    coordinates = [(10.23, 12.22)]
    src = MagicMock()
    src.sample.return_value = [[x] for x in expected_response]
    mocker.patch('src.hwsd_provider.tools.rasterio.open', return_value=src)
    # When
    response = retrieve_mu_global_from_raster(coordinates)
    # Then
    assert response == expected_response[0]


# def test_retrieve_mu_global_from_raster_by_zone(mocker):
#    # Given
#    geojson = {'type': 'Polygon', 'coordinates':
#    [[(-72.2268, 44.8530), (-72.2268, 44.9530), (-72.5268, 44.9530), (-72.5268, 44.8530), (-72.2268, 44.8530)]]}
#   expected_mu_global_list = [{'mu_global': 1234, 'area_perc': 0.7}, {'mu_global': 5678, 'area_perc': 0.3}]
#   with mocker.patch("src.hwsd_provider.tools.rasterio.open") as mock_file:
#   mocker.patch("src.hwsd_provider.tools.rasterio.mask.mask",
#            return_value=[np.array([[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                                      0, 0, 0, 0, 0, 0, 0],
#                                     [0, 4970, 4970, 4970, 4962, 4962,
#                                      4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962],
#                                     [0, 4970, 4970, 4970, 4970, 4962,
#                                      4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962],
#                                     [0, 4970, 4970, 4970, 4970, 4962,
#                                      4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962],
#                                     [0, 4970, 4970, 4970, 4970, 4962,
#                                      4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                      4962, 4962, 4962, 4962, 4962,
#                                               4962, 4962, 4962, 4962, 4962,
#                                               4962, 4962, 4962, 4962, 4962,
#                                               4962, 4962]]]), None])
#
#        # When
#        mu_global_list = retrieve_mu_global_from_raster_by_zone(geojson)
#        # Then
#        assert mu_global_list == expected_mu_global_list


def test_retrieve_soil_composition_from_mu_global(mocker):
    # Given
    mu_global = 1234
    soil_connection = None
    top_soil = (16, 37, 44, 1.41, 1.24, 2.13, 7.5, 80.0, 27.0, 100.0, 28.8, 6.0, 0.0, 2.0, 0.1)
    hwsd_soil_dto = HwsdSoilDto()
    hwsd_soil_dto.complete(top_soil, top_soil)
    mocker.patch('src.hwsd_provider.tools.__execute_mbd_query', return_value=[top_soil])
    # When
    response = retrieve_soil_composition_from_mu_global(mu_global, soil_connection)
    # Then
    assert response[0].__dict__['top_soil'].__dict__ == hwsd_soil_dto.__dict__['top_soil'].__dict__
    assert response[0].__dict__['sub_soil'].__dict__ == hwsd_soil_dto.__dict__['sub_soil'].__dict__

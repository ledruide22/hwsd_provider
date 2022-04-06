from mock.mock import MagicMock

from src.hwsd_provider.object.hwsd_soil_dto import HwsdSoilDto
from src.hwsd_provider.tools import retrieve_soil_composition, retrieve_soil_id_from_raster, \
    retrieve_soil_composition_from_soil_id


def test_retrieve_soil_composition(mocker):
    # Given
    coordinates = [(10.23, 12.22)]
    hwsd_soil_dto = HwsdSoilDto('top_soil', 'sub_soil')
    mocker.patch('src.hwsd_provider.tools.retrieve_soil_id_from_raster', return_value=(1234, 5678))
    mocker.patch('src.hwsd_provider.tools.retrieve_soil_composition_from_soil_id', return_value=[hwsd_soil_dto])
    # When
    response = retrieve_soil_composition(coordinates)
    # Then
    assert response[0] == hwsd_soil_dto


def test_retrieve_soil_id_from_raster(mocker):
    # Given
    expected_response = (1, 2, 3)
    coordinates = [(10.23, 12.22)]
    src = MagicMock()
    src.sample.return_value = [[x] for x in expected_response]
    mocker.patch('src.hwsd_provider.tools.rasterio.open', return_value=src)
    # When
    response = retrieve_soil_id_from_raster(coordinates)
    # Then
    assert response == expected_response


def test_retrieve_soil_composition_from_soil_id(mocker):
    # Given
    soil_ids = (1234, 4567)
    soil_connection = None
    top_soil = (16, 37, 44, 1.41, 1.24, 2.13, 7.5, 80.0, 27.0, 100.0, 28.8, 6.0, 0.0, 2.0, 0.1)
    sub_soil = (1, 3, 4, 1.4, 1.2, 2.1, 7, 8, 2, 10, 28, 6, 0, 2.0, 0)
    hwsd_soil_dto = HwsdSoilDto()
    hwsd_soil_dto.complete(top_soil, sub_soil)
    mocker.patch('src.hwsd_provider.tools.__execute_mbd_query', return_value=[[top_soil], [sub_soil]])
    # When
    response = retrieve_soil_composition_from_soil_id(soil_ids, soil_connection)
    # Then
    assert response[0].__dict__['top_soil'].__dict__ == hwsd_soil_dto.__dict__['top_soil'].__dict__
    assert response[0].__dict__['sub_soil'].__dict__ == hwsd_soil_dto.__dict__['sub_soil'].__dict__


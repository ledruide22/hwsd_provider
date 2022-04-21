from src.hwsd_provider.object.hwsd_soil_dto import SoilComposition, HwsdSoilDto

TOP_SOIL_COMPOSITION = {'share': 100,
                        'gravel': 10,
                        'sand': 80,
                        'silt': 10,
                        'clay': 10,
                        'ref_bulk_density': 1,
                        'bulk_density': 1,
                        'oc': 1,
                        'ph': 7,
                        'cec_clay': 1,
                        'cec_soil': 1,
                        'bs': 1,
                        'teb': 1,
                        'caco3': 1,
                        'caso4': 1,
                        'esp': 1,
                        'ece': 1}

SUB_SOIL_COMPOSITION = {'share': 100,
                        'gravel': 20,
                        'sand': 20,
                        'silt': 60,
                        'clay': 20,
                        'ref_bulk_density': 2,
                        'bulk_density': 2,
                        'oc': 2,
                        'ph': 6,
                        'cec_clay': 2,
                        'cec_soil': 2,
                        'bs': 2,
                        'teb': 2,
                        'caco3': 2,
                        'caso4': 2,
                        'esp': 2,
                        'ece': 2}


def test_should_instantiate_soil_composition():
    # Given
    soil_composition = TOP_SOIL_COMPOSITION
    # When
    soil_composition_obj = SoilComposition(share=soil_composition['share'], gravel=soil_composition['gravel'],
                                           sand=soil_composition['sand'],
                                           clay=soil_composition['clay'],
                                           silt=soil_composition['silt'],
                                           ref_bulk_density=soil_composition['ref_bulk_density'],
                                           bulk_density=soil_composition['bulk_density'],
                                           oc=soil_composition['oc'], ph=soil_composition['ph'],
                                           cec_clay=soil_composition['cec_clay'], cec_soil=soil_composition['cec_soil'],
                                           bs=soil_composition['bs'],
                                           teb=soil_composition['teb'], caco3=soil_composition['caco3'],
                                           caso4=soil_composition['caso4'],
                                           esp=soil_composition['esp'], ece=soil_composition['ece'])
    # Then
    for key in soil_composition.keys():
        assert soil_composition[key] == getattr(soil_composition_obj, key)


def test_should_instantiate_soil_dto_from_obj():
    # Given
    top_soil_composition = TOP_SOIL_COMPOSITION
    sub_soil_composition = SUB_SOIL_COMPOSITION
    # When
    top_soil_composition_obj = SoilComposition(share=top_soil_composition['share'],
                                               gravel=top_soil_composition['gravel'],
                                               sand=top_soil_composition['sand'],
                                               clay=top_soil_composition['clay'],
                                               silt=top_soil_composition['silt'],
                                               ref_bulk_density=top_soil_composition['ref_bulk_density'],
                                               bulk_density=top_soil_composition['bulk_density'],
                                               oc=top_soil_composition['oc'], ph=top_soil_composition['ph'],
                                               cec_clay=top_soil_composition['cec_clay'],
                                               cec_soil=top_soil_composition['cec_soil'],
                                               bs=top_soil_composition['bs'],
                                               teb=top_soil_composition['teb'], caco3=top_soil_composition['caco3'],
                                               caso4=top_soil_composition['caso4'],
                                               esp=top_soil_composition['esp'], ece=top_soil_composition['ece'])
    sub_soil_composition_obj = SoilComposition(share=sub_soil_composition['share'],
                                               gravel=sub_soil_composition['gravel'],
                                               clay=sub_soil_composition['clay'],
                                               sand=sub_soil_composition['sand'],
                                               silt=sub_soil_composition['silt'],
                                               ref_bulk_density=sub_soil_composition['ref_bulk_density'],
                                               bulk_density=sub_soil_composition['bulk_density'],
                                               oc=sub_soil_composition['oc'], ph=sub_soil_composition['ph'],
                                               cec_clay=sub_soil_composition['cec_clay'],
                                               cec_soil=sub_soil_composition['cec_soil'],
                                               bs=sub_soil_composition['bs'],
                                               teb=sub_soil_composition['teb'], caco3=sub_soil_composition['caco3'],
                                               caso4=sub_soil_composition['caso4'],
                                               esp=sub_soil_composition['esp'], ece=sub_soil_composition['ece'])
    hwsd_dto_obj = HwsdSoilDto(top_soil=top_soil_composition_obj, sub_soil=sub_soil_composition_obj)
    # Then
    for key in top_soil_composition.keys():
        assert top_soil_composition[key] == getattr(hwsd_dto_obj.top_soil, key)
    for key in sub_soil_composition.keys():
        assert sub_soil_composition[key] == getattr(hwsd_dto_obj.sub_soil, key)


def test_should_complete_soil_dto():
    # Given
    top_soil_composition = tuple(TOP_SOIL_COMPOSITION.values())
    sub_soil_composition = tuple(SUB_SOIL_COMPOSITION.values())
    # When
    hwsd_dto_obj = HwsdSoilDto()
    hwsd_dto_obj.complete(top_soil_data=top_soil_composition, sub_soil_data=sub_soil_composition)
    # Then
    for key in TOP_SOIL_COMPOSITION.keys():
        assert TOP_SOIL_COMPOSITION[key] == getattr(hwsd_dto_obj.top_soil, key)
    for key in SUB_SOIL_COMPOSITION.keys():
        print(key)
        assert SUB_SOIL_COMPOSITION[key] == getattr(hwsd_dto_obj.sub_soil, key)

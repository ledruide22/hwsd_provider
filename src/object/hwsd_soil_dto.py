class SoilComposition(object):
    def __init__(self, gravel=None, sand=None, silt=None, ref_bulk_density=None, bulk_density=None, oc=None, ph=None,
                 cec_clay=None, cec_soil=None, bs=None, teb=None, caco3=None, caso4=None, esp=None, ece=None):
        self.gravel = gravel
        self.sand = sand
        self.silt = silt
        self.ref_bulk_density = ref_bulk_density
        self.bulk_density = bulk_density
        self.oc = oc
        self.ph = ph
        self.cec_clay = cec_clay
        self.cec_soil = cec_soil
        self.bs = bs
        self.teb = teb
        self.caco3 = caco3
        self.caso4 = caso4
        self.esp = esp
        self.ece = ece

    def complete(self, data_soil):
        """
            Fill HwsdSoilDto from HWSD db data

        Args:
            data_soil (tuple): containing all data obtain from HWSD ms db
        """
        for value, atr in zip(data_soil, self.__dir__()):
            self.__setattr__(atr, value)


class HwsdSoilDto(object):
    """Objct containing all data of top and sub soil provide by HWSD db for an location """

    def __init__(self, top_soil=None, sub_soil=None):
        self.top_soil = top_soil
        self.sub_soil = sub_soil

    def complete(self, top_soil_data, sub_soil_data):
        top_soil = SoilComposition()
        top_soil.complete(top_soil_data)
        sub_soil = SoilComposition()
        sub_soil.complete(sub_soil_data)
        self.top_soil = top_soil
        self.sub_soil = sub_soil

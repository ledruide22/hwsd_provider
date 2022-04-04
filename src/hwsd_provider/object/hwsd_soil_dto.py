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
    """Object containing all data of top and sub soil provide by HWSD db for a location """

    def __init__(self, top_soil=None, sub_soil=None):
        self.top_soil = top_soil
        self.sub_soil = sub_soil

    def complete(self, top_soil_data, sub_soil_data):
        """
        Complete HwsdSoilDto with top_soil_data and sub_soil_data
        Args:
            top_soil_data (SoilComposition): contains top soil data information
            sub_soil_data (SoilComposition): contains sub soil data information
        """
        top_soil = SoilComposition()
        top_soil.complete(top_soil_data)
        sub_soil = SoilComposition()
        sub_soil.complete(sub_soil_data)
        self.top_soil = top_soil
        self.sub_soil = sub_soil

    def to_dict(self):
        """
        Convert HwsdSoilDto to dict and return
        Returns:
            (dict): HwsdSoilDto convert to dict
        """
        hwsd_soil_dict = {'top_soil': self.top_soil.__dict__,
                          'sub_soil': self.sub_soil.__dict__}
        return hwsd_soil_dict

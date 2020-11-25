from Region import Region

class RegionManager:
    def __init__(self):
        self.__current_region = Region(self.region_data(0.0, 0.0, 10.0, 210.0))
        self.__regions = [ self.__current_region ]

    def region_data(self, sx, sy, pad, w):
        return {
            "start_x": sx,
            "start_y": sy,
            "padding": pad,
            "width": w
        }

    def region(self):
        return self.__current_region

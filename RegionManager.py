from Region import Region

class RegionManager:
    def __init__(self):
        self.__current_region = Region(self.region_data(0.0, 0.0, 10.0, 210.0))
        self.__regions = [ self.__current_region ]

    def region(self):
        return self.__current_region

    def regions(self):
        return self.__regions

    def change_region(self, region_no):
        self.__current_region = self.__regions[region_no]

    def split_region(self, percentage_string):
        percentage = float(percentage_string.replace('%', '')) / 100
        padding = 3.0

        r = self.__current_region
        parent_width = r.wpad()
        parent_padding = r.padding()

        start_y = r.cursor_y()

        left_width = parent_width * percentage
        right_width = parent_width * (1 - percentage)
        left_x = parent_padding + r.sx()
        right_x = left_x + left_width

        left_data = self.region_data(left_x, start_y, padding, left_width)
        right_data = self.region_data(right_x, start_y, padding, right_width)

        left_region = Region(left_data)
        right_region = Region(right_data)

        self.__regions = [ left_region, right_region ]
        self.__current_region = self.__regions[0]

    def region_data(self, sx, sy, pad, w):
        return {
            "start_x": sx,
            "start_y": sy,
            "padding": pad,
            "width": w
        }

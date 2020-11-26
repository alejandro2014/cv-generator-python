from Region import Region

class RegionManager:
    def __init__(self):
        self.__main_region = Region(self.region_data(0.0, 0.0, 10.0, 210.0))
        self.__current_region = self.__main_region
        self.__regions = [ self.__current_region ]

    def current_region(self):
        return self.__current_region

    def regions(self):
        return self.__regions

    def change_region(self, region_no):
        self.__current_region = self.__regions[region_no]

    def inc_region_cy(self, region_no, offset_y):
        region = self.__regions[region_no]
        region.inc_cursor_y(offset_y)

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

    def align_regions(self):
        left_region = self.__regions[0]
        right_region = self.__regions[1]

        cy_left = left_region.cursor_y()
        cy_right = right_region.cursor_y()

        max_cursor = cy_left if cy_left > cy_right else cy_right

        left_region.set_cursor_y(max_cursor)
        right_region.set_cursor_y(max_cursor)

    def inc_regions_cy(self, exp_line_spacing):
        left_region = self.__regions[0]
        right_region = self.__regions[1]

        left_region.inc_cursor_y(exp_line_spacing)
        right_region.inc_cursor_y(exp_line_spacing)

    def set_cy(self, new_cy):
        left_region = self.__regions[0]
        right_region = self.__regions[1]

        left_region.set_cursor_y(new_cy)
        right_region.set_cursor_y(new_cy)

    def set_height(self, height):
        left_region = self.__regions[0]
        right_region = self.__regions[1]

        left_region.set_height(height)
        right_region.set_height(height)

    def set_sy(self, height):
        left_region = self.__regions[0]
        right_region = self.__regions[1]

        left_region.set_sy(height)
        right_region.set_sy(height)

    def region_data(self, sx, sy, pad, w):
        return {
            "start_x": sx,
            "start_y": sy,
            "padding": pad,
            "width": w
        }

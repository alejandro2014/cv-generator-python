from ConfigLoader import ConfigLoader

class Region:
    def __init__(self, region_name):
        config_loader = ConfigLoader()
        #regions_data = config_loader.load_config_file("regions")
        #region_data = regions_data[region_name]
        #region_data = config_loader.getregions_data[region_name]

        region_data = {
            "start_x": 0.0,
            "start_y": 0.0,
            "padding": 10.0,
            "width": 210.0,
            "height": 297.0
        }

        self.__start_x = region_data['start_x']
        self.__start_y = region_data['start_y']
        self.__end_x = region_data['start_x'] + region_data['width']
        self.__padding = region_data['padding']

        self.__start_x_padded = self.__start_x + self.__padding
        self.__start_y_padded = self.__start_y + self.__padding

        self.__end_x_padded = self.__end_x - self.__padding
        #self.__end_y_padded = self.__start_y + region_data['width'] - self.__padding

        #self.padding = region_data['padding']
        #self.width = region_data['width']

        #self.mid_x = self.x + self.width / 2
        #self.start_x_padded = self.x + self.padding
        #self.width_padded = self.width - 2 * self.padding

        #self.cursor_x = 0
        #self.cursor_y = 0

    def start_x(self):
        return self.__start_x

    def start_y(self):
        return self.__start_y

    def start_x_padded(self):
        return self.__start_x_padded

    def start_y_padded(self):
        return self.__start_y_padded

    def end_x(self):
        return self.__end_x

    def end_x_padded(self):
        return self.__end_x_padded

    def padding(self):
        return self.__padding

    def get_default_region(self):
        return {
            "start_x": 0.0,
            "padding": 10.0,
            "width": 210.0,
            "height": 297.0
        }

    #def process_region(self, region):

    def process_y(self, y):
        self.y = y
        self.start_y_padded = self.y + self.padding

    def add_height(self, height):
        self.height = height
